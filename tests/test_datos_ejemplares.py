import sqlite3
from pathlib import Path

import pytest

from orquidea.coleccion.modelo import Ejemplar
from orquidea.datos.base import abrir_base
from orquidea.datos.ejemplares import agregar, agregar_sin_especie, listar

AHORA = 1_780_000_000


@pytest.fixture
def conexion(tmp_path: Path) -> sqlite3.Connection:
    return abrir_base(tmp_path / "o.sqlite3")


def test_agregar_guarda_y_devuelve_el_ejemplar(conexion: sqlite3.Connection) -> None:
    ejemplar = agregar(conexion, "epidendrum-radicans", AHORA)

    assert ejemplar == Ejemplar(
        id=ejemplar.id, especie_id="epidendrum-radicans", nombre="", notas="", creado=AHORA
    )
    assert listar(conexion) == [ejemplar]


def test_dos_ejemplares_de_la_misma_especie_son_independientes(
    conexion: sqlite3.Connection,
) -> None:
    uno = agregar(conexion, "epidendrum-radicans", AHORA)
    otro = agregar(conexion, "epidendrum-radicans", AHORA + 5)

    assert uno.id != otro.id
    assert [e.id for e in listar(conexion)] == [uno.id, otro.id]


def test_listar_ordena_por_id_ascendente(conexion: sqlite3.Connection) -> None:
    ids = [agregar(conexion, f"especie-{n}", AHORA - n).id for n in range(3)]

    assert [e.id for e in listar(conexion)] == ids == sorted(ids)


def test_listar_una_coleccion_vacia(conexion: sqlite3.Connection) -> None:
    assert listar(conexion) == []


def test_los_ejemplares_persisten_al_reabrir_la_base(tmp_path: Path) -> None:
    ruta = tmp_path / "o.sqlite3"
    primera = abrir_base(ruta)
    ejemplar = agregar(primera, "epidendrum-radicans", AHORA)
    primera.close()

    assert listar(abrir_base(ruta)) == [ejemplar]


def test_un_especie_id_con_comillas_se_guarda_literal(conexion: sqlite3.Connection) -> None:
    raro = "x'); DROP TABLE ejemplares; --"

    agregar(conexion, raro, AHORA)

    assert [e.especie_id for e in listar(conexion)] == [raro]


def test_la_base_rechaza_un_ejemplar_sin_especie_ni_nombre(conexion: sqlite3.Connection) -> None:
    for nombre in ("", "   "):
        with pytest.raises(sqlite3.IntegrityError):
            conexion.execute(
                "INSERT INTO ejemplares (especie_id, nombre, creado) VALUES (NULL, ?, ?)",
                (nombre, AHORA),
            )


def test_la_base_acepta_un_ejemplar_solo_con_nombre(conexion: sqlite3.Connection) -> None:
    conexion.execute(
        "INSERT INTO ejemplares (especie_id, nombre, creado) VALUES (NULL, 'Mi rara', ?)",
        (AHORA,),
    )

    (ejemplar,) = listar(conexion)
    assert ejemplar.especie_id is None
    assert ejemplar.nombre == "Mi rara"


def test_agregar_sin_especie_guarda_nombre_y_notas(conexion: sqlite3.Connection) -> None:
    ejemplar = agregar_sin_especie(conexion, "Cattleya de mi abuela", "Regalo de 2019", AHORA)

    assert ejemplar == Ejemplar(
        id=ejemplar.id,
        especie_id=None,
        nombre="Cattleya de mi abuela",
        notas="Regalo de 2019",
        creado=AHORA,
    )
    assert listar(conexion) == [ejemplar]


def test_agregar_sin_especie_usa_parametros(conexion: sqlite3.Connection) -> None:
    raro = "x'); DROP TABLE ejemplares; --"

    agregar_sin_especie(conexion, raro, raro, AHORA)

    (ejemplar,) = listar(conexion)
    assert (ejemplar.nombre, ejemplar.notas) == (raro, raro)
