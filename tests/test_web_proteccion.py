import hmac
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


def filas_de_sesion() -> list[tuple[str, str]]:
    conexion = sqlite3.connect(app.state.ruta_base)
    try:
        return conexion.execute("SELECT id_hash, csrf FROM sesiones").fetchall()
    finally:
        conexion.close()


def test_un_post_sin_token_da_403_y_no_cambia_nada(client: TestClient) -> None:
    respuesta = client.post("/salir", follow_redirects=False)

    assert respuesta.status_code == 403
    assert len(filas_de_sesion()) == 1


@pytest.mark.parametrize("token", ["", "otro-token"])
def test_un_post_con_un_token_incorrecto_da_403(client: TestClient, token: str) -> None:
    for como in ({"data": {"csrf": token}}, {"headers": {"X-CSRF-Token": token}}):
        respuesta = client.post("/salir", follow_redirects=False, **como)  # type: ignore[arg-type]

        assert respuesta.status_code == 403
    assert len(filas_de_sesion()) == 1


def test_el_token_de_otra_sesion_no_vale(anonimo: TestClient) -> None:
    iniciar_sesion(anonimo)
    otra = iniciar_sesion(TestClient(app, base_url="https://testserver"))

    respuesta = anonimo.post("/salir", data={"csrf": otra.csrf}, follow_redirects=False)

    assert respuesta.status_code == 403
    assert len(filas_de_sesion()) == 2


def test_un_post_con_el_token_en_el_formulario_se_procesa(anonimo: TestClient) -> None:
    sesion = iniciar_sesion(anonimo)

    respuesta = anonimo.post("/salir", data={"csrf": sesion.csrf}, follow_redirects=False)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/acceso"
    assert filas_de_sesion() == []


def test_un_post_con_el_token_en_la_cabecera_se_procesa(anonimo: TestClient) -> None:
    sesion = iniciar_sesion(anonimo)

    respuesta = anonimo.post(
        "/salir", headers={"X-CSRF-Token": sesion.csrf}, follow_redirects=False
    )

    assert respuesta.status_code == 303
    assert filas_de_sesion() == []


def test_el_token_se_compara_en_tiempo_constante(
    anonimo: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    sesion = iniciar_sesion(anonimo)
    llamadas: list[int] = []
    original = hmac.compare_digest

    def espia(a: bytes, b: bytes) -> bool:
        llamadas.append(1)
        return original(a, b)

    monkeypatch.setattr(hmac, "compare_digest", espia)

    anonimo.post("/salir", data={"csrf": sesion.csrf}, follow_redirects=False)

    assert llamadas


def test_las_paginas_autenticadas_traen_salir_con_el_token_y_el_de_htmx(
    anonimo: TestClient,
) -> None:
    sesion = iniciar_sesion(anonimo)

    html = anonimo.get("/especies").text

    assert 'action="/salir"' in html
    assert f'name="csrf" value="{sesion.csrf}"' in html
    assert f"""hx-headers='{{"X-CSRF-Token": "{sesion.csrf}"}}'""" in html


def test_el_formulario_de_acceso_no_trae_token_ni_boton_de_salir(anonimo: TestClient) -> None:
    html = anonimo.get("/acceso").text

    assert "/salir" not in html
    assert "csrf" not in html.lower()


RUTAS_PARA_CABECERAS = ["/acceso", "/salud", "/static/htmx.min.js", "/no-existe", "/especies", "/"]


@pytest.mark.parametrize("ruta", RUTAS_PARA_CABECERAS)
def test_toda_respuesta_trae_las_cabeceras_de_seguridad(anonimo: TestClient, ruta: str) -> None:
    cabeceras = anonimo.get(ruta, follow_redirects=False).headers

    assert cabeceras["x-content-type-options"] == "nosniff"
    assert cabeceras["referrer-policy"] == "same-origin"
    assert cabeceras["x-frame-options"] == "DENY"
    assert "default-src 'self'" in cabeceras["content-security-policy"]
    assert "frame-ancestors 'none'" in cabeceras["content-security-policy"]


def test_las_respuestas_de_htmx_y_las_autenticadas_tambien(client: TestClient) -> None:
    assert "x-frame-options" in client.get("/").headers
    assert "x-frame-options" in client.get("/", headers={"HX-Request": "true"}).headers
    assert "x-frame-options" in client.post("/salir", follow_redirects=False).headers  # 403


def test_la_csp_no_permite_scripts_en_linea(anonimo: TestClient) -> None:
    csp = anonimo.get("/acceso").headers["content-security-policy"]
    directivas = {d.split()[0]: d for d in (parte.strip() for parte in csp.split(";")) if d}

    assert "unsafe-inline" not in directivas["default-src"]
    assert "script-src" not in directivas or "unsafe-inline" not in directivas["script-src"]
    assert "'unsafe-inline'" in directivas["style-src"]
    assert "form-action 'self'" in csp
    assert "base-uri 'none'" in csp


@pytest.mark.parametrize("ruta", ["/acceso", "/salud", "/especies", "/no-existe"])
def test_las_paginas_y_las_redirecciones_no_se_guardan_en_cache(
    anonimo: TestClient, ruta: str
) -> None:
    assert anonimo.get(ruta, follow_redirects=False).headers["cache-control"] == "no-store"


def test_los_estaticos_se_pueden_guardar_en_cache(anonimo: TestClient) -> None:
    assert "no-store" not in anonimo.get("/static/htmx.min.js").headers.get("cache-control", "")


def test_hsts_solo_cuando_la_cookie_es_secure(
    anonimo: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert anonimo.get("/salud").headers["strict-transport-security"] == "max-age=31536000"

    monkeypatch.setenv("ORQUIDEA_COOKIE_SEGURA", "0")

    assert "strict-transport-security" not in anonimo.get("/salud").headers
