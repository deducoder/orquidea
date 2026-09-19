import sqlite3

from orquidea.coleccion.modelo import CUIDADOS_MAXIMO, CuidadoInvalido, Floracion


def _floracion(fila: tuple[int, int, str, str | None]) -> Floracion:
    return Floracion(id=fila[0], ejemplar_id=fila[1], inicio=fila[2], fin=fila[3])


def agregar(
    conexion: sqlite3.Connection, ejemplar_id: int, inicio: str, fin: str | None
) -> Floracion | None:
    """Guarda una floración; `None` si el ejemplar no existe. Como en `riegos.agregar`, el tope
    se comprueba en la misma sentencia para que las altas simultáneas no lo rebasen."""
    cursor = conexion.execute(
        "INSERT INTO floraciones (ejemplar_id, inicio, fin) SELECT ?, ?, ? "
        "WHERE EXISTS (SELECT 1 FROM ejemplares WHERE id = ?) "
        "AND (SELECT COUNT(*) FROM floraciones WHERE ejemplar_id = ?) < ?",
        (ejemplar_id, inicio, fin, ejemplar_id, ejemplar_id, CUIDADOS_MAXIMO),
    )
    if cursor.rowcount == 1:
        return Floracion(
            id=int(cursor.lastrowid or 0), ejemplar_id=ejemplar_id, inicio=inicio, fin=fin
        )
    existe = conexion.execute("SELECT 1 FROM ejemplares WHERE id = ?", (ejemplar_id,)).fetchone()
    if existe is None:
        return None
    raise CuidadoInvalido(
        f"Este ejemplar ya tiene {CUIDADOS_MAXIMO} floraciones; quita alguna para agregar otra."
    )


def listar(conexion: sqlite3.Connection, ejemplar_id: int) -> list[Floracion]:
    filas = conexion.execute(
        "SELECT id, ejemplar_id, inicio, fin FROM floraciones WHERE ejemplar_id = ? "
        "ORDER BY inicio, id",
        (ejemplar_id,),
    ).fetchall()
    return [_floracion(fila) for fila in filas]


def terminar(conexion: sqlite3.Connection, ejemplar_id: int, id: int, fin: str) -> bool:
    """Fija el fin de una floración propia, en curso y con inicio no posterior a `fin`.

    Una sola sentencia: dos «terminar» simultáneos no se pisan. `False` si la floración no es de
    ese ejemplar o no existe; `CuidadoInvalido` si ya terminó o el fin es anterior al inicio."""
    cursor = conexion.execute(
        "UPDATE floraciones SET fin = ? "
        "WHERE id = ? AND ejemplar_id = ? AND fin IS NULL AND inicio <= ?",
        (fin, id, ejemplar_id, fin),
    )
    if cursor.rowcount == 1:
        return True
    fila = conexion.execute(
        "SELECT inicio, fin FROM floraciones WHERE id = ? AND ejemplar_id = ?", (id, ejemplar_id)
    ).fetchone()
    if fila is None:
        return False
    if fila[1] is not None:
        raise CuidadoInvalido("Esa floración ya terminó.")
    raise CuidadoInvalido("El fin no puede ser anterior al inicio.")


def quitar(conexion: sqlite3.Connection, ejemplar_id: int, id: int) -> bool:
    cursor = conexion.execute(
        "DELETE FROM floraciones WHERE id = ? AND ejemplar_id = ?", (id, ejemplar_id)
    )
    return cursor.rowcount == 1
