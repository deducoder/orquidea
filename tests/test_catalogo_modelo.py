from typing import Any

import pytest
from pydantic import ValidationError

from orquidea.catalogo.modelo import Especie


def cuidado(texto: str) -> dict[str, str]:
    return {"texto": texto, "fuente": "Hágsater et al. 2015"}


def especie_valida() -> dict[str, Any]:
    return {
        "id": "epidendrum-radicans",
        "nombre_cientifico": "Epidendrum radicans",
        "nombres_comunes": ["orquídea de fuego"],
        "descripcion": "Epífita o terrestre de flores anaranjadas.",
        "cuidados": {
            "luz": cuidado("Luz brillante"),
            "riego": cuidado("Regular"),
            "temperatura": cuidado("15 a 28 °C"),
            "sustrato": cuidado("Corteza gruesa"),
        },
        "fuentes": ["Hágsater et al. 2015"],
    }


def test_especie_completa_es_valida() -> None:
    especie = Especie.model_validate(especie_valida())

    assert especie.id == "epidendrum-radicans"
    assert especie.cuidados.riego.fuente == "Hágsater et al. 2015"


def test_sin_fuentes_se_rechaza() -> None:
    datos = especie_valida()
    del datos["fuentes"]

    with pytest.raises(ValidationError, match="fuentes"):
        Especie.model_validate(datos)


def test_fuentes_vacias_se_rechazan() -> None:
    datos = especie_valida()
    datos["fuentes"] = []

    with pytest.raises(ValidationError, match="fuentes"):
        Especie.model_validate(datos)


def test_fuente_en_blanco_se_rechaza() -> None:
    datos = especie_valida()
    datos["fuentes"] = [""]

    with pytest.raises(ValidationError, match="fuentes"):
        Especie.model_validate(datos)


def test_cuidado_sin_fuente_se_rechaza() -> None:
    datos = especie_valida()
    del datos["cuidados"]["riego"]["fuente"]

    with pytest.raises(ValidationError, match="cuidados.riego.fuente"):
        Especie.model_validate(datos)


def test_campo_desconocido_se_rechaza() -> None:
    datos = especie_valida()
    datos["fuents"] = ["typo"]

    with pytest.raises(ValidationError, match="fuents"):
        Especie.model_validate(datos)


@pytest.mark.parametrize("id_invalido", ["Epidendrum Radicans", "con_guion_bajo", "", "-a"])
def test_id_debe_ser_slug(id_invalido: str) -> None:
    datos = especie_valida()
    datos["id"] = id_invalido

    with pytest.raises(ValidationError, match="id"):
        Especie.model_validate(datos)


def test_nombre_comun_en_blanco_se_rechaza() -> None:
    datos = especie_valida()
    datos["nombres_comunes"] = [""]

    with pytest.raises(ValidationError, match="nombres_comunes"):
        Especie.model_validate(datos)
