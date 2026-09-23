"""Comprueba que cada dimensión de interfaz con destino `ui` tenga respuesta (V1 de ADR-016).

    uv run python scripts/comprobar-dimensiones.py CATALOGO.md ENTREGABLE.md

CATALOGO.md es `conventions/interface-dimensions.md` de gemba-design: de su tabla
`Dimension | … | Destination` toma las claves cuyo destino es la técnica `ui`. ENTREGABLE.md lleva
una tabla `Dimension | Answer | Where`: cada dimensión ui tiene que estar con una respuesta no vacía
(declarada, o "no aplica, porque…"), y ninguna fila puede nombrar una dimensión ui que el catálogo
no tenga. El catálogo vive en el plugin; este script no guarda una copia de la lista.

Sale con 0 si todas están respondidas, con 1 si falta alguna o sobra una (y la nombra), y con 2 si
no juzgó nada: un catálogo sin dimensiones ui, un entregable sin la tabla o sin filas, o un archivo
que no existe. Cada veredicto cuenta su población.
"""

import re
import sys
from pathlib import Path

CLAVE = re.compile(r"`([a-z][a-z-]*)`")


def _tabla(texto: str, primera: str) -> list[list[str]] | None:
    """Las filas de la primera tabla cuyo encabezado empieza por `primera`; None si no hay."""
    filas: list[list[str]] | None = None
    for linea in [*texto.splitlines(), ""]:
        s = linea.strip()
        if not s.startswith("|"):
            if filas is not None:
                return filas
            continue
        celdas = [c.strip() for c in s.strip("|").split("|")]
        if filas is None:
            if celdas[0] == primera:
                filas = []
            continue
        if not all(re.fullmatch(r":?-+:?", c) for c in celdas):
            filas.append(celdas)
    return filas


def dimensiones_ui(catalogo: str) -> list[str]:
    """Las claves del catálogo cuyo destino es la técnica `ui`, en su orden."""
    claves = []
    for fila in _tabla(catalogo, "Dimension") or []:
        clave = CLAVE.fullmatch(fila[0])
        if clave and "techniques/ui/" in fila[-1]:
            claves.append(clave.group(1))
    return claves


def respuestas(entregable: str) -> dict[str, str]:
    """Dimensión → respuesta, de la tabla `Dimension | Answer | Where` del entregable."""
    salida = {}
    for fila in _tabla(entregable, "Dimension") or []:
        clave = CLAVE.fullmatch(fila[0])
        if clave:
            salida[clave.group(1)] = fila[1] if len(fila) > 1 else ""
    return salida


def main(argumentos: list[str]) -> int:
    if len(argumentos) != 2 or not all(Path(a).is_file() for a in argumentos):
        print(
            "uso: comprobar-dimensiones.py CATALOGO.md ENTREGABLE.md (que existan) — nada juzgado"
        )
        return 2
    catalogo, entregable = (Path(a).read_text(encoding="utf-8") for a in argumentos)
    claves = dimensiones_ui(catalogo)
    dadas = respuestas(entregable)
    if not claves or not dadas:
        print("0 dimensión(es) ui juzgada(s) — nada que juzgar")
        return 2
    fallas = 0
    for clave in claves:
        respuesta = dadas.get(clave, "")
        fallas += not respuesta
        print(f"{clave}: {respuesta}  SÍ" if respuesta else f"{clave}: sin respuesta  NO")
    for clave in (c for c in dadas if c not in claves):
        fallas += 1
        print(f"{clave}: no está en el catálogo  NO")
    sin_respuesta = sum(not dadas.get(c, "") for c in claves)
    print(f"{len(claves)} dimensión(es) ui juzgada(s), {sin_respuesta} sin respuesta")
    return 1 if fallas else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
