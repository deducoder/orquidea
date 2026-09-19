import sqlite3
from pathlib import Path

import pytest

from orquidea.datos.base import MigracionFallida, abrir_base


def migraciones(carpeta: Path, **archivos: str) -> Path:
    carpeta.mkdir(exist_ok=True)
    for nombre, sql in archivos.items():
        (carpeta / f"{nombre.replace('_', '-', 1)}.sql").write_text(sql, encoding="utf-8")
    return carpeta


def version(conexion: sqlite3.Connection) -> int:
    fila = conexion.execute("PRAGMA user_version").fetchone()
    return int(fila[0])


def tablas(conexion: sqlite3.Connection) -> set[str]:
    filas = conexion.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    return {fila[0] for fila in filas}


def test_aplica_las_migraciones_en_orden(tmp_path: Path) -> None:
    carpeta = migraciones(
        tmp_path / "m",
        # La segunda depende de la primera: solo funciona si van en orden.
        **{
            "0002_b": "INSERT INTO a (x) VALUES ('uno'); CREATE TABLE b (y TEXT);",
            "0001_a": "CREATE TABLE a (x TEXT);",
        },
    )

    conexion = abrir_base(tmp_path / "o.sqlite3", carpeta)

    assert version(conexion) == 2
    assert {"a", "b"} <= tablas(conexion)
    assert conexion.execute("SELECT x FROM a").fetchall() == [("uno",)]


def test_reabrir_no_reaplica_y_conserva_los_datos(tmp_path: Path) -> None:
    carpeta = migraciones(tmp_path / "m", **{"0001_a": "CREATE TABLE a (x TEXT);"})
    ruta = tmp_path / "o.sqlite3"
    primera = abrir_base(ruta, carpeta)
    primera.execute("INSERT INTO a (x) VALUES ('dato')")
    primera.commit()
    primera.close()

    segunda = abrir_base(ruta, carpeta)

    assert version(segunda) == 1
    assert segunda.execute("SELECT x FROM a").fetchall() == [("dato",)]


def test_una_base_en_la_version_1_aplica_solo_la_2(tmp_path: Path) -> None:
    carpeta = migraciones(tmp_path / "m", **{"0001_a": "CREATE TABLE a (x TEXT);"})
    ruta = tmp_path / "o.sqlite3"
    abrir_base(ruta, carpeta).close()
    migraciones(carpeta, **{"0002_b": "CREATE TABLE b (y TEXT);"})

    conexion = abrir_base(ruta, carpeta)

    assert version(conexion) == 2
    assert {"a", "b"} <= tablas(conexion)


def test_una_migracion_que_falla_no_deja_cambios_parciales(tmp_path: Path) -> None:
    carpeta = migraciones(
        tmp_path / "m",
        **{
            "0001_a": "CREATE TABLE a (x TEXT);",
            "0002_rota": "CREATE TABLE b (y TEXT); INSERT INTO no_existe VALUES (1);",
        },
    )
    ruta = tmp_path / "o.sqlite3"

    with pytest.raises(MigracionFallida, match="0002-rota.sql"):
        abrir_base(ruta, carpeta)

    fuera = sqlite3.connect(ruta)
    assert version(fuera) == 1
    assert "b" not in tablas(fuera)
    assert "a" in tablas(fuera)


def test_un_hueco_de_numeracion_falla_sin_aplicar_ninguna(tmp_path: Path) -> None:
    carpeta = migraciones(
        tmp_path / "m",
        **{"0001_a": "CREATE TABLE a (x TEXT);", "0003_c": "CREATE TABLE c (z TEXT);"},
    )
    ruta = tmp_path / "o.sqlite3"

    with pytest.raises(MigracionFallida, match="0003"):
        abrir_base(ruta, carpeta)

    fuera = sqlite3.connect(ruta)
    assert version(fuera) == 0
    assert tablas(fuera) == set()


def test_un_nombre_de_migracion_invalido_falla(tmp_path: Path) -> None:
    carpeta = tmp_path / "m"
    carpeta.mkdir()
    (carpeta / "cero-uno.sql").write_text("CREATE TABLE a (x TEXT);", encoding="utf-8")

    with pytest.raises(MigracionFallida, match="cero-uno.sql"):
        abrir_base(tmp_path / "o.sqlite3", carpeta)
