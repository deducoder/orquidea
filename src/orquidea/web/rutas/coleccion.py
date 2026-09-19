import logging
import sqlite3
import time
from datetime import UTC, date, datetime
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, Response

from orquidea.coleccion.modelo import Ejemplar, EjemplarInvalido, resolver, validar_ejemplar
from orquidea.datos.almacen_fotos import (
    NombreDeFotoInvalido,
    poner_foto,
    quitar_con_foto,
    quitar_foto,
    ruta_de_foto,
)
from orquidea.datos.ejemplares import (
    actualizar,
    agregar,
    agregar_sin_especie,
    listar,
    obtener,
)
from orquidea.datos.fotos import FotoInvalida, procesar_foto
from orquidea.datos.riegos import listar as listar_riegos
from orquidea.web.plantillas import templates
from orquidea.web.sesion import Base

router = APIRouter()
registro = logging.getLogger("orquidea.fotos")


@router.get("/coleccion", response_class=HTMLResponse)
def mi_coleccion(request: Request, conexion: Base) -> HTMLResponse:
    ejemplares = resolver(listar(conexion), request.app.state.catalogo)
    return templates.TemplateResponse(request, "coleccion.html", {"ejemplares": ejemplares})


@router.post("/coleccion")
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


def ejemplar_o_404(conexion: sqlite3.Connection, id: int) -> Ejemplar:
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


@router.get("/coleccion/nuevo", response_class=HTMLResponse)
def formulario_de_ejemplar_propio(request: Request) -> HTMLResponse:
    return _formulario_de_ejemplar_propio(request, 200)


@router.post("/coleccion/nuevo", response_model=None)
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


def hoy() -> date:
    return datetime.now(UTC).date()


def ficha(
    request: Request,
    conexion: sqlite3.Connection,
    estado: int,
    ejemplar: Ejemplar,
    error: str = "",
    fecha: str = "",
) -> HTMLResponse:
    (resuelto,) = resolver([ejemplar], request.app.state.catalogo)
    dia = hoy().isoformat()
    riegos = listar_riegos(conexion, ejemplar.id)
    contexto = {
        "item": resuelto,
        "error": error,
        "hoy": dia,
        "fecha": fecha or dia,
        "riegos": riegos[::-1],
        "ultimo": riegos[-1] if riegos else None,
    }
    return templates.TemplateResponse(request, "ejemplar_ficha.html", contexto, status_code=estado)


# Se registra después de `/coleccion/nuevo`: en el orden inverso, "nuevo" se leería como un id.
@router.get("/coleccion/{id}", response_class=HTMLResponse)
def ficha_del_ejemplar(request: Request, id: int, conexion: Base) -> HTMLResponse:
    return ficha(request, conexion, 200, ejemplar_o_404(conexion, id))


@router.post("/coleccion/{id}/foto", response_model=None)
def subir_foto(
    request: Request,
    id: int,
    conexion: Base,
    foto: Annotated[UploadFile | None, File()] = None,
) -> Response:
    ejemplar = ejemplar_o_404(conexion, id)
    # `LimiteDeCuerpo` ya acotó el cuerpo entero; `procesar_foto` rechaza lo que pase de 10 MB.
    datos = foto.file.read() if foto is not None else b""
    if not datos:
        return ficha(request, conexion, 422, ejemplar, "Elige una foto.")
    try:
        procesada = procesar_foto(datos)
    except FotoInvalida as fallo:
        return ficha(request, conexion, 422, ejemplar, str(fallo))
    try:
        guardada = poner_foto(conexion, request.app.state.directorio_fotos, id, procesada)
    except OSError as fallo:
        registro.warning("no se pudo guardar una foto: %s", fallo)
        return ficha(request, conexion, 500, ejemplar, "No se pudo guardar la foto.")
    if not guardada:
        raise HTTPException(status_code=404, detail="Ejemplar no encontrado")
    return RedirectResponse(f"/coleccion/{id}", status_code=303)


def _imagen(request: Request, id: int, conexion: sqlite3.Connection, miniatura: bool) -> Response:
    ejemplar = obtener(conexion, id)
    if ejemplar is None or not ejemplar.foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    try:
        ruta = ruta_de_foto(request.app.state.directorio_fotos, ejemplar.foto, miniatura=miniatura)
    except NombreDeFotoInvalido:
        raise HTTPException(status_code=404, detail="Foto no encontrada") from None
    if not ruta.is_file():
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    # El tipo es fijo: el archivo lo generó `procesar_foto`, nunca lo subido por el usuario.
    return FileResponse(ruta, media_type="image/jpeg")


@router.get("/coleccion/{id}/foto")
def imagen_del_ejemplar(request: Request, id: int, conexion: Base) -> Response:
    return _imagen(request, id, conexion, miniatura=False)


@router.get("/coleccion/{id}/foto/miniatura")
def miniatura_del_ejemplar(request: Request, id: int, conexion: Base) -> Response:
    return _imagen(request, id, conexion, miniatura=True)


@router.post("/coleccion/{id}/foto/quitar")
def quitar_la_foto(request: Request, id: int, conexion: Base) -> RedirectResponse:
    if not quitar_foto(conexion, request.app.state.directorio_fotos, id):
        raise HTTPException(status_code=404, detail="Ejemplar no encontrado")
    return RedirectResponse(f"/coleccion/{id}", status_code=303)


@router.get("/coleccion/{id}/editar", response_class=HTMLResponse)
def formulario_de_edicion(request: Request, id: int, conexion: Base) -> HTMLResponse:
    ejemplar = ejemplar_o_404(conexion, id)
    return _formulario_de_edicion(request, 200, ejemplar, ejemplar.nombre, ejemplar.notas)


@router.post("/coleccion/{id}/editar", response_model=None)
def editar_ejemplar(
    request: Request,
    id: int,
    conexion: Base,
    nombre: Annotated[str, Form()] = "",
    notas: Annotated[str, Form()] = "",
) -> Response:
    ejemplar = ejemplar_o_404(conexion, id)
    try:
        nombre_limpio, notas_limpias = validar_ejemplar(
            nombre, notas, con_especie=ejemplar.especie_id is not None
        )
    except EjemplarInvalido as fallo:
        return _formulario_de_edicion(request, 422, ejemplar, nombre, notas, str(fallo))
    actualizar(conexion, id, nombre_limpio, notas_limpias)
    return RedirectResponse("/coleccion", status_code=303)


@router.get("/coleccion/{id}/quitar", response_class=HTMLResponse)
def confirmar_baja(request: Request, id: int, conexion: Base) -> HTMLResponse:
    ejemplar = ejemplar_o_404(conexion, id)
    (resuelto,) = resolver([ejemplar], request.app.state.catalogo)
    return templates.TemplateResponse(request, "confirmar_baja.html", {"item": resuelto})


@router.post("/coleccion/{id}/quitar")
def quitar_ejemplar(request: Request, id: int, conexion: Base) -> RedirectResponse:
    if not quitar_con_foto(conexion, request.app.state.directorio_fotos, id):
        raise HTTPException(status_code=404, detail="Ejemplar no encontrado")
    return RedirectResponse("/coleccion", status_code=303)
