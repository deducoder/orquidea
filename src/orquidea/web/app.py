from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
def lista_de_especies(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request, "especies.html", {"especies": request.app.state.catalogo}
    )
