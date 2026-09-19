from fastapi.testclient import TestClient

from orquidea.web.app import app

client = TestClient(app)


def test_inicio_responde_html() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "<title>Orquídea" in response.text
