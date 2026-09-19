# Story s2.5: Specimens outside the catalog — Design

> Complexity: simple

## 1 · What & why

**Problem:** una colección real incluye plantas que el catálogo no tiene; hoy solo se pueden agregar especies del catálogo.
**Value:** el brief promete registrar "toda la colección real, incluidas plantas fuera del catálogo"; sin esto el registro personal queda incompleto y el usuario vuelve a su hoja de cálculo.

## 2 · Approach

Un formulario propio (`GET`/`POST /coleccion/nuevo`) con nombre y notas. La validación vive en el dominio (`validar_ejemplar_propio`); el repositorio añade `agregar_sin_especie`. La tabla ya existe (s2.4): sin migración.

**Components affected:**

- `src/orquidea/coleccion/modelo.py`: modify — `EjemplarInvalido` y `validar_ejemplar_propio(nombre, notas)`.
- `src/orquidea/datos/ejemplares.py`: modify — `agregar_sin_especie`.
- `src/orquidea/web/app.py`: modify — rutas `GET`/`POST /coleccion/nuevo`.
- `src/orquidea/web/templates/nuevo_ejemplar.html`: create; `coleccion.html`: modify (enlace, rama sin especie, notas).
- `tests/test_coleccion_modelo.py`, `tests/test_datos_ejemplares.py`, `tests/test_web_coleccion.py`: modify.

**Legacy sweep:** nada se orfana. La rama de `coleccion.html` para ejemplares sin especie que s2.4 omitió a propósito (código sin prueba) nace aquí con su prueba.

**Gobernanza:** RF-04; ADR-003 (SQL parametrizado); system-design (validación en el dominio, sin HTTP ni SQL); ASVS V5 (validar longitud y tipo de entrada, V5.1.3/V5.1.4), V5.3 (salida escapada por Jinja), CSRF ya global. `must-perf-001`: sin JavaScript nuevo.

## 3 · Interface / examples

### Usage (API / CLI)

```http
GET  /coleccion/nuevo                                                    -> 200 formulario (nombre, notas, csrf)
POST /coleccion/nuevo  csrf=…&nombre=Cattleya de mi abuela&notas=Regalo de 2019   -> 303 Location: /coleccion
POST /coleccion/nuevo  csrf=…&nombre=%20%20&notas=x                       -> 422 formulario con "El nombre es obligatorio." y notas conservadas
```

```python
validar_ejemplar_propio(
    "  Cattleya de mi abuela ", "Regalo\nde 2019"
)  # -> ("Cattleya de mi abuela", "Regalo\nde 2019")
validar_ejemplar_propio("   ", "")  # -> EjemplarInvalido("El nombre es obligatorio.")
validar_ejemplar_propio(
    "x" * 121, ""
)  # -> EjemplarInvalido("El nombre no puede pasar de 120 caracteres.")
validar_ejemplar_propio(
    "ok", "x" * 2001
)  # -> EjemplarInvalido("Las notas no pueden pasar de 2000 caracteres.")
agregar_sin_especie(
    conexion, "Cattleya de mi abuela", "Regalo de 2019", ahora
)  # -> Ejemplar(especie_id=None, ...)
```

### Key data structures (if applicable)

```python
NOMBRE_MAXIMO = 120
NOTAS_MAXIMO = 2000


class EjemplarInvalido(ValueError): ...
```

Las notas se muestran con `white-space: pre-line` (atributo `style`, permitido por la CSP de s2.3 en estilos) para conservar los saltos de línea sin `|safe` ni `<br>`. Los límites se aplican después de recortar los espacios; los saltos de línea de las notas se normalizan a `\n`.

## 4 · Acceptance criteria

- **Must:** alta sin especie con nombre y notas; aparece en la lista sin enlace; nombre vacío o excesivo, y notas excesivas, se rechazan con mensaje y sin guardar; la salida se escapa.
- **Should:** el formulario conserva lo escrito al fallar; se recortan los espacios del nombre.
- **Must NOT:** guardar un ejemplar sin especie y sin nombre; armar SQL con el texto; usar `|safe`.

### Deduced criteria

- Nombre vacío o solo espacios → error, conserva lo escrito, no guarda: confirmed
- Nombre > 120 o notas > 2000 → rechazo sin guardar: confirmed
- Se recortan los espacios del nombre: confirmed
- HTML en nombre o notas aparece escapado: confirmed
- Sin sesión o sin token → redirección o 403, sin guardar: confirmed — lo hace la dependencia global; se prueba para esta ruta
- Las notas con saltos de línea los conservan: confirmed — con `white-space: pre-line`

### Scenarios (delta over the scope)

```gherkin
Given un ejemplar propio sin notas
When se lista
Then no muestra un bloque de notas vacío

Given un ejemplar del catálogo con notas (s2.6 las permitirá)
When se lista
Then muestra sus notas igual

Given el formulario de planta fuera del catálogo
When lo abro
Then trae el campo csrf y no trae JavaScript nuevo
```
