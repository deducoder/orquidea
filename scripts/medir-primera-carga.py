"""Mide cuánto transfiere la primera carga de "Mi colección" con miniaturas (must-perf-001).

Cuenta el HTML y el JavaScript en gzip (así los sirve un proxy) y las miniaturas tal como son
(un JPEG no se comprime más). No cuenta las fotos a tamaño completo. Sale con 1 si pasa del
presupuesto.

    uv run python scripts/medir-primera-carga.py               # 25 fotos de ejemplo con detalle
    uv run python scripts/medir-primera-carga.py --n 40        # otra cantidad
    uv run python scripts/medir-primera-carga.py ~/fotos/*.jpg # con tus fotos reales

Con `--identidad DIR` mide solo los recursos de la identidad (CSS y fuentes, en gzip) contra su
tope de 50 KB (criterio 1 de ADR-009): sale con 1 si pasa del tope y con 2 si no hay nada que medir.

    uv run python scripts/medir-primera-carga.py --identidad src/orquidea/web/static/identidad

Las fotos de ejemplo son ruido fractal: tienen detalle a la escala de la miniatura, pero no son
fotos de orquídeas. Con las tuyas la cifra es la verdadera.
"""

import argparse
import gzip
import io
import re
import sqlite3
import tempfile
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image, ImageChops

from orquidea.coleccion.modelo import CUIDADOS_MAXIMO
from orquidea.datos.almacen_fotos import poner_foto, preparar_directorio
from orquidea.datos.base import abrir_base, conectar
from orquidea.datos.ejemplares import agregar_sin_especie
from orquidea.datos.fotos import procesar_foto
from orquidea.datos.sesiones import crear
from orquidea.web.app import app
from orquidea.web.sesion import nombre_de_cookie

PRESUPUESTO = 200 * 1024
TOPE_DE_IDENTIDAD = 50 * 1024  # criterio 1 de ADR-009
OCTAVAS = (8, 20, 50, 120, 300)


@dataclass(frozen=True)
class Medicion:
    cantidad: int
    html: int
    javascript: int
    miniaturas: int

    @property
    def total(self) -> int:
        return self.html + self.javascript + self.miniaturas


@dataclass(frozen=True)
class MedicionDeFicha:
    riegos: int
    floraciones: int
    filas: int  # filas del historial que la página trae (una por registro)
    html_sin_comprimir: int
    html: int
    javascript: int

    @property
    def total(self) -> int:
        return self.html + self.javascript


@dataclass(frozen=True)
class MedicionDeIdentidad:
    archivos: tuple[tuple[str, int], ...]  # (ruta relativa, octetos en gzip)

    @property
    def total(self) -> int:
        return sum(octetos for _, octetos in self.archivos)


def foto_con_detalle(ancho: int = 1600, alto: int = 1200) -> bytes:
    """Un JPEG con detalle a varias escalas: más parecido a una foto que un color liso."""
    total = Image.new("RGB", (ancho, alto), (128, 128, 128))
    for i, base in enumerate(OCTAVAS):
        capa = Image.effect_noise((base, base * 3 // 4), 60).convert("RGB")
        capa = capa.resize((ancho, alto), Image.Resampling.BICUBIC)
        total = ImageChops.blend(total, capa, 1.0 / (i + 2))
    salida = io.BytesIO()
    total.save(salida, "JPEG", quality=92)
    return salida.getvalue()


@contextmanager
def coleccion_temporal() -> Iterator[tuple[TestClient, sqlite3.Connection, int]]:
    """Base y fotos temporales sobre `app.state`, con una sesión iniciada; restaura al salir.

    Devuelve el cliente con la cookie de sesión, una conexión a la base temporal y la hora usada
    para crear los registros. La conexión se cierra al salir; la aplicación queda como estaba."""
    ruta_base, directorio = app.state.ruta_base, app.state.directorio_fotos
    with tempfile.TemporaryDirectory() as temporal:
        app.state.ruta_base = Path(temporal) / "orquidea.sqlite3"
        app.state.directorio_fotos = Path(temporal) / "fotos"
        try:
            abrir_base(app.state.ruta_base).close()
            preparar_directorio(app.state.directorio_fotos)
            conexion = conectar(app.state.ruta_base)
            try:
                ahora = int(time.time())
                identificador, _ = crear(conexion, ahora)
                cliente = TestClient(app, base_url="https://testserver")
                cliente.cookies.set(nombre_de_cookie(), identificador)
                yield cliente, conexion, ahora
            finally:
                conexion.close()
        finally:
            app.state.ruta_base, app.state.directorio_fotos = ruta_base, directorio


def medir(fotos: list[bytes] | None = None, n: int = 25) -> Medicion:
    """Monta una colección temporal con `n` ejemplares con foto y mide la primera carga."""
    fotos = fotos or [foto_con_detalle() for _ in range(3)]
    with coleccion_temporal() as (cliente, conexion, ahora):
        for i in range(n):
            ejemplar = agregar_sin_especie(conexion, f"Planta {i + 1}", "", ahora)
            procesada = procesar_foto(fotos[i % len(fotos)])
            poner_foto(conexion, app.state.directorio_fotos, ejemplar.id, procesada)
        pagina = cliente.get("/coleccion")
        texto = pagina.text
        estaticos = sorted(set(re.findall(r'(?:src|href)="(/static/[^"]+)"', texto)))
        miniaturas = re.findall(r'src="(/coleccion/\d+/foto/miniatura)"', texto)
        return Medicion(
            cantidad=len(miniaturas),
            html=len(gzip.compress(pagina.content)),
            javascript=sum(len(gzip.compress(cliente.get(u).content)) for u in estaticos),
            miniaturas=sum(len(cliente.get(u).content) for u in miniaturas),
        )


def medir_ficha(riegos: int, floraciones: int) -> MedicionDeFicha:
    """Monta un ejemplar con `riegos` riegos y `floraciones` floraciones en curso (el caso más
    pesado: cada una lleva su formulario de «Terminar») y mide la primera carga de su ficha."""
    with coleccion_temporal() as (cliente, conexion, ahora):
        ejemplar = agregar_sin_especie(conexion, "Ejemplar de prueba", "", ahora).id
        dias = [(date(2025, 1, 1) + timedelta(days=i)).isoformat() for i in range(riegos)]
        conexion.executemany(
            "INSERT INTO riegos (ejemplar_id, fecha) VALUES (?, ?)", [(ejemplar, d) for d in dias]
        )
        dias = [(date(2025, 1, 1) + timedelta(days=i)).isoformat() for i in range(floraciones)]
        conexion.executemany(
            "INSERT INTO floraciones (ejemplar_id, inicio) VALUES (?, ?)",
            [(ejemplar, d) for d in dias],
        )
        pagina = cliente.get(f"/coleccion/{ejemplar}")
        estaticos = sorted(set(re.findall(r'(?:src|href)="(/static/[^"]+)"', pagina.text)))
        return MedicionDeFicha(
            riegos=riegos,
            floraciones=floraciones,
            filas=pagina.text.count("<li>"),
            html_sin_comprimir=len(pagina.content),
            html=len(gzip.compress(pagina.content)),
            javascript=sum(len(gzip.compress(cliente.get(u).content)) for u in estaticos),
        )


def medir_identidad(directorio: Path) -> MedicionDeIdentidad:
    """Cada archivo bajo `directorio`, en gzip; un directorio que no existe no tiene ninguno.

    Los ocultos (`.gitkeep`, o lo que cuelga de un directorio oculto) no son recursos de la
    identidad: contarlos daría un verde con población sin haber medido nada de ella."""
    archivos = sorted(
        r
        for r in directorio.rglob("*")
        if r.is_file() and not any(p.startswith(".") for p in r.relative_to(directorio).parts)
    )
    return MedicionDeIdentidad(
        tuple(
            (r.relative_to(directorio).as_posix(), len(gzip.compress(r.read_bytes())))
            for r in archivos
        )
    )


def _identidad(directorio: Path) -> int:
    m = medir_identidad(directorio)
    if not m.archivos:
        print(f"Recursos de la identidad en {directorio}: 0 archivo(s) — nada que medir")
        return 2
    print(f"Recursos de la identidad en {directorio}: {len(m.archivos)} archivo(s)")
    for nombre, octetos in m.archivos:
        print(f"  {nombre} (gzip)  {_kb(octetos)}")
    dentro = m.total <= TOPE_DE_IDENTIDAD
    print(f"  Total              {_kb(m.total)}   tope {TOPE_DE_IDENTIDAD // 1024} KB", end="  ")
    print("OK" if dentro else "PASA DEL TOPE")
    return 0 if dentro else 1


def _kb(octetos: int) -> str:
    return f"{octetos / 1024:6.1f} KB"


def main(argumentos: list[str] | None = None) -> int:
    analizador = argparse.ArgumentParser(description=__doc__.split("\n")[0] if __doc__ else "")
    analizador.add_argument("fotos", nargs="*", type=Path, help="fotos reales (una por ejemplar)")
    analizador.add_argument("--n", type=int, default=25, help="ejemplares con las fotos de ejemplo")
    analizador.add_argument("--presupuesto", type=int, default=PRESUPUESTO // 1024, help="en KB")
    analizador.add_argument(
        "--identidad", type=Path, help="mide solo los recursos de la identidad de ese directorio"
    )
    parametros = analizador.parse_args(argumentos)
    if parametros.identidad is not None:
        return _identidad(parametros.identidad)

    reales = [ruta.read_bytes() for ruta in parametros.fotos]
    m = medir(reales or None, len(reales) or parametros.n)
    presupuesto = parametros.presupuesto * 1024
    promedio = m.miniaturas // max(m.cantidad, 1)
    dentro = m.total <= presupuesto
    print(f'Primera carga de "Mi colección" con {m.cantidad} ejemplares con foto:')
    print(f"  HTML (gzip)        {_kb(m.html)}")
    print(f"  JavaScript (gzip)  {_kb(m.javascript)}")
    print(f"  Miniaturas ({m.cantidad})   {_kb(m.miniaturas)}   ({_kb(promedio).strip()} c/u)")
    print(
        f"  Total              {_kb(m.total)}   presupuesto {parametros.presupuesto} KB", end="  "
    )
    print("OK" if dentro else "PASA DEL PRESUPUESTO")
    todo_dentro = dentro
    for riegos, floraciones, nota in (
        (50, 50, ""),
        (CUIDADOS_MAXIMO, CUIDADOS_MAXIMO, " (el tope)"),
    ):
        f = medir_ficha(riegos, floraciones)
        print(f"Primera carga de la ficha con {riegos} riegos y {floraciones} floraciones{nota}:")
        crudo = _kb(f.html_sin_comprimir).strip()
        print(f"  HTML (gzip)        {_kb(f.html)}   ({crudo} sin comprimir)")
        print(f"  JavaScript (gzip)  {_kb(f.javascript)}")
        print(
            f"  Total              {_kb(f.total)}   presupuesto {parametros.presupuesto} KB",
            end="  ",
        )
        ficha_dentro = f.total <= presupuesto
        print("OK" if ficha_dentro else "PASA DEL PRESUPUESTO")
        todo_dentro = todo_dentro and ficha_dentro
    return 0 if todo_dentro else 1


if __name__ == "__main__":
    raise SystemExit(main())
