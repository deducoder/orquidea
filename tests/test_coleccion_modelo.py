from orquidea.coleccion.modelo import Ejemplar, EjemplarConEspecie, resolver
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
