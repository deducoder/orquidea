from dataclasses import dataclass

from pydantic import BaseModel

from orquidea.catalogo.modelo import Especie


class Ejemplar(BaseModel):
    id: int
    especie_id: str | None
    nombre: str
    notas: str
    creado: int
    foto: str | None = None


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


NOMBRE_MAXIMO = 120
NOTAS_MAXIMO = 2000


class EjemplarInvalido(ValueError):
    pass


def validar_ejemplar(nombre: str, notas: str, con_especie: bool = False) -> tuple[str, str]:
    nombre = nombre.strip()
    notas = notas.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not nombre and not con_especie:
        raise EjemplarInvalido("El nombre es obligatorio.")
    if len(nombre) > NOMBRE_MAXIMO:
        raise EjemplarInvalido(f"El nombre no puede pasar de {NOMBRE_MAXIMO} caracteres.")
    if len(notas) > NOTAS_MAXIMO:
        raise EjemplarInvalido(f"Las notas no pueden pasar de {NOTAS_MAXIMO} caracteres.")
    return nombre, notas
