# Story s1.4: Catalog search — Design

> Complexity: simple

## 1 · What & why

**Problem:** la lista de especies no se puede filtrar; con cientos de especies recorrerla es inviable.
**Value:** RF-02 cumplido con una función de dominio pequeña y una ruta existente, con actualización en vivo gracias a htmx ya cargado.

## 2 · Approach

`buscar(especies, consulta)` en el dominio normaliza texto (minúsculas y sin marcas diacríticas, con `unicodedata`) y devuelve las especies cuyo nombre científico o algún nombre común contiene la consulta normalizada. `/especies` acepta `q`. La plantilla añade un formulario `GET` con el campo y atributos htmx (`hx-get`, `hx-trigger`, `hx-target`, `hx-select`, `hx-push-url`) que reemplazan solo `#resultados` de la misma página: sin ruta parcial nueva.

**Components affected:**

- `src/orquidea/catalogo/busqueda.py`: create — `buscar`.
- `src/orquidea/web/app.py`: modify — `q: str = ""` en la lista.
- `src/orquidea/web/templates/especies.html`: modify — formulario, `#resultados`, mensaje sin coincidencias.
- `tests/test_catalogo_busqueda.py`, `tests/test_web_especies.py`: create / modify.

**Legacy sweep:** nada — net-new. Gemba: `modelo.py`, `app.py` y `especies.html` leídos; `unicodedata` de la biblioteca estándar cubre la normalización (sin dependencias). Gobernanza: RF-02; system-design (la búsqueda es dominio, no conoce HTTP; la ruta la invoca); `must-perf-001` (sin JS nuevo: htmx ya está). Búsqueda por subcadena lineal, suficiente para ~700 especies.

## 3 · Interface / examples

### Usage (API / CLI)

```python
from orquidea.catalogo.busqueda import buscar

buscar(especies, "ORQUIDEA")
```

### Expected output (success + error)

```
buscar(catalogo, "ORQUIDEA")   -> [Epidendrum radicans]   (común: "orquídea de fuego")
buscar(catalogo, "radicáns")   -> [Epidendrum radicans]
buscar(catalogo, "  ")         -> todas, en el orden recibido
buscar(catalogo, "zzz")        -> []
GET /especies?q=zzz            -> 200, "No hay especies que coincidan con la búsqueda."
GET /especies?q=ORQUIDEA       -> 200, solo Epidendrum radicans
```

### Key data structures (if applicable)

```python
def buscar(especies: list[Especie], consulta: str) -> list[Especie]: ...
```

## 4 · Acceptance criteria

- **Must:** subcadena en nombre científico o en cualquier nombre común; sin distinguir mayúsculas ni acentos; consulta vacía o en blanco devuelve todas; sin coincidencias, mensaje y 200; el formulario funciona sin JavaScript (`GET /especies?q=`).
- **Should:** los resultados se actualizan al escribir vía htmx sin recargar; el campo conserva el valor buscado.
- **Must NOT:** buscar en otros campos; ordenar por relevancia; agregar dependencias o JavaScript propio.

### Deduced criteria

- vacía o en blanco devuelve todas: confirmed.
- sin coincidencias → mensaje, no error: confirmed.
- actualización con htmx y funcionamiento sin JavaScript: confirmed — htmx 2 con `hx-select` reemplaza solo `#resultados` con la respuesta completa; la prueba automatizada comprueba los atributos y el formulario, la actualización en vivo se verifica en la prueba manual (sin navegador en las pruebas unitarias).

### Scenarios (delta over the scope)

```gherkin
Given una consulta con la ñ o con diéresis
When busco sin ellas
Then coincide igual (se normaliza toda marca diacrítica)
```
