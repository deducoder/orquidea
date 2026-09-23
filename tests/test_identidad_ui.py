import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).parent.parent
UI = RAIZ / "governance" / "identity" / "ui"


def _cargar() -> ModuleType:
    ruta = RAIZ / "scripts" / "comprobar-medidas.py"
    spec = importlib.util.spec_from_file_location("comprobar_medidas_ui", ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


comprobar = _cargar()


def test_los_controles_de_design_md_miden_al_menos_44(capsys: pytest.CaptureFixture[str]) -> None:
    # M2 de ADR-014 sobre el DESIGN.md commiteado; no lo regenera, así que no depende del addon
    codigo = comprobar.main(["objetivos", str(UI / "DESIGN.md"), "--minimo", "44"])

    assert codigo == 0
    assert "4 objetivo(s) medidos, 0 bajo 44 px" in capsys.readouterr().out


def test_ningun_rol_de_lectura_de_la_escala_baja_de_16(capsys: pytest.CaptureFixture[str]) -> None:
    # M1 de ADR-014 sobre type-scale.md
    argumentos = ["piso", str(UI / "type-scale.md"), "--piso", "16"]
    codigo = comprobar.main([*argumentos, "--lectura", "text,binomial,date"])

    assert codigo == 0
    assert "3 rol(es) de lectura medidos, 0 bajo el piso, 0 colapsado(s)" in capsys.readouterr().out


def _cargar_dimensiones() -> ModuleType:
    ruta = RAIZ / "scripts" / "comprobar-dimensiones.py"
    spec = importlib.util.spec_from_file_location("comprobar_dimensiones_ui", ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_components_responde_las_catorce_dimensiones_ui() -> None:
    # V1 de ADR-016 sobre la tabla del entregable. La comparación con el catálogo del plugin se
    # corre a mano (vive fuera del repositorio); 14 es la población que esa corrida contó.
    respuestas = _cargar_dimensiones().respuestas(
        (UI / "components.md").read_text(encoding="utf-8")
    )

    assert len(respuestas) == 14
    assert [d for d, r in respuestas.items() if not r] == []


def _cadena(primitivas: str, semanticos: str, design: str) -> tuple[list[str], int]:
    """Lo que rompe la cadena de colores, y cuántos roles se compararon.

    Cada rol de `semantics.md` vale lo que su escalón en `primitives.md`, en su tabla
    `Role | Value` (la que lee `design-md.py`) y en la `Token | Value | From`; y los colores de
    `DESIGN.md` son esos mismos roles con esos mismos valores (entrada del parking lot de e5).
    """
    escalones = {f[0]: f[1] for f in comprobar._filas(primitivas, "Step") or []}
    roles = {f[0]: f[1] for f in comprobar._filas(semanticos, "Role") or []}
    procedencia = {f[0]: (f[1], f[2]) for f in comprobar._filas(semanticos, "Token") or []}
    generados = {f[0]: f[1] for f in comprobar._filas(design, "Role") or []}
    rotos = []
    for rol, valor in roles.items():
        if rol not in procedencia:
            rotos.append(f"{rol}: sin fila en Token | Value | From")
            continue
        valor_token, escalon = procedencia[rol]
        if valor_token != valor:
            rotos.append(f"{rol}: {valor} en Role y {valor_token} en Token")
        if escalones.get(escalon) != valor:
            rotos.append(f"{rol}: {valor}, y su escalón {escalon} es {escalones.get(escalon)}")
    if generados != roles:
        distintos = sorted(set(generados.items()) ^ set(roles.items()))
        rotos.append(f"DESIGN.md no tiene los colores de semantics.md: {distintos}")
    return rotos, len(roles)


def _leer_cadena() -> tuple[str, str, str]:
    return tuple(  # type: ignore[return-value]
        (UI / n).read_text(encoding="utf-8") for n in ("primitives.md", "semantics.md", "DESIGN.md")
    )


def test_la_cadena_de_colores_esta_atada() -> None:
    rotos, comparados = _cadena(*_leer_cadena())

    assert comparados == 13
    assert rotos == []


@pytest.mark.parametrize(
    ("archivo", "viejo", "nuevo", "nombrado"),
    [
        (
            1,
            "| acción-fondo | #1F3A5F | `azul-800`",
            "| acción-fondo | #1F3A60 | `azul-800`",
            "acción-fondo",
        ),
        (
            1,
            "| acción-fondo | #1F3A5F | azul-800 |",
            "| acción-fondo | #1F3A60 | azul-800 |",
            "acción-fondo",
        ),
        (2, "| acción-fondo | #1F3A5F |", "| acción-fondo | #1F3A60 |", "DESIGN.md"),
        (2, "| foco | #1F3A5F |\n", "", "DESIGN.md"),
    ],
)
def test_un_color_que_cambia_en_un_eslabon_rompe_la_cadena(
    archivo: int, viejo: str, nuevo: str, nombrado: str
) -> None:
    textos = list(_leer_cadena())
    assert viejo in textos[archivo]
    textos[archivo] = textos[archivo].replace(viejo, nuevo, 1)

    rotos, _ = _cadena(*textos)

    assert any(nombrado in r for r in rotos), rotos


def test_sin_tablas_no_hay_verde() -> None:
    assert _cadena("", "", "") == ([], 0)
