import hashlib
import secrets
import sqlite3
from dataclasses import dataclass

INACTIVIDAD_MAXIMA = 30 * 60
ANTIGUEDAD_MAXIMA = 12 * 60 * 60


@dataclass(frozen=True)
class Sesion:
    csrf: str


def _hash(identificador: str) -> str:
    return hashlib.sha256(identificador.encode("utf-8")).hexdigest()


def _caducada(ahora: int, creada: int, ultima_actividad: int) -> bool:
    return ahora - ultima_actividad >= INACTIVIDAD_MAXIMA or ahora - creada >= ANTIGUEDAD_MAXIMA


def crear(conexion: sqlite3.Connection, ahora: int) -> tuple[str, Sesion]:
    conexion.execute(
        "DELETE FROM sesiones WHERE ? - ultima_actividad >= ? OR ? - creada >= ?",
        (ahora, INACTIVIDAD_MAXIMA, ahora, ANTIGUEDAD_MAXIMA),
    )
    identificador = secrets.token_urlsafe(32)
    sesion = Sesion(csrf=secrets.token_urlsafe(32))
    conexion.execute(
        "INSERT INTO sesiones (id_hash, csrf, creada, ultima_actividad) VALUES (?, ?, ?, ?)",
        (_hash(identificador), sesion.csrf, ahora, ahora),
    )
    return identificador, sesion


def obtener(conexion: sqlite3.Connection, identificador: str, ahora: int) -> Sesion | None:
    id_hash = _hash(identificador)
    fila = conexion.execute(
        "SELECT csrf, creada, ultima_actividad FROM sesiones WHERE id_hash = ?", (id_hash,)
    ).fetchone()
    if fila is None:
        return None
    csrf, creada, ultima_actividad = fila
    if _caducada(ahora, creada, ultima_actividad):
        conexion.execute("DELETE FROM sesiones WHERE id_hash = ?", (id_hash,))
        return None
    conexion.execute("UPDATE sesiones SET ultima_actividad = ? WHERE id_hash = ?", (ahora, id_hash))
    return Sesion(csrf=csrf)


def cerrar(conexion: sqlite3.Connection, identificador: str) -> None:
    conexion.execute("DELETE FROM sesiones WHERE id_hash = ?", (_hash(identificador),))
