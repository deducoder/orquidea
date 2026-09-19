import os
import re
import sqlite3
from pathlib import Path

RUTA_POR_DEFECTO = Path("data/orquidea.sqlite3")
MIGRACIONES = Path(__file__).parent / "migraciones"

_NOMBRE = re.compile(r"^(\d{4})-.+\.sql$")


class MigracionFallida(Exception):
    pass


def ruta_de_la_base() -> Path:
    return Path(os.environ.get("ORQUIDEA_DB") or RUTA_POR_DEFECTO)


def _pendientes(carpeta: Path, aplicada: int) -> list[tuple[int, Path]]:
    encontradas: list[tuple[int, Path]] = []
    for archivo in carpeta.glob("*.sql"):
        coincide = _NOMBRE.match(archivo.name)
        if coincide is None:
            raise MigracionFallida(f"{archivo.name}: el nombre debe ser NNNN-nombre.sql")
        encontradas.append((int(coincide.group(1)), archivo))
    encontradas.sort()
    for esperado, (numero, archivo) in enumerate(encontradas, start=1):
        if numero != esperado:
            raise MigracionFallida(
                f"{archivo.name}: la numeración debe ser continua (se esperaba {esperado:04d})"
            )
    return [(numero, archivo) for numero, archivo in encontradas if numero > aplicada]


def _aplicar(conexion: sqlite3.Connection, numero: int, archivo: Path) -> None:
    sql = archivo.read_text(encoding="utf-8")
    try:
        conexion.executescript(f"BEGIN;\n{sql}\nPRAGMA user_version = {int(numero)};\nCOMMIT;")
    except sqlite3.Error as fallo:
        # La transacción queda abierta: `abrir_base` cierra la conexión y SQLite la descarta.
        raise MigracionFallida(f"{archivo.name}: {fallo}") from fallo


def conectar(ruta: Path) -> sqlite3.Connection:
    conexion = sqlite3.connect(ruta, isolation_level=None)
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.execute("PRAGMA journal_mode = WAL")
    return conexion


def abrir_base(ruta: Path, migraciones: Path = MIGRACIONES) -> sqlite3.Connection:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    conexion = conectar(ruta)
    try:
        aplicada = int(conexion.execute("PRAGMA user_version").fetchone()[0])
        for numero, archivo in _pendientes(migraciones, aplicada):
            _aplicar(conexion, numero, archivo)
    except BaseException:
        conexion.close()
        raise
    return conexion
