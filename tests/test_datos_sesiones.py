import hashlib
import sqlite3
from pathlib import Path

import pytest

from orquidea.datos.base import abrir_base, conectar
from orquidea.datos.sesiones import (
    ANTIGUEDAD_MAXIMA,
    INACTIVIDAD_MAXIMA,
    cerrar,
    crear,
    obtener,
)

AHORA = 1_000_000


@pytest.fixture
def conexion(tmp_path: Path) -> sqlite3.Connection:
    return abrir_base(tmp_path / "o.sqlite3")


def filas(conexion: sqlite3.Connection) -> list[tuple[str, str, int, int]]:
    return conexion.execute(
        "SELECT id_hash, csrf, creada, ultima_actividad FROM sesiones"
    ).fetchall()


def test_crear_guarda_solo_el_hash_del_identificador(conexion: sqlite3.Connection) -> None:
    identificador, sesion = crear(conexion, AHORA)

    ((id_hash, csrf, creada, actividad),) = filas(conexion)
    assert id_hash == hashlib.sha256(identificador.encode()).hexdigest()
    assert identificador not in (id_hash, csrf)
    assert csrf == sesion.csrf
    assert (creada, actividad) == (AHORA, AHORA)
    assert len(identificador) >= 43  # 32 bytes en base64 url-safe
    assert len(sesion.csrf) >= 43


def test_dos_sesiones_tienen_identificadores_y_csrf_distintos(
    conexion: sqlite3.Connection,
) -> None:
    uno, sesion_uno = crear(conexion, AHORA)
    otro, sesion_otra = crear(conexion, AHORA)

    assert uno != otro
    assert sesion_uno.csrf != sesion_otra.csrf


def test_obtener_devuelve_la_sesion_y_renueva_la_actividad(conexion: sqlite3.Connection) -> None:
    identificador, creada = crear(conexion, AHORA)

    sesion = obtener(conexion, identificador, AHORA + 60)

    assert sesion == creada
    assert filas(conexion)[0][3] == AHORA + 60
    assert filas(conexion)[0][2] == AHORA


def test_un_identificador_inexistente_no_vale(conexion: sqlite3.Connection) -> None:
    crear(conexion, AHORA)

    assert obtener(conexion, "no-existe", AHORA) is None
    assert obtener(conexion, "", AHORA) is None


def test_no_vale_al_superar_la_inactividad_y_se_borra(conexion: sqlite3.Connection) -> None:
    identificador, _ = crear(conexion, AHORA)

    assert obtener(conexion, identificador, AHORA + INACTIVIDAD_MAXIMA - 1) is not None
    ultimo = AHORA + INACTIVIDAD_MAXIMA - 1
    assert obtener(conexion, identificador, ultimo + INACTIVIDAD_MAXIMA) is None
    assert filas(conexion) == []


def test_la_inactividad_se_mide_desde_la_ultima_actividad(conexion: sqlite3.Connection) -> None:
    identificador, _ = crear(conexion, AHORA)
    obtener(conexion, identificador, AHORA + INACTIVIDAD_MAXIMA - 1)

    assert obtener(conexion, identificador, AHORA + 2 * INACTIVIDAD_MAXIMA - 2) is not None


def test_no_vale_al_superar_la_antiguedad_aunque_haya_actividad(
    conexion: sqlite3.Connection,
) -> None:
    identificador, _ = crear(conexion, AHORA)
    momento = AHORA
    while momento + INACTIVIDAD_MAXIMA - 1 < AHORA + ANTIGUEDAD_MAXIMA:
        momento += INACTIVIDAD_MAXIMA - 1
        assert obtener(conexion, identificador, momento) is not None

    assert obtener(conexion, identificador, AHORA + ANTIGUEDAD_MAXIMA) is None
    assert filas(conexion) == []


def test_cerrar_borra_la_sesion(conexion: sqlite3.Connection) -> None:
    identificador, _ = crear(conexion, AHORA)
    otra, _ = crear(conexion, AHORA)

    cerrar(conexion, identificador)

    assert obtener(conexion, identificador, AHORA) is None
    assert obtener(conexion, otra, AHORA) is not None


def test_conectar_no_migra_y_activa_claves_foraneas_y_wal(tmp_path: Path) -> None:
    ruta = tmp_path / "solo.sqlite3"

    conexion = conectar(ruta)

    assert conexion.execute("PRAGMA user_version").fetchone() == (0,)
    assert conexion.execute("PRAGMA foreign_keys").fetchone() == (1,)
    assert conexion.execute("PRAGMA journal_mode").fetchone() == ("wal",)


def test_crear_purga_las_sesiones_caducadas(conexion: sqlite3.Connection) -> None:
    crear(conexion, AHORA)
    reciente, _ = crear(conexion, AHORA + INACTIVIDAD_MAXIMA)

    assert len(filas(conexion)) == 1
    assert obtener(conexion, reciente, AHORA + INACTIVIDAD_MAXIMA) is not None
