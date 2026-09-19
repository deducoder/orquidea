# Story s4.5: Last watering in my collection — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · El último riego de todos los ejemplares en una consulta

- **Files:** modify `datos/riegos.py`, `tests/test_datos_riegos.py`
- **TDD:** RED pruebas de `ultimos`: sin riegos → `{}`; varios ejemplares con varios riegos → el mayor de cada uno; un ejemplar sin riegos no aparece; a igual fecha un solo valor; una sola sentencia SQL (con `set_trace_callback` sobre la conexión) aun con cinco ejemplares → GREEN `ultimos` → REFACTOR
- **Satisfies:** `@stated` de la consulta única; `@deduced` de el de mayor fecha y el de su propio ejemplar
- **Mold:** `datos/riegos.py::ultimo` (s4.1)
- **Verify:** `ultimos` da el mayor de cada ejemplar en una sentencia — forced mutations: `MIN(fecha)` en lugar de `MAX` (devuelve el más antiguo); quitar el `GROUP BY` (mezcla ejemplares o una sola fila); una consulta por ejemplar en un bucle (la prueba de una sola sentencia falla); then `uv run pytest tests/test_datos_riegos.py -q` y `./scripts/check`
- **Commit:** feat(datos): el último riego de todos los ejemplares en una consulta

### T2 · Mostrarlo en "Mi colección"

- **Files:** modify `web/rutas/coleccion.py`, `web/templates/coleccion.html`, `tests/test_web_cuidados.py`
- **TDD:** RED pruebas web: la fila con riegos muestra «Último riego: AAAA-MM-DD» (el mayor) y la sin riegos «Sin riegos»; cada fila el suyo con dos ejemplares; coincide con la ficha; quitar el último en la ficha actualiza la lista; con tres ejemplares `ultimos` se llama una sola vez (monkeypatch que cuenta) → GREEN ruta y plantilla → REFACTOR
- **Satisfies:** los dos `@stated` y los `@deduced` de la lista
- **Mold:** `web/rutas/coleccion.py::mi_coleccion` y `coleccion.html`
- **Verify:** cada fila muestra el último de su ejemplar y se pide una vez — forced mutations: buscar en el diccionario con el id de otra fila (un ejemplar muestra el riego de otro; usar ids desfasados, memoria del proyecto); llamar a `ultimo` por cada ejemplar dentro del bucle de la plantilla o de la ruta (la prueba de una sola llamada falla); no pasar `ultimos` a la plantilla (las pruebas no encuentran el texto); then `uv run pytest tests/test_web_cuidados.py tests/test_web_coleccion.py tests/test_web_fotos.py tests/test_medicion.py -q` y `./scripts/check`
- **Commit:** feat(coleccion): el último riego de cada ejemplar en "Mi colección"

### T3 · Manual integration test

- Con `uvicorn` real: agregar tres ejemplares, registrar riegos en dos, abrir "Mi colección" y ver «Último riego» en las filas con riegos y «Sin riegos» en la otra; quitar el último riego de uno en su ficha y volver a la lista; medir el peso de la lista con `scripts/medir-primera-carga.py` para ver que sigue dentro del presupuesto. Apagar el servidor por PID.
- **Verify:** la lista muestra lo esperado y `medir-primera-carga.py` sale con 0.

## Order & risks

- **Execution order:** T1 → T2 → T3 — T1 es la consulta (lo único con lógica); T2 solo la muestra.
- **Dependencies:** secuencial.
- **Risks:** mostrar el riego de otra fila por un desfase de ids → ids desfasados en las pruebas y mutación de id cruzado; una consulta por ejemplar escondida en la plantilla → prueba que cuenta las llamadas y otra que cuenta sentencias; el peso de la lista crece → medición en T3 con el script existente.
