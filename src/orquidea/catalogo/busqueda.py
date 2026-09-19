import unicodedata

from orquidea.catalogo.modelo import Especie


def _normalizar(texto: str) -> str:
    descompuesto = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(c for c in descompuesto if not unicodedata.combining(c))


def buscar(especies: list[Especie], consulta: str) -> list[Especie]:
    buscada = _normalizar(consulta).strip()
    if not buscada:
        return list(especies)
    return [
        especie
        for especie in especies
        if any(
            buscada in _normalizar(nombre)
            for nombre in [especie.nombre_cientifico, *especie.nombres_comunes]
        )
    ]
