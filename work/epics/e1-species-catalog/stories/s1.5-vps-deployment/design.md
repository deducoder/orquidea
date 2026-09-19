# Story s1.5: VPS deployment — Design

> Complexity: simple

## 1 · What & why

**Problem:** la aplicación solo corre con `TestClient` y un `uvicorn` ad hoc; no hay forma reproducible de ponerla en el VPS.
**Value:** con un Dockerfile y una guía, el humano despliega en su Dokploy (Debian 13) con unos clics una vez que el repositorio está en GitHub, y Dokploy sabe si la aplicación está viva.

## 2 · Approach

Un Dockerfile de una etapa (Python 3.13 slim, uv, usuario sin privilegios) que instala las dependencias de ejecución con `uv sync --frozen --no-dev` y arranca `uvicorn` en el puerto 8000; un endpoint `/salud` como healthcheck; una sección del README que dice qué configurar en Dokploy. Una sola etapa y sin compose: Dokploy ya provee el proxy, el dominio y el HTTPS.

**Components affected:**

- `src/orquidea/web/app.py`: modify — ruta `GET /salud`.
- `pyproject.toml`, `uv.lock`: modify — `uvicorn` como dependencia de ejecución.
- `Dockerfile`, `.dockerignore`: create.
- `README.md`: modify — sección "Despliegue con Dokploy".
- `tests/test_web_inicio.py`: modify — prueba de `/salud`.

**Legacy sweep:** nada — net-new.

Gemba: `app.py` es la aplicación ASGI (`orquidea.web.app:app`); `uv_build` es el backend y no se sabía si empaqueta plantillas, estáticos y JSON (riesgo de s1.1): se comprueba construyendo el wheel. Gobernanza: ADR-001 (un proceso y un archivo de base en el VPS), system-context (VPS propio, HTTPS lo termina el proxy), system-design (toda ruta exige sesión salvo el login: `/salud` queda como excepción explícita para e2; no expone datos). `uvicorn` es un paquete muy conocido (N/A supply-chain). Sin Docker utilizable en esta máquina, el Dockerfile no se construye aquí: su verificación es la instalación desde el wheel en un entorno limpio, que reproduce lo que hace la imagen salvo el propio `docker build`; queda dicho en la retrospectiva.

## 3 · Interface / examples

### Usage (API / CLI)

```python
from fastapi.testclient import TestClient
from orquidea.web.app import app

TestClient(app).get("/salud")
```

### Expected output (success + error)

```
GET /salud   -> 200, {"estado":"ok"}
```

```dockerfile
FROM python:3.13-slim
ENV UV_PYTHON_DOWNLOADS=never PATH="/app/.venv/bin:$PATH"
WORKDIR /app
RUN pip install --no-cache-dir uv==0.12.7
COPY pyproject.toml uv.lock ./
COPY src ./src
RUN uv sync --frozen --no-dev && useradd --system --uid 10001 app
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request as u; u.urlopen('http://127.0.0.1:8000/salud')"
CMD ["uvicorn", "orquidea.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Key data structures (if applicable)

Ninguna.

## 4 · Acceptance criteria

- **Must:** `/salud` responde 200 sin sesión ni catálogo; `uvicorn` declarado en las dependencias de ejecución; el wheel incluye plantillas, `htmx.min.js` y los 100 JSON, y una instalación limpia sirve `/especies` con 100 enlaces; Dockerfile y guía en el repositorio; `./scripts/check` en verde.
- **Should:** el contenedor corre sin privilegios y con healthcheck.
- **Must NOT:** ejecutar el despliegue real; guardar secretos o dominios en el repositorio; abrir puertos distintos del 8000.

### Deduced criteria

- `/salud` responde 200 sin depender del catálogo ni de una sesión: confirmed — la ruta no lee `app.state.catalogo`; e2 debe mantenerla fuera de la sesión.
- instalación limpia sirve plantillas, htmx y las 100 fichas: confirmed como criterio; se verifica en la prueba manual (wheel en un entorno nuevo), no en una prueba unitaria, porque construir el paquete en cada corrida del gate lo haría lento.

### Scenarios (delta over the scope)

```gherkin
Given el contenedor construido por Dokploy
When corre como usuario sin privilegios
Then escribe solo en lugares permitidos (no escribe en disco)
```
