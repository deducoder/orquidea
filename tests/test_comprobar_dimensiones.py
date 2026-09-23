import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "comprobar-dimensiones.py"


def _cargar() -> ModuleType:
    spec = importlib.util.spec_from_file_location("comprobar_dimensiones", SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


dimensiones = _cargar()

# La forma de la tabla de conventions/interface-dimensions.md de gemba-design 0.23.0
CATALOGO = """
| Dimension | Declares | Evidence class | Source | Mode | Destination |
|---|---|---|---|---|---|
| `palette` | colours | `taste` | none | `declared` | [color](techniques/color/) |
| `spacing` | a unit | `conventional` | Utopia | `derived` | [ui](techniques/ui/) |
| `measure` | line length | `conventional` | Bringhurst | `declared` | [ui](techniques/ui/) |
| `iconography` | icons | `conventional` | Material | `declared` | [ui](techniques/ui/) |
| `motion-duration` | how long | `conventional` | IBM | `declared` | out — no technique |
"""

ENTREGABLE = """
| Dimension | Answer | Where |
|---|---|---|
| `spacing` | declarada: unidad de 8 px | ADR-014 |
| `measure` | declarada: 34em | ADR-016 |
| `iconography` | no aplica, porque la interfaz no usa íconos | ADR-016 |
"""


def _archivos(tmp_path: Path, catalogo: str, entregable: str) -> list[str]:
    rutas = [tmp_path / "catalogo.md", tmp_path / "entregable.md"]
    for ruta, texto in zip(rutas, (catalogo, entregable), strict=True):
        ruta.write_text(texto, encoding="utf-8")
    return [str(r) for r in rutas]


def test_todas_respondidas_sale_con_0_y_cuenta_la_poblacion(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    codigo = dimensiones.main(_archivos(tmp_path, CATALOGO, ENTREGABLE))

    salida = capsys.readouterr().out
    assert codigo == 0
    assert "measure: declarada: 34em  SÍ" in salida
    assert "3 dimensión(es) ui juzgada(s), 0 sin respuesta" in salida


@pytest.mark.parametrize(
    "entregable",
    [
        ENTREGABLE.replace("| `measure` | declarada: 34em | ADR-016 |\n", ""),
        ENTREGABLE.replace("| declarada: 34em |", "|  |"),
        ENTREGABLE.replace("| declarada: 34em |", "|    |"),
    ],
)
def test_una_sin_respuesta_sale_con_1_y_se_nombra(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], entregable: str
) -> None:
    codigo = dimensiones.main(_archivos(tmp_path, CATALOGO, entregable))

    salida = capsys.readouterr().out
    assert codigo == 1
    assert "measure: sin respuesta  NO" in salida
    assert "3 dimensión(es) ui juzgada(s), 1 sin respuesta" in salida


def test_una_respondida_que_el_catalogo_no_tiene_sale_con_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    entregable = ENTREGABLE + "| `sombra` | declarada | ADR-016 |\n"

    codigo = dimensiones.main(_archivos(tmp_path, CATALOGO, entregable))

    assert codigo == 1
    assert "sombra: no está en el catálogo  NO" in capsys.readouterr().out


def test_solo_cuentan_las_de_destino_ui(tmp_path: Path) -> None:
    entregable = ENTREGABLE + "| `palette` | declarada | ADR-012 |\n"

    assert dimensiones.main(_archivos(tmp_path, CATALOGO, entregable)) == 1


@pytest.mark.parametrize(
    ("catalogo", "entregable"),
    [
        ("Sin tablas.\n", ENTREGABLE),
        (CATALOGO.replace("techniques/ui/", "techniques/color/"), ENTREGABLE),  # ninguna ui
        (CATALOGO, "Sin tablas.\n"),
        (CATALOGO, "| Dimension | Answer | Where |\n|---|---|---|\n"),
    ],
)
def test_sin_sujeto_sale_con_2(tmp_path: Path, catalogo: str, entregable: str) -> None:
    assert dimensiones.main(_archivos(tmp_path, catalogo, entregable)) == 2


@pytest.mark.parametrize("argumentos", [[], ["a.md"], ["no-existe.md", "tampoco.md"]])
def test_argumentos_ilegibles_salen_con_2(argumentos: list[str]) -> None:
    assert dimensiones.main(argumentos) == 2


def test_respuestas_lee_la_tabla_del_entregable() -> None:
    assert dimensiones.respuestas(ENTREGABLE) == {
        "spacing": "declarada: unidad de 8 px",
        "measure": "declarada: 34em",
        "iconography": "no aplica, porque la interfaz no usa íconos",
    }
