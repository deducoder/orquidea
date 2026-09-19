import re
import time
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from orquidea.datos.base import conectar
from orquidea.datos.ejemplares import agregar, listar
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
