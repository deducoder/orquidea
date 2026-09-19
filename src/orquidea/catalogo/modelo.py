from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Texto = Annotated[str, StringConstraints(min_length=1)]


class Cuidado(BaseModel):
    model_config = ConfigDict(extra="forbid")

    texto: Texto
    fuente: Texto


class Cuidados(BaseModel):
    model_config = ConfigDict(extra="forbid")

    luz: Cuidado
    riego: Cuidado
    temperatura: Cuidado
    sustrato: Cuidado


class Especie(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$")
    nombre_cientifico: Texto
    nombres_comunes: list[str] = []
    descripcion: Texto
    cuidados: Cuidados
    fuentes: list[Texto] = Field(min_length=1)
