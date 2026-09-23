import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "derivar-medidas.py"


def _cargar() -> ModuleType:
    spec = importlib.util.spec_from_file_location("derivar_medidas", SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


medidas = _cargar()

ESCALA_A = [
    "escala",
    "--base",
    "16",
    "--razon",
    "1.25",
    "--escalones",
    "0,1,2",
    "--roles",
    "text=0,binomial=0,date=0,subtitulo=1,titulo=2",
]


# --- las funciones de la regla ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [(12.5, 13), (13.333, 13), (19.2, 19), (20.25, 20), (23.04, 23), (24.5, 25)],
)
def test_el_tamano_se_redondea_al_mas_cercano_medio_hacia_arriba(
    valor: float, esperado: int
) -> None:
    assert medidas.redondear(valor) == esperado


@pytest.mark.parametrize(
    ("tamano", "esperada"),
    [(16, 24), (20, 32), (25, 36), (13, 20), (24, 36), (36, 56), (19, 28), (23, 36), (12, 20)],
)
def test_la_altura_de_linea_es_el_multiplo_de_4_mas_cercano_a_1_5_veces(
    tamano: int, esperada: int
) -> None:
    # 20 · 1.5 = 30, a medio camino entre 28 y 32: medio hacia arriba; con 12 (4.5 cuartos) el
    # redondeo al par de `round` daría 16
    assert medidas.altura_de_linea(tamano) == esperada


def test_la_escala_da_base_por_razon_a_la_n() -> None:
    escalones = medidas.escala(16, 1.2, [-1, 0, 1, 2], {"date": -1, "text": 0})

    assert [(e.id, e.tamano) for e in escalones] == [(-1, 13), (0, 16), (1, 19), (2, 23)]
    assert escalones[0].roles == ["date"]
    assert escalones[1].roles == ["text"]
    assert escalones[2].roles == []


def test_el_espaciado_da_la_unidad_por_cada_multiplicador() -> None:
    pasos = medidas.espaciado(16, 3, [1, 2, 3, 4, 6])

    assert [(p.id, p.valor) for p in pasos] == [(1, 8), (2, 16), (3, 24), (4, 32), (6, 48)]


def test_una_unidad_que_no_es_entera_se_rechaza() -> None:
    with pytest.raises(ValueError, match="unidad"):
        medidas.espaciado(16, 5, [1, 2])  # 24 / 5 = 4.8


# --- la salida -------------------------------------------------------------------------------


def test_la_escala_sale_en_la_tabla_que_lee_design_md(capsys: pytest.CaptureFixture[str]) -> None:
    codigo = medidas.main(ESCALA_A)

    assert codigo == 0
    assert capsys.readouterr().out == (
        "| Step | Size | Line height | Roles |\n"
        "|---|---|---|---|\n"
        "| 0 | 16px | 24px | text, binomial, date |\n"
        "| 1 | 20px | 32px | subtitulo |\n"
        "| 2 | 25px | 36px | titulo |\n"
    )


def test_un_escalon_negativo_y_uno_sin_roles_se_escriben(
    capsys: pytest.CaptureFixture[str],
) -> None:
    argumentos = ["escala", "--base", "16", "--razon", "1.2", "--escalones", "-1,0,1"]
    medidas.main([*argumentos, "--roles", "date=-1,text=0"])

    salida = capsys.readouterr().out
    assert "| -1 | 13px | 20px | date |\n" in salida
    assert "| 1 | 19px | 28px | — |\n" in salida


def test_el_espaciado_sale_en_la_tabla_que_lee_design_md_y_marca_el_control(
    capsys: pytest.CaptureFixture[str],
) -> None:
    argumentos = ["espaciado", "--base", "16", "--divisor", "3", "--multiplicadores"]
    codigo = medidas.main([*argumentos, "1,2,3,4,6", "--control", "6"])

    assert codigo == 0
    assert capsys.readouterr().out == (
        "| Step | Value | Where it is used |\n"
        "|---|---|---|\n"
        "| 1 | 8px | 1 unidad |\n"
        "| 2 | 16px | 2 unidades |\n"
        "| 3 | 24px | 3 unidades |\n"
        "| 4 | 32px | 4 unidades |\n"
        "| 6 | 48px | 6 unidades; tamaño de control |\n"
    )


def test_la_salida_es_la_misma_al_correr_otra_vez(capsys: pytest.CaptureFixture[str]) -> None:
    medidas.main(ESCALA_A)
    primera = capsys.readouterr().out
    medidas.main(ESCALA_A)

    assert capsys.readouterr().out == primera


@pytest.mark.parametrize(
    "argumentos",
    [
        [],
        ["otra"],
        ["escala", "--base", "16", "--razon", "1.25", "--escalones", "0,1"],  # sin roles
        [*ESCALA_A[:-1], "text=7"],  # un rol en un escalón que no existe
        [*ESCALA_A[:4], "uno", *ESCALA_A[5:]],  # razón ilegible
        ["espaciado", "--base", "16", "--divisor", "5", "--multiplicadores", "1", "--control", "1"],
        [
            "espaciado",
            "--base",
            "16",
            "--divisor",
            "3",
            "--multiplicadores",
            "1,2",
            "--control",
            "6",
        ],
    ],
)
def test_argumentos_ilegibles_salen_con_2_sin_tabla(
    argumentos: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    assert medidas.main(argumentos) == 2
    assert "| Step |" not in capsys.readouterr().out
