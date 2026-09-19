import re
import time
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

from orquidea.datos.base import conectar
from orquidea.datos.ejemplares import agregar, agregar_sin_especie, listar
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
