import sqlite3
import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from orquidea.coleccion.modelo import CUIDADOS_MAXIMO, CuidadoInvalido, Floracion
from orquidea.datos.base import MIGRACIONES, abrir_base, conectar
from orquidea.datos.ejemplares import agregar as agregar_ejemplar
from orquidea.datos.ejemplares import fijar_foto, listar
from orquidea.datos.ejemplares import quitar as quitar_ejemplar
from orquidea.datos.floraciones import agregar, quitar, terminar
from orquidea.datos.floraciones import listar as listar_floraciones
from orquidea.datos.riegos import agregar as agregar_riego

AHORA = 1_780_000_000


@pytest.fixture
def conexion(tmp_path: Path) -> sqlite3.Connection:
    return abrir_base(tmp_path / "o.sqlite3")


def un_ejemplar(conexion: sqlite3.Connection) -> int:
    return agregar_ejemplar(conexion, "epidendrum-radicans", AHORA).id


def una_floracion(conexion: sqlite3.Connection, ejemplar: int, inicio: str, fin: str | None) -> int:
    floracion = agregar(conexion, ejemplar, inicio, fin)
    assert floracion is not None
    return floracion.id


def test_agregar_sin_fin_deja_la_floracion_en_curso(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)

    floracion = agregar(conexion, ejemplar, "2026-03-01", None)

    assert floracion is not None
    assert floracion == Floracion(
        id=floracion.id, ejemplar_id=ejemplar, inicio="2026-03-01", fin=None
    )
    assert listar_floraciones(conexion, ejemplar) == [floracion]


def test_agregar_con_fin_guarda_las_dos_fechas(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)

    floracion = agregar(conexion, ejemplar, "2026-03-01", "2026-03-20")

    assert floracion is not None and (floracion.inicio, floracion.fin) == (
        "2026-03-01",
        "2026-03-20",
    )
    assert listar_floraciones(conexion, ejemplar) == [floracion]


def test_agregar_a_un_ejemplar_inexistente_no_guarda_nada(conexion: sqlite3.Connection) -> None:
    assert agregar(conexion, 999, "2026-03-01", None) is None
    assert conexion.execute("SELECT COUNT(*) FROM floraciones").fetchone() == (0,)


def test_el_historial_sale_por_inicio_y_a_igual_inicio_por_id(
    conexion: sqlite3.Connection,
) -> None:
    ejemplar = un_ejemplar(conexion)
    for inicio in ("2026-03-15", "2026-01-10", "2026-03-15"):
        agregar(conexion, ejemplar, inicio, None)

    historial = listar_floraciones(conexion, ejemplar)

    assert [(f.inicio, f.id) for f in historial] == [
        ("2026-01-10", 2),
        ("2026-03-15", 1),
        ("2026-03-15", 3),
    ]


def test_el_historial_es_solo_del_ejemplar(conexion: sqlite3.Connection) -> None:
    uno, otro = un_ejemplar(conexion), un_ejemplar(conexion)
    agregar(conexion, uno, "2026-03-01", None)
    agregar(conexion, otro, "2026-04-01", None)

    assert [f.inicio for f in listar_floraciones(conexion, uno)] == ["2026-03-01"]


def test_terminar_una_floracion_en_curso_fija_su_fin(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)
    id = una_floracion(conexion, ejemplar, "2026-03-01", None)

    assert terminar(conexion, ejemplar, id, "2026-03-20") is True

    (floracion,) = listar_floraciones(conexion, ejemplar)
    assert floracion.fin == "2026-03-20"


def test_terminar_el_mismo_dia_del_inicio_se_acepta(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)
    id = una_floracion(conexion, ejemplar, "2026-03-01", None)

    assert terminar(conexion, ejemplar, id, "2026-03-01") is True


def test_terminar_una_ya_terminada_se_rechaza_y_no_cambia(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)
    id = una_floracion(conexion, ejemplar, "2026-03-01", "2026-03-20")

    with pytest.raises(CuidadoInvalido, match="ya terminó"):
        terminar(conexion, ejemplar, id, "2026-03-25")

    assert listar_floraciones(conexion, ejemplar)[0].fin == "2026-03-20"


def test_terminar_con_un_fin_anterior_al_inicio_se_rechaza_y_sigue_en_curso(
    conexion: sqlite3.Connection,
) -> None:
    ejemplar = un_ejemplar(conexion)
    id = una_floracion(conexion, ejemplar, "2026-03-10", None)

    with pytest.raises(CuidadoInvalido, match="fin no puede ser anterior al inicio"):
        terminar(conexion, ejemplar, id, "2026-03-01")

    assert listar_floraciones(conexion, ejemplar)[0].fin is None


def test_terminar_la_floracion_de_otro_ejemplar_no_cambia_nada(
    conexion: sqlite3.Connection,
) -> None:
    uno, otro = un_ejemplar(conexion), un_ejemplar(conexion)
    ajena = una_floracion(conexion, otro, "2026-03-01", None)

    assert terminar(conexion, uno, ajena, "2026-03-20") is False

    assert listar_floraciones(conexion, otro)[0].fin is None


def test_terminar_una_floracion_inexistente_devuelve_false(conexion: sqlite3.Connection) -> None:
    assert terminar(conexion, un_ejemplar(conexion), 999, "2026-03-20") is False


def test_quitar_borra_solo_esa_floracion(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)
    primera = una_floracion(conexion, ejemplar, "2026-03-01", None)
    segunda = una_floracion(conexion, ejemplar, "2026-04-01", None)

    assert quitar(conexion, ejemplar, primera) is True

    assert [f.id for f in listar_floraciones(conexion, ejemplar)] == [segunda]


def test_quitar_con_el_ejemplar_equivocado_no_borra_nada(conexion: sqlite3.Connection) -> None:
    uno, otro = un_ejemplar(conexion), un_ejemplar(conexion)
    ajena = una_floracion(conexion, otro, "2026-03-01", None)

    assert quitar(conexion, uno, ajena) is False

    assert [f.id for f in listar_floraciones(conexion, otro)] == [ajena]


def test_quitar_una_floracion_inexistente_devuelve_false(conexion: sqlite3.Connection) -> None:
    assert quitar(conexion, un_ejemplar(conexion), 999) is False


def test_quitar_el_ejemplar_borra_sus_floraciones_y_no_las_de_otros(
    conexion: sqlite3.Connection,
) -> None:
    uno, otro = un_ejemplar(conexion), un_ejemplar(conexion)
    agregar(conexion, uno, "2026-03-01", None)
    agregar(conexion, otro, "2026-04-01", None)

    quitar_ejemplar(conexion, uno)

    assert conexion.execute("SELECT ejemplar_id FROM floraciones").fetchall() == [(otro,)]


def test_el_ejemplar_con_el_tope_rechaza_una_floracion_mas(conexion: sqlite3.Connection) -> None:
    ejemplar = un_ejemplar(conexion)
    conexion.executemany(
        "INSERT INTO floraciones (ejemplar_id, inicio) VALUES (?, '2026-01-01')",
        [(ejemplar,)] * CUIDADOS_MAXIMO,
    )

    with pytest.raises(CuidadoInvalido, match="500 floraciones"):
        agregar(conexion, ejemplar, "2026-03-01", None)

    assert conexion.execute("SELECT COUNT(*) FROM floraciones").fetchone() == (CUIDADOS_MAXIMO,)


def test_el_tope_es_por_ejemplar(conexion: sqlite3.Connection) -> None:
    lleno, otro = un_ejemplar(conexion), un_ejemplar(conexion)
    conexion.executemany(
        "INSERT INTO floraciones (ejemplar_id, inicio) VALUES (?, '2026-01-01')",
        [(lleno,)] * CUIDADOS_MAXIMO,
    )

    assert agregar(conexion, otro, "2026-03-01", None) is not None


@pytest.mark.parametrize(
    ("inicio", "fin"),
    [
        ("ayer", None),
        ("2026-3-1", None),
        ("20260301", None),
        ("", None),
        ("2026-03-01", "mañana"),
        ("2026-03-01", ""),
        ("2026-03-20", "2026-03-01"),
    ],
)
def test_la_tabla_rechaza_fechas_con_otra_forma_o_un_fin_anterior(
    conexion: sqlite3.Connection, inicio: str, fin: str | None
) -> None:
    ejemplar = un_ejemplar(conexion)

    with pytest.raises(sqlite3.IntegrityError):
        conexion.execute(
            "INSERT INTO floraciones (ejemplar_id, inicio, fin) VALUES (?, ?, ?)",
            (ejemplar, inicio, fin),
        )


def test_la_migracion_conserva_ejemplares_fotos_y_riegos(tmp_path: Path) -> None:
    anteriores = tmp_path / "hasta-0004"
    anteriores.mkdir()
    for archivo in sorted(MIGRACIONES.glob("000[1234]-*.sql")):
        (anteriores / archivo.name).write_text(archivo.read_text(encoding="utf-8"))
    ruta = tmp_path / "o.sqlite3"
    vieja = abrir_base(ruta, anteriores)
    ejemplar = un_ejemplar(vieja)
    fijar_foto(vieja, ejemplar, "Xq3vT")
    agregar_riego(vieja, ejemplar, "2026-09-15")
    assert vieja.execute("PRAGMA user_version").fetchone() == (4,)
    vieja.close()

    nueva = abrir_base(ruta)

    (conservado,) = listar(nueva)
    assert (conservado.id, conservado.foto) == (ejemplar, "Xq3vT")
    assert nueva.execute("SELECT COUNT(*) FROM riegos").fetchone() == (1,)
    assert nueva.execute("SELECT COUNT(*) FROM floraciones").fetchone() == (0,)
    assert nueva.execute("PRAGMA user_version").fetchone() == (5,)


HILOS = 8


def _en_paralelo(ruta: Path, accion: Callable[[sqlite3.Connection], object]) -> list[bool]:
    """Ejecuta `accion` en varios hilos a la vez, cada uno con su conexión."""
    salida = threading.Barrier(HILOS)

    def uno(_: int) -> bool:
        conexion = conectar(ruta)
        try:
            salida.wait()
            accion(conexion)
            return True
        except CuidadoInvalido:
            return False
        finally:
            conexion.close()

    with ThreadPoolExecutor(max_workers=HILOS) as pool:
        return list(pool.map(uno, range(HILOS)))


def test_altas_simultaneas_no_rebasan_el_tope(tmp_path: Path) -> None:
    ruta = tmp_path / "o.sqlite3"
    base = abrir_base(ruta)
    ejemplar = un_ejemplar(base)
    base.executemany(
        "INSERT INTO floraciones (ejemplar_id, inicio) VALUES (?, '2026-01-01')",
        [(ejemplar,)] * (CUIDADOS_MAXIMO - 1),
    )

    resultados = _en_paralelo(ruta, lambda c: agregar(c, ejemplar, "2026-03-01", None))

    assert resultados.count(True) == 1
    assert base.execute("SELECT COUNT(*) FROM floraciones").fetchone() == (CUIDADOS_MAXIMO,)


def test_terminar_simultaneo_deja_un_solo_exito_y_un_solo_fin(tmp_path: Path) -> None:
    ruta = tmp_path / "o.sqlite3"
    base = abrir_base(ruta)
    ejemplar = un_ejemplar(base)
    id = una_floracion(base, ejemplar, "2026-03-01", None)
    fines = iter(f"2026-03-{dia:02d}" for dia in range(10, 10 + HILOS))
    turno = threading.Lock()

    def terminar_con_mi_fecha(conexion: sqlite3.Connection) -> None:
        with turno:
            fin = next(fines)
        terminar(conexion, ejemplar, id, fin)

    resultados = _en_paralelo(ruta, terminar_con_mi_fecha)

    assert resultados.count(True) == 1
    (floracion,) = listar_floraciones(base, ejemplar)
    assert floracion.fin is not None and floracion.fin.startswith("2026-03-1")
