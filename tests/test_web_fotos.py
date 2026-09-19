import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from orquidea.datos.almacen_fotos import poner_foto
from orquidea.datos.base import conectar
from orquidea.datos.ejemplares import agregar, agregar_sin_especie, obtener
from orquidea.datos.fotos import procesar_foto
from orquidea.web.app import app
from tests.fabricas import especie, imagen_jpeg

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
