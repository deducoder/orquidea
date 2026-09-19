# Story s2.4: Add catalog specimens and see them — Design

> Complexity: moderate

## 1 · What & why

**Problem:** el catálogo es solo consulta; el usuario no puede registrar las plantas que posee.
**Value:** primera pieza de la colección personal: un ejemplar ligado a su especie, con los cuidados a un clic. Cierra el recorrido de la métrica líder del brief.

## 2 · Approach

Tabla `ejemplares` (migración `0002`), un modelo `Ejemplar` del dominio, un repositorio con `agregar` y `listar`, y dos rutas (`POST /coleccion`, `GET /coleccion`) con patrón POST-redirección-GET. El nombre de la especie se resuelve contra el catálogo en memoria, no en la base (ADR-003, punto 5).

**Components affected:**

- `src/orquidea/datos/migraciones/0002-ejemplares.sql`: create.
- `src/orquidea/coleccion/__init__.py`, `modelo.py`: create — `Ejemplar`, `EjemplarConEspecie` y `resolver(ejemplares, catalogo)`.
- `src/orquidea/datos/ejemplares.py`: create — `agregar`, `listar`.
- `src/orquidea/web/app.py`: modify — rutas `GET`/`POST /coleccion`, filtro de plantilla `fecha`.
- `src/orquidea/web/templates/coleccion.html`: create; `_csrf.html`: create (campo oculto reutilizable); `especie.html`: modify (botón); `base.html`: modify (enlace "Mi colección" y uso de `_csrf.html`).
- `tests/test_coleccion_modelo.py`, `tests/test_datos_ejemplares.py`, `tests/test_web_coleccion.py`: create.

**Legacy sweep:** nada se orfana. `base.html` sustituye su campo `csrf` en línea por el parcial `_csrf.html` (mismo comportamiento, cubierto por `test_web_proteccion.py`). La tabla completa de RF-04 (con `nombre` y `notas`) se crea aquí para que s2.5 y s2.6 no necesiten otra migración de esquema.

**Gobernanza:** RF-04; ADR-003 (SQL parametrizado, sin clave foránea a la especie); system-design (el dominio no conoce HTTP ni SQL: `orquidea.coleccion` no importa `sqlite3` ni `orquidea.web`); `should-security-002` (CSRF ya exigido por la dependencia global; consultas parametrizadas; Jinja escapa la salida); ASVS V5 (validación de la entrada): el `especie_id` se valida contra el catálogo antes de guardar y se guarda tal cual solo si existe. `must-perf-001`: la lista no trae JS nuevo.

## 3 · Interface / examples

### Usage (API / CLI)

```http
POST /coleccion   csrf=…&especie_id=epidendrum-radicans   -> 303 Location: /coleccion
POST /coleccion   csrf=…&especie_id=no-existe             -> 404
GET  /coleccion                                           -> 200 lista (o mensaje de colección vacía)
```

```python
ejemplar = agregar(
    conexion, "epidendrum-radicans", ahora=1_780_000_000
)  # -> Ejemplar(id=1, especie_id="epidendrum-radicans", nombre="", notas="", creado=...)
listar(conexion)  # -> [Ejemplar, ...] por id ascendente
resolver(
    listar(conexion), catalogo
)  # -> [EjemplarConEspecie(ejemplar=..., especie=Especie | None)]
```

### Key data structures (if applicable)

```sql
CREATE TABLE ejemplares (
    id INTEGER PRIMARY KEY,
    especie_id TEXT,                         -- Especie.id del catálogo, sin clave foránea
    nombre TEXT NOT NULL DEFAULT '',         -- solo para ejemplares sin especie de catálogo (s2.5)
    notas TEXT NOT NULL DEFAULT '',
    creado INTEGER NOT NULL,                 -- segundos epoch
    CHECK (especie_id IS NOT NULL OR length(trim(nombre)) > 0)
);
```

```python
class Ejemplar(BaseModel):
    id: int
    especie_id: str | None
    nombre: str
    notas: str
    creado: int


@dataclass(frozen=True)
class EjemplarConEspecie:
    ejemplar: Ejemplar
    especie: Especie | None  # None: sin especie de catálogo, o desaparecida del catálogo
```

Diseño: la validación de que la especie existe la hace la ruta (404) contra `app.state.catalogo`; el repositorio no conoce el catálogo. El botón de la ficha es un formulario `POST` sin JavaScript. La lista ordena por `id`. La fecha se muestra `AAAA-MM-DD` con un filtro Jinja (no hay zona horaria del usuario; se usa UTC y se dice).

## 4 · Acceptance criteria

- **Must:** agregar desde la ficha crea el ejemplar; la lista lo muestra enlazado a su especie; dos ejemplares de la misma especie son dos filas; colección vacía con mensaje; especie inexistente 404 sin fila.
- **Should:** especie desaparecida del catálogo se lista con aviso; recargar tras agregar no duplica.
- **Must NOT:** guardar un `especie_id` que no está en el catálogo; armar SQL con texto del usuario; importar `sqlite3` en `orquidea.coleccion`; mostrar datos de ejemplares sin sesión.

### Deduced criteria

- Identificador inexistente → 404 sin guardar: confirmed
- Ejemplar con especie desaparecida se lista con aviso: confirmed — `resolver` devuelve `especie=None` y la plantilla lo trata
- Sin sesión o sin token → redirección o 403 sin guardar: confirmed — lo garantiza la dependencia global de s2.3 y se prueba aquí para esta ruta
- Recargar no duplica: confirmed — patrón POST-redirección-GET
- Persisten tras reiniciar: confirmed — SQLite en archivo; se prueba reabriendo la base
- `./scripts/check` en verde y `security-review` sin críticos: confirmed

### Scenarios (delta over the scope)

```gherkin
Given una especie cuyo nombre científico contiene HTML
When se lista un ejemplar suyo
Then el nombre aparece escapado

Given un POST sin el campo especie_id
When se envía
Then responde 422 y no se guarda nada

Given la lista de la colección
When la abro
Then trae el enlace "Mi colección" en la cabecera y no trae JavaScript nuevo
```
