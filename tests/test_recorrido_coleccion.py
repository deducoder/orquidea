"""Recorrido de la métrica líder del brief, sin atajos y sobre el catálogo real."""

import re

import pytest
from fastapi.testclient import TestClient

from orquidea.autenticacion import hashear_contrasena
from orquidea.datos.base import abrir_base, conectar
from orquidea.datos.ejemplares import listar
from orquidea.web.app import app

CONTRASENA = "orquidea-2026"
ESPECIE = "epidendrum-radicans"


def test_iniciar_sesion_agregar_un_ejemplar_del_catalogo_y_verlo(
    anonimo: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ORQUIDEA_PASSWORD_HASH", hashear_contrasena(CONTRASENA, n=2**4))

    # 1. Sin sesión, la colección lleva al acceso.
    assert anonimo.get("/coleccion", follow_redirects=False).headers["location"] == "/acceso"

    # 2. Inicia sesión con la contraseña.
    acceso = anonimo.post("/acceso", data={"contrasena": CONTRASENA}, follow_redirects=False)
    assert acceso.status_code == 303

    # 3. Abre la ficha de una especie real del catálogo y agrega el ejemplar con su propio botón.
    ficha = anonimo.get(f"/especies/{ESPECIE}")
    assert ficha.status_code == 200
    formulario = re.search(r'<form method="post" action="/coleccion">.*?</form>', ficha.text, re.S)
    assert formulario is not None
    token = re.search(r'name="csrf" value="([^"]+)"', formulario.group())
    assert token is not None
    agregado = anonimo.post(
        "/coleccion",
        data={"especie_id": ESPECIE, "csrf": token.group(1)},
        follow_redirects=True,
    )

    # 4. Aterriza en "Mi colección" y ve el ejemplar con el enlace a los cuidados de su especie.
    assert str(agregado.url).endswith("/coleccion")
    assert "Epidendrum radicans" in agregado.text
    assert f'href="/especies/{ESPECIE}"' in agregado.text

    # 5. El ejemplar sigue ahí tras reabrir la base (persistencia).
    assert [e.especie_id for e in listar(abrir_base(app.state.ruta_base))] == [ESPECIE]


def test_registrar_un_riego_y_ver_el_ultimo_en_la_ficha_del_ejemplar(
    anonimo: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Métrica líder del brief de e4 (RF-06), por la interfaz y hasta la baja del ejemplar."""
    monkeypatch.setenv("ORQUIDEA_PASSWORD_HASH", hashear_contrasena(CONTRASENA, n=2**4))
    anonimo.post("/acceso", data={"contrasena": CONTRASENA}, follow_redirects=False)

    # 1. Agrega un ejemplar desde la ficha de la especie y abre su ficha.
    especie = anonimo.get(f"/especies/{ESPECIE}")
    token = re.search(r'name="csrf" value="([^"]+)"', especie.text)
    assert token is not None
    anonimo.post("/coleccion", data={"especie_id": ESPECIE, "csrf": token.group(1)})
    (ejemplar,) = listar(abrir_base(app.state.ruta_base))
    ficha = anonimo.get(f"/coleccion/{ejemplar.id}")
    assert "Aún no hay riegos." in ficha.text

    # 2. Registra un riego con el formulario de la ficha.
    formulario = re.search(
        rf'<form method="post" action="/coleccion/{ejemplar.id}/riegos">.*?</form>',
        ficha.text,
        re.S,
    )
    assert formulario is not None
    token_de_la_ficha = re.search(r'name="csrf" value="([^"]+)"', formulario.group())
    assert token_de_la_ficha is not None
    registrado = anonimo.post(
        f"/coleccion/{ejemplar.id}/riegos",
        data={"fecha": "2026-09-15", "csrf": token_de_la_ficha.group(1)},
    )

    # 3. Aterriza en la ficha y ve la fecha del último riego.
    assert str(registrado.url).endswith(f"/coleccion/{ejemplar.id}")
    assert "Último riego: <strong>2026-09-15</strong>" in registrado.text

    # 4. Al quitar el ejemplar, su historial desaparece con él.
    anonimo.post(f"/coleccion/{ejemplar.id}/quitar", data={"csrf": token_de_la_ficha.group(1)})
    conexion = conectar(app.state.ruta_base)
    try:
        assert conexion.execute("SELECT COUNT(*) FROM riegos").fetchone() == (0,)
    finally:
        conexion.close()


def _formulario(html: str, accion: str) -> tuple[str, str]:
    """La acción de un formulario de la página y el token CSRF que ese mismo formulario lleva."""
    formulario = re.search(rf'<form method="post" action="({accion})".*?</form>', html, re.S)
    assert formulario is not None, accion
    token = re.search(r'name="csrf" value="([^"]+)"', formulario.group())
    assert token is not None, accion
    return formulario.group(1), token.group(1)


def test_registrar_terminar_y_quitar_una_floracion_desde_la_ficha(
    anonimo: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """RF-07 por la interfaz: el historial de floración de un ejemplar, de punta a punta."""
    monkeypatch.setenv("ORQUIDEA_PASSWORD_HASH", hashear_contrasena(CONTRASENA, n=2**4))
    anonimo.post("/acceso", data={"contrasena": CONTRASENA}, follow_redirects=False)
    especie = anonimo.get(f"/especies/{ESPECIE}")
    _, csrf = _formulario(especie.text, "/coleccion")
    anonimo.post("/coleccion", data={"especie_id": ESPECIE, "csrf": csrf})
    (ejemplar,) = listar(abrir_base(app.state.ruta_base))
    base = f"/coleccion/{ejemplar.id}/floraciones"

    # 1. Registra una floración en curso con el formulario de la ficha.
    ficha = anonimo.get(f"/coleccion/{ejemplar.id}")
    assert "Aún no hay floraciones." in ficha.text
    accion, token = _formulario(ficha.text, base)
    registrada = anonimo.post(accion, data={"inicio": "2026-03-01", "fin": "", "csrf": token})
    assert re.search(r"<li>\s*2026-03-01 — en curso", registrada.text)

    # 2. La termina con el formulario de esa fila y ve las dos fechas.
    accion, token = _formulario(registrada.text, rf"{base}/\d+/fin")
    terminada = anonimo.post(accion, data={"fin": "2026-03-20", "csrf": token})
    assert re.search(r"<li>\s*2026-03-01 — 2026-03-20", terminada.text)
    assert "Terminar" not in terminada.text  # ya no ofrece cerrarla otra vez

    # 3. La quita con el formulario de esa fila y el historial vuelve a estar vacío.
    accion, token = _formulario(terminada.text, rf"{base}/\d+/quitar")
    quitada = anonimo.post(accion, data={"csrf": token})
    assert "Aún no hay floraciones." in quitada.text
