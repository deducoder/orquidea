import re

from fastapi.testclient import TestClient

from orquidea.web.app import app


def test_inicio_responde_html(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "<title>Orquídea" in response.text


def test_htmx_se_sirve_localmente(client: TestClient) -> None:
    inicio = client.get("/")
    htmx = client.get("/static/htmx.min.js")

    assert 'src="/static/htmx.min.js"' in inicio.text
    assert htmx.status_code == 200
    assert len(htmx.content) > 0


def test_sin_recursos_externos(client: TestClient) -> None:
    html = client.get("/").text

    assert not re.search(r"""(?:src|href)=["']https?://""", html)


def test_salud_responde_ok_sin_depender_del_catalogo(client: TestClient) -> None:
    app.state.catalogo = []

    respuesta = client.get("/salud")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}
