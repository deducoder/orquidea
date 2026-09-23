import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "comprobar-medidas.py"


def _cargar() -> ModuleType:
    spec = importlib.util.spec_from_file_location("comprobar_medidas", SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


comprobar = _cargar()

ESCALA = (
    "| Step | Size | Line height | Roles |\n|---|---|---|---|\n"
    "| 0 | 16px | 24px | text, binomial, date |\n"
    "| 1 | 20px | 32px | subtitulo |\n"
)
PISO = ["--piso", "16", "--lectura", "text,binomial,date"]


def _sujeto(tmp_path: Path, texto: str) -> str:
    ruta = tmp_path / "sujeto.md"
    ruta.write_text(texto, encoding="utf-8")
    return str(ruta)


# --- piso ------------------------------------------------------------------------------------


def test_piso_en_verde_cuenta_escalones_y_roles(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    codigo = comprobar.main(["piso", _sujeto(tmp_path, ESCALA), *PISO])

    salida = capsys.readouterr().out
    assert codigo == 0
    assert "text: escalón 0 = 16px  piso 16px  SÍ" in salida
    assert "2 escalón(es) y 3 rol(es) de lectura medidos, 0 bajo el piso, 0 colapsado(s)" in salida


def test_un_rol_de_lectura_bajo_el_piso_sale_con_1_y_se_nombra(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    escala = (
        ESCALA.replace("text, binomial, date", "text, binomial") + "| -1 | 15px | 24px | date |\n"
    )

    codigo = comprobar.main(["piso", _sujeto(tmp_path, escala), *PISO])

    salida = capsys.readouterr().out
    assert codigo == 1
    assert "date: escalón -1 = 15px  piso 16px  NO" in salida
    assert "1 bajo el piso" in salida


def test_exactamente_en_el_piso_pasa(tmp_path: Path) -> None:
    assert comprobar.main(["piso", _sujeto(tmp_path, ESCALA), *PISO]) == 0


def test_dos_escalones_con_el_mismo_tamano_colapsan(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    escala = ESCALA + "| 2 | 20px | 32px | titulo |\n"

    codigo = comprobar.main(["piso", _sujeto(tmp_path, escala), *PISO])

    salida = capsys.readouterr().out
    assert codigo == 1
    assert "escalones 1 y 2 colapsan en 20px" in salida
    assert "1 colapsado(s)" in salida


@pytest.mark.parametrize(
    ("texto", "nombrado"),
    [
        ("Sin tablas.\n", "0 escalón(es)"),
        (ESCALA.replace("text, binomial, date", "text, binomial"), "date"),  # un rol sin escalón
        (ESCALA.replace("16px | 24px", "dieciséis | 24px"), "dieciséis"),  # tamaño ilegible
        (ESCALA.replace("| 1 | 20px | 32px | subtitulo |", "| 1 |"), "fila"),  # fila corta
    ],
)
def test_piso_sin_sujeto_o_ilegible_sale_con_2_y_lo_nombra(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], texto: str, nombrado: str
) -> None:
    codigo = comprobar.main(["piso", _sujeto(tmp_path, texto), *PISO])

    assert codigo == 2
    assert nombrado in capsys.readouterr().out


# --- objetivos -------------------------------------------------------------------------------

OBJETIVOS = (
    "| Target | Width | Height |\n|--------|-------|--------|\n"
    "| boton | 48 | 48 |\n| campo | 48 | 48 |\n"
)


def test_objetivos_en_verde_cuenta_la_poblacion(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    codigo = comprobar.main(["objetivos", _sujeto(tmp_path, OBJETIVOS), "--minimo", "44"])

    salida = capsys.readouterr().out
    assert codigo == 0
    assert "boton 48×48  necesita 44×44  SÍ" in salida
    assert "2 objetivo(s) medidos, 0 bajo 44 px" in salida


@pytest.mark.parametrize(
    ("fila", "dimension"), [("| boton | 48 | 40 |", "alto"), ("| boton | 20 | 48 |", "ancho")]
)
def test_un_objetivo_bajo_el_minimo_en_una_dimension_sale_con_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], fila: str, dimension: str
) -> None:
    texto = OBJETIVOS.replace("| boton | 48 | 48 |", fila)

    codigo = comprobar.main(["objetivos", _sujeto(tmp_path, texto), "--minimo", "44"])

    salida = capsys.readouterr().out
    assert codigo == 1
    assert f"boton: {dimension} bajo 44" in salida
    assert "1 bajo 44 px" in salida


def test_exactamente_en_el_minimo_pasa(tmp_path: Path) -> None:
    texto = OBJETIVOS.replace("| boton | 48 | 48 |", "| boton | 44 | 44 |")

    assert comprobar.main(["objetivos", _sujeto(tmp_path, texto), "--minimo", "44"]) == 0


@pytest.mark.parametrize(
    "texto",
    [
        "Sin tablas.\n",
        "| Target | Width | Height |\n|---|---|---|\n",
        OBJETIVOS.replace("| 48 | 48 |\n| campo", "| ancho | 48 |\n| campo"),
        OBJETIVOS.replace("| boton | 48 | 48 |", "| boton | 48 |"),  # fila corta: no es un rojo
    ],
)
def test_objetivos_sin_sujeto_o_ilegible_sale_con_2(tmp_path: Path, texto: str) -> None:
    assert comprobar.main(["objetivos", _sujeto(tmp_path, texto), "--minimo", "44"]) == 2


MINIMOS = (
    "| Token | Value | From |\n|-------|-------|------|\n"
    "| components.tarjeta.padding | 16px | spacing.step-2 |\n"
    "| components.boton.minHeight | 48px | spacing.step-6 |\n"
    "| components.boton.minWidth | 48px | spacing.step-6 |\n"
)


def test_los_minimos_declarados_se_miden_sin_tabla_target(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    codigo = comprobar.main(["objetivos", _sujeto(tmp_path, MINIMOS), "--minimo", "44"])

    salida = capsys.readouterr().out
    assert codigo == 0
    assert "boton mínimo 48×48  necesita 44×44  SÍ" in salida
    assert "1 objetivo(s) medidos, 0 bajo 44 px" in salida


@pytest.mark.parametrize(("token", "dimension"), [("minHeight", "alto"), ("minWidth", "ancho")])
def test_un_minimo_bajo_el_umbral_sale_con_1_y_se_nombra(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], token: str, dimension: str
) -> None:
    texto = MINIMOS.replace(f"boton.{token} | 48px", f"boton.{token} | 32px")

    codigo = comprobar.main(["objetivos", _sujeto(tmp_path, texto), "--minimo", "44"])

    salida = capsys.readouterr().out
    assert codigo == 1
    assert f"boton: {dimension} bajo 44" in salida
    assert "1 objetivo(s) medidos, 1 bajo 44 px" in salida


def test_un_minimo_exactamente_en_el_umbral_pasa(tmp_path: Path) -> None:
    texto = MINIMOS.replace("| 48px |", "| 44px |")

    assert comprobar.main(["objetivos", _sujeto(tmp_path, texto), "--minimo", "44"]) == 0


def test_una_dimension_sin_minimo_se_dice_no_medida(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    texto = MINIMOS.replace("| components.boton.minHeight | 48px | spacing.step-6 |\n", "")

    codigo = comprobar.main(["objetivos", _sujeto(tmp_path, texto), "--minimo", "44"])

    salida = capsys.readouterr().out
    assert codigo == 0
    assert "boton mínimo ancho 48  necesita 44  SÍ — alto no declarado, no se midió" in salida
    assert "1 objetivo(s) medidos, 0 bajo 44 px" in salida


def test_la_tabla_target_y_los_minimos_se_cuentan_juntos(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    codigo = comprobar.main(
        ["objetivos", _sujeto(tmp_path, OBJETIVOS + "\n" + MINIMOS), "--minimo", "44"]
    )

    assert codigo == 0
    assert "3 objetivo(s) medidos, 0 bajo 44 px" in capsys.readouterr().out


def test_sin_target_y_sin_minimos_sale_con_2(tmp_path: Path) -> None:
    texto = "| Token | Value | From |\n|---|---|---|\n| components.tarjeta.padding | 16px | x |\n"

    assert comprobar.main(["objetivos", _sujeto(tmp_path, texto), "--minimo", "44"]) == 2


@pytest.mark.parametrize(
    "argumentos",
    [
        [],
        ["otra", "x.md"],
        ["piso", "no-existe.md", *PISO],
        ["objetivos", "no-existe.md", "--minimo", "44"],
    ],
)
def test_argumentos_ilegibles_salen_con_2(argumentos: list[str]) -> None:
    assert comprobar.main(argumentos) == 2
