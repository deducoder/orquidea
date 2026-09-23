"""Comprueba las medidas de la interfaz contra los criterios M1 y M2 de ADR-014.

    uv run python scripts/comprobar-medidas.py piso TYPE-SCALE.md \\
        --piso 16 --lectura text,binomial,date
    uv run python scripts/comprobar-medidas.py objetivos DESIGN.md --minimo 44

`piso` lee la tabla `Step | Size | … | Roles` y juzga que cada rol de lectura esté en un escalón de
al menos el piso, y que no haya dos escalones del mismo tamaño (colapsados al redondear).
`objetivos` lee la tabla `Target | Width | Height` (la que escribe `design-md.py`) y juzga que cada
objetivo llegue al mínimo en sus dos dimensiones; existe porque `tokens.py targets` fija 24 px y M2
pide 44 (WCAG 2.2 SC 2.5.5, AAA). No modela las excepciones de la fuente (inline, espaciado,
equivalente): un objetivo que se apoye en una se declara y se firma, no se mide aquí.

Sale con 0 si todo lo juzgado pasa, con 1 si algo no (y lo nombra), y con 2 si no juzgó nada: sin
tabla, sin filas, un rol de lectura que ningún escalón lleva, un valor ilegible o un archivo que no
existe. Cada veredicto cuenta su población.
"""

import re
import sys
from pathlib import Path

PX = re.compile(r"(\d+)(px)?")


def _filas(texto: str, primera: str) -> list[list[str]] | None:
    """Las filas de la primera tabla cuyo encabezado empieza por `primera`; None si no hay."""
    filas: list[list[str]] | None = None
    for linea in [*texto.splitlines(), ""]:
        s = linea.strip()
        if not s.startswith("|"):
            if filas is not None:
                return filas
            continue
        celdas = [c.strip().strip("`") for c in s.strip("|").split("|")]
        if filas is None:
            if celdas[0] == primera:
                filas = []
            continue
        if not all(re.fullmatch(r":?-+:?", c) for c in celdas):
            filas.append(celdas)
    return filas


def _px(celda: str) -> int:
    m = PX.fullmatch(celda)
    if not m:
        raise ValueError(f"no se puede leer {celda!r} como px")
    return int(m.group(1))


def piso(texto: str, minimo: int, lectura: list[str]) -> int:
    filas = _filas(texto, "Step")
    if not filas:
        print("0 escalón(es) medidos — nada que juzgar")
        return 2
    escalones = [(f[0], _px(f[1]), [r.strip() for r in f[-1].split(",")]) for f in filas]
    bajo = 0
    for rol in lectura:
        donde = [(id_, tamano) for id_, tamano, roles in escalones if rol in roles]
        if not donde:
            print(f"el rol de lectura {rol} no está en ningún escalón — nada juzgado")
            return 2
        id_, tamano = donde[0]
        llega = tamano >= minimo
        bajo += not llega
        print(f"{rol}: escalón {id_} = {tamano}px  piso {minimo}px  {'SÍ' if llega else 'NO'}")
    colapsados = 0
    for i, (id_a, tamano_a, _) in enumerate(escalones):
        for id_b, tamano_b, _ in escalones[i + 1 :]:
            if tamano_a == tamano_b:
                colapsados += 1
                print(f"escalones {id_a} y {id_b} colapsan en {tamano_a}px")
    print(
        f"{len(escalones)} escalón(es) y {len(lectura)} rol(es) de lectura medidos, "
        f"{bajo} bajo el piso, {colapsados} colapsado(s)"
    )
    return 1 if bajo or colapsados else 0


def objetivos(texto: str, minimo: int) -> int:
    filas = _filas(texto, "Target")
    if not filas:
        print("0 objetivo(s) medidos — nada que juzgar")
        return 2
    bajo = 0
    for fila in filas:
        nombre, ancho, alto = fila[0], _px(fila[1]), _px(fila[2])
        faltan = [d for d, v in (("ancho", ancho), ("alto", alto)) if v < minimo]
        bajo += bool(faltan)
        veredicto = (
            "SÍ"
            if not faltan
            else "NO — " + ", ".join(f"{nombre}: {d} bajo {minimo}" for d in faltan)
        )
        print(f"{nombre} {ancho}×{alto}  necesita {minimo}×{minimo}  {veredicto}")
    print(f"{len(filas)} objetivo(s) medidos, {bajo} bajo {minimo} px")
    return 1 if bajo else 0


def main(argumentos: list[str]) -> int:
    try:
        if len(argumentos) < 2 or argumentos[0] not in ("piso", "objetivos"):
            raise ValueError("uso: comprobar-medidas.py piso|objetivos ARCHIVO …")
        ruta = Path(argumentos[1])
        if not ruta.is_file():
            raise ValueError(f"no existe {ruta}")
        opciones = dict(zip(argumentos[2::2], argumentos[3::2], strict=False))
        texto = ruta.read_text(encoding="utf-8")
        if argumentos[0] == "piso":
            return piso(texto, int(opciones["--piso"]), opciones["--lectura"].split(","))
        return objetivos(texto, int(opciones["--minimo"]))
    except (ValueError, KeyError) as error:
        print(f"nada juzgado: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
