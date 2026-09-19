import sqlite3
import time

import pytest
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

from orquidea.datos.sesiones import INACTIVIDAD_MAXIMA
from orquidea.web.app import RUTAS_PUBLICAS, app
from tests.conftest import iniciar_sesion


def rutas_de_la_aplicacion() -> list[tuple[str, str]]:
    rutas: list[tuple[str, str]] = []
    for ruta in app.routes:
        if isinstance(ruta, APIRoute):
            path = ruta.path.replace("{id}", "epidendrum-radicans")
            rutas.extend((metodo, path) for metodo in sorted(ruta.methods or set()))
    return rutas


def test_la_enumeracion_de_rutas_no_esta_vacia() -> None:
    assert ("GET", "/especies") in rutas_de_la_aplicacion()
    assert ("POST", "/salir") in rutas_de_la_aplicacion()


def test_sin_sesion_toda_ruta_salvo_las_publicas_redirige_al_acceso(anonimo: TestClient) -> None:
    protegidas = [(m, p) for m, p in rutas_de_la_aplicacion() if p not in RUTAS_PUBLICAS]
    assert len(protegidas) >= 4

    for metodo, path in protegidas:
        respuesta = anonimo.request(metodo, path, follow_redirects=False)

        assert respuesta.status_code == 303, (metodo, path)
        assert respuesta.headers["location"] == "/acceso", (metodo, path)


def test_las_rutas_publicas_son_solo_el_acceso_y_la_salud() -> None:
    assert RUTAS_PUBLICAS == {"/acceso", "/salud"}


def test_las_rutas_publicas_responden_sin_sesion(anonimo: TestClient) -> None:
    assert anonimo.get("/acceso").status_code == 200
    assert anonimo.get("/salud").status_code == 200
    assert anonimo.get("/static/htmx.min.js").status_code == 200


def test_htmx_sin_sesion_recibe_401_y_hx_redirect(anonimo: TestClient) -> None:
    respuesta = anonimo.get("/especies", headers={"HX-Request": "true"}, follow_redirects=False)

    assert respuesta.status_code == 401
    assert respuesta.headers["hx-redirect"] == "/acceso"
    assert "<form" not in respuesta.text


def test_con_sesion_las_paginas_se_ven(client: TestClient) -> None:
    assert client.get("/").status_code == 200
    assert client.get("/especies").status_code == 200
    assert client.get("/especies/epidendrum-radicans").status_code in (200, 404)


def test_una_cookie_inventada_no_vale(anonimo: TestClient) -> None:
    anonimo.cookies.set("__Host-sesion", "inventada")

    assert anonimo.get("/", follow_redirects=False).status_code == 303


def test_una_sesion_caducada_redirige_como_sin_sesion(anonimo: TestClient) -> None:
    iniciar_sesion(anonimo, ahora=int(time.time()) - INACTIVIDAD_MAXIMA - 10)

    respuesta = anonimo.get("/", follow_redirects=False)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/acceso"


def test_cada_peticion_autenticada_renueva_la_actividad(anonimo: TestClient) -> None:
    antes = int(time.time()) - 600
    iniciar_sesion(anonimo, ahora=antes)

    anonimo.get("/")

    conexion = sqlite3.connect(app.state.ruta_base)
    (actividad,) = conexion.execute("SELECT ultima_actividad FROM sesiones").fetchone()
    conexion.close()
    assert actividad >= int(time.time()) - 5


def test_una_ruta_nueva_sin_declararla_publica_queda_protegida(anonimo: TestClient) -> None:
    @app.get("/ruta-nueva-de-prueba")
    def nueva() -> dict[str, str]:
        return {"secreto": "x"}

    try:
        respuesta = anonimo.get("/ruta-nueva-de-prueba", follow_redirects=False)
    finally:
        app.router.routes.pop()

    assert respuesta.status_code == 303


@pytest.mark.parametrize("ruta", ["/docs", "/redoc", "/openapi.json"])
def test_la_documentacion_automatica_no_existe(client: TestClient, ruta: str) -> None:
    assert client.get(ruta, follow_redirects=False).status_code == 404
