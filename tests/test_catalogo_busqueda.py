from typing import Any

import pytest

from orquidea.catalogo.busqueda import buscar
from orquidea.catalogo.modelo import Especie


def especie(id: str, cientifico: str, comunes: list[str]) -> Especie:
    cuidado = {"texto": "t", "fuente": "f"}
    datos: dict[str, Any] = {
        "id": id,
        "nombre_cientifico": cientifico,
        "nombres_comunes": comunes,
        "descripcion": "d",
        "cuidados": {
            "luz": cuidado,
            "riego": cuidado,
            "temperatura": cuidado,
            "sustrato": cuidado,
        },
        "fuentes": ["f"],
    }
    return Especie.model_validate(datos)


EPIDENDRUM = especie("epidendrum-radicans", "Epidendrum radicans", ["orquídea de fuego"])
LAELIA = especie("laelia-anceps", "Laelia anceps", ["monja blanca", "flor de niño"])
CATALOGO = [EPIDENDRUM, LAELIA]


def test_busca_por_parte_del_nombre_cientifico() -> None:
    assert buscar(CATALOGO, "radic") == [EPIDENDRUM]


def test_busca_por_nombre_comun() -> None:
    assert buscar(CATALOGO, "monja") == [LAELIA]


@pytest.mark.parametrize("consulta", ["ORQUIDEA", "orquidea", "OrQuÍdEa", "ORQUÍDEA de fuego"])
def test_ignora_mayusculas_y_acentos_de_la_consulta(consulta: str) -> None:
    assert buscar(CATALOGO, consulta) == [EPIDENDRUM]


def test_ignora_los_acentos_del_catalogo() -> None:
    catalogo = [especie("x", "Especie x", ["Orquídea"])]

    assert buscar(catalogo, "orquidea") == catalogo


def test_ignora_la_enie_y_la_dieresis() -> None:
    assert buscar(CATALOGO, "nino") == [LAELIA]
    assert buscar(CATALOGO, "FLOR DE NIÑO") == [LAELIA]


@pytest.mark.parametrize("consulta", ["", "   "])
def test_consulta_vacia_o_en_blanco_devuelve_todas(consulta: str) -> None:
    assert buscar(CATALOGO, consulta) == CATALOGO


def test_sin_coincidencias_devuelve_lista_vacia() -> None:
    assert buscar(CATALOGO, "zzz") == []


def test_no_busca_en_la_descripcion() -> None:
    con_descripcion = especie("x", "Especie x", [])
    con_descripcion = con_descripcion.model_copy(update={"descripcion": "zzzunico"})

    assert buscar([con_descripcion], "zzzunico") == []
