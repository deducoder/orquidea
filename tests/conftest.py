from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from orquidea.autenticacion import LimiteDeIntentos
from orquidea.datos.base import abrir_base
from orquidea.web.app import app


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    """Cliente sobre una base temporal migrada; restaura el estado de la app al terminar."""
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
