import logging
import os
import re
import secrets
import sqlite3
import tempfile
import threading
from pathlib import Path

from orquidea.datos.ejemplares import fijar_foto, obtener, quitar
from orquidea.datos.fotos import FotoProcesada

registro = logging.getLogger("orquidea.fotos")

# Un solo proceso (ADR-001): el cerrojo serializa leer la foto vigente, cambiarla y borrar la
# anterior, para que dos subidas del mismo ejemplar no dejen archivos huérfanos.
_cerrojo = threading.Lock()
_NOMBRE = re.compile(r"[A-Za-z0-9_-]{1,64}")


class NombreDeFotoInvalido(ValueError):
    pass


class DirectorioDeFotosNoEscribible(Exception):
    pass


def directorio_de_fotos(ruta_base: Path) -> Path:
    """`ORQUIDEA_FOTOS`, o `fotos/` junto a la base: en la imagen, dentro del volumen `/data`."""
    return Path(os.environ.get("ORQUIDEA_FOTOS") or ruta_base.parent / "fotos")


def preparar_directorio(directorio: Path) -> None:
    try:
        directorio.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryFile(dir=directorio):
            pass
    except OSError as fallo:
        raise DirectorioDeFotosNoEscribible(
            f"No se puede escribir en el directorio de fotos {directorio}: {fallo}"
        ) from fallo


def ruta_de_foto(directorio: Path, nombre: str, *, miniatura: bool) -> Path:
    # Es el único lugar donde se forma la ruta de un archivo, y solo desde el nombre guardado.
    if _NOMBRE.fullmatch(nombre) is None:
        raise NombreDeFotoInvalido("Nombre de foto inválido.")
    return directorio / (f"{nombre}-mini.jpg" if miniatura else f"{nombre}.jpg")


def _escribir(destino: Path, datos: bytes) -> None:
    temporal = destino.with_name(destino.name + ".tmp")
    try:
        temporal.write_bytes(datos)
        os.replace(temporal, destino)
    except BaseException:
        temporal.unlink(missing_ok=True)
        raise


def _guardar(directorio: Path, foto: FotoProcesada) -> str:
    nombre = secrets.token_urlsafe(16)
    escritos: list[Path] = []
    try:
        for datos, miniatura in ((foto.imagen, False), (foto.miniatura, True)):
            destino = ruta_de_foto(directorio, nombre, miniatura=miniatura)
            _escribir(destino, datos)
            escritos.append(destino)
    except BaseException:
        for archivo in escritos:
            archivo.unlink(missing_ok=True)
        raise
    return nombre


def _borrar(directorio: Path, nombre: str) -> None:
    # Un archivo que no se borra es basura, no una fuga: se registra y la operación sigue.
    for miniatura in (False, True):
        try:
            ruta_de_foto(directorio, nombre, miniatura=miniatura).unlink(missing_ok=True)
        except (OSError, NombreDeFotoInvalido) as fallo:
            registro.warning("no se pudo borrar una foto: %s", fallo)


def poner_foto(
    conexion: sqlite3.Connection, directorio: Path, id: int, foto: FotoProcesada
) -> bool:
    """Guarda la foto del ejemplar y borra la anterior: escribe, actualiza, borra."""
    with _cerrojo:
        actual = obtener(conexion, id)
        nombre = _guardar(directorio, foto)
        try:
            cambiada = fijar_foto(conexion, id, nombre)
        except BaseException:
            _borrar(directorio, nombre)
            raise
        if not cambiada:  # el ejemplar no existe: no queda nada de lo escrito
            _borrar(directorio, nombre)
            return False
        if actual is not None and actual.foto:
            _borrar(directorio, actual.foto)
        return True


def quitar_foto(conexion: sqlite3.Connection, directorio: Path, id: int) -> bool:
    with _cerrojo:
        ejemplar = obtener(conexion, id)
        if ejemplar is None:
            return False
        fijar_foto(conexion, id, None)
        if ejemplar.foto:
            _borrar(directorio, ejemplar.foto)
        return True


def quitar_con_foto(conexion: sqlite3.Connection, directorio: Path, id: int) -> bool:
    with _cerrojo:
        ejemplar = obtener(conexion, id)
        if ejemplar is None:
            return False
        quitar(conexion, id)
        if ejemplar.foto:
            _borrar(directorio, ejemplar.foto)
        return True
