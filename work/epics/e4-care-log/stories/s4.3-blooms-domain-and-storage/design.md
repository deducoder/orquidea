# Story s4.3: Blooms domain and storage — Design

> Complexity: moderate

## 1 · What & why

**Problem:** no hay dónde guardar las floraciones de un ejemplar (RF-07) ni reglas para su intervalo abierto: un inicio, un fin opcional que se fija después, y un fin que nunca puede ser anterior al inicio.
**Value:** el historial de floración es confiable desde la capa de datos, sin HTTP; s4.4 solo llama a cuatro funciones, igual que s4.2 con los riegos.

## 2 · Approach

Tabla `floraciones` (ADR-008) con cascada y `CHECK`s de forma y de orden, un módulo `datos.floraciones` con la forma de `datos.riegos`, y en el dominio `Floracion` y la validación del intervalo. Lo nuevo frente a los riegos es `terminar`: **una sola sentencia** `UPDATE … WHERE id = ? AND ejemplar_id = ? AND fin IS NULL AND inicio <= ?` que solo toca una floración propia, en curso y con inicio no posterior al fin; si no toca nada, una consulta posterior distingue la causa (ajena o inexistente → `False`; ya terminada o fin anterior al inicio → `CuidadoInvalido`). Así dos «terminar» simultáneos no pisan el fin. El alta repite el `INSERT … SELECT … WHERE EXISTS … AND COUNT < tope` de s4.1.

**Components affected:**

- `orquidea/datos/migraciones/0005-floraciones.sql`: create — tabla `floraciones (id, ejemplar_id REFERENCES ejemplares ON DELETE CASCADE, inicio, fin NULL)` con `CHECK` de forma de ambas fechas y `fin IS NULL OR fin >= inicio`, e índice `(ejemplar_id, inicio)`.
- `orquidea/coleccion/modelo.py`: modify — `Floracion` y `validar_floracion(inicio, fin, hoy)`.
- `orquidea/datos/floraciones.py`: create — `agregar`, `terminar`, `listar`, `quitar`.
- `tests/test_coleccion_modelo.py`, `tests/test_datos_floraciones.py`: modify/create.

**Legacy sweep:** nada — net-new. La constante `CUIDADOS_MAXIMO` de s4.1 se comparte; cada módulo pone su propio mensaje (la observación de la revisión de s4.1). Orphaned tests: los que importan `coleccion.modelo` o cuentan migraciones se corren; `tests/test_datos_riegos.py::test_la_migracion_conserva_los_ejemplares_y_sus_fotos` afirma `user_version == 4` y **fallará** al existir `0005`: se actualiza en esta historia (T2).

## 3 · Interface / examples

### Usage (API)

```python
from datetime import date
from orquidea.coleccion.modelo import CuidadoInvalido, validar_floracion
from orquidea.datos.floraciones import agregar, listar, quitar, terminar

hoy = date(2026, 9, 19)
inicio, fin = validar_floracion(" 2026-03-01 ", "", hoy)  # ("2026-03-01", None)
inicio, fin = validar_floracion("2026-03-01", "2026-03-20", hoy)
floracion = agregar(conexion, 1, inicio, fin)  # Floracion(id=1, ejemplar_id=1, inicio=..., fin=...)
agregar(conexion, 999, inicio, None)  # None: el ejemplar no existe
terminar(conexion, 1, floracion.id, "2026-03-20")  # True
terminar(conexion, 2, floracion.id, "2026-03-20")  # False: no es del ejemplar 2
listar(conexion, 1)  # por inicio, luego id (ascendente)
quitar(conexion, 1, floracion.id)  # True
```

### Expected output (success + error)

```
validar_floracion("2026-03-01", "", hoy)            -> ("2026-03-01", None)
validar_floracion("2026-03-20", "2026-03-01", hoy)  -> CuidadoInvalido("El fin no puede ser anterior al inicio.")
validar_floracion("", "", hoy)                      -> CuidadoInvalido("La fecha es obligatoria.")
validar_floracion("2026-03-01", "2026-09-20", hoy)  -> CuidadoInvalido("La fecha no puede ser posterior a hoy.")
terminar(...) sobre una ya terminada                -> CuidadoInvalido("Esa floración ya terminó.")
terminar(...) con fin anterior al inicio            -> CuidadoInvalido("El fin no puede ser anterior al inicio.")
agregar(...) con 500 floraciones                    -> CuidadoInvalido("Este ejemplar ya tiene 500 floraciones; quita alguna para agregar otra.")
```

### Key data structures

```python
class Floracion(BaseModel):
    id: int
    ejemplar_id: int
    inicio: str  # "AAAA-MM-DD"
    fin: str | None  # None = en curso


def validar_floracion(inicio: str, fin: str, hoy: date) -> tuple[str, str | None]: ...
```

```sql
CREATE TABLE floraciones (
    id INTEGER PRIMARY KEY,
    ejemplar_id INTEGER NOT NULL REFERENCES ejemplares (id) ON DELETE CASCADE,
    inicio TEXT NOT NULL CHECK (inicio GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
    fin TEXT CHECK (fin GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
    CHECK (fin IS NULL OR fin >= inicio)
);
CREATE INDEX floraciones_por_ejemplar ON floraciones (ejemplar_id, inicio);
```

### Gemba: lo medido con el tamaño máximo

500 floraciones de un ejemplar (proceso aparte): altas en 7 ms, listado en 0,3 ms. El HTML de la ficha con dos formularios por fila (quitar y terminar, con token CSRF) es de ~210 KB **sin comprimir**, el doble que los riegos; se comprime mucho porque cada fila repite el mismo esqueleto y el mismo token. Dos consecuencias para s4.4 y s4.6: «Terminar» solo se ofrece en las floraciones en curso (la mayoría de las terminadas no lo lleva) y el peso en gzip se mide con los dos historiales llenos.

## 4 · Acceptance criteria

**Must:**

- `validar_floracion` reutiliza `validar_fecha` para el inicio y el fin (mismo formato ASCII, existencia y «no posterior a hoy»); el fin vacío es `None`; un fin anterior al inicio se rechaza (uno igual al inicio se acepta: florece un solo día).
- `agregar` comprueba existencia del ejemplar y tope en la misma sentencia; `None` si no existe, `CuidadoInvalido` en el tope con «floraciones» en el mensaje.
- `terminar` es una sola sentencia condicionada a propia, en curso y con inicio no posterior; distingue después la causa; nunca cambia una floración ajena ni una ya terminada.
- `quitar`, `terminar` y toda consulta filtran por `ejemplar_id` **y** `id`.
- La tabla rechaza por sí misma una fecha con otra forma y un `fin` anterior al `inicio`, aunque el dominio falle; quitar el ejemplar borra sus floraciones.

**Should:**

- Pruebas con hilos y una conexión por hilo: el tope no se rebasa con altas simultáneas y dos `terminar` simultáneos sobre la misma floración dejan uno con éxito y otro rechazado.

**Must NOT:**

- No usar el reloj dentro del dominio ni de `datos` (`hoy` es parámetro).
- No formar SQL con datos de entrada.
- No editar ni reabrir una floración (fuera de alcance de la épica).

### ASVS L2 (`should-security-002`), recorrido desde el diseño

- **V5 validación de entrada:** cubierto aquí — dominio estricto, `CHECK` de forma y de orden, SQL parametrizado; la ruta que recibe las fechas, en s4.4.
- **V4 control de acceso (IDOR):** cubierto a nivel de datos — filtro por ejemplar y floración en `quitar` y `terminar`, con prueba de dos ejemplares; sesión y CSRF, en s4.4 (dependencia global).
- **V11 lógica de negocio:** cubierto — tope atómico, fecha no futura, fin no anterior al inicio, no terminar dos veces.
- **V2/V3, V7, V8:** no aplican a esta capa.

### Deduced criteria

- Historial ordenado por inicio y, a igual inicio, por id: confirmed — `ORDER BY inicio, id`, servido por el índice.
- Fijar otro fin a una floración terminada se rechaza: confirmed — `AND fin IS NULL` en el `UPDATE`; el mensaje sale de la consulta posterior.
- Fin anterior al inicio al terminar se rechaza y sigue en curso: confirmed — `AND inicio <= ?` en el `UPDATE` (y el `CHECK` de respaldo).
- Quitar o terminar solo cambia esa floración: confirmed.
- Un id de ejemplar ajeno no cambia nada: confirmed — `terminar` y `quitar` devuelven `False`.
- Quitar el ejemplar borra sus floraciones: confirmed — cascada con `foreign_keys = ON`.
- Tope con mensaje que nombra las floraciones: confirmed.
- Migración `0005` sobre una base en la versión 4 con datos: confirmed — solo crea una tabla y un índice.

### Scenarios (delta over the scope)

```gherkin
Given una floración con inicio y fin el mismo día
When se agrega
Then se acepta (fin igual al inicio no es anterior)

Given una floración en curso y dos intentos simultáneos de terminarla desde conexiones distintas
When ambos terminan
Then queda una sola fecha de fin y a lo más uno tuvo éxito

Given un ejemplar con 499 floraciones y dos altas simultáneas
When ambas terminan
Then el ejemplar tiene como máximo 500 y a lo más una fue rechazada por el tope

Given una inserción directa en SQL con fin anterior al inicio o con una fecha "ayer"
When se intenta
Then las restricciones de la tabla la rechazan
```
