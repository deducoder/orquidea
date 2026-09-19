import pytest

from orquidea.coleccion.modelo import (
    Ejemplar,
    EjemplarConEspecie,
    EjemplarInvalido,
    resolver,
    validar_ejemplar_propio,
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
    assert validar_ejemplar_propio("  Cattleya de mi abuela ", "") == ("Cattleya de mi abuela", "")


@pytest.mark.parametrize("nombre", ["", " ", "   \t\n"])
def test_el_nombre_es_obligatorio(nombre: str) -> None:
    with pytest.raises(EjemplarInvalido, match="El nombre es obligatorio."):
        validar_ejemplar_propio(nombre, "")


def test_el_nombre_admite_120_y_rechaza_121_caracteres() -> None:
    assert validar_ejemplar_propio("x" * 120, "")[0] == "x" * 120

    with pytest.raises(EjemplarInvalido, match="El nombre no puede pasar de 120 caracteres."):
        validar_ejemplar_propio("x" * 121, "")


def test_el_limite_del_nombre_se_mide_despues_de_recortar() -> None:
    assert validar_ejemplar_propio(" " + "x" * 120 + " ", "")[0] == "x" * 120


def test_las_notas_admiten_2000_y_rechazan_2001_caracteres() -> None:
    assert validar_ejemplar_propio("ok", "n" * 2000)[1] == "n" * 2000

    with pytest.raises(EjemplarInvalido, match="Las notas no pueden pasar de 2000 caracteres."):
        validar_ejemplar_propio("ok", "n" * 2001)


def test_las_notas_normalizan_los_saltos_de_linea_y_se_recortan() -> None:
    assert validar_ejemplar_propio("ok", "  Regalo\r\nde 2019\rfloreció \n")[1] == (
        "Regalo\nde 2019\nfloreció"
    )
