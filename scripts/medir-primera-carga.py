"""Mide cuánto transfiere la primera carga de "Mi colección" con miniaturas (must-perf-001).

Cuenta el HTML y el JavaScript en gzip (así los sirve un proxy) y las miniaturas tal como son
(un JPEG no se comprime más). No cuenta las fotos a tamaño completo. Sale con 1 si pasa del
presupuesto.

    uv run python scripts/medir-primera-carga.py               # 25 fotos de ejemplo con detalle
    uv run python scripts/medir-primera-carga.py --n 40        # otra cantidad
    uv run python scripts/medir-primera-carga.py ~/fotos/*.jpg # con tus fotos reales

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
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image, ImageChops

from orquidea.datos.almacen_fotos import poner_foto, preparar_directorio
from orquidea.datos.base import abrir_base, conectar
from orquidea.datos.ejemplares import agregar_sin_especie
from orquidea.datos.fotos import procesar_foto
from orquidea.datos.sesiones import crear
from orquidea.web.app import app
from orquidea.web.sesion import nombre_de_cookie

PRESUPUESTO = 200 * 1024
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


def _kb(octetos: int) -> str:
    return f"{octetos / 1024:6.1f} KB"


def main(argumentos: list[str] | None = None) -> int:
    analizador = argparse.ArgumentParser(description=__doc__.split("\n")[0] if __doc__ else "")
    analizador.add_argument("fotos", nargs="*", type=Path, help="fotos reales (una por ejemplar)")
    analizador.add_argument("--n", type=int, default=25, help="ejemplares con las fotos de ejemplo")
    analizador.add_argument("--presupuesto", type=int, default=PRESUPUESTO // 1024, help="en KB")
    parametros = analizador.parse_args(argumentos)

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
    return 0 if dentro else 1


if __name__ == "__main__":
    raise SystemExit(main())
