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


def acceder(anonimo: TestClient, contrasena: str = CONTRASENA) -> Response:
    return anonimo.post("/acceso", data={"contrasena": contrasena}, follow_redirects=False)


def test_el_formulario_de_acceso_pide_solo_la_contrasena(anonimo: TestClient) -> None:
    respuesta = anonimo.get("/acceso")

    assert respuesta.status_code == 200
    assert 'type="password"' in respuesta.text
    assert 'name="contrasena"' in respuesta.text
    assert 'method="post"' in respuesta.text
    assert 'autocomplete="current-password"' in respuesta.text


def test_la_contrasena_correcta_crea_la_sesion_y_redirige(anonimo: TestClient) -> None:
    respuesta = acceder(anonimo)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/"
    identificador = respuesta.cookies["__Host-sesion"]
    assert hashes_de_sesion() == [hashlib.sha256(identificador.encode()).hexdigest()]
    assert identificador not in hashes_de_sesion()


def test_la_cookie_es_httponly_samesite_lax_y_secure(anonimo: TestClient) -> None:
    cookie = acceder(anonimo).headers["set-cookie"].lower()

    assert "httponly" in cookie
    assert "samesite=lax" in cookie
    assert "secure" in cookie
    assert "path=/" in cookie
    assert "domain" not in cookie
    assert cookie.startswith("__host-sesion=")


def test_la_cookie_sin_secure_solo_si_el_entorno_lo_desactiva(
    anonimo: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ORQUIDEA_COOKIE_SEGURA", "0")

    cookie = acceder(anonimo).headers["set-cookie"].lower()

    assert cookie.startswith("sesion=")
    assert "secure" not in cookie
    assert "httponly" in cookie


def test_una_contrasena_incorrecta_muestra_el_error_y_no_crea_sesion(anonimo: TestClient) -> None:
    respuesta = acceder(anonimo, "otra")

    assert respuesta.status_code == 401
    assert "Contraseña incorrecta" in respuesta.text
    assert 'name="contrasena"' in respuesta.text
    assert "set-cookie" not in respuesta.headers
    assert hashes_de_sesion() == []


@pytest.mark.parametrize("configurado", [None, "", "basura"])
def test_sin_hash_valido_configurado_el_acceso_falla_cerrado(
    anonimo: TestClient, monkeypatch: pytest.MonkeyPatch, configurado: str | None
) -> None:
    if configurado is None:
        monkeypatch.delenv("ORQUIDEA_PASSWORD_HASH")
    else:
        monkeypatch.setenv("ORQUIDEA_PASSWORD_HASH", configurado)

    respuesta = acceder(anonimo)

    assert respuesta.status_code == 401
    assert hashes_de_sesion() == []


def test_cerrar_la_sesion_borra_la_fila_y_la_cookie(anonimo: TestClient) -> None:
    acceder(anonimo)
    otra = TestClient(app, base_url="https://testserver")
    acceder(otra)
    assert len(hashes_de_sesion()) == 2
    conexion = sqlite3.connect(app.state.ruta_base)
    id_hash = hashlib.sha256(anonimo.cookies["__Host-sesion"].encode()).hexdigest()
    (csrf,) = conexion.execute("SELECT csrf FROM sesiones WHERE id_hash = ?", (id_hash,)).fetchone()
    conexion.close()

    respuesta = anonimo.post("/salir", data={"csrf": csrf}, follow_redirects=False)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/acceso"
    assert "__Host-sesion=" in respuesta.headers["set-cookie"]
    assert "max-age=0" in respuesta.headers["set-cookie"].lower()
    assert len(hashes_de_sesion()) == 1


def test_cerrar_sin_sesion_redirige_sin_error(anonimo: TestClient) -> None:
    respuesta = anonimo.post("/salir", follow_redirects=False)

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/acceso"


def test_cinco_fallos_bloquean_incluso_la_contrasena_correcta(anonimo: TestClient) -> None:
    for _ in range(5):
        assert acceder(anonimo, "otra").status_code == 401

    respuesta = acceder(anonimo)

    assert respuesta.status_code == 429
    assert "Demasiados intentos" in respuesta.text
    assert hashes_de_sesion() == []


def test_cuatro_fallos_y_un_acierto_no_bloquean(anonimo: TestClient) -> None:
    for _ in range(4):
        acceder(anonimo, "otra")

    assert acceder(anonimo).status_code == 303
    for _ in range(4):
        assert acceder(anonimo, "otra").status_code == 401


def test_el_acceso_no_redirige_a_una_url_dada_por_el_usuario(anonimo: TestClient) -> None:
    respuesta = anonimo.post(
        "/acceso?siguiente=https://malo.example",
        data={"contrasena": CONTRASENA, "siguiente": "https://malo.example"},
        follow_redirects=False,
    )

    assert respuesta.headers["location"] == "/"


def test_los_accesos_se_registran_sin_la_contrasena(
    anonimo: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO, logger="orquidea.acceso"):
        acceder(anonimo, "secreto-erroneo")
        acceder(anonimo)
        for _ in range(5):
            acceder(anonimo, "x")
        acceder(anonimo)

    mensajes = [registro.getMessage() for registro in caplog.records]
    assert "acceso fallido" in mensajes
    assert "acceso correcto" in mensajes
    assert "acceso bloqueado" in mensajes
    assert not any("secreto-erroneo" in mensaje or CONTRASENA in mensaje for mensaje in mensajes)


def test_los_accesos_llegan_a_la_salida_de_error_con_la_configuracion_por_defecto_de_uvicorn(
    anonimo: TestClient, capsys: pytest.CaptureFixture[str]
) -> None:
    registro = logging.getLogger("orquidea.acceso")
    anteriores = list(registro.handlers)
    try:
        with anonimo:  # ejecuta el ciclo de vida, que configura el registro
            acceder(anonimo, "mala")
            acceder(anonimo)
    finally:
        for manejador in registro.handlers:
            if manejador not in anteriores:
                registro.removeHandler(manejador)
        registro.setLevel(logging.NOTSET)

    salida = capsys.readouterr().err
    assert "acceso fallido" in salida
    assert "acceso correcto" in salida
    assert CONTRASENA not in salida


def test_arrancar_dos_veces_no_duplica_el_manejador(anonimo: TestClient) -> None:
    registro = logging.getLogger("orquidea.acceso")
    anteriores = list(registro.handlers)
    try:
        with anonimo:
            pass
        with anonimo:
            pass
        nuevos = [m for m in registro.handlers if m not in anteriores]
    finally:
        for manejador in list(registro.handlers):
            if manejador not in anteriores:
                registro.removeHandler(manejador)
        registro.setLevel(logging.NOTSET)

    assert len(nuevos) == 1
