import re

from orquidea.web.app import app
from tests.fabricas import rutas_registradas

RUTAS = [
    ("GET", "/"),
    ("GET", "/acceso"),
    ("GET", "/coleccion"),
    ("GET", "/coleccion/nuevo"),
    ("GET", "/coleccion/{id}"),
    ("GET", "/coleccion/{id}/foto"),
    ("GET", "/coleccion/{id}/foto/miniatura"),
    ("GET", "/coleccion/{id}/editar"),
    ("GET", "/coleccion/{id}/quitar"),
    ("GET", "/especies"),
    ("GET", "/especies/{id}"),
    ("GET", "/salud"),
    ("POST", "/acceso"),
    ("POST", "/coleccion"),
    ("POST", "/coleccion/nuevo"),
    ("POST", "/coleccion/{id}/editar"),
    ("POST", "/coleccion/{id}/foto"),
    ("POST", "/coleccion/{id}/foto/quitar"),
    ("POST", "/coleccion/{id}/quitar"),
    ("POST", "/salir"),
]


def _registradas() -> list[tuple[str, str]]:
    return rutas_registradas(app.routes)


def test_el_mapa_de_rutas_es_el_declarado() -> None:
    assert sorted(_registradas()) == sorted(RUTAS)


def test_nuevo_se_registra_antes_que_una_ruta_con_id_sin_sufijo() -> None:
    caminos = [path for _, path in _registradas()]
    con_id = [i for i, p in enumerate(caminos) if re.fullmatch(r"/coleccion/\{[^/}]+\}", p)]

    assert caminos.index("/coleccion/nuevo") < min(con_id, default=len(caminos))
