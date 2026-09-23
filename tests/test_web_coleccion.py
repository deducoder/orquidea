import io
import re
import time
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response
from PIL import Image

from orquidea.datos.almacen_fotos import DirectorioDeFotosNoEscribible, poner_foto
from orquidea.datos.base import conectar
from orquidea.datos.ejemplares import (
    actualizar,
    agregar,
    agregar_sin_especie,
    listar,
    obtener,
)
from orquidea.datos.fotos import procesar_foto
from orquidea.datos.sesiones import Sesion
from orquidea.web.app import app
from tests.fabricas import especie

RADICANS = "epidendrum-radicans"


def ejemplares_guardados() -> list[str | None]:
    conexion = conectar(app.state.ruta_base)
    try:
        return [e.especie_id for e in listar(conexion)]
    finally:
        conexion.close()


def guardar(especie_id: str, ahora: int = 1_780_000_000) -> None:
    conexion = conectar(app.state.ruta_base)
    try:
        agregar(conexion, especie_id, ahora)
    finally:
        conexion.close()


def test_agregar_del_catalogo_crea_el_ejemplar_y_redirige_a_la_lista(
    client: TestClient, sesion: Sesion
) -> None:
    app.state.catalogo = [especie()]

    respuesta = client.post(
        "/coleccion", data={"especie_id": RADICANS, "csrf": sesion.csrf}, follow_redirects=False
    )

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/coleccion"
    assert ejemplares_guardados() == [RADICANS]


def test_una_especie_inexistente_da_404_y_no_guarda(client: TestClient, sesion: Sesion) -> None:
    app.state.catalogo = [especie()]

    respuesta = client.post("/coleccion", data={"especie_id": "no-existe", "csrf": sesion.csrf})

    assert respuesta.status_code == 404
    assert ejemplares_guardados() == []


def test_sin_especie_id_da_422_y_no_guarda(client: TestClient, sesion: Sesion) -> None:
    respuesta = client.post("/coleccion", data={"csrf": sesion.csrf})

    assert respuesta.status_code == 422
    assert ejemplares_guardados() == []


def test_sin_token_da_403_y_no_guarda(client: TestClient) -> None:
    app.state.catalogo = [especie()]

    respuesta = client.post("/coleccion", data={"especie_id": RADICANS})

    assert respuesta.status_code == 403
    assert ejemplares_guardados() == []


def test_sin_sesion_redirige_al_acceso_y_no_guarda(anonimo: TestClient) -> None:
    app.state.catalogo = [especie()]

    respuesta = anonimo.post("/coleccion", data={"especie_id": RADICANS}, follow_redirects=False)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/acceso"
    assert ejemplares_guardados() == []


def test_la_coleccion_vacia_invita_a_agregar_desde_el_catalogo(client: TestClient) -> None:
    html = client.get("/coleccion").text

    assert "Aún no tienes ejemplares" in html
    assert 'href="/especies"' in html


def test_dos_ejemplares_de_la_misma_especie_aparecen_como_dos_entradas(client: TestClient) -> None:
    app.state.catalogo = [especie(), especie("laelia-anceps", "Laelia anceps")]
    guardar(RADICANS)
    guardar(RADICANS)
    guardar("laelia-anceps")

    html = client.get("/coleccion").text

    assert html.count("<li") == 3
    assert html.count(f'href="/especies/{RADICANS}"') == 2
    assert html.count("Epidendrum radicans") == 2
    assert 'href="/especies/laelia-anceps"' in html


def test_la_lista_muestra_la_fecha_de_alta_en_utc(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    app.state.catalogo = [especie()]
    alta = int(datetime(2026, 5, 28, 2, 0, tzinfo=UTC).timestamp())
    guardar(RADICANS, ahora=alta)
    monkeypatch.setenv("TZ", "America/Mexico_City")  # allí todavía es el 27
    time.tzset()
    try:
        html = client.get("/coleccion").text
    finally:
        monkeypatch.undo()
        time.tzset()

    assert "2026-05-28" in html


def test_una_especie_desaparecida_del_catalogo_se_lista_con_aviso(client: TestClient) -> None:
    app.state.catalogo = [especie()]
    guardar("ya-no-esta")

    respuesta = client.get("/coleccion")

    assert respuesta.status_code == 200
    assert "ya-no-esta" in respuesta.text
    assert "ya no está en el catálogo" in respuesta.text


def test_el_nombre_cientifico_se_escapa(client: TestClient) -> None:
    app.state.catalogo = [especie(nombre="<script>alert(1)</script>")]
    guardar(RADICANS)

    html = client.get("/coleccion").text

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_la_ficha_trae_el_boton_de_agregar_con_el_token(client: TestClient, sesion: Sesion) -> None:
    app.state.catalogo = [especie()]

    html = client.get(f"/especies/{RADICANS}").text

    formulario = re.search(r'<form method="post" action="/coleccion">.*?</form>', html, re.S)
    assert formulario is not None
    assert f'name="especie_id" value="{RADICANS}"' in formulario.group()
    assert f'name="csrf" value="{sesion.csrf}"' in formulario.group()
    assert "Agregar a mi colección" in formulario.group()


def test_la_cabecera_enlaza_a_mi_coleccion(client: TestClient) -> None:
    assert 'href="/coleccion"' in client.get("/especies").text


def test_la_lista_no_trae_javascript_nuevo(client: TestClient) -> None:
    html = client.get("/coleccion").text

    assert html.count("<script") == 1  # solo htmx, de la plantilla base


def guardar_propio(nombre: str, notas: str = "") -> None:
    conexion = conectar(app.state.ruta_base)
    try:
        agregar_sin_especie(conexion, nombre, notas, 1_780_000_000)
    finally:
        conexion.close()


def ejemplares_propios() -> list[tuple[str | None, str, str]]:
    conexion = conectar(app.state.ruta_base)
    try:
        return [(e.especie_id, e.nombre, e.notas) for e in listar(conexion)]
    finally:
        conexion.close()


def enviar_propio(client: TestClient, sesion: Sesion, nombre: str, notas: str = "") -> Response:
    return client.post(
        "/coleccion/nuevo",
        data={"nombre": nombre, "notas": notas, "csrf": sesion.csrf},
        follow_redirects=False,
    )


def test_mi_coleccion_enlaza_al_formulario_de_plantas_fuera_del_catalogo(
    client: TestClient,
) -> None:
    assert 'href="/coleccion/nuevo"' in client.get("/coleccion").text


def test_el_titulo_de_mi_coleccion_es_texto_y_el_enlace_aparece_una_vez(
    client: TestClient,
) -> None:
    html = client.get("/coleccion").text
    titulo = re.search(r"<title>(.*?)</title>", html, re.S)

    assert titulo is not None
    assert titulo.group(1) == "Mi colección — Orquídea"
    assert html.count('href="/coleccion/nuevo"') == 1


def test_el_formulario_de_planta_propia_trae_los_campos_y_el_token(
    client: TestClient, sesion: Sesion
) -> None:
    html = client.get("/coleccion/nuevo").text

    formulario = re.search(r'<form method="post" action="/coleccion/nuevo">.*?</form>', html, re.S)
    assert formulario is not None
    assert 'name="nombre"' in formulario.group()
    assert 'name="notas"' in formulario.group()
    assert f'name="csrf" value="{sesion.csrf}"' in formulario.group()
    assert html.count("<script") == 1


def test_una_planta_fuera_del_catalogo_se_guarda_recortada_y_redirige(
    client: TestClient, sesion: Sesion
) -> None:
    respuesta = enviar_propio(
        client, sesion, "  Cattleya de mi abuela ", "Regalo de 2019; florece en enero"
    )

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/coleccion"
    assert ejemplares_propios() == [
        (None, "Cattleya de mi abuela", "Regalo de 2019; florece en enero")
    ]


def test_la_planta_propia_se_lista_sin_enlace_y_con_sus_notas(client: TestClient) -> None:
    guardar_propio("Cattleya de mi abuela", "Regalo de 2019\nflorece en enero")

    html = client.get("/coleccion").text

    assert "Cattleya de mi abuela" in html
    assert "Regalo de 2019\nflorece en enero" in html
    assert 'style="white-space: pre-line"' in html
    assert "/especies/" not in html


def test_un_ejemplar_sin_notas_no_trae_bloque_de_notas(client: TestClient) -> None:
    guardar_propio("Sin notas")

    assert "pre-line" not in client.get("/coleccion").text


def test_un_ejemplar_del_catalogo_con_notas_las_muestra(client: TestClient) -> None:
    app.state.catalogo = [especie()]
    conexion = conectar(app.state.ruta_base)
    agregar(conexion, RADICANS, 1_780_000_000)
    conexion.execute("UPDATE ejemplares SET notas = 'Nota del ejemplar'")
    conexion.close()

    assert "Nota del ejemplar" in client.get("/coleccion").text


def test_nombre_y_notas_con_html_se_escapan(client: TestClient) -> None:
    guardar_propio("<b>negrita</b>", "<img src=x onerror=alert(1)>")

    html = client.get("/coleccion").text

    assert "<b>negrita</b>" not in html
    assert "<img" not in html
    assert "&lt;b&gt;negrita&lt;/b&gt;" in html


@pytest.mark.parametrize("nombre", ["", "   "])
def test_un_nombre_vacio_da_422_conserva_lo_escrito_y_no_guarda(
    client: TestClient, sesion: Sesion, nombre: str
) -> None:
    respuesta = enviar_propio(client, sesion, nombre, "mis notas")

    assert respuesta.status_code == 422
    assert "El nombre es obligatorio." in respuesta.text
    assert "mis notas" in respuesta.text
    assert ejemplares_propios() == []


def test_el_formulario_conserva_el_nombre_al_fallar_por_las_notas(
    client: TestClient, sesion: Sesion
) -> None:
    respuesta = enviar_propio(client, sesion, "Mi rara", "n" * 2001)

    assert respuesta.status_code == 422
    assert "Las notas no pueden pasar de 2000 caracteres." in respuesta.text
    assert 'value="Mi rara"' in respuesta.text
    assert ejemplares_propios() == []


def test_un_nombre_de_121_caracteres_da_422(client: TestClient, sesion: Sesion) -> None:
    respuesta = enviar_propio(client, sesion, "x" * 121)

    assert respuesta.status_code == 422
    assert ejemplares_propios() == []


def test_lo_escrito_se_escapa_al_volver_a_mostrar_el_formulario(
    client: TestClient, sesion: Sesion
) -> None:
    respuesta = enviar_propio(client, sesion, '"><script>alert(1)</script>', "n" * 2001)

    assert respuesta.status_code == 422
    assert "<script>alert(1)</script>" not in respuesta.text
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in respuesta.text


def test_planta_propia_sin_token_da_403_y_no_guarda(client: TestClient) -> None:
    respuesta = client.post("/coleccion/nuevo", data={"nombre": "Mi rara"})

    assert respuesta.status_code == 403
    assert ejemplares_propios() == []


def test_planta_propia_sin_sesion_redirige_al_acceso_y_no_guarda(anonimo: TestClient) -> None:
    respuesta = anonimo.post("/coleccion/nuevo", data={"nombre": "Mi rara"}, follow_redirects=False)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/acceso"
    assert ejemplares_propios() == []


def test_las_notas_se_escapan_al_volver_a_mostrar_el_formulario(
    client: TestClient, sesion: Sesion
) -> None:
    respuesta = enviar_propio(client, sesion, "", "</textarea><script>alert(1)</script>")

    assert respuesta.status_code == 422
    assert "<script>alert(1)</script>" not in respuesta.text
    assert "&lt;/textarea&gt;&lt;script&gt;" in respuesta.text


def alta(especie_id: str | None, nombre: str = "", notas: str = "") -> int:
    conexion = conectar(app.state.ruta_base)
    try:
        if especie_id is None:
            return agregar_sin_especie(conexion, nombre, notas, 1_780_000_000).id
        ejemplar = agregar(conexion, especie_id, 1_780_000_000)
        actualizar(conexion, ejemplar.id, nombre, notas)
        return ejemplar.id
    finally:
        conexion.close()


def fila(id: int) -> tuple[str | None, str, str] | None:
    conexion = conectar(app.state.ruta_base)
    try:
        e = obtener(conexion, id)
        return None if e is None else (e.especie_id, e.nombre, e.notas)
    finally:
        conexion.close()


def editar(client: TestClient, sesion: Sesion, id: int, nombre: str, notas: str = "") -> Response:
    return client.post(
        f"/coleccion/{id}/editar",
        data={"nombre": nombre, "notas": notas, "csrf": sesion.csrf},
        follow_redirects=False,
    )


def test_el_formulario_de_edicion_trae_los_datos_actuales_y_el_token(
    client: TestClient, sesion: Sesion
) -> None:
    id = alta(None, "Mi rara", "Florece en marzo")

    html = client.get(f"/coleccion/{id}/editar").text

    formulario = re.search(
        rf'<form method="post" action="/coleccion/{id}/editar">.*?</form>', html, re.S
    )
    assert formulario is not None
    assert 'value="Mi rara"' in formulario.group()
    assert ">Florece en marzo</textarea>" in formulario.group()
    assert f'name="csrf" value="{sesion.csrf}"' in formulario.group()


def test_editar_un_ejemplar_del_catalogo_muestra_su_especie_como_texto(client: TestClient) -> None:
    app.state.catalogo = [especie()]
    id = alta(RADICANS, "Mi primera")

    html = client.get(f"/coleccion/{id}/editar").text

    assert "Epidendrum radicans" in html
    assert 'name="especie_id"' not in html
    assert 'value="Mi primera"' in html


def test_editar_cambia_solo_ese_ejemplar(client: TestClient, sesion: Sesion) -> None:
    app.state.catalogo = [especie()]
    uno = alta(RADICANS)
    otro = alta(RADICANS, "", "notas del otro")

    respuesta = editar(client, sesion, uno, "  Mi primera ", "Florece en marzo")

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/coleccion"
    assert fila(uno) == (RADICANS, "Mi primera", "Florece en marzo")
    assert fila(otro) == (RADICANS, "", "notas del otro")


def test_editar_un_ejemplar_propio_cambia_nombre_y_notas(
    client: TestClient, sesion: Sesion
) -> None:
    id = alta(None, "Vieja", "vieja")

    editar(client, sesion, id, "Nueva", "nueva")

    assert fila(id) == (None, "Nueva", "nueva")


def test_editar_no_puede_cambiar_la_especie(client: TestClient, sesion: Sesion) -> None:
    app.state.catalogo = [especie(), especie("laelia-anceps", "Laelia anceps")]
    id = alta(RADICANS)

    client.post(
        f"/coleccion/{id}/editar",
        data={"nombre": "x", "notas": "", "csrf": sesion.csrf, "especie_id": "laelia-anceps"},
    )

    assert fila(id) == (RADICANS, "x", "")


@pytest.mark.parametrize("nombre", ["", "   "])
def test_un_ejemplar_propio_sin_nombre_da_422_conserva_lo_escrito_y_no_cambia(
    client: TestClient, sesion: Sesion, nombre: str
) -> None:
    id = alta(None, "Mi rara", "vieja")

    respuesta = editar(client, sesion, id, nombre, "nueva")

    assert respuesta.status_code == 422
    assert "El nombre es obligatorio." in respuesta.text
    assert ">nueva</textarea>" in respuesta.text
    assert fila(id) == (None, "Mi rara", "vieja")


def test_los_limites_de_nombre_y_notas_dan_422_al_editar(
    client: TestClient, sesion: Sesion
) -> None:
    id = alta(None, "Mi rara", "vieja")

    assert editar(client, sesion, id, "x" * 121).status_code == 422
    assert editar(client, sesion, id, "ok", "n" * 2001).status_code == 422
    assert fila(id) == (None, "Mi rara", "vieja")


def test_un_ejemplar_del_catalogo_puede_quedarse_sin_nombre_propio(
    client: TestClient, sesion: Sesion
) -> None:
    app.state.catalogo = [especie()]
    id = alta(RADICANS, "Mi primera", "n")

    respuesta = editar(client, sesion, id, "", "n")

    assert respuesta.status_code == 303
    assert fila(id) == (RADICANS, "", "n")


def test_editar_un_id_inexistente_da_404_en_get_y_post(client: TestClient, sesion: Sesion) -> None:
    assert client.get("/coleccion/999/editar").status_code == 404
    assert editar(client, sesion, 999, "x").status_code == 404


def test_editar_con_un_id_no_numerico_da_422(client: TestClient) -> None:
    assert client.get("/coleccion/abc/editar").status_code == 422


def test_editar_sin_token_da_403_y_no_cambia(client: TestClient) -> None:
    id = alta(None, "Mi rara", "vieja")

    respuesta = client.post(f"/coleccion/{id}/editar", data={"nombre": "x", "notas": "y"})

    assert respuesta.status_code == 403
    assert fila(id) == (None, "Mi rara", "vieja")


def test_editar_sin_sesion_redirige_al_acceso_y_no_cambia(anonimo: TestClient) -> None:
    id = alta(None, "Mi rara", "vieja")

    respuesta = anonimo.post(
        f"/coleccion/{id}/editar", data={"nombre": "x", "notas": "y"}, follow_redirects=False
    )

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/acceso"
    assert fila(id) == (None, "Mi rara", "vieja")


def test_lo_escrito_se_escapa_al_volver_a_mostrar_la_edicion(
    client: TestClient, sesion: Sesion
) -> None:
    id = alta(None, "Mi rara")

    respuesta = editar(client, sesion, id, '"><script>alert(1)</script>', "n" * 2001)

    assert respuesta.status_code == 422
    assert "<script>alert(1)</script>" not in respuesta.text


def test_la_lista_trae_editar_y_el_nombre_propio_de_un_ejemplar_del_catalogo(
    client: TestClient,
) -> None:
    app.state.catalogo = [especie()]
    con_nombre = alta(RADICANS, "Mi primera")
    propio = alta(None, "Mi rara")

    html = client.get("/coleccion").text

    assert f'href="/coleccion/{con_nombre}/editar"' in html
    assert f'href="/coleccion/{propio}/editar"' in html
    assert "Mi primera" in html


def test_editar_un_ejemplar_cuya_especie_desaparecio_muestra_el_identificador(
    client: TestClient,
) -> None:
    app.state.catalogo = [especie()]
    id = alta("ya-no-esta")

    html = client.get(f"/coleccion/{id}/editar").text

    assert "ya-no-esta" in html
    assert "Nombre propio (opcional)" in html


def test_el_nombre_cientifico_de_la_edicion_se_escapa(client: TestClient) -> None:
    app.state.catalogo = [especie(nombre="<script>alert(1)</script>")]
    id = alta(RADICANS)

    html = client.get(f"/coleccion/{id}/editar").text

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_el_nombre_es_requerido_en_el_formulario_solo_sin_especie(client: TestClient) -> None:
    app.state.catalogo = [especie()]
    propio = alta(None, "Mi rara")
    del_catalogo = alta(RADICANS)

    def campo_nombre(id: int) -> str:
        html = client.get(f"/coleccion/{id}/editar").text
        campo = re.search(r'<input id="nombre"[^>]*>', html)
        assert campo is not None
        return campo.group()

    assert " required" in campo_nombre(propio)
    assert " required" not in campo_nombre(del_catalogo)


def quitar_ejemplar(client: TestClient, sesion: Sesion, id: int) -> Response:
    return client.post(
        f"/coleccion/{id}/quitar", data={"csrf": sesion.csrf}, follow_redirects=False
    )


def test_la_confirmacion_de_baja_muestra_el_ejemplar_y_no_quita_nada(
    client: TestClient, sesion: Sesion
) -> None:
    app.state.catalogo = [especie()]
    id = alta(RADICANS, "Mi primera")

    respuesta = client.get(f"/coleccion/{id}/quitar")

    assert respuesta.status_code == 200
    assert "Epidendrum radicans" in respuesta.text
    assert "Mi primera" in respuesta.text
    formulario = re.search(
        rf'<form method="post" action="/coleccion/{id}/quitar">.*?</form>', respuesta.text, re.S
    )
    assert formulario is not None
    assert f'name="csrf" value="{sesion.csrf}"' in formulario.group()
    assert fila(id) is not None


def test_la_confirmacion_de_un_ejemplar_propio_muestra_su_nombre(client: TestClient) -> None:
    id = alta(None, "Cattleya de mi abuela")

    assert "Cattleya de mi abuela" in client.get(f"/coleccion/{id}/quitar").text


def test_confirmar_la_baja_quita_solo_ese_ejemplar(client: TestClient, sesion: Sesion) -> None:
    app.state.catalogo = [especie()]
    uno = alta(RADICANS, "", "notas de uno")
    otro = alta(RADICANS, "", "notas del otro")
    propio = alta(None, "Mi rara")

    respuesta = quitar_ejemplar(client, sesion, uno)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/coleccion"
    assert fila(uno) is None
    assert fila(otro) == (RADICANS, "", "notas del otro")
    assert fila(propio) == (None, "Mi rara", "")
    assert "notas del otro" in client.get("/coleccion").text


def test_quitar_un_ejemplar_con_foto_borra_sus_archivos(client: TestClient, sesion: Sesion) -> None:
    con_foto = alta(None, "Con foto")
    sin_foto = alta(None, "Sin foto")
    entrada = io.BytesIO()
    Image.new("RGB", (60, 40), (10, 200, 90)).save(entrada, "JPEG")
    conexion = conectar(app.state.ruta_base)
    try:
        assert poner_foto(
            conexion, app.state.directorio_fotos, con_foto, procesar_foto(entrada.getvalue())
        )
    finally:
        conexion.close()
    assert len(list(app.state.directorio_fotos.iterdir())) == 2

    respuesta = quitar_ejemplar(client, sesion, con_foto)

    assert respuesta.status_code == 303
    assert fila(con_foto) is None and fila(sin_foto) is not None
    assert list(app.state.directorio_fotos.iterdir()) == []


def test_un_directorio_de_fotos_que_no_se_puede_escribir_detiene_el_arranque(
    anonimo: TestClient, tmp_path: Path
) -> None:
    archivo = tmp_path / "archivo"
    archivo.write_text("no soy un directorio")
    app.state.directorio_fotos = archivo / "fotos"

    with pytest.raises(DirectorioDeFotosNoEscribible, match="archivo"), TestClient(app):
        pass


def test_quitar_un_id_inexistente_da_404_en_get_y_post(client: TestClient, sesion: Sesion) -> None:
    alta(None, "Mi rara")

    assert client.get("/coleccion/999/quitar").status_code == 404
    assert quitar_ejemplar(client, sesion, 999).status_code == 404
    assert len(ejemplares_propios()) == 1


def test_quitar_con_un_id_no_numerico_da_422(client: TestClient) -> None:
    assert client.get("/coleccion/abc/quitar").status_code == 422


def test_quitar_sin_token_da_403_y_la_fila_sigue(client: TestClient) -> None:
    id = alta(None, "Mi rara")

    assert client.post(f"/coleccion/{id}/quitar").status_code == 403
    assert fila(id) is not None


def test_quitar_sin_sesion_redirige_al_acceso_y_la_fila_sigue(anonimo: TestClient) -> None:
    id = alta(None, "Mi rara")

    respuesta = anonimo.post(f"/coleccion/{id}/quitar", follow_redirects=False)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/acceso"
    assert fila(id) is not None


def test_la_confirmacion_escapa_el_nombre(client: TestClient) -> None:
    id = alta(None, "<script>alert(1)</script>")

    html = client.get(f"/coleccion/{id}/quitar").text

    assert "<script>alert(1)</script>" not in html


def test_la_lista_trae_quitar_en_cada_ejemplar(client: TestClient) -> None:
    app.state.catalogo = [especie()]
    uno = alta(RADICANS)
    propio = alta(None, "Mi rara")

    html = client.get("/coleccion").text

    assert f'href="/coleccion/{uno}/quitar"' in html
    assert f'href="/coleccion/{propio}/quitar"' in html
