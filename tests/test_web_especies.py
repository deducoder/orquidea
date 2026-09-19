import importlib.util
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from orquidea.datos import catalogo as catalogo_datos
from orquidea.datos.catalogo import CatalogoInvalido
from orquidea.web import app as app_modulo
from orquidea.web.app import app
from tests.fabricas import especie


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


def test_busqueda_filtra_la_lista(client: TestClient) -> None:
    app.state.catalogo = [especie(), especie("laelia-anceps", "Laelia anceps")]

    html = client.get("/especies", params={"q": "RADICÁNS"}).text

    assert "Epidendrum radicans" in html
    assert "Laelia anceps" not in html


def test_busqueda_sin_coincidencias_muestra_mensaje(client: TestClient) -> None:
    app.state.catalogo = [especie()]

    respuesta = client.get("/especies", params={"q": "zzz"})

    assert respuesta.status_code == 200
    assert "No hay especies que coincidan con la búsqueda." in respuesta.text
    assert "Aún no hay especies en el catálogo." not in respuesta.text


def test_formulario_de_busqueda_funciona_sin_javascript_y_con_htmx(
    client: TestClient,
) -> None:
    app.state.catalogo = [especie()]

    html = client.get("/especies", params={"q": "radic"}).text

    assert '<form method="get" action="/especies"' in html
    assert 'name="q"' in html
    assert 'value="radic"' in html
    assert 'hx-get="/especies"' in html
    assert 'hx-target="#resultados"' in html
    assert 'id="resultados"' in html


def test_la_aplicacion_sirve_el_catalogo_real(client: TestClient) -> None:
    lista = client.get("/especies")
    ficha = client.get("/especies/epidendrum-radicans")

    assert lista.status_code == 200
    assert lista.text.count('href="/especies/') >= 100
    assert ficha.status_code == 200
    assert "Reedstem Epidendrum Culture" in ficha.text
