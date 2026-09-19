# Story s1.3: Species sheet — Design

> Complexity: simple

## 1 · What & why

**Problem:** el catálogo se carga pero no se ve: no hay rutas ni plantillas que lo muestren.
**Value:** el coleccionista consulta cuidados y fuentes de cada especie (RF-03); es el primer camino completo de JSON validado a pantalla.

## 2 · Approach

`app.py` carga el catálogo una vez al importarse (`app.state.catalogo = cargar_catalogo(DIRECTORIO_CATALOGO)`), de modo que un JSON inválido detiene el arranque con el error explícito de s1.2. Dos rutas leen `request.app.state.catalogo`: la lista y la ficha, con plantillas que extienden `base.html`.

**Components affected:**

- `src/orquidea/web/app.py`: modify — carga del catálogo y rutas `GET /especies`, `GET /especies/{id}` (404 si no existe).
- `src/orquidea/web/templates/especies.html`, `especie.html`: create.
- `src/orquidea/web/templates/inicio.html`: modify — enlace a `/especies`.
- `tests/test_web_especies.py`: create — las pruebas fijan `app.state.catalogo` con una fixture que lo restaura.

**Legacy sweep:** nada — net-new. Gemba: `app.py` (s1.1) y `catalogo/modelo.py` (s1.2) leídos; se reutiliza `Especie` tal cual y `cargar_catalogo`. Gobernanza: RF-03; system-design (Web depende de Dominio; el dominio no importa web); `must-perf-001` (HTML mínimo, sin JS nuevo). Jinja2Templates escapa por defecto en `.html`. La búsqueda lineal por id es suficiente para ~700 especies. Sin dependencias nuevas.

## 3 · Interface / examples

### Usage (API / CLI)

```python
from fastapi.testclient import TestClient
from orquidea.web.app import app

client = TestClient(app)
client.get("/especies")
client.get("/especies/epidendrum-radicans")
```

### Expected output (success + error)

```
GET /especies                        -> 200, un <li> por especie: <a href="/especies/epidendrum-radicans">Epidendrum radicans</a>
GET /especies (catálogo vacío)       -> 200, "Aún no hay especies en el catálogo."
GET /especies/epidendrum-radicans    -> 200, nombre científico, nombres comunes, descripción,
                                        Luz/Riego/Temperatura/Sustrato cada uno con su texto y "Fuente: ...",
                                        y la lista de fuentes de la especie
GET /especies/no-existe              -> 404
```

### Key data structures (if applicable)

Se usa `orquidea.catalogo.modelo.Especie` tal como está; sin estructuras nuevas.

## 4 · Acceptance criteria

- **Must:** la lista muestra nombre científico y enlace por especie; la ficha muestra nombre científico, nombres comunes, descripción, los cuatro cuidados cada uno con su fuente, y las fuentes de la especie; id inexistente da 404; los datos se escapan; catálogo vacío da 200 con mensaje.
- **Should:** enlace de la página de inicio a `/especies`; el título de la página es el nombre científico en la ficha.
- **Must NOT:** cargar el catálogo en cada petición; mostrar un dato de cuidado sin su fuente; agregar JavaScript.

### Deduced criteria

- id inexistente → 404: confirmed.
- datos escapados: confirmed — Jinja2Templates activa el autoescape para plantillas `.html`; la prueba lo fija.
- catálogo vacío → mensaje, no error: confirmed — el directorio real está vacío hasta s1.6, así que es el estado actual del despliegue.
- `./scripts/check` en verde: confirmed.

### Scenarios (delta over the scope)

```gherkin
Given un JSON inválido en el directorio del catálogo
When importo la aplicación
Then falla con CatalogoInvalido y no arranca
```
