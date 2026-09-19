from typing import Any

from orquidea.catalogo.modelo import Especie


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
