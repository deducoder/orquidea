import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "contraste-de-lectura.py"


def _cargar() -> ModuleType:
    spec = importlib.util.spec_from_file_location("contraste_de_lectura", SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


contraste = _cargar()

ROLES = """
| Role  | Value   |
|-------|---------|
| tinta | #595959 |
| papel | #ffffff |
"""


def _sujeto(tmp_path: Path, texto: str) -> str:
    ruta = tmp_path / "sujeto.md"
    ruta.write_text(texto, encoding="utf-8")
    return str(ruta)


@pytest.mark.parametrize(
    ("frente", "fondo", "esperada"),
    [
        ("#767676", "#ffffff", 4.54),  # el caso de control del instrumento del addon
        ("#595959", "#ffffff", 7.00),
        ("#5a5a5a", "#ffffff", 6.90),
        ("#ffffff", "#595959", 7.00),  # simétrica
    ],
)
def test_la_razon_es_la_de_wcag(frente: str, fondo: str, esperada: float) -> None:
    assert contraste.razon(frente, fondo) == pytest.approx(esperada, abs=0.005)


def test_7_a_1_exacto_llega_y_un_poco_menos_no() -> None:
    assert contraste.llega_al_umbral(7.0)
    assert not contraste.llega_al_umbral(6.999)


def test_un_par_de_texto_bajo_7_a_1_sale_con_1_y_se_nombra(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sujeto = _sujeto(
        tmp_path,
        "Texto antes.\n\n"
        "| Foreground | Ground | Kind |\n|---|---|---|\n| #767676 | #ffffff | text |\n",
    )

    codigo = contraste.main([sujeto])

    salida = capsys.readouterr().out
    assert codigo == 1
    assert "#767676 sobre #ffffff (texto): 4.54:1  necesita 7:1  NO" in salida
    assert "1 par(es) de texto juzgado(s), 1 bajo el umbral" in salida


def test_los_roles_se_resuelven_por_nombre_y_7_a_1_pasa(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sujeto = _sujeto(
        tmp_path,
        ROLES + "\n| Foreground | Ground | Kind |\n|---|---|---|\n| tinta | papel | text |\n",
    )

    codigo = contraste.main([sujeto])

    salida = capsys.readouterr().out
    assert codigo == 0
    assert "tinta sobre papel (texto): 7.00:1  necesita 7:1  SÍ" in salida
    assert "1 par(es) de texto juzgado(s), 0 bajo el umbral" in salida


def test_justo_debajo_de_7_a_1_no_pasa(tmp_path: Path) -> None:
    sujeto = _sujeto(
        tmp_path, "| Foreground | Ground | Kind |\n|---|---|---|\n| #5a5a5a | #ffffff | text |\n"
    )

    assert contraste.main([sujeto]) == 1


def test_el_texto_grande_y_los_componentes_no_se_juzgan_ni_se_cuentan(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sujeto = _sujeto(
        tmp_path,
        ROLES
        + "\n| Foreground | Ground | Kind |\n|---|---|---|\n"
        + "| tinta | papel | text |\n"
        + "| #949494 | #ffffff | large |\n"  # ~3:1
        + "| #949494 | #ffffff | component |\n",
    )

    codigo = contraste.main([sujeto])

    assert codigo == 0
    assert "1 par(es) de texto juzgado(s), 0 bajo el umbral" in capsys.readouterr().out


@pytest.mark.parametrize(
    "texto",
    [
        "Un documento sin tablas.\n",
        ROLES,
        "| Foreground | Ground | Kind |\n|---|---|---|\n| #949494 | #ffffff | large |\n",
    ],
)
def test_sin_pares_de_texto_no_hay_verde(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], texto: str
) -> None:
    codigo = contraste.main([_sujeto(tmp_path, texto)])

    assert codigo == 2
    assert "0 par(es) de texto juzgado(s) — nada que juzgar" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("par", "nombrado"),
    [
        ("| hueso | papel | text |", "hueso"),  # un rol que no existe
        ("| #12345 | #ffffff | text |", "#12345"),  # un color ilegible
    ],
)
def test_una_entrada_que_no_se_puede_leer_sale_con_2_y_se_nombra(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], par: str, nombrado: str
) -> None:
    sujeto = _sujeto(tmp_path, ROLES + "\n| Foreground | Ground | Kind |\n|---|---|---|\n" + par)

    codigo = contraste.main([sujeto])

    assert codigo == 2
    assert nombrado in capsys.readouterr().out


def test_sin_argumento_o_con_un_archivo_que_no_existe_sale_con_2(tmp_path: Path) -> None:
    assert contraste.main([]) == 2
    assert contraste.main([str(tmp_path / "no-existe.md")]) == 2
