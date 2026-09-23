"""Cada página tiene un `<title>` de texto (clase de b1: un bloque `title` con marcado dentro).

La lista de páginas se compara con las rutas GET registradas, así que una página nueva sin título
probado pone la prueba de cobertura en rojo.
"""

import re

import pytest
from fastapi.testclient import TestClient

from orquidea.datos.base import conectar
from orquidea.datos.ejemplares import agregar
from orquidea.web.app import app
from tests.fabricas import especie, rutas_registradas

# ruta → quién la pide ("anonimo" o "sesion")
PAGINAS = {
    "/": "sesion",
    "/acceso": "anonimo",
    "/especies": "sesion",
    "/especies/{id}": "sesion",
    "/coleccion": "sesion",
    "/coleccion/nuevo": "sesion",
    "/coleccion/{id}": "sesion",
    "/coleccion/{id}/editar": "sesion",
    "/coleccion/{id}/quitar": "sesion",
}
# GET que no devuelven una página HTML
NO_SON_PAGINAS = {"/coleccion/{id}/foto", "/coleccion/{id}/foto/miniatura", "/salud"}


def test_la_lista_cubre_todas_las_paginas_get() -> None:
    get = {ruta for metodo, ruta in rutas_registradas(app.routes) if metodo == "GET"}

    assert get - NO_SON_PAGINAS - set(PAGINAS) == set(), "páginas sin título probado"
    assert set(PAGINAS) - get == set(), "páginas que ya no existen"


def _url(ruta: str, ejemplar_id: int) -> str:
    if ruta.startswith("/especies/"):
        return ruta.replace("{id}", "epidendrum-radicans")
    return ruta.replace("{id}", str(ejemplar_id))


def titulos(html: str) -> list[str]:
    return re.findall(r"<title>(.*?)</title>", html, re.S)


@pytest.mark.parametrize("ruta", sorted(PAGINAS))
def test_el_titulo_de_cada_pagina_es_texto(
    ruta: str, anonimo: TestClient, client: TestClient
) -> None:
    app.state.catalogo = [especie()]
    conexion = conectar(app.state.ruta_base)
    try:
        ejemplar = agregar(conexion, "epidendrum-radicans", 1_780_000_000)
    finally:
        conexion.close()
    cliente = client if PAGINAS[ruta] == "sesion" else anonimo
    if PAGINAS[ruta] == "anonimo":
        cliente.cookies.clear()

    respuesta = cliente.get(_url(ruta, ejemplar.id), follow_redirects=False)

    assert respuesta.status_code == 200
    encontrados = titulos(respuesta.text)
    assert len(encontrados) == 1, encontrados
    assert "<" not in encontrados[0] and ">" not in encontrados[0], encontrados[0]
    assert encontrados[0].strip().endswith("Orquídea")


@pytest.mark.parametrize(
    "html",
    [
        "<title><p><a href='/'>Mi colección</a></p> — Orquídea</title>",  # la forma de b1
        "<html><head></head></html>",  # sin título: no hay nada que juzgar, y no es verde
    ],
)
def test_un_titulo_con_marcado_o_ausente_no_pasa(html: str) -> None:
    encontrados = titulos(html)

    assert len(encontrados) != 1 or "<" in encontrados[0]
