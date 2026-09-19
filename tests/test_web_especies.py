import importlib.util
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from orquidea.catalogo.modelo import Especie
from orquidea.datos import catalogo as catalogo_datos
from orquidea.datos.catalogo import CatalogoInvalido
from orquidea.web import app as app_modulo
from orquidea.web.app import app


def especie(id: str = "epidendrum-radicans", nombre: str = "Epidendrum radicans") -> Especie:
    def cuidado(nombre_cuidado: str) -> dict[str, str]:
        return {
            "texto": f"texto de {nombre_cuidado}",
            "fuente": f"fuente de {nombre_cuidado}",
        }

    datos: dict[str, Any] = {
        "id": id,
        "nombre_cientifico": nombre,
        "nombres_comunes": ["orquídea de fuego"],
        "descripcion": "Epífita de flores anaranjadas.",
        "cuidados": {
            "luz": cuidado("luz"),
            "riego": cuidado("riego"),
            "temperatura": cuidado("temperatura"),
            "sustrato": cuidado("sustrato"),
        },
        "fuentes": ["Hágsater et al. 2015"],
    }
    return Especie.model_validate(datos)


@pytest.fixture
def client() -> Iterator[TestClient]:
    original = app.state.catalogo
    yield TestClient(app)
    app.state.catalogo = original


def test_lista_muestra_nombre_y_enlace_de_cada_especie(client: TestClient) -> None:
    app.state.catalogo = [especie(), especie("laelia-anceps", "Laelia anceps")]

    html = client.get("/especies").text

    assert 'href="/especies/epidendrum-radicans"' in html
    assert "Epidendrum radicans" in html
    assert 'href="/especies/laelia-anceps"' in html
    assert "Laelia anceps" in html


def test_lista_vacia_muestra_mensaje(client: TestClient) -> None:
    app.state.catalogo = []

    respuesta = client.get("/especies")

    assert respuesta.status_code == 200
    assert "Aún no hay especies en el catálogo." in respuesta.text


def test_lista_escapa_el_html_de_los_datos(client: TestClient) -> None:
    app.state.catalogo = [especie(nombre="<script>alert(1)</script>")]

    html = client.get("/especies").text

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_ficha_muestra_datos_generales_y_cada_cuidado_con_su_fuente(
    client: TestClient,
) -> None:
    app.state.catalogo = [especie()]

    respuesta = client.get("/especies/epidendrum-radicans")

    assert respuesta.status_code == 200
    html = respuesta.text
    for esperado in (
        "Epidendrum radicans",
        "orquídea de fuego",
        "Epífita de flores anaranjadas.",
        "Hágsater et al. 2015",
    ):
        assert esperado in html
    for cuidado in ("luz", "riego", "temperatura", "sustrato"):
        assert f"texto de {cuidado}" in html
        assert f"Fuente: fuente de {cuidado}" in html


def test_ficha_de_id_inexistente_da_404(client: TestClient) -> None:
    app.state.catalogo = [especie()]

    assert client.get("/especies/no-existe").status_code == 404


def test_catalogo_invalido_detiene_el_arranque(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "roto.json").write_text("no es json", encoding="utf-8")
    monkeypatch.setattr(catalogo_datos, "DIRECTORIO_CATALOGO", tmp_path)
    spec = importlib.util.spec_from_file_location("app_de_prueba", app_modulo.__file__)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)

    with pytest.raises(CatalogoInvalido, match="roto.json"):
        spec.loader.exec_module(modulo)
