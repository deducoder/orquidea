import os
import sqlite3
import time
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from orquidea.autenticacion import LimiteDeIntentos, verificar_contrasena
from orquidea.catalogo.busqueda import buscar
from orquidea.datos.base import abrir_base, conectar, ruta_de_la_base
from orquidea.datos.catalogo import DIRECTORIO_CATALOGO, cargar_catalogo
from orquidea.datos.sesiones import ANTIGUEDAD_MAXIMA, cerrar, crear

BASE_DIR = Path(__file__).parent
COOKIE_SESION = "sesion"


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI) -> AsyncIterator[None]:
    abrir_base(app.state.ruta_base).close()
    yield


app = FastAPI(lifespan=ciclo_de_vida)
app.state.catalogo = cargar_catalogo(DIRECTORIO_CATALOGO)
app.state.ruta_base = ruta_de_la_base()
app.state.limite = LimiteDeIntentos()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def base_de_datos(request: Request) -> Iterator[sqlite3.Connection]:
    conexion = conectar(request.app.state.ruta_base)
    try:
        yield conexion
    finally:
        conexion.close()


Base = Annotated[sqlite3.Connection, Depends(base_de_datos)]


def _cookie_segura() -> bool:
    return os.environ.get("ORQUIDEA_COOKIE_SEGURA") != "0"


def _formulario_de_acceso(request: Request, estado: int, mensaje: str = "") -> HTMLResponse:
    return templates.TemplateResponse(
        request, "acceso.html", {"mensaje": mensaje}, status_code=estado
    )


@app.get("/acceso", response_class=HTMLResponse)
def formulario_de_acceso(request: Request) -> HTMLResponse:
    return _formulario_de_acceso(request, 200)


@app.post("/acceso", response_model=None)
def iniciar_sesion(
    request: Request, contrasena: Annotated[str, Form()], conexion: Base
) -> Response:
    limite: LimiteDeIntentos = request.app.state.limite
    ahora = time.time()
    if limite.bloqueado(ahora):
        return _formulario_de_acceso(request, 429, "Demasiados intentos; espera unos minutos.")
    if not verificar_contrasena(contrasena, os.environ.get("ORQUIDEA_PASSWORD_HASH")):
        limite.fallo(ahora)
        return _formulario_de_acceso(request, 401, "Contraseña incorrecta.")
    limite.acierto()
    identificador, _ = crear(conexion, int(ahora))
    respuesta = RedirectResponse("/", status_code=303)
    respuesta.set_cookie(
        COOKIE_SESION,
        identificador,
        max_age=ANTIGUEDAD_MAXIMA,
        httponly=True,
        samesite="lax",
        secure=_cookie_segura(),
    )
    return respuesta


@app.post("/salir")
def cerrar_sesion(request: Request, conexion: Base) -> RedirectResponse:
    identificador = request.cookies.get(COOKIE_SESION)
    if identificador:
        cerrar(conexion, identificador)
    respuesta = RedirectResponse("/acceso", status_code=303)
    respuesta.delete_cookie(COOKIE_SESION, httponly=True, samesite="lax", secure=_cookie_segura())
    return respuesta


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "inicio.html")


@app.get("/especies", response_class=HTMLResponse)
def lista_de_especies(request: Request, q: str = "") -> HTMLResponse:
    especies = buscar(request.app.state.catalogo, q)
    return templates.TemplateResponse(request, "especies.html", {"especies": especies, "q": q})


@app.get("/especies/{id}", response_class=HTMLResponse)
def ficha_de_especie(request: Request, id: str) -> HTMLResponse:
    especie = next((e for e in request.app.state.catalogo if e.id == id), None)
    if especie is None:
        raise HTTPException(status_code=404, detail="Especie no encontrada")
    return templates.TemplateResponse(request, "especie.html", {"especie": especie})


@app.get("/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok"}
