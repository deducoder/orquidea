# Story s1.1: Web skeleton — Design

> Complexity: simple

## 1 · What & why

**Problem:** el repositorio no tiene aplicación: `src/orquidea/__init__.py` está vacío y `dependencies = []`, así que ninguna historia posterior tiene dónde montar rutas ni plantillas.
**Value:** un `GET /` que responde HTML desde una plantilla base prueba el stack de ADR-001 y los gates de extremo a extremo con lo mínimo, y deja el punto de extensión para el catálogo.

## 2 · Approach

Una aplicación FastAPI en `orquidea.web.app` con una plantilla Jinja base (bloque `content`), una página de inicio que la extiende y htmx servido como archivo estático propio.

**Components affected:**

- `src/orquidea/web/app.py`: create — `app = FastAPI()`, monta `/static`, define `GET /` que renderiza `inicio.html`.
- `src/orquidea/web/templates/base.html`, `inicio.html`: create — base con `<script src="/static/htmx.min.js">` y bloque `content`.
- `src/orquidea/web/static/htmx.min.js`: create — htmx 2.x descargado una vez y versionado; sin CDN en tiempo de ejecución (system-context: no hay sistemas externos).
- `pyproject.toml`, `uv.lock`: modify — dependencias de ejecución `fastapi`, `jinja2`; de desarrollo `httpx` (requerido por `TestClient`).
- `tests/test_web_inicio.py`: create.

**Legacy sweep:** nada — net-new (el `__init__.py` vacío se conserva).

Gemba: no hay código que reutilizar. Gobernanza consultada: ADR-001 (stack), system-design (capa Web), system-context (sin externos), `must-perf-001` (un solo script pequeño), `must-quality-001..003` (ruff, format, mypy strict). Dependencias nuevas: `fastapi`, `jinja2` y `httpx` son paquetes muy conocidos, N/A en supply-chain. Se descarta `uvicorn` ahora (YAGNI): la prueba usa `TestClient`; el servidor entra con el despliegue (s1.5).

## 3 · Interface / examples

### Usage (API / CLI)

```python
from fastapi.testclient import TestClient
from orquidea.web.app import app

client = TestClient(app)
response = client.get("/")
```

### Expected output (success + error)

```
GET /                 -> 200, text/html; charset=utf-8, contiene "<title>Orquídea" y src="/static/htmx.min.js"
GET /static/htmx.min.js -> 200, application/javascript (o text/javascript)
GET /no-existe        -> 404 (comportamiento por defecto de FastAPI)
```

### Key data structures (if applicable)

Ninguna.

## 4 · Acceptance criteria

- **Must:** `GET /` responde 200 HTML con título "Orquídea"; el HTML referencia htmx en `/static/htmx.min.js` y ese archivo se sirve con 200; `base.html` define `{% block content %}` y `inicio.html` lo extiende; `./scripts/check` en verde.
- **Should:** el título de página es un bloque de la base que cada vista puede sobrescribir.
- **Must NOT:** referenciar recursos de dominios externos; agregar `uvicorn`, sesión ni base de datos.

### Deduced criteria

- La página no depende de recursos externos: confirmed — htmx se sirve desde `/static`; la prueba comprueba que ninguna URL absoluta `http(s)://` aparezca en `src=`/`href=`.
- `./scripts/check` en verde: confirmed.

### Scenarios (delta over the scope)

```gherkin
Given la aplicación arrancada
When pido GET /static/htmx.min.js
Then recibo 200 con el contenido de htmx
```
