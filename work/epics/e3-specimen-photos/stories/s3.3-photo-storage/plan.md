# Story s3.3: Photo storage — Plan

> Size: M
> Pause: none (default)

## Tasks

### T1 · Columna de la foto y consultas

- **Files:** create `datos/migraciones/0003-foto-del-ejemplar.sql`; modify `coleccion/modelo.py`, `datos/ejemplares.py`, `tests/test_datos_ejemplares.py`, `tests/test_datos_base.py`
- **TDD:** RED prueba de `fijar_foto` y de la migración sobre una base con ejemplares en la versión 2 → GREEN migración, `Ejemplar.foto`, consultas y `fijar_foto` → REFACTOR
- **Satisfies:** escenario de la migración 0003; base de `poner_foto`
- **Mold:** `datos/ejemplares.py` (consultas parametrizadas) y ADR-003 (migración nueva, la aplicada no se edita)
- **Verify:** `foto` sale en `obtener` y `listar` y una migración sobre datos los conserva — forced mutations: no seleccionar `foto` en `listar` (solo `obtener` la trae: la prueba de `listar` falla); `fijar_foto` sin `WHERE id` (otro ejemplar cambia); editar `0002` en lugar de añadir `0003` (la prueba de migración sobre datos falla); then `uv run pytest tests/test_datos_ejemplares.py tests/test_datos_base.py -q` y `./scripts/check` completo
- **Commit:** feat(datos): guardar el nombre de la foto en el ejemplar

### T2 · Archivos de fotos y operaciones coherentes

- **Files:** create `datos/almacen_fotos.py`, `tests/test_datos_almacen_fotos.py`
- **TDD:** RED pruebas de guardar, reemplazar, quitar foto, quitar ejemplar, ejemplar inexistente, nombres inválidos, fallo de la segunda escritura y dos hilos → GREEN módulo con escritura atómica y cerrojo → REFACTOR
- **Satisfies:** todos los escenarios del scope y los del diseño salvo el arranque
- **Mold:** ADR-006; `datos/ejemplares.py` (funciones sobre `sqlite3.Connection`)
- **Verify:** el directorio contiene exactamente los archivos de las fotos vigentes tras cada operación — forced mutations: no borrar los archivos anteriores al reemplazar; no borrarlos al quitar el ejemplar; quitar el cerrojo (la prueba de hilos deja huérfanos); formar la ruta con `str(id)` (equivalent form: la prueba de nombre `..` y la de nombre aleatorio fallan); no limpiar la primera escritura si falla la segunda; then `uv run pytest tests/test_datos_almacen_fotos.py -q` y `./scripts/check` completo
- **Commit:** feat(datos): guardar, reemplazar y borrar las fotos de un ejemplar

### T3 · Directorio al arrancar y quitar el ejemplar con sus archivos

- **Files:** modify `datos/almacen_fotos.py` (`directorio_de_fotos`, `preparar_directorio`), `web/app.py`, `web/rutas/coleccion.py`, `tests/conftest.py`, `tests/test_web_coleccion.py`, `tests/test_datos_almacen_fotos.py`
- **TDD:** RED prueba web: quitar un ejemplar con foto borra los archivos; prueba de arranque con directorio no escribible → GREEN `app.state.directorio_fotos`, ciclo de vida y la ruta usan las funciones → REFACTOR
- **Satisfies:** el criterio `@stated`, quitar el ejemplar y el arranque
- **Mold:** `web/app.py` (`app.state.ruta_base`, `abrir_base` en el ciclo de vida)
- **Verify:** quitar por HTTP deja el directorio vacío y un directorio no escribible detiene el arranque con la ruta en el mensaje — forced mutations: volver a llamar a `quitar` en la ruta (archivos huérfanos: la prueba web falla); no llamar `preparar_directorio` en el ciclo de vida; then `./scripts/check` completo
- **Commit:** feat(coleccion): quitar un ejemplar borra su foto

### T4 · Manual integration test

- Con `uvicorn` real y `ORQUIDEA_DB`/`ORQUIDEA_FOTOS` en una carpeta temporal: arrancar (el directorio se crea), poner una foto por el módulo, reiniciar el proceso (la foto sigue), quitar el ejemplar por HTTP y ver el directorio vacío.
- **Verify:** los archivos aparecen, sobreviven al reinicio y desaparecen al quitar el ejemplar.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 — T2 (coherencia base-disco, concurrencia) es el riesgo; T1 lo habilita.
- **Dependencies:** secuencial.
- **Risks:** la carrera entre dos subidas del mismo ejemplar → cerrojo de proceso y prueba con hilos (memoria del proyecto); un fallo entre escribir y actualizar → orden escribir → actualizar → borrar; peor caso un archivo huérfano.
