import hmac
import os
import sqlite3
import time
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Form, Header, HTTPException, Request

from orquidea.datos.base import conectar
from orquidea.datos.sesiones import obtener as obtener_sesion


class SesionRequerida(Exception):
    pass


RUTAS_PUBLICAS = frozenset({"/acceso", "/salud"})
METODOS_SEGUROS = frozenset({"GET", "HEAD", "OPTIONS"})


def base_de_datos(request: Request) -> Iterator[sqlite3.Connection]:
    conexion = conectar(request.app.state.ruta_base)
    try:
        yield conexion
    finally:
        conexion.close()


Base = Annotated[sqlite3.Connection, Depends(base_de_datos)]


def cookie_segura() -> bool:
    return os.environ.get("ORQUIDEA_COOKIE_SEGURA") != "0"


def nombre_de_cookie() -> str:
    # El prefijo __Host- exige Secure: solo se usa cuando la cookie lo lleva.
    return "__Host-sesion" if cookie_segura() else "sesion"


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
    identificador = request.cookies.get(nombre_de_cookie())
    sesion = obtener_sesion(conexion, identificador, int(time.time())) if identificador else None
    if sesion is None:
        raise SesionRequerida
    if request.method not in METODOS_SEGUROS:
        enviado = csrf or x_csrf_token or ""
        if not hmac.compare_digest(enviado.encode(), sesion.csrf.encode()):
            raise HTTPException(status_code=403, detail="Token CSRF inválido")
    request.state.sesion = sesion
