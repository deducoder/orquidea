import colorsys
import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "derivar-primitivas.py"


def _cargar() -> ModuleType:
    spec = importlib.util.spec_from_file_location("derivar_primitivas", SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


primitivas = _cargar()

PALETA = {
    "papel": "#F7F3EA",
    "hoja": "#FFFFFF",
    "tinta": "#1E1C19",
    "tinta suave": "#4A453E",
    "renglón": "#8C8475",
    "acento": "#1F3A5F",
    "alerta": "#8A1C1C",
}

TABLA_PALETA = "| Role | Value |\n|---|---|\n" + "".join(
    f"| {rol} | {valor} |\n" for rol, valor in PALETA.items()
)


def _sujeto(tmp_path: Path, texto: str) -> str:
    ruta = tmp_path / "paleta.md"
    ruta.write_text(texto, encoding="utf-8")
    return str(ruta)


def _pasos(regla: str) -> dict[str, str]:
    return {nombre: valor for nombre, valor, _ in primitivas.derivar(PALETA, regla).primitivas}


def _asignados(regla: str) -> dict[str, str]:
    return {a.rol: a.escalon for a in primitivas.derivar(PALETA, regla).asignaciones}


# --- la conversión ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("hexa", "esperado"),
    [
        ("#FFFFFF", (1.0, 0.0, 0.0)),
        ("#FF0000", (0.62796, 0.22486, 0.12585)),  # valores de referencia de Ottosson (OKLab)
        ("#00FF00", (0.86644, -0.23389, 0.17950)),
        ("#0000FF", (0.45201, -0.03246, -0.31153)),
        ("#808080", (0.59987, 0.0, 0.0)),  # un gris medio: aquí se ve la linealización
    ],
)
def test_oklab_da_los_valores_de_referencia(
    hexa: str, esperado: tuple[float, float, float]
) -> None:
    assert primitivas.oklab(hexa) == pytest.approx(esperado, abs=5e-4)


def test_el_hex_se_redondea_al_mas_cercano_no_se_trunca() -> None:
    assert primitivas.a_hexa((0.5, 0.5, 0.5)) == "#808080"  # 127.5 → 128


@pytest.mark.parametrize("hexa", PALETA.values())
def test_ida_y_vuelta_de_la_paleta_da_el_mismo_hex(hexa: str) -> None:
    assert primitivas.hexa_desde_oklab(primitivas.oklab(hexa)) == hexa


# --- la rejilla y las reglas -----------------------------------------------------------------


def test_la_rejilla_son_doce_escalones_de_1_a_0_20_en_pasos_iguales() -> None:
    rejilla = primitivas.rejilla()

    assert len(rejilla) == 12
    assert rejilla[0] == pytest.approx(1.0)
    assert rejilla[-1] == pytest.approx(0.20)
    saltos = [a - b for a, b in zip(rejilla, rejilla[1:], strict=False)]
    assert max(saltos) - min(saltos) < 1e-12


@pytest.mark.parametrize("regla", ["anclas", "oklch", "hsl"])
def test_cada_regla_da_tres_rampas_de_doce_escalones_con_blanco_en_el_0(regla: str) -> None:
    derivacion = primitivas.derivar(PALETA, regla)

    nombres = [nombre for nombre, _, _ in derivacion.primitivas]
    assert len(nombres) == 36
    assert nombres[:12] == [
        f"neutro-{e}" for e in (0, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950)
    ]
    assert {rampa for _, _, rampa in derivacion.primitivas} == {"neutro", "azul", "rojo"}
    pasos = _pasos(regla)
    assert pasos["neutro-0"] == pasos["azul-0"] == pasos["rojo-0"] == "#FFFFFF"


def test_anclas_cada_rol_resuelve_a_su_valor_exacto() -> None:
    pasos = _pasos("anclas")

    for rol, escalon in _asignados("anclas").items():
        assert pasos[escalon] == PALETA[rol]


def test_anclas_los_escalones_intermedios_siguen_la_luminosidad_de_la_rejilla() -> None:
    rejilla = primitivas.rejilla()
    anclas = set(_asignados("anclas").values()) | {"neutro-0", "azul-0", "rojo-0"}
    derivacion = primitivas.derivar(PALETA, "anclas")

    medidos = 0
    for i, (nombre, valor, _) in enumerate(derivacion.primitivas):
        if nombre in anclas:
            continue
        medidos += 1
        assert primitivas.oklab(valor)[0] == pytest.approx(rejilla[i % 12], abs=0.005), nombre
    assert medidos > 20


def test_anclas_el_croma_entre_dos_anclas_queda_entre_los_de_ellas() -> None:
    # entre el blanco (croma 0) y el acento, en OKLCH, el croma crece; interpolar en sRGB no lo da
    pasos = _pasos("anclas")
    escalon_acento = _asignados("anclas")["acento"]
    indice = primitivas.ESCALONES.index(int(escalon_acento.split("-")[1]))
    cromas = [primitivas.oklch(pasos[f"azul-{e}"])[1] for e in primitivas.ESCALONES[: indice + 1]]

    assert cromas == sorted(cromas)
    assert len(cromas) >= 3


def test_oklch_luminosidad_de_la_rejilla_y_tono_constante() -> None:
    rejilla = primitivas.rejilla()
    tono_acento = primitivas.oklch(PALETA["acento"])[2]

    for i, e in enumerate(primitivas.ESCALONES):
        valor = _pasos("oklch")[f"azul-{e}"]
        l_, c, h = primitivas.oklch(valor)
        assert l_ == pytest.approx(rejilla[i], abs=0.005)
        if c > 0.02:
            assert h == pytest.approx(tono_acento, abs=2.0)


def test_hsl_luminosidad_de_hsl_de_la_rejilla() -> None:
    rejilla = primitivas.rejilla()

    for i, e in enumerate(primitivas.ESCALONES):
        valor = _pasos("hsl")[f"rojo-{e}"]
        rgb = [int(valor[k : k + 2], 16) / 255 for k in (1, 3, 5)]
        assert colorsys.rgb_to_hls(*rgb)[1] == pytest.approx(rejilla[i], abs=0.005)


# --- la asignación ---------------------------------------------------------------------------


def test_en_empate_se_toma_el_escalon_mas_oscuro() -> None:
    rejilla = primitivas.rejilla()
    medio = (rejilla[3] + rejilla[4]) / 2

    assert primitivas.mas_cercano(medio, rejilla, ocupados=set()) == 4


def test_dos_roles_no_comparten_escalon() -> None:
    rejilla = primitivas.rejilla()

    # 2 y 4 quedan a la misma distancia: el empate va al más oscuro
    assert primitivas.mas_cercano(rejilla[3], rejilla, ocupados={3}) == 4


@pytest.mark.parametrize("regla", ["anclas", "oklch", "hsl"])
def test_cada_rol_de_la_paleta_se_asigna_una_vez_y_el_desvio_se_mide(regla: str) -> None:
    derivacion = primitivas.derivar(PALETA, regla)
    pasos = _pasos(regla)

    assert {a.rol for a in derivacion.asignaciones} == set(PALETA)
    assert len({a.escalon for a in derivacion.asignaciones}) == len(PALETA)
    for a in derivacion.asignaciones:
        assert a.valor == pasos[a.escalon]
        assert a.desvio == pytest.approx(primitivas.delta_e(PALETA[a.rol], a.valor))


def test_una_regla_desconocida_no_cae_en_otra() -> None:
    with pytest.raises(ValueError, match="anclass"):
        primitivas.derivar(PALETA, "anclass")


def test_con_anclas_el_desvio_es_cero() -> None:
    assert all(a.desvio == 0 for a in primitivas.derivar(PALETA, "anclas").asignaciones)


# --- la salida -------------------------------------------------------------------------------


def test_la_salida_son_las_dos_tablas_y_sale_con_0(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    codigo = primitivas.main([_sujeto(tmp_path, TABLA_PALETA), "--regla", "anclas"])

    salida = capsys.readouterr().out
    assert codigo == 0
    assert salida.startswith(
        "| Step | Value | Ramp |\n|---|---|---|\n| neutro-0 | #FFFFFF | neutro |\n"
    )
    assert "| Identity role | Identity value | Resolves to | Primitive | Drift |" in salida
    assert "| acento | #1F3A5F | " in salida
    assert salida.count("\n| ") == 36 + 1 + 7  # filas de datos más la cabecera de la segunda tabla


def test_la_salida_es_la_misma_al_correr_otra_vez(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sujeto = _sujeto(tmp_path, TABLA_PALETA)
    primitivas.main([sujeto, "--regla", "oklch"])
    primera = capsys.readouterr().out
    primitivas.main([sujeto, "--regla", "oklch"])

    assert capsys.readouterr().out == primera


def test_un_rol_ausente_sale_con_2_y_se_nombra(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    sin_renglon = TABLA_PALETA.replace("| renglón | #8C8475 |\n", "")

    codigo = primitivas.main([_sujeto(tmp_path, sin_renglon), "--regla", "anclas"])

    salida = capsys.readouterr().out
    assert codigo == 2
    assert "renglón" in salida
    assert "| Step |" not in salida


def test_un_valor_ilegible_sale_con_2_y_se_nombra(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    ilegible = TABLA_PALETA.replace("#8A1C1C", "#8A1C1")

    codigo = primitivas.main([_sujeto(tmp_path, ilegible), "--regla", "anclas"])

    assert codigo == 2
    assert "alerta" in capsys.readouterr().out


@pytest.mark.parametrize(
    "argumentos",
    [[], ["--regla", "anclas"], ["no-existe.md", "--regla", "anclas"], ["PALETA", "--regla", "x"]],
)
def test_argumentos_ilegibles_salen_con_2(tmp_path: Path, argumentos: list[str]) -> None:
    sujeto = _sujeto(tmp_path, TABLA_PALETA)
    argumentos = [sujeto if a == "PALETA" else a for a in argumentos]

    assert primitivas.main(argumentos) == 2


# --- el entregable ---------------------------------------------------------------------------

RAIZ = Path(__file__).parent.parent
PRIMITIVAS = RAIZ / "governance" / "identity" / "ui" / "primitives.md"
PALETA_REAL = RAIZ / "governance" / "identity" / "palette.md"


def _filas_de(texto: str, primeras: tuple[str, ...]) -> list[str]:
    """Las filas (cabecera incluida) de las tablas cuyo encabezado empieza por una de `primeras`."""
    filas: list[str] = []
    en_tabla = False
    for linea in texto.splitlines():
        if not linea.startswith("|"):
            en_tabla = False
            continue
        primera = linea.strip("|").split("|")[0].strip()
        if primera in primeras:
            en_tabla = True
        if en_tabla and not primera.startswith("---"):
            filas.append(linea.strip())
    return filas


def test_primitives_md_es_lo_que_la_regla_registrada_produce(
    capsys: pytest.CaptureFixture[str],
) -> None:
    texto = PRIMITIVAS.read_text(encoding="utf-8")
    regla = next(
        f.split("|")[2].strip().strip("`")
        for f in _filas_de(texto, ("Parameter",))
        if f.split("|")[1].strip() == "regla"
    )

    assert primitivas.main([str(PALETA_REAL), "--regla", regla]) == 0
    esperadas = _filas_de(capsys.readouterr().out, ("Step", "Identity role"))
    escritas = _filas_de(texto, ("Step", "Identity role"))
    assert len(escritas) == 36 + 7 + 2  # sin tablas no hay verde
    assert escritas == esperadas
