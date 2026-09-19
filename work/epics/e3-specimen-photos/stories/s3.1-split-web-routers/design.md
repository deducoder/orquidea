# Story s3.1: Split web routers — Design

> Complexity: moderate

## 1 · What & why

**Problem:** `app.py` (376 líneas) reúne acceso, catálogo, colección, sesión, cabeceras y ciclo de vida; e3 y e4 añaden tres grupos de rutas más.
**Value:** las rutas nuevas nacen en su área y el archivo que construye la aplicación deja de crecer; ninguna ruta cambia.

## 2 · Approach

Mover cada grupo de rutas a un `APIRouter` y la dependencia de sesión a su módulo, sin tocar cuerpos de funciones. `app.py` queda con el ciclo de vida, el middleware de cabeceras, el manejador de `SesionRequerida`, `/salud` y `include_router`. La dependencia global `exigir_sesion` se queda en `FastAPI(dependencies=...)`, así que todo router incluido nace protegido.

**Components affected:**

- `orquidea/web/sesion.py`: create — `SesionRequerida`, `RUTAS_PUBLICAS`, `METODOS_SEGUROS`, `base_de_datos`, `Base`, `cookie_segura`, `nombre_de_cookie`, `exigir_sesion`.
- `orquidea/web/plantillas.py`: create — la instancia `templates` y el filtro `fecha`, que comparten los tres routers.
- `orquidea/web/rutas/{__init__,acceso,catalogo,coleccion}.py`: create — `router = APIRouter()` con las rutas de hoy (`acceso.py` lleva `registro`, `_verificacion` y `configurar_registro`; `catalogo.py` lleva `/`, `/especies`, `/especies/{id}`).
- `orquidea/web/app.py`: modify — solo construye.
- `tests/test_web_acceso.py`, `tests/test_web_proteccion.py`: modify — el destino del `monkeypatch` de `verificar_contrasena` pasa a `orquidea.web.rutas.acceso`; `RUTAS_PUBLICAS` se importa de `orquidea.web.sesion`.

**Legacy sweep:** `app.py` deja de definir todos esos nombres; ningún archivo de `src/` los importa fuera de él. Orphaned tests: los que importan `orquidea.web.app` solo usan `app`, que sigue ahí; `test_web_especies.py` carga `app.py` desde su archivo para probar que un catálogo roto detiene el arranque y sigue valiendo porque `app.py` conserva la carga del catálogo. Las dos pruebas que apuntan a nombres movidos se actualizan.

## 3 · Interface / examples

```python
from orquidea.web.app import app                      # sin cambio: `uvicorn orquidea.web.app:app`
from orquidea.web.sesion import RUTAS_PUBLICAS       # frozenset({"/acceso", "/salud"})
sorted((m, r.path) for r in app.routes for m in getattr(r, "methods", []) or [])
# idéntico antes y después de la división (se captura antes y se compara en la prueba de T1)
```

## 4 · Acceptance criteria

**Must:**

- El conjunto `(método, ruta)` de la aplicación es idéntico al de antes.
- Todas las pruebas existentes pasan; solo cambian el destino de un `monkeypatch` y un import.
- `exigir_sesion` sigue siendo la dependencia global; un router incluido sin más queda protegido.
- `app.py` conserva la carga del catálogo al importarse (la prueba de arranque lo exige).

**Should:** `app.py` queda por debajo de ~120 líneas y ningún router importa a otro.

**Must NOT:** cambiar el cuerpo de una función, una ruta, un nombre de plantilla o una cabecera; añadir rutas.

### Deduced criteria

- Sin sesión sigue redirigiendo, y una ruta nueva nace protegida: confirmed (dependencia global sin cambio).
- `/coleccion/nuevo` sigue resolviendo antes que una futura `/coleccion/{id}`: confirmed — hoy `GET /coleccion/nuevo` se registra antes que `/coleccion/{id}/editar`; la prueba fija el orden de registro de `nuevo` frente a las rutas con `{id}`.
- `uvicorn orquidea.web.app:app` sigue igual: confirmed — `app` se define en `app.py`.
- Un catálogo inválido detiene la importación: confirmed.

### Scenarios (delta over the scope)

```gherkin
Given el orden de las rutas de la colección
When se listan los caminos registrados
Then "/coleccion/nuevo" aparece antes que cualquier ruta con "{id}" sin sufijo
```
