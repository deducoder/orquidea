import io
import os
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from PIL import Image

from orquidea.datos import almacen_fotos
from orquidea.datos.almacen_fotos import (
    NombreDeFotoInvalido,
    poner_foto,
    quitar_con_foto,
    quitar_foto,
    ruta_de_foto,
)
from orquidea.datos.base import abrir_base, conectar
from orquidea.datos.ejemplares import agregar, listar, obtener
from orquidea.datos.ejemplares import fijar_foto as fijar_foto_original
from orquidea.datos.fotos import FotoProcesada, procesar_foto

AHORA = 1_780_000_000


def _foto(color: int = 120) -> FotoProcesada:
    entrada = io.BytesIO()
    Image.new("RGB", (100, 80), (color, 60, 90)).save(entrada, "JPEG")
    return procesar_foto(entrada.getvalue())


@pytest.fixture
def conexion(tmp_path: Path) -> sqlite3.Connection:
    return abrir_base(tmp_path / "o.sqlite3")


@pytest.fixture
def directorio(tmp_path: Path) -> Path:
    carpeta = tmp_path / "fotos"
    carpeta.mkdir()
    return carpeta


def _archivos(directorio: Path) -> set[str]:
    return {archivo.name for archivo in directorio.iterdir()}


def _nombre(conexion: sqlite3.Connection, id: int) -> str:
    ejemplar = obtener(conexion, id)
    assert ejemplar is not None and ejemplar.foto is not None
    return ejemplar.foto


def _esperados(nombre: str) -> set[str]:
    return {f"{nombre}.jpg", f"{nombre}-mini.jpg"}


def test_poner_foto_guarda_dos_archivos_y_liga_el_nombre(
    conexion: sqlite3.Connection, directorio: Path
) -> None:
    ejemplar = agregar(conexion, "epidendrum-radicans", AHORA)
    foto = _foto()

    assert poner_foto(conexion, directorio, ejemplar.id, foto) is True

    nombre = _nombre(conexion, ejemplar.id)
    assert _archivos(directorio) == _esperados(nombre)
    assert ruta_de_foto(directorio, nombre, miniatura=False).read_bytes() == foto.imagen
    assert ruta_de_foto(directorio, nombre, miniatura=True).read_bytes() == foto.miniatura


def test_los_nombres_de_las_fotos_no_dependen_del_ejemplar(
    conexion: sqlite3.Connection, directorio: Path
) -> None:
    uno = agregar(conexion, "epidendrum-radicans", AHORA)
    otro = agregar(conexion, "epidendrum-radicans", AHORA)
    poner_foto(conexion, directorio, uno.id, _foto())
    poner_foto(conexion, directorio, otro.id, _foto())

    nombres = [e.foto for e in listar(conexion)]

    assert None not in nombres and nombres[0] != nombres[1]
    assert all(len(nombre or "") >= 16 for nombre in nombres)  # aleatorio, no el id


def test_reemplazar_la_foto_borra_los_archivos_anteriores(
    conexion: sqlite3.Connection, directorio: Path
) -> None:
    ejemplar = agregar(conexion, "epidendrum-radicans", AHORA)
    poner_foto(conexion, directorio, ejemplar.id, _foto(10))
    anterior = _nombre(conexion, ejemplar.id)

    poner_foto(conexion, directorio, ejemplar.id, _foto(200))

    nueva = _nombre(conexion, ejemplar.id)
    assert nueva != anterior
    assert _archivos(directorio) == _esperados(nueva)


def test_quitar_solo_la_foto_deja_el_ejemplar_sin_foto(
    conexion: sqlite3.Connection, directorio: Path
) -> None:
    ejemplar = agregar(conexion, "epidendrum-radicans", AHORA)
    poner_foto(conexion, directorio, ejemplar.id, _foto())

    assert quitar_foto(conexion, directorio, ejemplar.id) is True

    assert obtener(conexion, ejemplar.id) == ejemplar
    assert _archivos(directorio) == set()


def test_quitar_la_foto_de_un_ejemplar_sin_foto_no_es_un_error(
    conexion: sqlite3.Connection, directorio: Path
) -> None:
    ejemplar = agregar(conexion, "epidendrum-radicans", AHORA)

    assert quitar_foto(conexion, directorio, ejemplar.id) is True
    assert quitar_foto(conexion, directorio, 999) is False


def test_quitar_el_ejemplar_borra_la_fila_y_los_archivos(
    conexion: sqlite3.Connection, directorio: Path
) -> None:
    con_foto = agregar(conexion, "epidendrum-radicans", AHORA)
    sin_foto = agregar(conexion, "laelia-anceps", AHORA)
    poner_foto(conexion, directorio, con_foto.id, _foto())
    poner_foto(conexion, directorio, sin_foto.id, _foto())
    quedan = _nombre(conexion, sin_foto.id)

    assert quitar_con_foto(conexion, directorio, con_foto.id) is True

    assert [e.id for e in listar(conexion)] == [sin_foto.id]
    assert _archivos(directorio) == _esperados(quedan)
    assert quitar_con_foto(conexion, directorio, con_foto.id) is False


def test_un_ejemplar_inexistente_no_deja_archivos(
    conexion: sqlite3.Connection, directorio: Path
) -> None:
    assert poner_foto(conexion, directorio, 999, _foto()) is False

    assert _archivos(directorio) == set()


@pytest.mark.parametrize("nombre", ["", "..", "../x", "a/b", "a\\b", "x\n", "a" * 65, "ñ", "a.jpg"])
def test_un_nombre_invalido_no_forma_ruta(directorio: Path, nombre: str) -> None:
    with pytest.raises(NombreDeFotoInvalido):
        ruta_de_foto(directorio, nombre, miniatura=False)


def test_si_falla_la_segunda_escritura_no_queda_nada(
    conexion: sqlite3.Connection, directorio: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ejemplar = agregar(conexion, "epidendrum-radicans", AHORA)
    reemplazos = 0
    original = os.replace

    def falla_la_segunda(origen: str | Path, destino: str | Path) -> None:
        nonlocal reemplazos
        reemplazos += 1
        if reemplazos == 2:
            raise OSError("disco lleno")
        original(origen, destino)

    monkeypatch.setattr(os, "replace", falla_la_segunda)

    with pytest.raises(OSError, match="disco lleno"):
        poner_foto(conexion, directorio, ejemplar.id, _foto())

    assert _archivos(directorio) == set()
    assert obtener(conexion, ejemplar.id) == ejemplar


def test_un_archivo_que_no_se_puede_borrar_no_impide_quitar_el_ejemplar(
    conexion: sqlite3.Connection, directorio: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ejemplar = agregar(conexion, "epidendrum-radicans", AHORA)
    poner_foto(conexion, directorio, ejemplar.id, _foto())

    def no_se_puede(self: Path, missing_ok: bool = False) -> None:
        raise PermissionError("sin permiso")

    monkeypatch.setattr(Path, "unlink", no_se_puede)

    assert quitar_con_foto(conexion, directorio, ejemplar.id) is True
    assert listar(conexion) == []


def test_dos_subidas_simultaneas_dejan_una_sola_foto(
    tmp_path: Path, directorio: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ruta = tmp_path / "o.sqlite3"
    ejemplar = agregar(abrir_base(ruta), "epidendrum-radicans", AHORA)
    fijar = fijar_foto_original

    def lenta(conexion: sqlite3.Connection, id: int, foto: str | None) -> bool:
        time.sleep(0.02)  # ensancha la ventana entre leer la foto vigente y cambiarla
        return fijar(conexion, id, foto)

    monkeypatch.setattr(almacen_fotos, "fijar_foto", lenta)

    def subir(color: int) -> bool:
        conexion = conectar(ruta)
        try:
            return poner_foto(conexion, directorio, ejemplar.id, _foto(color))
        finally:
            conexion.close()

    with ThreadPoolExecutor(max_workers=8) as pool:
        resultados = list(pool.map(subir, range(0, 240, 30)))

    vigente = _nombre(conectar(ruta), ejemplar.id)
    assert all(resultados)
    assert _archivos(directorio) == _esperados(vigente)
