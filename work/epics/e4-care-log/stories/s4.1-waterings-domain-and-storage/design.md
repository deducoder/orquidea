# Story s4.1: Waterings domain and storage — Design

> Complexity: moderate

## 1 · What & why

**Problem:** no existe nada de cuidados: ningún riego se puede guardar, y sin reglas de fecha ni tope el historial que la ficha mostrará (s4.2) puede contaminarse o crecer sin límite.
**Value:** el historial de riegos y "el último riego" son confiables desde la capa de datos, sin HTTP; s4.2 solo llama a cuatro funciones y s4.3 repite el patrón.

## 2 · Approach

Tabla `riegos` (ADR-008) con la baja en cascada y una restricción de forma de la fecha; un módulo `datos.riegos` de funciones sobre la conexión, como `datos.ejemplares`; y en el dominio, un `Riego`, la validación estricta de la fecha y el tope de 500. El tope y la existencia del ejemplar se comprueban **dentro del mismo `INSERT`** (`INSERT … SELECT … WHERE EXISTS … AND (SELECT COUNT(*)) < 500`): cada petición abre su propia conexión y las rutas síncronas corren en hilos, así que contar y luego insertar dejaría pasar el 501.º con dos altas simultáneas.

**Components affected:**

- `orquidea/datos/migraciones/0004-riegos.sql`: create — tabla `riegos (id, ejemplar_id REFERENCES ejemplares ON DELETE CASCADE, fecha TEXT CHECK GLOB 'AAAA-MM-DD')` e índice `(ejemplar_id, fecha)`.
- `orquidea/coleccion/modelo.py`: modify — `Riego`, `CuidadoInvalido`, `validar_fecha(texto, hoy)`, `CUIDADOS_MAXIMO = 500`.
- `orquidea/datos/riegos.py`: create — `agregar`, `listar`, `ultimo`, `quitar`.
- `tests/test_datos_riegos.py`, `tests/test_coleccion_modelo.py`, `tests/test_datos_base.py`: create/modify.

**Legacy sweep:** nada — net-new. Ningún código existente cambia de comportamiento; la migración añade una tabla. Orphaned tests: los que importan `orquidea.coleccion.modelo` (`test_coleccion_modelo.py`) o cuentan migraciones (`test_datos_base.py`, `test_datos_ejemplares.py` que usa `MIGRACIONES`) se corren y, si contaban tres migraciones, se actualizan.

## 3 · Interface / examples

### Usage (API)

```python
from datetime import date
from orquidea.coleccion.modelo import CuidadoInvalido, validar_fecha
from orquidea.datos.riegos import agregar, listar, quitar, ultimo

hoy = date(2026, 9, 19)
fecha = validar_fecha(" 2026-09-15 ", hoy)   # "2026-09-15"
riego = agregar(conexion, 1, fecha)          # Riego(id=1, ejemplar_id=1, fecha="2026-09-15")
agregar(conexion, 999, fecha)                # None: el ejemplar no existe, no se guarda nada
listar(conexion, 1)                          # [Riego(...)] por fecha, luego id (ascendente)
ultimo(conexion, 1)                          # el de mayor fecha (a igual fecha, el mayor id) o None
quitar(conexion, 1, riego.id)                # True
quitar(conexion, 2, riego.id)                # False: ese riego no es del ejemplar 2
```

### Expected output (success + error)

```
validar_fecha("2026-09-19", hoy)   -> "2026-09-19"
validar_fecha("19/09/2026", hoy)   -> CuidadoInvalido("La fecha debe tener el formato AAAA-MM-DD.")
validar_fecha("2026-02-30", hoy)   -> CuidadoInvalido("Esa fecha no existe en el calendario.")
validar_fecha("2026-09-20", hoy)   -> CuidadoInvalido("La fecha no puede ser posterior a hoy.")
validar_fecha("", hoy)             -> CuidadoInvalido("La fecha es obligatoria.")
agregar(...) con 500 riegos        -> CuidadoInvalido("Este ejemplar ya tiene 500 riegos; quita alguno para agregar otro.")
```

### Key data structures

```python
class Riego(BaseModel):
    id: int
    ejemplar_id: int
    fecha: str  # "AAAA-MM-DD", ya validada

CUIDADOS_MAXIMO = 500
_FORMATO = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")  # solo dígitos ASCII

def validar_fecha(texto: str, hoy: date) -> str: ...
```

```sql
CREATE TABLE riegos (
    id INTEGER PRIMARY KEY,
    ejemplar_id INTEGER NOT NULL REFERENCES ejemplares(id) ON DELETE CASCADE,
    fecha TEXT NOT NULL CHECK (fecha GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
);
CREATE INDEX riegos_por_ejemplar ON riegos (ejemplar_id, fecha);
```

### Gemba: lo medido con el tamaño máximo

500 riegos de un ejemplar (proceso aparte): 500 altas con el `INSERT … SELECT` en 7 ms, el listado en 0,3 ms, y el HTML de la ficha con un formulario de "Quitar" por fila (token CSRF incluido) en ~97 KB sin comprimir; comprime mucho porque cada fila repite el mismo esqueleto. No hay riesgo de memoria ni de tiempo; el peso en gzip lo mide s4.6 con los dos historiales llenos.

## 4 · Acceptance criteria

**Must:**

- `validar_fecha` acepta solo `AAAA-MM-DD` con dígitos ASCII (nada de `20260919`, `2026-W38-3`, ni dígitos de otros alfabetos, que `date.fromisoformat` sí admite) y rechaza fechas inexistentes y posteriores a `hoy`; `hoy` es un parámetro, no un `date.today()` escondido.
- `agregar` comprueba existencia del ejemplar y tope en la misma sentencia; devuelve `None` si el ejemplar no existe y lanza `CuidadoInvalido` en el tope.
- `quitar` y toda consulta filtran por `ejemplar_id` **y** `id`; un id ajeno devuelve `False` y no borra.
- La tabla rechaza por sí misma una fecha con otra forma (`CHECK`), aunque el dominio falle.
- Con `PRAGMA foreign_keys = ON` (toda conexión de `conectar`), quitar el ejemplar borra sus riegos.

**Should:**

- Una prueba con `ThreadPoolExecutor` y varias conexiones que intenta rebasar el tope: nunca hay más de 500 (memoria del proyecto sobre hilos en rutas síncronas).

**Must NOT:**

- No usar `date.today()` dentro del dominio ni de `datos`; la ruta (s4.2) lo pasa.
- No formar SQL con datos de entrada; todo va parametrizado.
- No editar un riego (fuera de alcance de la épica).

### ASVS L2 (`should-security-002`), recorrido desde el diseño

- **V5 validación de entrada:** cubierto aquí — fecha estricta, `CHECK` de la tabla, parametrizado; cubierto en s4.2 — la ruta que la recibe.
- **V4 control de acceso (IDOR):** cubierto aquí a nivel de datos — filtro por ejemplar y registro; la sesión y CSRF de la ruta se cubren en s4.2 (dependencia global).
- **V11 lógica de negocio:** cubierto — tope atómico de 500 y fecha no futura.
- **V2/V3 (contraseñas, sesión), V7 (registro de eventos de seguridad), V8 (protección de datos):** no aplican a esta capa; V7 se revisa en s4.2 si la ruta rechaza por 404/422 (no hay evento de seguridad).

### Deduced criteria

- Historial ordenado por fecha y, a igual fecha, por id: confirmed — `ORDER BY fecha, id`; el índice `(ejemplar_id, fecha)` lo sirve.
- Quitar un riego con ejemplar y riego no toca otros: confirmed.
- Quitar con el id del ejemplar equivocado no quita nada: confirmed — `DELETE … WHERE id = ? AND ejemplar_id = ?`.
- Quitar el ejemplar borra sus riegos: confirmed — cascada, con `foreign_keys = ON` en `conectar`; se prueba con la conexión de `abrir_base`.
- Ejemplar con el tope rechaza uno más: confirmed — dentro del `INSERT`; la causa (tope o ejemplar ausente) se distingue después con una consulta de existencia.
- Ejemplar inexistente no guarda nada: confirmed — el `WHERE EXISTS` lo impide (y la clave foránea lo respaldaría).
- Migración `0004` sobre una base de la versión 3 con ejemplares y fotos: confirmed — solo crea una tabla y un índice; se prueba con una base a `user_version = 3`.

### Scenarios (delta over the scope)

```gherkin
Given el texto "20260919" o "2026-W38-3" o dígitos de otro alfabeto
When se valida como fecha
Then se rechaza con el mensaje de formato (fromisoformat los aceptaría)

Given un ejemplar con 499 riegos y dos altas simultáneas desde conexiones distintas
When ambas terminan
Then el ejemplar tiene como máximo 500 riegos y a lo más una alta fue rechazada por el tope

Given una inserción directa en SQL con fecha "ayer"
When se intenta
Then la restricción de la tabla la rechaza
```
