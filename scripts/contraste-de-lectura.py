"""Comprueba que todo par de texto de tamaño normal llegue a 7:1 (criterio 2 de ADR-009).

Lee un markdown con las tablas del formato de `tokens.py pairs` (gemba-design): una
`Foreground | Ground | Kind`, cuyos colores son `#rrggbb` o el nombre de un rol, y opcionalmente una
`Role | Value` que resuelve esos nombres. Juzga solo los pares `Kind = text`: el texto grande queda
en el piso de `contrast` (4.5:1 / 3:1) y los componentes en `component-contrast` (3:1).

    uv run python scripts/contraste-de-lectura.py governance/identity/palette.md

Sale con 0 si todos los pares de texto llegan a 7:1, con 1 si alguno no (y lo nombra), y con 2
si no juzgó nada: ningún par de texto, un rol que no resuelve, un color ilegible o un archivo que
no existe.

La fórmula es la de WCAG 2.2 (luminancia relativa), la misma que `contrast.py` del addon; su caso de
control, `#767676` sobre blanco = 4.54:1, está en las pruebas.
"""

import re
import sys
from pathlib import Path

UMBRAL = 7.0  # criterio 2 de ADR-009
HEXA = re.compile(r"#[0-9a-fA-F]{6}")


def luminancia(hexa: str) -> float:
    canales = [int(hexa[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = (c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canales)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def razon(frente: str, fondo: str) -> float:
    claro, oscuro = sorted((luminancia(frente), luminancia(fondo)), reverse=True)
    return (claro + 0.05) / (oscuro + 0.05)


def llega_al_umbral(r: float) -> bool:
    return r >= UMBRAL


def tablas(texto: str) -> list[list[list[str]]]:
    """Cada tabla de barras del markdown, como filas de celdas, sin la fila separadora."""
    encontradas: list[list[list[str]]] = []
    actual: list[list[str]] = []
    for linea in [*texto.splitlines(), ""]:
        if linea.strip().startswith("|"):
            celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-+:?", c) for c in celdas):
                actual.append(celdas)
        elif actual:
            encontradas.append(actual)
            actual = []
    return encontradas


def filas(texto: str, primera: str) -> list[dict[str, str]]:
    """Las filas de las tablas cuyo encabezado empieza por `primera`, por nombre de columna."""
    return [
        dict(zip(tabla[0], fila, strict=False))
        for tabla in tablas(texto)
        if tabla[0][0] == primera
        for fila in tabla[1:]
    ]


def main(argumentos: list[str]) -> int:
    if len(argumentos) != 1 or not Path(argumentos[0]).is_file():
        print("uso: contraste-de-lectura.py SUJETO.md (un archivo que exista) — nada juzgado")
        return 2
    texto = Path(argumentos[0]).read_text(encoding="utf-8")
    roles = {f.get("Role", ""): f.get("Value", "") for f in filas(texto, "Role")}
    pares = [f for f in filas(texto, "Foreground") if f.get("Kind") == "text"]
    bajo = 0
    for par in pares:
        nombres = (par.get("Foreground", ""), par.get("Ground", ""))
        colores = [roles.get(n, n) for n in nombres]
        ilegibles = [n for n, c in zip(nombres, colores, strict=True) if not HEXA.fullmatch(c)]
        if ilegibles:
            print(f"no se puede leer {', '.join(ilegibles)}: ni un rol declarado ni #rrggbb")
            return 2
        r = razon(*colores)
        bajo += not llega_al_umbral(r)
        veredicto = "SÍ" if llega_al_umbral(r) else "NO"
        print(f"{nombres[0]} sobre {nombres[1]} (texto): {r:.2f}:1  necesita 7:1  {veredicto}")
    if not pares:
        print("0 par(es) de texto juzgado(s) — nada que juzgar")
        return 2
    print(f"{len(pares)} par(es) de texto juzgado(s), {bajo} bajo el umbral")
    return 1 if bajo else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
