from typing import Any

from fastapi.routing import APIRoute

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


def rutas_registradas(rutas: Any) -> list[tuple[str, str]]:
    """Pares (método, ruta) de una aplicación, entrando en los routers incluidos."""
    pares: list[tuple[str, str]] = []
    for ruta in rutas:
        if isinstance(ruta, APIRoute):
            pares.extend((metodo, ruta.path) for metodo in sorted(ruta.methods or set()))
        elif hasattr(ruta, "original_router"):
            pares.extend(rutas_registradas(ruta.original_router.routes))
    return pares
