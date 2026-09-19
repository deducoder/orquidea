# Story s2.6: Edit and remove specimens — Design

> Complexity: moderate

## 1 · What & why

**Problem:** una colección real cambia: se corrigen datos, se anotan floraciones en las notas, se pierden plantas. Hoy un ejemplar agregado no se puede tocar.
**Value:** RF-04 completo; el registro personal se puede mantener sin volver a otra herramienta.

## 2 · Approach

Rutas por identificador de ejemplar: `GET`/`POST /coleccion/{id}/editar` y `GET`/`POST /coleccion/{id}/quitar` (el `GET` de la baja es la confirmación y no cambia nada). El formulario de s2.5 se generaliza para reutilizarlo en la edición; la validación se generaliza con un parámetro (con o sin especie).

**Components affected:**

- `src/orquidea/coleccion/modelo.py`: modify — `validar_ejemplar_propio` pasa a `validar_ejemplar(nombre, notas, con_especie=False)` (nombre opcional si hay especie).
- `src/orquidea/datos/ejemplares.py`: modify — `obtener`, `actualizar`, `quitar`.
- `src/orquidea/web/app.py`: modify — rutas de edición y baja; `_formulario_de_ejemplar_propio` pasa a un formulario genérico.
- `src/orquidea/web/templates/nuevo_ejemplar.html` → `ejemplar.html`: modify (renombrar y parametrizar: título, acción, botón, especie de contexto); `confirmar_baja.html`: create; `coleccion.html`: modify (enlaces y nombre propio de un ejemplar del catálogo).
- `tests/test_coleccion_modelo.py`, `tests/test_datos_ejemplares.py`, `tests/test_web_coleccion.py`: modify.

**Legacy sweep:** `validar_ejemplar_propio` y su uso en `agregar_ejemplar_propio` (s2.5) se reemplazan por `validar_ejemplar(..., con_especie=False)`; los nombres en las pruebas de s2.5 se actualizan en el mismo cambio. `nuevo_ejemplar.html` se renombra a `ejemplar.html`. Nada más se orfana.

**Gobernanza:** RF-04; ADR-003 (SQL parametrizado); system-design (validación en el dominio); ASVS V4.2.1 (acceso a objetos por identificador: aquí solo hay un usuario y toda fila es suya; el identificador se valida como entero y una fila ausente da 404), V4.2.2 (CSRF: heredado de la dependencia global; `GET` no cambia estado), V5 (validación), V5.3 (escape).

## 3 · Interface / examples

### Usage (API / CLI)

```http
GET  /coleccion/3/editar                              -> 200 formulario con nombre y notas actuales
POST /coleccion/3/editar  csrf=…&nombre=…&notas=…     -> 303 /coleccion   (422 con el formulario si no valida; 404 si no existe)
GET  /coleccion/3/quitar                              -> 200 confirmación (no quita nada)
POST /coleccion/3/quitar  csrf=…                      -> 303 /coleccion   (404 si no existe)
GET  /coleccion/abc/editar                            -> 422
```

```python
obtener(conexion, 3)  # -> Ejemplar | None
actualizar(conexion, 3, "Mi rara", "Notas")  # -> True si existía, False si no
quitar(conexion, 3)  # -> True si existía, False si no
validar_ejemplar("", "n", con_especie=True)  # -> ("", "n")     (nombre opcional con especie)
validar_ejemplar("", "n")  # -> EjemplarInvalido("El nombre es obligatorio.")
```

### Key data structures (if applicable)

Sin tablas nuevas. Para un ejemplar del catálogo el formulario de edición muestra el nombre científico de la especie como contexto (no editable) y un campo "Nombre propio (opcional)"; para uno propio el campo "Nombre" es obligatorio. La lista muestra el nombre propio de un ejemplar del catálogo entre comillas tras el nombre científico. `actualizar` y `quitar` devuelven si la fila existía, con `cursor.rowcount`.

## 4 · Acceptance criteria

- **Must:** editar cambia solo ese ejemplar; quitar pide confirmación y solo el `POST` quita; identificador inexistente 404; los demás ejemplares (incluidos los de la misma especie) no cambian.
- **Should:** el formulario conserva lo escrito al fallar; nombre propio opcional en ejemplares del catálogo.
- **Must NOT:** cambiar estado con un `GET`; armar SQL con texto del usuario; permitir cambiar la especie; usar `|safe`.

### Deduced criteria

- Nombre vacío o excesivo en un ejemplar propio, o notas excesivas, se rechazan con mensaje: confirmed
- El nombre es opcional en un ejemplar del catálogo: confirmed
- Identificador inexistente 404; no numérico 422: confirmed
- Sin sesión o sin token → redirección o 403 sin cambios: confirmed — dependencia global, se prueba para estas rutas
- El `GET` de la confirmación no quita nada: confirmed
- Un identificador inexistente no cambia nada ni rompe la aplicación: confirmed

### Scenarios (delta over the scope)

```gherkin
Given un ejemplar del catálogo con nombre propio "Mi primera"
When lo veo en la lista
Then aparece "Epidendrum radicans" enlazado y "Mi primera" junto a él

Given la página de edición de un ejemplar del catálogo
When la abro
Then muestra su especie como texto y no permite cambiarla

Given una baja confirmada
When abro "Mi colección"
Then el ejemplar ya no está y sus vecinos conservan sus notas
```
