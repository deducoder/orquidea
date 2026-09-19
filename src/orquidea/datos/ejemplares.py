import sqlite3

from orquidea.coleccion.modelo import Ejemplar


def agregar(conexion: sqlite3.Connection, especie_id: str, ahora: int) -> Ejemplar:
    cursor = conexion.execute(
        "INSERT INTO ejemplares (especie_id, creado) VALUES (?, ?)", (especie_id, ahora)
    )
    return Ejemplar(
        id=int(cursor.lastrowid or 0), especie_id=especie_id, nombre="", notas="", creado=ahora
    )


def agregar_sin_especie(
    conexion: sqlite3.Connection, nombre: str, notas: str, ahora: int
) -> Ejemplar:
    cursor = conexion.execute(
        "INSERT INTO ejemplares (nombre, notas, creado) VALUES (?, ?, ?)", (nombre, notas, ahora)
    )
    return Ejemplar(
        id=int(cursor.lastrowid or 0), especie_id=None, nombre=nombre, notas=notas, creado=ahora
    )


def listar(conexion: sqlite3.Connection) -> list[Ejemplar]:
    filas = conexion.execute(
        "SELECT id, especie_id, nombre, notas, creado FROM ejemplares ORDER BY id"
    ).fetchall()
    return [Ejemplar(id=f[0], especie_id=f[1], nombre=f[2], notas=f[3], creado=f[4]) for f in filas]
