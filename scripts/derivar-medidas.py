"""Deriva la escala tipográfica y el espaciado por las reglas declaradas en ADR-014.

Imprime en markdown las tablas que lee `design-md.py` (gemba-design): `Step | Size | Line height |
Roles` para la escala y `Step | Value | Where it is used` para el espaciado. Con `--familia` y
`--pesos`, la escala lleva `Font family` y `Font weight`, en ese orden, antes de `Roles`: una pila
para todos los escalones y un peso por escalón, leídos del espécimen, nunca derivados aquí.

    uv run python scripts/derivar-medidas.py escala --base 16 --razon 1.25 \\
        --escalones 0,1,2 --roles text=0,binomial=0,date=0,subtitulo=1,titulo=2 \\
        --familia 'system-ui, sans-serif' --pesos 0=400,1=700,2=700
    uv run python scripts/derivar-medidas.py espaciado --base 16 --divisor 3 \\
        --multiplicadores 1,2,3,4,6 --control 6

La regla de ADR-014, una sola vez aquí: el escalón `n` mide `base · razón^n`, redondeado al entero
de px más cercano (medio hacia arriba); la altura de línea es el múltiplo de 4 px más cercano a
`1.5 · tamaño` (medio hacia arriba); la unidad del espaciado es la altura de línea de la base entre
el divisor, y tiene que ser entera; cada paso es `m · unidad`, nombrado por `m`.

Sale con 0 al imprimir la tabla y con 2 si no derivó nada: un subcomando desconocido, un parámetro
ilegible o ausente, un rol en un escalón que no existe, un escalón sin peso o un peso fuera de 1 a
1000 cuando se dan pesos, una familia vacía o con `|`, una unidad no entera o un control que no es
uno de los pasos. No juzga nada: eso es de `comprobar-medidas.py` y de `tokens.py`.
"""

import math
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Escalon:
    id: int
    tamano: int
    altura: int
    roles: list[str]


@dataclass(frozen=True)
class Paso:
    id: int
    valor: int


def redondear(valor: float) -> int:
    return math.floor(valor + 0.5)


def altura_de_linea(tamano: int) -> int:
    return 4 * redondear(1.5 * tamano / 4)


def escala(base: int, razon: float, ids: list[int], roles: dict[str, int]) -> list[Escalon]:
    for rol, id_ in roles.items():
        if id_ not in ids:
            raise ValueError(f"el rol {rol} va a un escalón que no existe ({id_})")
    escalones = []
    for id_ in sorted(ids):
        tamano = redondear(base * razon**id_)
        asignados = [rol for rol, destino in roles.items() if destino == id_]
        escalones.append(Escalon(id_, tamano, altura_de_linea(tamano), asignados))
    return escalones


def espaciado(base: int, divisor: int, multiplicadores: list[int]) -> list[Paso]:
    altura = altura_de_linea(base)
    if altura % divisor:
        raise ValueError(f"la unidad {altura}/{divisor} no es entera")
    unidad = altura // divisor
    return [Paso(m, m * unidad) for m in multiplicadores]


def tabla_escala(
    escalones: list[Escalon], pesos: dict[int, int] | None = None, familia: str | None = None
) -> str:
    cabecera, extra = ["Step", "Size", "Line height"], []
    if familia is not None:
        if not familia.strip() or "|" in familia:
            raise ValueError("la familia no puede ir vacía ni llevar |")
        cabecera.append("Font family")
        extra.append(lambda e: familia)
    if pesos is not None:
        ids = {e.id for e in escalones}
        if set(pesos) != ids:
            raise ValueError(f"los pesos van a los escalones {sorted(pesos)}, no a {sorted(ids)}")
        if not all(1 <= p <= 1000 for p in pesos.values()):
            raise ValueError("un peso va de 1 a 1000")
        cabecera.append("Font weight")
        extra.append(lambda e: str(pesos[e.id]))
    cabecera.append("Roles")
    lineas = ["| " + " | ".join(cabecera) + " |", "|" + "---|" * len(cabecera)]
    for e in escalones:
        celdas = [str(e.id), f"{e.tamano}px", f"{e.altura}px", *(f(e) for f in extra)]
        lineas.append("| " + " | ".join([*celdas, ", ".join(e.roles) or "—"]) + " |")
    return "\n".join(lineas) + "\n"


def tabla_espaciado(pasos: list[Paso], control: int) -> str:
    lineas = ["| Step | Value | Where it is used |", "|---|---|---|"]
    for p in pasos:
        uso = f"{p.id} unidad" if p.id == 1 else f"{p.id} unidades"
        if p.id == control:
            uso += "; tamaño de control"
        lineas.append(f"| {p.id} | {p.valor}px | {uso} |")
    return "\n".join(lineas) + "\n"


def _opciones(argumentos: list[str]) -> dict[str, str]:
    if len(argumentos) % 2 or not all(a.startswith("--") for a in argumentos[::2]):
        raise ValueError("las opciones van en pares --nombre valor")
    return {k[2:]: v for k, v in zip(argumentos[::2], argumentos[1::2], strict=True)}


def _enteros(texto: str) -> list[int]:
    return [int(x) for x in texto.split(",")]


def main(argumentos: list[str]) -> int:
    try:
        if not argumentos or argumentos[0] not in ("escala", "espaciado"):
            raise ValueError("subcomando: escala | espaciado")
        opciones = _opciones(argumentos[1:])
        base = int(opciones["base"])
        if argumentos[0] == "escala":
            roles = {
                rol: int(id_)
                for rol, id_ in (par.split("=") for par in opciones["roles"].split(","))
            }
            ids = _enteros(opciones["escalones"])
            pesos = None
            if "pesos" in opciones:
                pesos = {
                    int(id_): int(peso)
                    for id_, peso in (par.split("=") for par in opciones["pesos"].split(","))
                }
            salida = tabla_escala(
                escala(base, float(opciones["razon"]), ids, roles), pesos, opciones.get("familia")
            )
        else:
            multiplicadores = _enteros(opciones["multiplicadores"])
            control = int(opciones["control"])
            if control not in multiplicadores:
                raise ValueError(f"el control {control} no es uno de los pasos")
            pasos = espaciado(base, int(opciones["divisor"]), multiplicadores)
            salida = tabla_espaciado(pasos, control)
    except (ValueError, KeyError) as error:
        print(f"no se derivó nada: {error}")
        return 2
    print(salida, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
