import json
from pathlib import Path

from pydantic import ValidationError

from orquidea.catalogo.modelo import Especie

DIRECTORIO_CATALOGO = Path(__file__).parent / "catalogo"


class CatalogoInvalido(Exception):
    def __init__(self, errores: list[str]) -> None:
        super().__init__("\n".join(errores))
        self.errores = errores


def _campo(ruta: tuple[int | str, ...]) -> str:
    return ".".join(str(parte) for parte in ruta) or "(raíz)"


def cargar_catalogo(directorio: Path) -> list[Especie]:
    if not directorio.is_dir():
        raise CatalogoInvalido([f"{directorio}: el directorio del catálogo no existe"])

    especies: list[Especie] = []
    errores: list[str] = []
    for archivo in sorted(directorio.glob("*.json")):
        try:
            datos = json.loads(archivo.read_text(encoding="utf-8"))
        except json.JSONDecodeError as fallo:
            errores.append(
                f"{archivo.name}: JSON inválido (línea {fallo.lineno}, columna {fallo.colno})"
            )
            continue
        try:
            especies.append(Especie.model_validate(datos))
        except ValidationError as fallo:
            errores.extend(
                f"{archivo.name}: {_campo(error['loc'])}: {error['msg']}"
                for error in fallo.errors()
            )

    if errores:
        raise CatalogoInvalido(errores)
    return sorted(especies, key=lambda especie: especie.id)
