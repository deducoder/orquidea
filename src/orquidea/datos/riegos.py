import sqlite3

from orquidea.coleccion.modelo import CUIDADOS_MAXIMO, CuidadoInvalido, Riego


def _riego(fila: tuple[int, int, str]) -> Riego:
    return Riego(id=fila[0], ejemplar_id=fila[1], fecha=fila[2])


def agregar(conexion: sqlite3.Connection, ejemplar_id: int, fecha: str) -> Riego | None:
    """Guarda un riego; `None` si el ejemplar no existe. El tope se comprueba en la misma
    sentencia: cada petición tiene su conexión, y contar aparte dejaría pasar altas simultáneas."""
    cursor = conexion.execute(
        "INSERT INTO riegos (ejemplar_id, fecha) SELECT ?, ? "
        "WHERE EXISTS (SELECT 1 FROM ejemplares WHERE id = ?) "
        "AND (SELECT COUNT(*) FROM riegos WHERE ejemplar_id = ?) < ?",
        (ejemplar_id, fecha, ejemplar_id, ejemplar_id, CUIDADOS_MAXIMO),
    )
    if cursor.rowcount == 1:
        return Riego(id=int(cursor.lastrowid or 0), ejemplar_id=ejemplar_id, fecha=fecha)
    existe = conexion.execute("SELECT 1 FROM ejemplares WHERE id = ?", (ejemplar_id,)).fetchone()
    if existe is None:
        return None
    raise CuidadoInvalido(
        f"Este ejemplar ya tiene {CUIDADOS_MAXIMO} riegos; quita alguno para agregar otro."
    )


def listar(conexion: sqlite3.Connection, ejemplar_id: int) -> list[Riego]:
    filas = conexion.execute(
        "SELECT id, ejemplar_id, fecha FROM riegos WHERE ejemplar_id = ? ORDER BY fecha, id",
        (ejemplar_id,),
    ).fetchall()
    return [_riego(fila) for fila in filas]


def quitar(conexion: sqlite3.Connection, ejemplar_id: int, id: int) -> bool:
    cursor = conexion.execute(
        "DELETE FROM riegos WHERE id = ? AND ejemplar_id = ?", (id, ejemplar_id)
    )
    return cursor.rowcount == 1


def ultimos(conexion: sqlite3.Connection) -> dict[int, str]:
    """La fecha del último riego de cada ejemplar que tiene alguno, en una sola consulta."""
    filas = conexion.execute(
        "SELECT ejemplar_id, MAX(fecha) FROM riegos GROUP BY ejemplar_id"
    ).fetchall()
    return {ejemplar_id: fecha for ejemplar_id, fecha in filas}
