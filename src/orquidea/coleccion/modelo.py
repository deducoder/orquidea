from dataclasses import dataclass

from pydantic import BaseModel

from orquidea.catalogo.modelo import Especie


class Ejemplar(BaseModel):
    id: int
    especie_id: str | None
    nombre: str
    notas: str
    creado: int


@dataclass(frozen=True)
class EjemplarConEspecie:
    ejemplar: Ejemplar
    especie: Especie | None


def resolver(ejemplares: list[Ejemplar], catalogo: list[Especie]) -> list[EjemplarConEspecie]:
    por_id = {especie.id: especie for especie in catalogo}
    return [
        EjemplarConEspecie(ejemplar=ejemplar, especie=por_id.get(ejemplar.especie_id or ""))
        for ejemplar in ejemplares
    ]
