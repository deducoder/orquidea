import logging
import os
import threading
import time
from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from orquidea.autenticacion import LimiteDeIntentos, verificar_contrasena
from orquidea.datos.sesiones import ANTIGUEDAD_MAXIMA, cerrar, crear
from orquidea.web.plantillas import templates
from orquidea.web.sesion import Base, cookie_segura, nombre_de_cookie

router = APIRouter()
registro = logging.getLogger("orquidea.acceso")

_verificacion = threading.Lock()


def configurar_registro() -> None:
    # uvicorn solo configura sus propios registros: sin un manejador propio, el INFO de
    # "acceso correcto" se pierde y solo salen los avisos.
    if not registro.handlers:
        manejador = logging.StreamHandler()
        manejador.setFormatter(logging.Formatter("%(levelname)s:     %(name)s - %(message)s"))
        registro.addHandler(manejador)
    registro.setLevel(logging.INFO)


def _formulario_de_acceso(request: Request, estado: int, mensaje: str = "") -> HTMLResponse:
    return templates.TemplateResponse(
        request, "acceso.html", {"mensaje": mensaje}, status_code=estado
    )


@router.get("/acceso", response_class=HTMLResponse)
def formulario_de_acceso(request: Request) -> HTMLResponse:
    return _formulario_de_acceso(request, 200)


@router.post("/acceso", response_model=None)
def iniciar_sesion(
    request: Request, contrasena: Annotated[str, Form()], conexion: Base
) -> Response:
    limite: LimiteDeIntentos = request.app.state.limite
    # Las rutas síncronas corren en un pool de hilos y scrypt gasta 64 MiB por verificación:
    # en serie, una ráfaga no multiplica la memoria y el contador de intentos no se pisa.
    with _verificacion:
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
        nombre_de_cookie(),
        identificador,
        max_age=ANTIGUEDAD_MAXIMA,
        httponly=True,
        samesite="lax",
        secure=cookie_segura(),
    )
    return respuesta


@router.post("/salir")
def cerrar_sesion(request: Request, conexion: Base) -> RedirectResponse:
    identificador = request.cookies.get(nombre_de_cookie())
    if identificador:
        cerrar(conexion, identificador)
    respuesta = RedirectResponse("/acceso", status_code=303)
    respuesta.delete_cookie(
        nombre_de_cookie(), httponly=True, samesite="lax", secure=cookie_segura()
    )
    return respuesta
