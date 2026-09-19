import io
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response
from PIL import Image

from orquidea.datos.almacen_fotos import poner_foto
from orquidea.datos.base import conectar
from orquidea.datos.ejemplares import agregar, agregar_sin_especie, obtener
from orquidea.datos.fotos import TAMANO_MAXIMO, procesar_foto
from orquidea.datos.sesiones import Sesion
from orquidea.web.app import LIMITE_DE_CUERPO, app
from orquidea.web.rutas import coleccion as rutas_coleccion
from tests.fabricas import MARCADOR_XMP, especie, imagen_jpeg

AHORA = 1_780_000_000


def _conexion() -> sqlite3.Connection:
    return conectar(app.state.ruta_base)


def _ejemplar_propio(nombre: str = "Mi rara", notas: str = "") -> int:
    conexion = _conexion()
    try:
        return agregar_sin_especie(conexion, nombre, notas, AHORA).id
    finally:
        conexion.close()


def _con_foto(id: int) -> str:
    conexion = _conexion()
    try:
        assert poner_foto(
            conexion, app.state.directorio_fotos, id, procesar_foto(imagen_jpeg(800, 600))
        )
        ejemplar = obtener(conexion, id)
        assert ejemplar is not None and ejemplar.foto is not None
        return ejemplar.foto
    finally:
        conexion.close()


def _archivos() -> list[Path]:
    return sorted(app.state.directorio_fotos.iterdir())


def test_la_ficha_de_un_ejemplar_sin_foto_ofrece_subirla(client: TestClient) -> None:
    id = _ejemplar_propio("Cattleya de mi abuela", "Regalo de 2019")

    respuesta = client.get(f"/coleccion/{id}")

    assert respuesta.status_code == 200
    assert "Cattleya de mi abuela" in respuesta.text
    assert "Regalo de 2019" in respuesta.text
    assert "Aún no tiene foto." in respuesta.text
    assert "<img" not in respuesta.text
    assert 'enctype="multipart/form-data"' in respuesta.text
    assert f'action="/coleccion/{id}/foto"' in respuesta.text
    assert 'name="csrf"' in respuesta.text
    assert 'type="file"' in respuesta.text


def test_la_ficha_de_un_ejemplar_del_catalogo_muestra_su_especie(client: TestClient) -> None:
    app.state.catalogo = [especie()]
    conexion = _conexion()
    try:
        id = agregar(conexion, "epidendrum-radicans", AHORA).id
    finally:
        conexion.close()

    html = client.get(f"/coleccion/{id}").text

    assert "Epidendrum radicans" in html
    assert 'href="/especies/epidendrum-radicans"' in html


def test_la_ficha_muestra_la_foto_a_tamano_completo(client: TestClient) -> None:
    id = _ejemplar_propio("Mi rara")
    _con_foto(id)

    html = client.get(f"/coleccion/{id}").text

    assert f'src="/coleccion/{id}/foto"' in html
    assert 'alt="Foto de Mi rara"' in html
    assert "Aún no tiene foto." not in html


def test_la_ficha_de_un_id_inexistente_da_404(client: TestClient) -> None:
    assert client.get("/coleccion/999").status_code == 404


def test_nuevo_sigue_siendo_el_formulario_de_alta_y_no_una_ficha(client: TestClient) -> None:
    respuesta = client.get("/coleccion/nuevo")

    assert respuesta.status_code == 200
    assert "Planta fuera del catálogo" in respuesta.text


def test_la_imagen_y_la_miniatura_se_entregan_tal_como_se_guardaron(client: TestClient) -> None:
    id = _ejemplar_propio()
    nombre = _con_foto(id)
    directorio: Path = app.state.directorio_fotos

    imagen = client.get(f"/coleccion/{id}/foto")
    miniatura = client.get(f"/coleccion/{id}/foto/miniatura")

    assert imagen.status_code == miniatura.status_code == 200
    assert imagen.headers["content-type"] == miniatura.headers["content-type"] == "image/jpeg"
    assert imagen.headers["x-content-type-options"] == "nosniff"
    assert "content-disposition" not in imagen.headers
    assert imagen.content == (directorio / f"{nombre}.jpg").read_bytes()
    assert miniatura.content == (directorio / f"{nombre}-mini.jpg").read_bytes()


def test_pedir_la_imagen_de_un_ejemplar_sin_foto_o_inexistente_da_404(client: TestClient) -> None:
    id = _ejemplar_propio()

    assert client.get(f"/coleccion/{id}/foto").status_code == 404
    assert client.get(f"/coleccion/{id}/foto/miniatura").status_code == 404
    assert client.get("/coleccion/999/foto").status_code == 404


def test_si_el_archivo_falta_en_el_disco_es_404_y_no_500(client: TestClient) -> None:
    id = _ejemplar_propio()
    nombre = _con_foto(id)
    (app.state.directorio_fotos / f"{nombre}.jpg").unlink()

    assert client.get(f"/coleccion/{id}/foto").status_code == 404
    assert client.get(f"/coleccion/{id}/foto/miniatura").status_code == 200


@pytest.mark.parametrize("nombre", ["../secreto", "..", "a/b", ""])
def test_un_nombre_invalido_en_la_base_nunca_lee_fuera_del_directorio(
    client: TestClient, nombre: str, tmp_path: Path
) -> None:
    (tmp_path / "secreto.jpg").write_bytes(b"no debe salir")
    id = _ejemplar_propio()
    conexion = _conexion()
    try:
        conexion.execute("UPDATE ejemplares SET foto = ? WHERE id = ?", (nombre, id))
    finally:
        conexion.close()

    for ruta in (f"/coleccion/{id}/foto", f"/coleccion/{id}/foto/miniatura"):
        respuesta = client.get(ruta)
        assert respuesta.status_code == 404
        assert b"no debe salir" not in respuesta.content


def test_sin_sesion_la_ficha_y_las_imagenes_redirigen_al_acceso(anonimo: TestClient) -> None:
    id = _ejemplar_propio()
    _con_foto(id)

    for ruta in (f"/coleccion/{id}", f"/coleccion/{id}/foto", f"/coleccion/{id}/foto/miniatura"):
        respuesta = anonimo.get(ruta, follow_redirects=False)
        assert respuesta.status_code == 303, ruta
        assert respuesta.headers["location"] == "/acceso", ruta


def _subir(
    client: TestClient,
    csrf: str | None,
    id: int,
    datos: bytes | None,
    nombre: str = "orquidea.jpg",
    tipo: str = "image/jpeg",
) -> Response:
    formulario = {"csrf": csrf} if csrf is not None else {}
    archivos = {"foto": (nombre, datos, tipo)} if datos is not None else None
    return client.post(
        f"/coleccion/{id}/foto", data=formulario, files=archivos, follow_redirects=False
    )


def _foto_guardada(id: int) -> str | None:
    conexion = _conexion()
    try:
        ejemplar = obtener(conexion, id)
        assert ejemplar is not None
        return ejemplar.foto
    finally:
        conexion.close()


def test_subir_una_foto_con_gps_la_guarda_reducida_y_sin_metadatos(
    client: TestClient, sesion: Sesion
) -> None:
    id = _ejemplar_propio("Mi rara")

    respuesta = _subir(client, sesion.csrf, id, imagen_jpeg(4000, 3000, con_gps=True))

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == f"/coleccion/{id}"
    nombre = _foto_guardada(id)
    assert nombre is not None
    assert [a.name for a in _archivos()] == sorted([f"{nombre}.jpg", f"{nombre}-mini.jpg"])
    for archivo, ancho_maximo in ((f"{nombre}.jpg", 1600), (f"{nombre}-mini.jpg", 320)):
        datos = (app.state.directorio_fotos / archivo).read_bytes()
        with Image.open(io.BytesIO(datos)) as guardada:
            assert guardada.width <= ancho_maximo
            assert len(guardada.getexif()) == 0
        assert b"Exif" not in datos
        assert MARCADOR_XMP not in datos
        assert b"gps-secreto" not in datos
    assert f'src="/coleccion/{id}/foto"' in client.get(f"/coleccion/{id}").text


def test_subir_otra_foto_reemplaza_la_anterior_y_borra_sus_archivos(
    client: TestClient, sesion: Sesion
) -> None:
    id = _ejemplar_propio()
    _subir(client, sesion.csrf, id, imagen_jpeg(800, 600, con_gps=False))
    primera = _foto_guardada(id)

    respuesta = _subir(client, sesion.csrf, id, imagen_jpeg(600, 800, con_gps=False))

    assert respuesta.status_code == 303
    segunda = _foto_guardada(id)
    assert segunda is not None and segunda != primera
    assert len(_archivos()) == 2 and all(segunda in a.name for a in _archivos())


def test_subir_sin_el_token_csrf_da_403_y_no_guarda_nada(client: TestClient) -> None:
    id = _ejemplar_propio()

    respuesta = _subir(client, None, id, imagen_jpeg(800, 600))

    assert respuesta.status_code == 403
    assert _foto_guardada(id) is None and _archivos() == []


def test_sin_sesion_subir_redirige_al_acceso_y_no_guarda_nada(anonimo: TestClient) -> None:
    id = _ejemplar_propio()

    respuesta = _subir(anonimo, "cualquiera", id, imagen_jpeg(800, 600))

    assert respuesta.status_code == 303 and respuesta.headers["location"] == "/acceso"
    assert _foto_guardada(id) is None and _archivos() == []


@pytest.mark.parametrize(
    ("datos", "nombre", "tipo", "mensaje"),
    [
        (b"no soy una imagen", "nota.txt", "text/plain", "no es una imagen válida"),
        (b"no soy una imagen", "orquidea.jpg", "image/jpeg", "no es una imagen válida"),
        (b"", "vacia.jpg", "image/jpeg", "Elige una foto."),
    ],
)
def test_un_archivo_que_no_es_una_foto_da_422_y_no_guarda_nada(
    client: TestClient, sesion: Sesion, datos: bytes, nombre: str, tipo: str, mensaje: str
) -> None:
    id = _ejemplar_propio()

    respuesta = _subir(client, sesion.csrf, id, datos, nombre, tipo)

    assert respuesta.status_code == 422
    assert mensaje in respuesta.text and 'role="alert"' in respuesta.text
    assert 'type="file"' in respuesta.text
    assert _foto_guardada(id) is None and _archivos() == []


def test_un_gif_da_422_aunque_diga_ser_jpeg(client: TestClient, sesion: Sesion) -> None:
    id = _ejemplar_propio()
    entrada = io.BytesIO()
    Image.new("RGB", (40, 40)).save(entrada, "GIF")

    respuesta = _subir(client, sesion.csrf, id, entrada.getvalue(), "foto.jpg", "image/jpeg")

    assert respuesta.status_code == 422 and "JPEG, PNG o WebP" in respuesta.text
    assert _archivos() == []


def test_subir_sin_elegir_archivo_da_422(client: TestClient, sesion: Sesion) -> None:
    id = _ejemplar_propio()

    respuesta = _subir(client, sesion.csrf, id, None)

    assert respuesta.status_code == 422 and "Elige una foto." in respuesta.text
    assert _archivos() == []


def test_un_archivo_mayor_al_maximo_da_422_y_uno_mayor_al_cuerpo_permitido_da_413(
    client: TestClient, sesion: Sesion
) -> None:
    id = _ejemplar_propio()

    grande = _subir(client, sesion.csrf, id, b"\xff" * (TAMANO_MAXIMO + 1))
    enorme = _subir(client, sesion.csrf, id, b"\xff" * (LIMITE_DE_CUERPO + 1))

    assert grande.status_code == 422 and "10 MB" in grande.text
    assert enorme.status_code == 413
    assert _foto_guardada(id) is None and _archivos() == []


def test_subir_a_un_ejemplar_inexistente_da_404_y_no_deja_archivos(
    client: TestClient, sesion: Sesion
) -> None:
    assert _subir(client, sesion.csrf, 999, imagen_jpeg(800, 600)).status_code == 404
    assert _archivos() == []


def test_un_disco_lleno_da_500_controlado(
    client: TestClient, sesion: Sesion, monkeypatch: pytest.MonkeyPatch
) -> None:
    id = _ejemplar_propio()

    def sin_espacio(*_: object) -> bool:
        raise OSError("disco lleno")

    monkeypatch.setattr(rutas_coleccion, "poner_foto", sin_espacio)

    respuesta = _subir(client, sesion.csrf, id, imagen_jpeg(800, 600))

    assert respuesta.status_code == 500
    assert "No se pudo guardar la foto." in respuesta.text
    assert "disco lleno" not in respuesta.text
    assert 'type="file"' in respuesta.text


def test_subir_un_archivo_invalido_a_un_ejemplar_inexistente_da_404_y_no_500(
    client: TestClient, sesion: Sesion
) -> None:
    assert _subir(client, sesion.csrf, 999, b"no soy una imagen").status_code == 404
    assert _subir(client, sesion.csrf, 999, None).status_code == 404


def test_si_el_ejemplar_desaparece_al_guardar_la_respuesta_es_404(
    client: TestClient, sesion: Sesion, monkeypatch: pytest.MonkeyPatch
) -> None:
    id = _ejemplar_propio()
    monkeypatch.setattr(rutas_coleccion, "poner_foto", lambda *_: False)

    assert _subir(client, sesion.csrf, id, imagen_jpeg(800, 600)).status_code == 404


def test_la_lista_muestra_la_miniatura_enlazada_solo_de_los_ejemplares_con_foto(
    client: TestClient,
) -> None:
    con_foto = _ejemplar_propio("Con foto")
    sin_foto = _ejemplar_propio("Sin foto")
    _con_foto(con_foto)

    html = client.get("/coleccion").text

    assert html.count("<img") == 1
    assert f'href="/coleccion/{con_foto}"><img src="/coleccion/{con_foto}/foto/miniatura"' in html
    assert 'alt="Foto de Con foto"' in html and 'loading="lazy"' in html
    assert f"/coleccion/{sin_foto}/foto" not in html
    assert f'/coleccion/{con_foto}/foto"' not in html  # la lista no pide la imagen completa
