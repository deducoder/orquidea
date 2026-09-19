# Story s1.4: Catalog search — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · Búsqueda de dominio sin mayúsculas ni acentos

- **Files:** create `src/orquidea/catalogo/busqueda.py`, `tests/test_catalogo_busqueda.py`
- **TDD:** RED pruebas: por nombre científico parcial; por nombre común; consulta en mayúsculas; consulta sin acentos y catálogo con acentos (y a la inversa); ñ; vacía y en blanco devuelven todas; sin coincidencias devuelve `[]` → GREEN `buscar` con normalización → REFACTOR
- **Satisfies:** scenarios 1 a 4 del scope y el delta del diseño
- **Mold:** none
- **Verify:** mutaciones que las ponen en rojo: quitar `casefold`; quitar la eliminación de marcas; buscar solo en el nombre científico; comparar igualdad en vez de subcadena; luego `./scripts/check` completo (archivos nuevos)
- **Commit:** feat(catalogo): búsqueda por nombre sin mayúsculas ni acentos

### T2 · Búsqueda en la lista de especies

- **Files:** modify `src/orquidea/web/app.py`, `src/orquidea/web/templates/especies.html`, `tests/test_web_especies.py`
- **TDD:** RED pruebas: `?q=` filtra; sin coincidencias muestra el mensaje con 200; el HTML trae un formulario `GET` a `/especies` con campo `q` conservando el valor y los atributos `hx-get`, `hx-target="#resultados"` → GREEN → REFACTOR
- **Satisfies:** scenarios 5 y 6 del scope y `[stated]` 1 a 3 a nivel web
- **Mold:** T1
- **Verify:** mutaciones: ignorar `q` en la ruta; quitar el mensaje; quitar el `name="q"` del campo (el formulario sin JavaScript dejaría de buscar); luego `./scripts/check`
- **Commit:** feat(web): búsqueda en la lista de especies

### T3 · Manual integration test

- Con uvicorn real y un catálogo temporal de dos especies: `curl '/especies?q=ORQUIDEA'`, `q=zzz`, `q=`; y en el navegador (Claude in Chrome no disponible aquí: se verifica con `curl` que el HTML trae los atributos htmx y que la respuesta de `?q=` es la página completa de la que htmx toma `#resultados`).
- **Verify:** respuestas correctas y `./scripts/check` en verde.

## Order & risks

- **Execution order:** T1 → T2 → T3.
- **Dependencies:** secuenciales.
- **Risks:** la actualización en vivo de htmx no se puede comprobar con `TestClient` → se prueban los atributos y la respuesta, y queda dicho en la retrospectiva que la interacción de navegador no se ejercitó; el filtrado se pierde si htmx falla pero el formulario sigue funcionando (degradación).
