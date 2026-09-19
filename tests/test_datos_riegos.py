import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from orquidea.coleccion.modelo import CUIDADOS_MAXIMO, CuidadoInvalido, Riego
from orquidea.datos.base import MIGRACIONES, abrir_base, conectar
from orquidea.datos.ejemplares import agregar as agregar_ejemplar
from orquidea.datos.ejemplares import fijar_foto, listar
from orquidea.datos.ejemplares import quitar as quitar_ejemplar
from orquidea.datos.riegos import agregar, quitar, ultimo
from orquidea.datos.riegos import listar as listar_riegos

AHORA = 1_780_000_000


@pytest.fixture
def conexion(tmp_path: Path) -> sqlite3.Connection:
    return abrir_base(tmp_path / "o.sqlite3")


def un_ejemplar(conexion: sqlite3.Connection) -> int:
    return agregar_ejemplar(conexion, "epidendrum-radicans", AHORA).id


def test_agregar_guarda_el_riego_del_ejemplar(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)

    riego = agregar(conexion, ejemplar, "2026-09-15")

    assert riego is not None
    assert riego == Riego(id=riego.id, ejemplar_id=ejemplar, fecha="2026-09-15")
    assert listar_riegos(conexion, ejemplar) == [riego]


def test_agregar_a_un_ejemplar_inexistente_no_guarda_nada(conexion: sqlite3.Connection) -> None:
    assert agregar(conexion, 999, "2026-09-15") is None
    assert conexion.execute("SELECT COUNT(*) FROM riegos").fetchone() == (0,)


def test_el_historial_sale_por_fecha_y_a_igual_fecha_por_id(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)
    for fecha in ("2026-09-15", "2026-09-01", "2026-09-15"):
        agregar(conexion, ejemplar, fecha)

    historial = listar_riegos(conexion, ejemplar)

    assert [(r.fecha, r.id) for r in historial] == [
        ("2026-09-01", 2),
        ("2026-09-15", 1),
        ("2026-09-15", 3),
    ]


def test_el_historial_es_solo_del_ejemplar(conexion: sqlite3.Connection) -> None:
    uno, otro = un_ejemplar(conexion), un_ejemplar(conexion)
    agregar(conexion, uno, "2026-09-15")
    agregar(conexion, otro, "2026-09-16")

    assert [r.fecha for r in listar_riegos(conexion, uno)] == ["2026-09-15"]


def test_el_ultimo_es_el_de_mayor_fecha(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)
    for fecha in ("2026-09-01", "2026-09-15", "2026-09-10"):
        agregar(conexion, ejemplar, fecha)

    ultimo_riego = ultimo(conexion, ejemplar)

    assert ultimo_riego is not None and ultimo_riego.fecha == "2026-09-15"


def test_a_igual_fecha_el_ultimo_es_el_de_mayor_id(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)
    agregar(conexion, ejemplar, "2026-09-15")
    segundo = agregar(conexion, ejemplar, "2026-09-15")

    assert ultimo(conexion, ejemplar) == segundo


def test_sin_riegos_no_hay_ultimo(conexion: sqlite3.Connection) -> None:
    assert ultimo(conexion, un_ejemplar(conexion)) is None


def test_quitar_borra_solo_ese_riego(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)
    primero = agregar(conexion, ejemplar, "2026-09-01")
    segundo = agregar(conexion, ejemplar, "2026-09-02")
    assert primero is not None and segundo is not None

    assert quitar(conexion, ejemplar, primero.id) is True

    assert listar_riegos(conexion, ejemplar) == [segundo]


def test_quitar_con_el_ejemplar_equivocado_no_borra_nada(conexion: sqlite3.Connection) -> None:
    uno, otro = un_ejemplar(conexion), un_ejemplar(conexion)
    ajeno = agregar(conexion, otro, "2026-09-01")
    assert ajeno is not None

    assert quitar(conexion, uno, ajeno.id) is False

    assert listar_riegos(conexion, otro) == [ajeno]


def test_quitar_un_riego_inexistente_devuelve_false(conexion: sqlite3.Connection) -> None:
    assert quitar(conexion, un_ejemplar(conexion), 999) is False


def test_quitar_el_ejemplar_borra_sus_riegos_y_no_los_de_otros(
    conexion: sqlite3.Connection,
) -> None:
    uno, otro = un_ejemplar(conexion), un_ejemplar(conexion)
    agregar(conexion, uno, "2026-09-01")
    agregar(conexion, otro, "2026-09-02")

    quitar_ejemplar(conexion, uno)

    assert conexion.execute("SELECT ejemplar_id FROM riegos").fetchall() == [(otro,)]


def test_el_ejemplar_con_el_tope_rechaza_un_riego_mas(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)
    conexion.executemany(
        "INSERT INTO riegos (ejemplar_id, fecha) VALUES (?, '2026-01-01')",
        [(ejemplar,)] * CUIDADOS_MAXIMO,
    )

    with pytest.raises(CuidadoInvalido, match="500 riegos"):
        agregar(conexion, ejemplar, "2026-09-15")

    assert conexion.execute("SELECT COUNT(*) FROM riegos").fetchone() == (CUIDADOS_MAXIMO,)


def test_el_tope_es_por_ejemplar(conexion: sqlite3.Connection) -> None:
    lleno, otro = un_ejemplar(conexion), un_ejemplar(conexion)
    conexion.executemany(
        "INSERT INTO riegos (ejemplar_id, fecha) VALUES (?, '2026-01-01')",
        [(lleno,)] * CUIDADOS_MAXIMO,
    )

    assert agregar(conexion, otro, "2026-09-15") is not None


@pytest.mark.parametrize("fecha", ["ayer", "2026-9-1", "20260915", "2026-09-15 ", ""])
def test_la_tabla_rechaza_una_fecha_con_otra_forma(
    conexion: sqlite3.Connection, fecha: str
) -> None:
    ejemplar = un_ejemplar(conexion)

    with pytest.raises(sqlite3.IntegrityError):
        conexion.execute("INSERT INTO riegos (ejemplar_id, fecha) VALUES (?, ?)", (ejemplar, fecha))


def test_la_migracion_conserva_los_ejemplares_y_sus_fotos(tmp_path: Path) -> None:
    anteriores = tmp_path / "hasta-0003"
    anteriores.mkdir()
    for archivo in sorted(MIGRACIONES.glob("000[123]-*.sql")):
        (anteriores / archivo.name).write_text(archivo.read_text(encoding="utf-8"))
    ruta = tmp_path / "o.sqlite3"
    vieja = abrir_base(ruta, anteriores)
    ejemplar = un_ejemplar(vieja)
    fijar_foto(vieja, ejemplar, "Xq3vT")
    assert vieja.execute("PRAGMA user_version").fetchone() == (3,)
    vieja.close()

    nueva = abrir_base(ruta)

    (conservado,) = listar(nueva)
    assert (conservado.id, conservado.foto) == (ejemplar, "Xq3vT")
    assert nueva.execute("SELECT COUNT(*) FROM riegos").fetchone() == (0,)
    assert nueva.execute("PRAGMA user_version").fetchone() == (4,)


def test_altas_simultaneas_no_rebasan_el_tope(tmp_path: Path) -> None:
    ruta = tmp_path / "o.sqlite3"
    base = abrir_base(ruta)
    ejemplar = un_ejemplar(base)
    base.executemany(
        "INSERT INTO riegos (ejemplar_id, fecha) VALUES (?, '2026-01-01')",
        [(ejemplar,)] * (CUIDADOS_MAXIMO - 1),
    )
    hilos = 8
    salida = threading.Barrier(hilos)

    def alta(_: int) -> bool:
        conexion = conectar(ruta)  # como cada petición: una conexión propia
        try:
            salida.wait()
            agregar(conexion, ejemplar, "2026-09-15")
            return True
        except CuidadoInvalido:
            return False
        finally:
            conexion.close()

    with ThreadPoolExecutor(max_workers=hilos) as pool:
        resultados = list(pool.map(alta, range(hilos)))

    assert resultados.count(True) == 1
    assert base.execute("SELECT COUNT(*) FROM riegos").fetchone() == (CUIDADOS_MAXIMO,)
