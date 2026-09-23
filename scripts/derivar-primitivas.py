"""Deriva las primitivas de color de la paleta por una regla declarada (ADR-013).

Lee los roles de una tabla `Role | Value` (la de `governance/identity/palette.md`) y, con una de las
tres reglas de ADR-013, imprime dos tablas en markdown: `Step | Value | Ramp`, la escala que lee
`tokens.py provenance`, y `Identity role | Identity value | Resolves to | Primitive | Drift`, el
escalón que toma cada rol de la paleta y su desvío (ΔE en OKLab).

    uv run python scripts/derivar-primitivas.py governance/identity/palette.md --regla anclas

Las reglas: `anclas` (cada rampa pasa por sus roles, interpolando en OKLCH), `oklch` (luminosidad
uniforme en OKLCH, croma y tono de la fuente) y `hsl` (luminosidad uniforme en HSL, tono y
saturación de la fuente). Los parámetros comunes — rampas, escalones, rejilla, gama, asignación —
son los de ADR-013 y están aquí una sola vez.

Sale con 0 al imprimir las tablas y con 2 si no derivó nada: un archivo que no existe, una regla
desconocida, un rol de la paleta ausente o un color ilegible, nombrándolo. No juzga contraste:
eso es de `contraste-de-lectura.py` y de `tokens.py pairs`.
"""

import colorsys
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path

Lab = tuple[float, float, float]

ESCALONES = (0, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950)
L_MINIMA = 0.20
RAMPAS = {
    "neutro": ("hoja", "papel", "renglón", "tinta suave", "tinta"),
    "azul": ("acento",),
    "rojo": ("alerta",),
}
FUENTES = {"neutro": "renglón", "azul": "acento", "rojo": "alerta"}
REGLAS = ("anclas", "oklch", "hsl")
TOLERANCIA_GAMA = 1e-4
HEXA = re.compile(r"#[0-9a-fA-F]{6}")


@dataclass(frozen=True)
class Asignacion:
    rol: str
    identidad: str
    escalon: str
    valor: str
    desvio: float


@dataclass(frozen=True)
class Derivacion:
    primitivas: list[tuple[str, str, str]]
    asignaciones: list[Asignacion]


# --- sRGB ↔ OKLab (Björn Ottosson, 2020) -------------------------------------------------------


def _lineal(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gamma(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def _rgb(hexa: str) -> tuple[float, float, float]:
    r, g, b = (int(hexa[i : i + 2], 16) / 255 for i in (1, 3, 5))
    return r, g, b


def oklab(hexa: str) -> Lab:
    r, g, b = (_lineal(c) for c in _rgb(hexa))
    l_ = math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
    return (
        0.2104542553 * l_ + 0.7936177850 * m - 0.0040720468 * s,
        1.9779984951 * l_ - 2.4285922050 * m + 0.4505937099 * s,
        0.0259040371 * l_ + 0.7827717662 * m - 0.8086757660 * s,
    )


def _rgb_desde_oklab(lab: Lab) -> tuple[float, float, float]:
    """sRGB con gamma, sin recortar: un canal fuera de [0, 1] es un color fuera de la gama."""
    l0, a, b = lab
    l_ = (l0 + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (l0 - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (l0 - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l_ - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l_ + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l_ - 0.7034186147 * m + 1.7076147010 * s
    return (
        math.copysign(_gamma(abs(r)), r),
        math.copysign(_gamma(abs(g)), g),
        math.copysign(_gamma(abs(bb)), bb),
    )


def a_hexa(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{min(255, max(0, round(c * 255))):02X}" for c in rgb)


def hexa_desde_oklab(lab: Lab) -> str:
    return a_hexa(_rgb_desde_oklab(lab))


def oklch(hexa: str) -> Lab:
    l_, a, b = oklab(hexa)
    return l_, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def _desde_oklch(l_: float, c: float, h: float) -> Lab:
    return l_, c * math.cos(math.radians(h)), c * math.sin(math.radians(h))


def _en_gama(lab: Lab) -> bool:
    return all(-1e-7 <= c <= 1 + 1e-7 for c in _rgb_desde_oklab(lab))


def _recortado(l_: float, c: float, h: float) -> str:
    """Conserva L y h; reduce el croma por bisección hasta entrar en sRGB (ADR-013, gama)."""
    if _en_gama(_desde_oklch(l_, c, h)):
        return hexa_desde_oklab(_desde_oklch(l_, c, h))
    bajo, alto = 0.0, c
    while alto - bajo > TOLERANCIA_GAMA:
        medio = (bajo + alto) / 2
        bajo, alto = (medio, alto) if _en_gama(_desde_oklch(l_, medio, h)) else (bajo, medio)
    return hexa_desde_oklab(_desde_oklch(l_, bajo, h))


def delta_e(uno: str, otro: str) -> float:
    return math.dist(oklab(uno), oklab(otro))


# --- la regla ---------------------------------------------------------------------------------


def rejilla() -> list[float]:
    n = len(ESCALONES) - 1
    return [1 - i * (1 - L_MINIMA) / n for i in range(len(ESCALONES))]


def mas_cercano(luminosidad: float, niveles: list[float], ocupados: set[int]) -> int:
    """El índice libre más cercano; en empate, el más oscuro (el de índice mayor)."""
    libres = [i for i in range(len(niveles)) if i not in ocupados]
    return min(libres, key=lambda i: (round(abs(niveles[i] - luminosidad), 12), -i))


def _luminosidad_hsl(hexa: str) -> float:
    return colorsys.rgb_to_hls(*_rgb(hexa))[1]


def _asignar(roles: dict[str, str], rampa: str, medida: str) -> dict[int, str]:
    niveles = rejilla()
    ocupados: dict[int, str] = {}
    for rol in RAMPAS[rampa]:
        valor = roles[rol]
        luz = _luminosidad_hsl(valor) if medida == "hsl" else oklab(valor)[0]
        ocupados[mas_cercano(luz, niveles, set(ocupados))] = rol
    return ocupados


def _interpolar_tono(h1: float, h2: float, t: float) -> float:
    delta = (h2 - h1 + 180) % 360 - 180
    return (h1 + t * delta) % 360


def _rampa_anclas(roles: dict[str, str], rampa: str, anclados: dict[int, str]) -> list[str]:
    niveles = rejilla()
    anclas = {i: roles[rol] for i, rol in anclados.items()}
    anclas.setdefault(0, "#FFFFFF")
    indices = sorted(anclas)
    valores: list[str] = []
    for i, nivel in enumerate(niveles):
        if i in anclas:
            valores.append(anclas[i].upper())
            continue
        arriba = max(k for k in indices if k < i)  # el escalón 0 siempre es ancla
        abajo = min((k for k in indices if k > i), default=None)
        if abajo is None:
            _, c, h = oklch(anclas[indices[-1]])
            valores.append(_recortado(nivel, c, h))
            continue
        l1, c1, h1 = oklch(anclas[arriba])
        l2, c2, h2 = oklch(anclas[abajo])
        t = (l1 - nivel) / (l1 - l2)
        c = c1 + t * (c2 - c1)
        if c1 < 1e-4:
            h = h2
        elif c2 < 1e-4:
            h = h1
        else:
            h = _interpolar_tono(h1, h2, t)
        valores.append(_recortado(nivel, c, h))
    return valores


def _rampa_oklch(roles: dict[str, str], rampa: str) -> list[str]:
    _, c, h = oklch(roles[FUENTES[rampa]])
    return [_recortado(nivel, c, h) for nivel in rejilla()]


def _rampa_hsl(roles: dict[str, str], rampa: str) -> list[str]:
    h, _, s = colorsys.rgb_to_hls(*_rgb(roles[FUENTES[rampa]]))
    return [a_hexa(colorsys.hls_to_rgb(h, nivel, s)) for nivel in rejilla()]


def derivar(roles: dict[str, str], regla: str) -> Derivacion:
    if regla not in REGLAS:
        raise ValueError(f"regla desconocida: {regla}")
    primitivas: list[tuple[str, str, str]] = []
    asignaciones: list[Asignacion] = []
    for rampa in RAMPAS:
        anclados = _asignar(roles, rampa, "hsl" if regla == "hsl" else "oklch")
        if regla == "anclas":
            valores = _rampa_anclas(roles, rampa, anclados)
        elif regla == "oklch":
            valores = _rampa_oklch(roles, rampa)
        elif regla == "hsl":
            valores = _rampa_hsl(roles, rampa)
        nombres = [f"{rampa}-{e}" for e in ESCALONES]
        primitivas += [(n, v, rampa) for n, v in zip(nombres, valores, strict=True)]
        for i, rol in anclados.items():
            identidad = roles[rol].upper()
            asignaciones.append(
                Asignacion(rol, identidad, nombres[i], valores[i], delta_e(identidad, valores[i]))
            )
    orden = [rol for rampa in RAMPAS.values() for rol in rampa]
    asignaciones.sort(key=lambda a: orden.index(a.rol))
    return Derivacion(primitivas, asignaciones)


# --- entrada y salida -------------------------------------------------------------------------


def _roles_de(texto: str) -> dict[str, str]:
    """Las filas de toda tabla cuyo encabezado empieza por `Role`: nombre → valor."""
    roles: dict[str, str] = {}
    en_tabla = False
    for linea in texto.splitlines():
        s = linea.strip()
        if not s.startswith("|"):
            en_tabla = False
            continue
        celdas = [c.strip().strip("`") for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in celdas):
            continue
        if celdas[0] == "Role":
            en_tabla = True
        elif en_tabla and len(celdas) >= 2:
            roles[celdas[0]] = celdas[1]
    return roles


def tablas(derivacion: Derivacion) -> str:
    lineas = ["| Step | Value | Ramp |", "|---|---|---|"]
    lineas += [f"| {n} | {v} | {r} |" for n, v, r in derivacion.primitivas]
    lineas += [
        "",
        "| Identity role | Identity value | Resolves to | Primitive | Drift |",
        "|---|---|---|---|---|",
    ]
    lineas += [
        f"| {a.rol} | {a.identidad} | {a.escalon} | {a.valor} | {a.desvio:.3f} |"
        for a in derivacion.asignaciones
    ]
    return "\n".join(lineas) + "\n"


def main(argumentos: list[str]) -> int:
    uso = "uso: derivar-primitivas.py PALETA.md --regla {anclas|oklch|hsl} — nada derivado"
    if len(argumentos) != 3 or argumentos[1] != "--regla" or argumentos[2] not in REGLAS:
        print(uso)
        return 2
    ruta, regla = Path(argumentos[0]), argumentos[2]
    if not ruta.is_file():
        print(f"no existe {ruta} — nada derivado")
        return 2
    roles = _roles_de(ruta.read_text(encoding="utf-8"))
    for rol in (r for rampa in RAMPAS.values() for r in rampa):
        if rol not in roles:
            print(f"la paleta no declara el rol {rol} — nada derivado")
            return 2
        if not HEXA.fullmatch(roles[rol]):
            print(f"el rol {rol} tiene un color ilegible ({roles[rol]}) — nada derivado")
            return 2
    print(tablas(derivar(roles, regla)), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
