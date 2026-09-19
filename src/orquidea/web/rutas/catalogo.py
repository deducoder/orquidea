from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from orquidea.catalogo.busqueda import buscar
from orquidea.web.plantillas import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def inicio(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "inicio.html")


@router.get("/especies", response_class=HTMLResponse)
def lista_de_especies(request: Request, q: str = "") -> HTMLResponse:
    especies = buscar(request.app.state.catalogo, q)
    return templates.TemplateResponse(request, "especies.html", {"especies": especies, "q": q})


@router.get("/especies/{id}", response_class=HTMLResponse)
def ficha_de_especie(request: Request, id: str) -> HTMLResponse:
    especie = next((e for e in request.app.state.catalogo if e.id == id), None)
    if especie is None:
        raise HTTPException(status_code=404, detail="Especie no encontrada")
    return templates.TemplateResponse(request, "especie.html", {"especie": especie})
