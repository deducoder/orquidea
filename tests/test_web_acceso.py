import hashlib
import logging
import sqlite3

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

from orquidea.autenticacion import hashear_contrasena
from orquidea.web.app import app

CONTRASENA = "orquidea-2026"


@pytest.fixture(autouse=True)
def hash_configurado(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ORQUIDEA_PASSWORD_HASH", hashear_contrasena(CONTRASENA, n=2**4))
    monkeypatch.delenv("ORQUIDEA_COOKIE_SEGURA", raising=False)


def hashes_de_sesion() -> list[str]:
    conexion = sqlite3.connect(app.state.ruta_base)
    try:
        return [fila[0] for fila in conexion.execute("SELECT id_hash FROM sesiones")]
    finally:
        conexion.close()


def acceder(client: TestClient, contrasena: str = CONTRASENA) -> Response:
    return client.post("/acceso", data={"contrasena": contrasena}, follow_redirects=False)


def test_el_formulario_de_acceso_pide_solo_la_contrasena(client: TestClient) -> None:
    respuesta = client.get("/acceso")

    assert respuesta.status_code == 200
    assert 'type="password"' in respuesta.text
    assert 'name="contrasena"' in respuesta.text
    assert 'method="post"' in respuesta.text
    assert 'autocomplete="current-password"' in respuesta.text


def test_la_contrasena_correcta_crea_la_sesion_y_redirige(client: TestClient) -> None:
    respuesta = acceder(client)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/"
    identificador = respuesta.cookies["__Host-sesion"]
    assert hashes_de_sesion() == [hashlib.sha256(identificador.encode()).hexdigest()]
    assert identificador not in hashes_de_sesion()


def test_la_cookie_es_httponly_samesite_lax_y_secure(client: TestClient) -> None:
    cookie = acceder(client).headers["set-cookie"].lower()

    assert "httponly" in cookie
    assert "samesite=lax" in cookie
    assert "secure" in cookie
    assert "path=/" in cookie
    assert "domain" not in cookie
    assert cookie.startswith("__host-sesion=")


def test_la_cookie_sin_secure_solo_si_el_entorno_lo_desactiva(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ORQUIDEA_COOKIE_SEGURA", "0")

    cookie = acceder(client).headers["set-cookie"].lower()

    assert cookie.startswith("sesion=")
    assert "secure" not in cookie
    assert "httponly" in cookie


def test_una_contrasena_incorrecta_muestra_el_error_y_no_crea_sesion(client: TestClient) -> None:
    respuesta = acceder(client, "otra")

    assert respuesta.status_code == 401
    assert "Contraseña incorrecta" in respuesta.text
    assert 'name="contrasena"' in respuesta.text
    assert "set-cookie" not in respuesta.headers
    assert hashes_de_sesion() == []


@pytest.mark.parametrize("configurado", [None, "", "basura"])
def test_sin_hash_valido_configurado_el_acceso_falla_cerrado(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, configurado: str | None
) -> None:
    if configurado is None:
        monkeypatch.delenv("ORQUIDEA_PASSWORD_HASH")
    else:
        monkeypatch.setenv("ORQUIDEA_PASSWORD_HASH", configurado)

    respuesta = acceder(client)

    assert respuesta.status_code == 401
    assert hashes_de_sesion() == []


def test_cerrar_la_sesion_borra_la_fila_y_la_cookie(client: TestClient) -> None:
    acceder(client)
    otra = TestClient(app, base_url="https://testserver")
    acceder(otra)
    assert len(hashes_de_sesion()) == 2

    respuesta = client.post("/salir", follow_redirects=False)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/acceso"
    assert "__Host-sesion=" in respuesta.headers["set-cookie"]
    assert "max-age=0" in respuesta.headers["set-cookie"].lower()
    assert len(hashes_de_sesion()) == 1


def test_cerrar_sin_sesion_redirige_sin_error(client: TestClient) -> None:
    respuesta = client.post("/salir", follow_redirects=False)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/acceso"


def test_cinco_fallos_bloquean_incluso_la_contrasena_correcta(client: TestClient) -> None:
    for _ in range(5):
        assert acceder(client, "otra").status_code == 401

    respuesta = acceder(client)

    assert respuesta.status_code == 429
    assert "Demasiados intentos" in respuesta.text
    assert hashes_de_sesion() == []


def test_cuatro_fallos_y_un_acierto_no_bloquean(client: TestClient) -> None:
    for _ in range(4):
        acceder(client, "otra")

    assert acceder(client).status_code == 303
    for _ in range(4):
        assert acceder(client, "otra").status_code == 401


def test_el_acceso_no_redirige_a_una_url_dada_por_el_usuario(client: TestClient) -> None:
    respuesta = client.post(
        "/acceso?siguiente=https://malo.example",
        data={"contrasena": CONTRASENA, "siguiente": "https://malo.example"},
        follow_redirects=False,
    )

    assert respuesta.headers["location"] == "/"


def test_los_accesos_se_registran_sin_la_contrasena(
    client: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO, logger="orquidea.acceso"):
        acceder(client, "secreto-erroneo")
        acceder(client)
        for _ in range(5):
            acceder(client, "x")
        acceder(client)

    mensajes = [registro.getMessage() for registro in caplog.records]
    assert "acceso fallido" in mensajes
    assert "acceso correcto" in mensajes
    assert "acceso bloqueado" in mensajes
    assert not any("secreto-erroneo" in mensaje or CONTRASENA in mensaje for mensaje in mensajes)
