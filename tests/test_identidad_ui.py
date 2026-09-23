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
