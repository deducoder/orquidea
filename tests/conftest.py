import time
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from orquidea.autenticacion import LimiteDeIntentos
from orquidea.datos.base import abrir_base, conectar
from orquidea.datos.sesiones import Sesion, crear
from orquidea.web.app import app


@pytest.fixture
def anonimo(tmp_path: Path) -> Iterator[TestClient]:
    """Cliente sin sesión sobre una base temporal migrada; restaura el estado de la app."""
    catalogo = app.state.catalogo
    ruta_base = app.state.ruta_base
    limite = app.state.limite
    app.state.ruta_base = tmp_path / "orquidea.sqlite3"
    app.state.limite = LimiteDeIntentos()
    abrir_base(app.state.ruta_base).close()
    yield TestClient(app, base_url="https://testserver")
    app.state.catalogo = catalogo
    app.state.ruta_base = ruta_base
    app.state.limite = limite


def iniciar_sesion(cliente: TestClient, ahora: int | None = None) -> Sesion:
    """Crea una sesión directamente en la base y deja su cookie en el cliente."""
    conexion = conectar(app.state.ruta_base)
    try:
        identificador, sesion = crear(conexion, int(time.time()) if ahora is None else ahora)
    finally:
        conexion.close()
    cliente.cookies.set("__Host-sesion", identificador)
    return sesion


@pytest.fixture
def client(anonimo: TestClient) -> TestClient:
    """Cliente con una sesión iniciada."""
    iniciar_sesion(anonimo)
    return anonimo
