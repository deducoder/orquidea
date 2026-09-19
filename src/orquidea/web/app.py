from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from orquidea.catalogo.busqueda import buscar
from orquidea.datos.catalogo import DIRECTORIO_CATALOGO, cargar_catalogo

BASE_DIR = Path(__file__).parent

app = FastAPI()
app.state.catalogo = cargar_catalogo(DIRECTORIO_CATALOGO)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


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
