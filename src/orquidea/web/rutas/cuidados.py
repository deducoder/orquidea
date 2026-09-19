from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, Response

from orquidea.coleccion.modelo import CuidadoInvalido, validar_fecha, validar_floracion
from orquidea.datos.floraciones import agregar as agregar_floracion
from orquidea.datos.floraciones import quitar as quitar_floracion
from orquidea.datos.floraciones import terminar
from orquidea.datos.riegos import agregar, quitar
from orquidea.web.rutas.coleccion import ejemplar_o_404, ficha, hoy
from orquidea.web.sesion import Base

router = APIRouter()


@router.post("/coleccion/{id}/riegos", response_model=None)
def registrar_riego(
    request: Request, id: int, conexion: Base, fecha: Annotated[str, Form()] = ""
) -> Response:
    ejemplar = ejemplar_o_404(conexion, id)
    try:
        agregar(conexion, id, validar_fecha(fecha, hoy()))
    except CuidadoInvalido as fallo:
        return ficha(request, conexion, 422, ejemplar, str(fallo), {"fecha": fecha})
    return RedirectResponse(f"/coleccion/{id}", status_code=303)


@router.post("/coleccion/{id}/riegos/{riego}/quitar")
def quitar_riego(id: int, riego: int, conexion: Base) -> RedirectResponse:
    if not quitar(conexion, id, riego):
        raise HTTPException(status_code=404, detail="Riego no encontrado")
    return RedirectResponse(f"/coleccion/{id}", status_code=303)


@router.post("/coleccion/{id}/floraciones", response_model=None)
def registrar_floracion(
    request: Request,
    id: int,
    conexion: Base,
    inicio: Annotated[str, Form()] = "",
    fin: Annotated[str, Form()] = "",
) -> Response:
    ejemplar = ejemplar_o_404(conexion, id)
    try:
        agregar_floracion(conexion, id, *validar_floracion(inicio, fin, hoy()))
    except CuidadoInvalido as fallo:
        return ficha(request, conexion, 422, ejemplar, str(fallo), {"inicio": inicio, "fin": fin})
    return RedirectResponse(f"/coleccion/{id}", status_code=303)


@router.post("/coleccion/{id}/floraciones/{floracion}/fin", response_model=None)
def terminar_floracion(
    request: Request,
    id: int,
    floracion: int,
    conexion: Base,
    fin: Annotated[str, Form()] = "",
) -> Response:
    ejemplar = ejemplar_o_404(conexion, id)
    try:
        terminada = terminar(conexion, id, floracion, validar_fecha(fin, hoy()))
    except CuidadoInvalido as fallo:
        return ficha(request, conexion, 422, ejemplar, str(fallo))
    if not terminada:
        raise HTTPException(status_code=404, detail="Floración no encontrada")
    return RedirectResponse(f"/coleccion/{id}", status_code=303)


@router.post("/coleccion/{id}/floraciones/{floracion}/quitar")
def quitar_la_floracion(id: int, floracion: int, conexion: Base) -> RedirectResponse:
    if not quitar_floracion(conexion, id, floracion):
        raise HTTPException(status_code=404, detail="Floración no encontrada")
    return RedirectResponse(f"/coleccion/{id}", status_code=303)
