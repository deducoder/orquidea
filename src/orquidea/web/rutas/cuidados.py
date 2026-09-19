from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, Response

from orquidea.coleccion.modelo import CuidadoInvalido, validar_fecha
from orquidea.datos.riegos import agregar
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
        return ficha(request, conexion, 422, ejemplar, str(fallo), fecha)
    return RedirectResponse(f"/coleccion/{id}", status_code=303)
