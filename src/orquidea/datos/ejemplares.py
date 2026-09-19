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


def obtener(conexion: sqlite3.Connection, id: int) -> Ejemplar | None:
    fila = conexion.execute(
        "SELECT id, especie_id, nombre, notas, creado FROM ejemplares WHERE id = ?", (id,)
    ).fetchone()
    if fila is None:
        return None
    return Ejemplar(id=fila[0], especie_id=fila[1], nombre=fila[2], notas=fila[3], creado=fila[4])


def actualizar(conexion: sqlite3.Connection, id: int, nombre: str, notas: str) -> bool:
    cursor = conexion.execute(
        "UPDATE ejemplares SET nombre = ?, notas = ? WHERE id = ?", (nombre, notas, id)
    )
    return cursor.rowcount == 1


def quitar(conexion: sqlite3.Connection, id: int) -> bool:
    cursor = conexion.execute("DELETE FROM ejemplares WHERE id = ?", (id,))
    return cursor.rowcount == 1


def listar(conexion: sqlite3.Connection) -> list[Ejemplar]:
    filas = conexion.execute(
        "SELECT id, especie_id, nombre, notas, creado FROM ejemplares ORDER BY id"
    ).fetchall()
    return [Ejemplar(id=f[0], especie_id=f[1], nombre=f[2], notas=f[3], creado=f[4]) for f in filas]
