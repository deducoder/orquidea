import hmac
import logging
import os
import sqlite3
import time
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Form, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from orquidea.autenticacion import LimiteDeIntentos, verificar_contrasena
from orquidea.catalogo.busqueda import buscar
from orquidea.coleccion.modelo import Ejemplar, EjemplarInvalido, resolver, validar_ejemplar
from orquidea.datos.base import abrir_base, conectar, ruta_de_la_base
from orquidea.datos.catalogo import DIRECTORIO_CATALOGO, cargar_catalogo
from orquidea.datos.ejemplares import (
    actualizar,
    agregar,
    agregar_sin_especie,
    listar,
    obtener,
)
from orquidea.datos.sesiones import ANTIGUEDAD_MAXIMA, cerrar, crear
from orquidea.datos.sesiones import obtener as obtener_sesion

BASE_DIR = Path(__file__).parent
registro = logging.getLogger("orquidea.acceso")


class SesionRequerida(Exception):
    pass


RUTAS_PUBLICAS = frozenset({"/acceso", "/salud"})
METODOS_SEGUROS = frozenset({"GET", "HEAD", "OPTIONS"})


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI) -> AsyncIterator[None]:
    abrir_base(app.state.ruta_base).close()
    yield


def base_de_datos(request: Request) -> Iterator[sqlite3.Connection]:
    conexion = conectar(request.app.state.ruta_base)
    try:
        yield conexion
    finally:
        conexion.close()


Base = Annotated[sqlite3.Connection, Depends(base_de_datos)]


def _cookie_segura() -> bool:
    return os.environ.get("ORQUIDEA_COOKIE_SEGURA") != "0"


def _nombre_de_cookie() -> str:
    # El prefijo __Host- exige Secure: solo se usa cuando la cookie lo lleva.
    return "__Host-sesion" if _cookie_segura() else "sesion"


def exigir_sesion(
    request: Request,
    conexion: Base,
    csrf: Annotated[str | None, Form()] = None,
    x_csrf_token: Annotated[str | None, Header()] = None,
) -> None:
    """Dependencia global: toda ruta la exige salvo las declaradas en `RUTAS_PUBLICAS`.

    Los métodos que cambian datos exigen además el token CSRF de la sesión.
    """
    ruta = request.scope.get("route")
    if ruta is not None and ruta.path in RUTAS_PUBLICAS:
        return
    identificador = request.cookies.get(_nombre_de_cookie())
    sesion = obtener_sesion(conexion, identificador, int(time.time())) if identificador else None
    if sesion is None:
        raise SesionRequerida
    if request.method not in METODOS_SEGUROS:
        enviado = csrf or x_csrf_token or ""
        if not hmac.compare_digest(enviado.encode(), sesion.csrf.encode()):
            raise HTTPException(status_code=403, detail="Token CSRF inválido")
    request.state.sesion = sesion


app = FastAPI(
    lifespan=ciclo_de_vida,
    dependencies=[Depends(exigir_sesion)],
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.state.catalogo = cargar_catalogo(DIRECTORIO_CATALOGO)
app.state.ruta_base = ruta_de_la_base()
app.state.limite = LimiteDeIntentos()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.filters["fecha"] = lambda segundos: (
    datetime.fromtimestamp(segundos, UTC).date().isoformat()
)


CONTENT_SECURITY_POLICY = (
    "default-src 'self'; style-src 'self' 'unsafe-inline'; "
    "frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
)


@app.middleware("http")
async def cabeceras_de_seguridad(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    respuesta = await call_next(request)
    respuesta.headers["X-Content-Type-Options"] = "nosniff"
    respuesta.headers["Referrer-Policy"] = "same-origin"
    respuesta.headers["X-Frame-Options"] = "DENY"
    respuesta.headers["Content-Security-Policy"] = CONTENT_SECURITY_POLICY
    if not request.url.path.startswith("/static"):
        respuesta.headers["Cache-Control"] = "no-store"
    if _cookie_segura():
        respuesta.headers["Strict-Transport-Security"] = "max-age=31536000"
    return respuesta


@app.exception_handler(SesionRequerida)
def sin_sesion(request: Request, _: Exception) -> Response:
    if request.headers.get("hx-request") == "true":
        return Response(status_code=401, headers={"HX-Redirect": "/acceso"})
    return RedirectResponse("/acceso", status_code=303)


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
        registro.warning("acceso bloqueado")
        return _formulario_de_acceso(request, 429, "Demasiados intentos; espera unos minutos.")
    if not verificar_contrasena(contrasena, os.environ.get("ORQUIDEA_PASSWORD_HASH")):
        limite.fallo(ahora)
        registro.warning("acceso fallido")
        return _formulario_de_acceso(request, 401, "Contraseña incorrecta.")
    limite.acierto()
    registro.info("acceso correcto")
    identificador, _ = crear(conexion, int(ahora))
    respuesta = RedirectResponse("/", status_code=303)
    respuesta.set_cookie(
        _nombre_de_cookie(),
        identificador,
        max_age=ANTIGUEDAD_MAXIMA,
        httponly=True,
        samesite="lax",
        secure=_cookie_segura(),
    )
    return respuesta


@app.post("/salir")
def cerrar_sesion(request: Request, conexion: Base) -> RedirectResponse:
    identificador = request.cookies.get(_nombre_de_cookie())
    if identificador:
        cerrar(conexion, identificador)
    respuesta = RedirectResponse("/acceso", status_code=303)
    respuesta.delete_cookie(
        _nombre_de_cookie(), httponly=True, samesite="lax", secure=_cookie_segura()
    )
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


@app.get("/coleccion", response_class=HTMLResponse)
def mi_coleccion(request: Request, conexion: Base) -> HTMLResponse:
    ejemplares = resolver(listar(conexion), request.app.state.catalogo)
    return templates.TemplateResponse(request, "coleccion.html", {"ejemplares": ejemplares})


@app.post("/coleccion")
def agregar_a_mi_coleccion(
    request: Request, especie_id: Annotated[str, Form()], conexion: Base
) -> RedirectResponse:
    if not any(especie.id == especie_id for especie in request.app.state.catalogo):
        raise HTTPException(status_code=404, detail="Especie no encontrada")
    agregar(conexion, especie_id, int(time.time()))
    return RedirectResponse("/coleccion", status_code=303)


def _formulario_de_ejemplar(
    request: Request,
    estado: int,
    *,
    titulo: str,
    accion: str,
    boton: str,
    nombre: str = "",
    notas: str = "",
    error: str = "",
    especie: str = "",
) -> HTMLResponse:
    contexto = {
        "titulo": titulo,
        "accion": accion,
        "boton": boton,
        "nombre": nombre,
        "notas": notas,
        "error": error,
        "especie": especie,
    }
    return templates.TemplateResponse(request, "ejemplar.html", contexto, status_code=estado)


def _formulario_de_ejemplar_propio(
    request: Request, estado: int, nombre: str = "", notas: str = "", error: str = ""
) -> HTMLResponse:
    return _formulario_de_ejemplar(
        request,
        estado,
        titulo="Planta fuera del catálogo",
        accion="/coleccion/nuevo",
        boton="Agregar a mi colección",
        nombre=nombre,
        notas=notas,
        error=error,
    )


def _ejemplar_o_404(conexion: sqlite3.Connection, id: int) -> Ejemplar:
    ejemplar = obtener(conexion, id)
    if ejemplar is None:
        raise HTTPException(status_code=404, detail="Ejemplar no encontrado")
    return ejemplar


def _formulario_de_edicion(
    request: Request,
    estado: int,
    ejemplar: Ejemplar,
    nombre: str,
    notas: str,
    error: str = "",
) -> HTMLResponse:
    especie = ""
    if ejemplar.especie_id is not None:
        catalogo = request.app.state.catalogo
        encontrada = next((e for e in catalogo if e.id == ejemplar.especie_id), None)
        especie = encontrada.nombre_cientifico if encontrada else ejemplar.especie_id
    return _formulario_de_ejemplar(
        request,
        estado,
        titulo="Editar ejemplar",
        accion=f"/coleccion/{ejemplar.id}/editar",
        boton="Guardar cambios",
        nombre=nombre,
        notas=notas,
        error=error,
        especie=especie,
    )


@app.get("/coleccion/nuevo", response_class=HTMLResponse)
def formulario_de_ejemplar_propio(request: Request) -> HTMLResponse:
    return _formulario_de_ejemplar_propio(request, 200)


@app.post("/coleccion/nuevo", response_model=None)
def agregar_ejemplar_propio(
    request: Request,
    conexion: Base,
    nombre: Annotated[str, Form()] = "",
    notas: Annotated[str, Form()] = "",
) -> Response:
    try:
        nombre_limpio, notas_limpias = validar_ejemplar(nombre, notas)
    except EjemplarInvalido as fallo:
        return _formulario_de_ejemplar_propio(request, 422, nombre, notas, str(fallo))
    agregar_sin_especie(conexion, nombre_limpio, notas_limpias, int(time.time()))
    return RedirectResponse("/coleccion", status_code=303)


@app.get("/coleccion/{id}/editar", response_class=HTMLResponse)
def formulario_de_edicion(request: Request, id: int, conexion: Base) -> HTMLResponse:
    ejemplar = _ejemplar_o_404(conexion, id)
    return _formulario_de_edicion(request, 200, ejemplar, ejemplar.nombre, ejemplar.notas)


@app.post("/coleccion/{id}/editar", response_model=None)
def editar_ejemplar(
    request: Request,
    id: int,
    conexion: Base,
    nombre: Annotated[str, Form()] = "",
    notas: Annotated[str, Form()] = "",
) -> Response:
    ejemplar = _ejemplar_o_404(conexion, id)
    try:
        nombre_limpio, notas_limpias = validar_ejemplar(
            nombre, notas, con_especie=ejemplar.especie_id is not None
        )
    except EjemplarInvalido as fallo:
        return _formulario_de_edicion(request, 422, ejemplar, nombre, notas, str(fallo))
    actualizar(conexion, id, nombre_limpio, notas_limpias)
    return RedirectResponse("/coleccion", status_code=303)


@app.get("/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok"}
