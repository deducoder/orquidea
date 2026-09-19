# Story s4.1: Waterings domain and storage — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · Reglas de la fecha y del tope en el dominio

- **Files:** modify `coleccion/modelo.py`, `tests/test_coleccion_modelo.py`
- **TDD:** RED pruebas de `validar_fecha` (válida con espacios, formato distinto, `20260919`, `2026-W38-3`, dígitos de otro alfabeto, inexistente, futura, hoy, vacía) → GREEN `Riego`, `CuidadoInvalido`, `CUIDADOS_MAXIMO`, `validar_fecha(texto, hoy)` con regex ASCII y `date.fromisoformat` → REFACTOR
- **Satisfies:** los tres `@stated` de fecha; escenario añadido de formatos que `fromisoformat` aceptaría
- **Mold:** `validar_ejemplar` y `EjemplarInvalido` en `coleccion/modelo.py` (excepción del dominio con mensaje en español)
- **Verify:** solo `AAAA-MM-DD` con dígitos ASCII, existente y no posterior a `hoy`, se acepta — forced mutations: quitar el regex y dejar solo `fromisoformat` (`20260919` y `2026-W38-3` pasan: la prueba falla); regex con `\d` (equivalent form: los dígitos de otro alfabeto pasan); comparar con `<` en lugar de `<=` contra `hoy` (hoy se rechaza); no aplicar `strip` (la fecha con espacios falla); then `uv run pytest tests/test_coleccion_modelo.py -q` y `./scripts/check`
- **Commit:** feat(coleccion): validar la fecha de un cuidado

### T2 · Migración `0004` y almacenamiento de riegos

- **Files:** create `datos/migraciones/0004-riegos.sql`, `datos/riegos.py`, `tests/test_datos_riegos.py`; modify `tests/test_datos_base.py` si cuenta migraciones
- **TDD:** RED pruebas de `agregar` (guarda; ejemplar inexistente → `None`; tope 500 → `CuidadoInvalido`), `listar` (orden por fecha y luego id), `ultimo`, `quitar` (propio; de otro ejemplar → `False` y sigue), cascada al quitar el ejemplar, `CHECK` con SQL directo, migración sobre una base en la versión 3 con ejemplares y foto → GREEN migración y funciones, con un solo `INSERT … SELECT … WHERE EXISTS … AND (SELECT COUNT(*)) < ?` → REFACTOR
- **Satisfies:** los escenarios `@stated` de agregar y último; los `@deduced` de orden, quitar, cascada, tope, ejemplar inexistente y migración; el escenario añadido del `CHECK`
- **Mold:** `datos/ejemplares.py` (funciones parametrizadas sobre `sqlite3.Connection`), ADR-003 (migración nueva) y ADR-008
- **Verify:** el historial de un ejemplar solo contiene sus riegos, en orden, y nunca más de 500 — forced mutations: `quitar` sin `AND ejemplar_id = ?` (la prueba con dos ejemplares falla); `ORDER BY id` en lugar de `fecha, id` (la prueba con fechas fuera de orden falla); quitar `ON DELETE CASCADE` (los riegos sobreviven al ejemplar); `ultimo` con `ORDER BY fecha ASC` (equivalent form: devuelve el más antiguo); quitar el `WHERE EXISTS` (el ejemplar inexistente falla por la clave foránea en lugar de devolver `None`); contar el tope en una consulta aparte antes de insertar (la prueba con hilos, T3, la ve); then `uv run pytest tests/test_datos_riegos.py tests/test_datos_base.py tests/test_datos_ejemplares.py -q` y `./scripts/check` completo (archivo nuevo que el gate escanea)
- **Commit:** feat(datos): guardar los riegos de un ejemplar

### T3 · El tope resiste altas simultáneas

- **Files:** modify `tests/test_datos_riegos.py`
- **TDD:** RED prueba con `ThreadPoolExecutor` y una conexión por hilo: 499 riegos y 8 altas a la vez → GREEN (el `INSERT` atómico de T2 debe pasarla; si falla, corregir T2 antes de seguir) → REFACTOR; se corre en bucle (memoria del proyecto: pruebas con azar, 15 corridas)
- **Satisfies:** escenario añadido de altas simultáneas
- **Mold:** `tests/test_datos_almacen_fotos.py` (prueba con hilos)
- **Verify:** con 499 riegos y 8 altas concurrentes quedan exactamente 500 y las otras siete se rechazan — forced mutations: contar y luego insertar en dos sentencias (deja pasar más de 500 en alguna de las corridas); quitar la comprobación del tope (quedan 507); then `for i in $(seq 15); do uv run pytest tests/test_datos_riegos.py -q -k simultaneas || break; done` y `./scripts/check`
- **Commit:** test(datos): el tope de riegos resiste altas simultáneas

### T4 · Manual integration test

- Con una base temporal real (`ORQUIDEA_DB`), abrirla con `abrir_base` desde un proceso aparte: agregar un ejemplar, 3 riegos, pedir `ultimo`, quitar el ejemplar y comprobar con `sqlite3` que `riegos` quedó vacía; repetir sobre una copia de una base de e3 (versión 3) para ver que `0004` se aplica sin perder ejemplares.
- **Verify:** `PRAGMA user_version` es 4, `ultimo` devuelve la fecha mayor y la tabla queda vacía tras quitar el ejemplar.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 — T2 es el riesgo (IDOR, cascada, tope atómico); T1 le da la validación y T3 prueba la carrera.
- **Dependencies:** secuencial; T3 depende de T2.
- **Risks:** el tope contado fuera de la sentencia deja pasar altas simultáneas → un solo `INSERT … SELECT` y prueba con hilos; una base de e3 con datos que la migración rompa → prueba sobre una base en la versión 3; el SQL de `GLOB` no admite todo lo que admite el regex del dominio → las dos capas comprueban lo mismo (`AAAA-MM-DD` de dígitos ASCII).
