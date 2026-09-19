from datetime import date

import pytest

from orquidea.coleccion.modelo import (
    CuidadoInvalido,
    Ejemplar,
    EjemplarConEspecie,
    EjemplarInvalido,
    resolver,
    validar_ejemplar,
    validar_fecha,
    validar_floracion,
)
from tests.fabricas import especie

RADICANS = especie("epidendrum-radicans", "Epidendrum radicans")
ANCEPS = especie("laelia-anceps", "Laelia anceps")


def ejemplar(id: int, especie_id: str | None, nombre: str = "") -> Ejemplar:
    return Ejemplar(id=id, especie_id=especie_id, nombre=nombre, notas="", creado=0)


def test_resolver_empareja_cada_ejemplar_con_su_especie_por_id() -> None:
    ejemplares = [
        ejemplar(1, "laelia-anceps"),
        ejemplar(2, "epidendrum-radicans"),
        ejemplar(3, "laelia-anceps"),
    ]

    resueltos = resolver(ejemplares, [RADICANS, ANCEPS])

    assert [r.especie for r in resueltos] == [ANCEPS, RADICANS, ANCEPS]
    assert [r.ejemplar for r in resueltos] == ejemplares


def test_una_especie_desaparecida_del_catalogo_da_none() -> None:
    (resuelto,) = resolver([ejemplar(1, "ya-no-esta")], [RADICANS])

    assert resuelto == EjemplarConEspecie(ejemplar=ejemplar(1, "ya-no-esta"), especie=None)


def test_un_ejemplar_sin_especie_da_none() -> None:
    (resuelto,) = resolver([ejemplar(1, None, "Mi rara")], [RADICANS])

    assert resuelto.especie is None


def test_resolver_una_coleccion_vacia() -> None:
    assert resolver([], [RADICANS]) == []


def test_el_ejemplar_propio_recorta_el_nombre() -> None:
    assert validar_ejemplar("  Cattleya de mi abuela ", "") == ("Cattleya de mi abuela", "")


@pytest.mark.parametrize("nombre", ["", " ", "   \t\n"])
def test_el_nombre_es_obligatorio(nombre: str) -> None:
    with pytest.raises(EjemplarInvalido, match="El nombre es obligatorio."):
        validar_ejemplar(nombre, "")


def test_el_nombre_admite_120_y_rechaza_121_caracteres() -> None:
    assert validar_ejemplar("x" * 120, "")[0] == "x" * 120

    with pytest.raises(EjemplarInvalido, match="El nombre no puede pasar de 120 caracteres."):
        validar_ejemplar("x" * 121, "")


def test_el_limite_del_nombre_se_mide_despues_de_recortar() -> None:
    assert validar_ejemplar(" " + "x" * 120 + " ", "")[0] == "x" * 120


def test_las_notas_admiten_2000_y_rechazan_2001_caracteres() -> None:
    assert validar_ejemplar("ok", "n" * 2000)[1] == "n" * 2000

    with pytest.raises(EjemplarInvalido, match="Las notas no pueden pasar de 2000 caracteres."):
        validar_ejemplar("ok", "n" * 2001)


def test_las_notas_normalizan_los_saltos_de_linea_y_se_recortan() -> None:
    assert validar_ejemplar("ok", "  Regalo\r\nde 2019\rfloreció \n")[1] == (
        "Regalo\nde 2019\nfloreció"
    )


def test_con_especie_el_nombre_es_opcional() -> None:
    assert validar_ejemplar("", "notas", con_especie=True) == ("", "notas")
    assert validar_ejemplar("  ", "", con_especie=True) == ("", "")


def test_con_especie_el_nombre_propio_se_recorta_y_se_limita() -> None:
    assert validar_ejemplar("  Mi primera ", "", con_especie=True)[0] == "Mi primera"
    assert validar_ejemplar("x" * 120, "", con_especie=True)[0] == "x" * 120

    with pytest.raises(EjemplarInvalido, match="El nombre no puede pasar de 120 caracteres."):
        validar_ejemplar("x" * 121, "", con_especie=True)


def test_con_especie_las_notas_siguen_limitadas() -> None:
    with pytest.raises(EjemplarInvalido, match="Las notas no pueden pasar de 2000 caracteres."):
        validar_ejemplar("", "n" * 2001, con_especie=True)


def test_sin_especie_el_nombre_sigue_siendo_obligatorio_por_defecto() -> None:
    with pytest.raises(EjemplarInvalido, match="El nombre es obligatorio."):
        validar_ejemplar("", "notas")


HOY = date(2026, 9, 19)


def test_una_fecha_valida_se_devuelve_sin_espacios() -> None:
    assert validar_fecha(" 2026-09-15 ", HOY) == "2026-09-15"


def test_hoy_es_una_fecha_valida() -> None:
    assert validar_fecha("2026-09-19", HOY) == "2026-09-19"


@pytest.mark.parametrize(
    "texto",
    ["19/09/2026", "2026-9-1", "hoy", "2026-09-19T10:00", "20260919", "2026-W38-3", "٢٠٢٦-٠٩-١٥"],
)
def test_una_fecha_con_otro_formato_se_rechaza(texto: str) -> None:
    with pytest.raises(CuidadoInvalido, match="formato AAAA-MM-DD"):
        validar_fecha(texto, HOY)


@pytest.mark.parametrize("texto", ["2026-02-30", "2026-13-01", "2026-00-10"])
def test_una_fecha_que_no_existe_se_rechaza(texto: str) -> None:
    with pytest.raises(CuidadoInvalido, match="no existe"):
        validar_fecha(texto, HOY)


def test_una_fecha_posterior_a_hoy_se_rechaza() -> None:
    with pytest.raises(CuidadoInvalido, match="posterior a hoy"):
        validar_fecha("2026-09-20", HOY)


@pytest.mark.parametrize("texto", ["", "   "])
def test_la_fecha_es_obligatoria(texto: str) -> None:
    with pytest.raises(CuidadoInvalido, match="obligatoria"):
        validar_fecha(texto, HOY)


def test_una_floracion_sin_fin_esta_en_curso() -> None:
    assert validar_floracion(" 2026-03-01 ", "", HOY) == ("2026-03-01", None)
    assert validar_floracion("2026-03-01", "   ", HOY) == ("2026-03-01", None)


def test_una_floracion_con_inicio_y_fin() -> None:
    assert validar_floracion("2026-03-01", " 2026-03-20 ", HOY) == ("2026-03-01", "2026-03-20")


def test_una_floracion_de_un_solo_dia_es_valida() -> None:
    assert validar_floracion("2026-03-01", "2026-03-01", HOY) == ("2026-03-01", "2026-03-01")


def test_un_fin_anterior_al_inicio_se_rechaza() -> None:
    with pytest.raises(CuidadoInvalido, match="fin no puede ser anterior al inicio"):
        validar_floracion("2026-03-20", "2026-03-01", HOY)


def test_el_inicio_es_obligatorio() -> None:
    with pytest.raises(CuidadoInvalido, match="obligatoria"):
        validar_floracion("", "2026-03-01", HOY)


@pytest.mark.parametrize("fin", ["20/03/2026", "2026-02-30", "2026-09-20"])
def test_un_fin_invalido_se_rechaza_como_cualquier_fecha(fin: str) -> None:
    with pytest.raises(CuidadoInvalido):
        validar_floracion("2026-01-01", fin, HOY)


def test_un_inicio_posterior_a_hoy_se_rechaza() -> None:
    with pytest.raises(CuidadoInvalido, match="posterior a hoy"):
        validar_floracion("2026-09-20", "", HOY)
