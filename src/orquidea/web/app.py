from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles

from orquidea.autenticacion import LimiteDeIntentos
from orquidea.datos.almacen_fotos import directorio_de_fotos, preparar_directorio
from orquidea.datos.base import abrir_base, ruta_de_la_base
from orquidea.datos.catalogo import DIRECTORIO_CATALOGO, cargar_catalogo
from orquidea.web.rutas import acceso, catalogo, coleccion
from orquidea.web.sesion import SesionRequerida, cookie_segura, exigir_sesion

BASE_DIR = Path(__file__).parent


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI) -> AsyncIterator[None]:
    acceso.configurar_registro()
    abrir_base(app.state.ruta_base).close()
    preparar_directorio(app.state.directorio_fotos)
    yield


app = FastAPI(
    lifespan=ciclo_de_vida,
    dependencies=[Depends(exigir_sesion)],
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.state.catalogo = cargar_catalogo(DIRECTORIO_CATALOGO)
app.state.ruta_base = ruta_de_la_base()
app.state.directorio_fotos = directorio_de_fotos(app.state.ruta_base)
app.state.limite = LimiteDeIntentos()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


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
    if cookie_segura():
        respuesta.headers["Strict-Transport-Security"] = "max-age=31536000"
    return respuesta


@app.exception_handler(SesionRequerida)
def sin_sesion(request: Request, _: Exception) -> Response:
    if request.headers.get("hx-request") == "true":
        return Response(status_code=401, headers={"HX-Redirect": "/acceso"})
    return RedirectResponse("/acceso", status_code=303)


app.include_router(acceso.router)
app.include_router(catalogo.router)
app.include_router(coleccion.router)


@app.get("/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok"}
