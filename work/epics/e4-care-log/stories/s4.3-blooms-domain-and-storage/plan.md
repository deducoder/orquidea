# Story s4.3: Blooms domain and storage — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · Reglas del intervalo de una floración en el dominio

- **Files:** modify `coleccion/modelo.py`, `tests/test_coleccion_modelo.py`
- **TDD:** RED pruebas de `validar_floracion` (inicio sin fin → `None`; inicio y fin; fin igual al inicio; fin anterior al inicio; inicio vacío; fin con formato inválido, inexistente o futuro; inicio futuro; espacios) → GREEN `Floracion` y `validar_floracion` que reutiliza `validar_fecha` → REFACTOR
- **Satisfies:** `@stated` de inicio sin fin, con fin y de fechas inválidas; escenario añadido del fin igual al inicio
- **Mold:** `validar_fecha` y `Riego` en `coleccion/modelo.py` (s4.1)
- **Verify:** el intervalo solo se acepta con fechas válidas, ninguna futura y `fin >= inicio` — forced mutations: comparar con `<=` en lugar de `<` para el fin anterior (un fin igual al inicio se rechaza: la prueba del mismo día falla); no validar el fin con `validar_fecha` (un fin con formato inválido pasa); tratar el fin vacío como error en vez de `None` (la floración en curso falla); no aplicar `strip` al fin; then `uv run pytest tests/test_coleccion_modelo.py -q` y `./scripts/check`
- **Commit:** feat(coleccion): validar el intervalo de una floración

### T2 · Migración `0005` y almacenamiento de floraciones

- **Files:** create `datos/migraciones/0005-floraciones.sql`, `datos/floraciones.py`, `tests/test_datos_floraciones.py`; modify `tests/test_datos_riegos.py` (la prueba de la migración afirma `user_version == 4`)
- **TDD:** RED pruebas de `agregar` (en curso, con fin, ejemplar inexistente → `None`, tope → `CuidadoInvalido` con «floraciones»), `listar` (orden por inicio y luego id), `terminar` (éxito; ya terminada; fin anterior al inicio; ajena → `False`; inexistente → `False`), `quitar` (propia; ajena → `False`), cascada al quitar el ejemplar, `CHECK` con SQL directo (forma y `fin < inicio`), migración sobre una base en la versión 4 con ejemplares, foto y riegos → GREEN migración y funciones (`INSERT … SELECT` y `UPDATE` condicionado) → REFACTOR
- **Satisfies:** todos los `@stated` y `@deduced` del scope salvo la concurrencia; escenario añadido del `CHECK`
- **Mold:** `datos/riegos.py` y `tests/test_datos_riegos.py` (s4.1), ADR-003 y ADR-008
- **Verify:** el historial de un ejemplar solo contiene sus floraciones, en orden, sin más de 500, y una ya terminada o ajena no cambia — forced mutations: `terminar` sin `AND fin IS NULL` (una terminada cambia de fecha: la prueba falla); `terminar` sin `AND ejemplar_id = ?` (la ajena cambia); `terminar` sin `AND inicio <= ?` (el `CHECK` lanza `IntegrityError` en lugar de `CuidadoInvalido`: la prueba falla); `quitar` sin `AND ejemplar_id = ?`; `ORDER BY id` en lugar de `inicio, id`; quitar `ON DELETE CASCADE`; quitar el `WHERE EXISTS` del alta; then `uv run pytest tests/test_datos_floraciones.py tests/test_datos_riegos.py tests/test_datos_base.py -q` y `./scripts/check` completo (archivo nuevo que el gate escanea)
- **Commit:** feat(datos): guardar las floraciones de un ejemplar

### T3 · Tope y fin resisten operaciones simultáneas

- **Files:** modify `tests/test_datos_floraciones.py`
- **TDD:** RED/caracterización con `ThreadPoolExecutor`, `threading.Barrier` y una conexión por hilo: 499 floraciones y 8 altas a la vez; una floración en curso y 8 `terminar` a la vez → GREEN (T2 debe pasarlas; si fallan, corregir T2 antes) → REFACTOR; en bucle de 15 corridas (memoria del proyecto)
- **Satisfies:** escenarios añadidos de altas y de `terminar` simultáneos
- **Mold:** `test_altas_simultaneas_no_rebasan_el_tope` en `tests/test_datos_riegos.py` (s4.1)
- **Verify:** con 499 floraciones y 8 altas quedan exactamente 500 y 7 rechazos; con 8 `terminar` sobre la misma floración hay un éxito, siete rechazos y una sola fecha de fin — forced mutations: contar y luego insertar en dos sentencias (el tope se rebasa en alguna de las 15 corridas); leer `fin` y luego escribirlo en dos sentencias (varios éxitos); quitar la comprobación del tope; then `for i in $(seq 15); do uv run pytest tests/test_datos_floraciones.py -q -k simultane || break; done` y `./scripts/check`
- **Commit:** test(datos): el tope y el fin de una floración resisten operaciones simultáneas

### T4 · Manual integration test

- Con una base temporal real (`ORQUIDEA_DB`) desde un proceso aparte: partir de una copia en la versión 4 con ejemplar, foto y riegos, abrirla con `abrir_base` (migra a la 5), agregar dos floraciones (una en curso y otra terminada), terminar la primera, intentar terminarla de nuevo y con un fin anterior, quitar el ejemplar y comprobar con `sqlite3` que `floraciones` y `riegos` quedaron vacías.
- **Verify:** `PRAGMA user_version` es 5, los ejemplares, fotos y riegos previos siguen, los errores tienen mensaje y la tabla queda vacía tras quitar el ejemplar.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 — T2 es el riesgo (`terminar` condicionado, IDOR, cascada, tope); T1 le da la validación y T3 prueba las carreras.
- **Dependencies:** secuencial; T3 depende de T2.
- **Risks:** la prueba de la migración de s4.1 afirma la versión 4 y se rompe al añadir `0005` → se actualiza en T2 (orphaned test); `terminar` con lectura y escritura separadas deja pasar dos éxitos → una sola sentencia y prueba con hilos; la diferencia entre «ajena/inexistente» y «ya terminada» debe salir de una consulta posterior sin cambiar nada → pruebas de los tres desenlaces.
