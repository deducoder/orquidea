# Story s1.6: Seed catalog — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · Las 100 fichas y la prueba del catálogo real

- **Files:** create `src/orquidea/datos/catalogo/*.json` (100), `tests/test_catalogo_real.py`; delete `src/orquidea/datos/catalogo/.gitkeep`
- **TDD:** RED pruebas: el catálogo real carga con al menos 100 especies; cada fuente de especie y de cuidado contiene `https://` y `consultada el`; toda especie que use una hoja de otro género lo dice en su fuente → GREEN copiar los 100 JSON generados (validados con `cargar_catalogo` antes de copiar) → REFACTOR
- **Satisfies:** scenarios 1 a 3 del scope, el deducido de género y el delta del diseño
- **Mold:** none
- **Verify:** mutaciones que las ponen en rojo: quitar un JSON hasta quedar 99; borrar la URL de una fuente de cuidado; quitar el campo `fuentes` de un archivo (el cargador debe rechazar todo el catálogo); luego `uv run pytest tests/test_catalogo_real.py` y `./scripts/check` completo (archivos nuevos)
- **Commit:** feat(catalogo): cien especies nativas de Chiapas con sus fuentes

### T2 · La aplicación sirve el catálogo real

- **Files:** modify `tests/test_web_especies.py`
- **TDD:** RED prueba: con el catálogo real (sin sobrescribir `app.state.catalogo`), `/especies` responde 200 con al menos 100 enlaces, y la ficha de `epidendrum-radicans` muestra su fuente → GREEN ya debería pasar por T1; se demuestra su valor con mutación → REFACTOR
- **Satisfies:** el `Should` del diseño
- **Mold:** T1
- **Verify:** mutación: vaciar el directorio (borrar los JSON) pone en rojo la prueba; luego `./scripts/check`
- **Commit:** test(web): la aplicación sirve el catálogo real

### T3 · Manual integration test

- Con uvicorn real y el catálogo real: `curl` a `/especies`, a una ficha y a la búsqueda `?q=orquidea`; medir bytes y bytes con gzip de la lista y de una ficha (referencia para `must-perf-001`).
- **Verify:** 200 en las tres; la lista con 100 enlaces; peso de la lista y de la ficha muy por debajo de 200 KB con gzip; `./scripts/check` en verde.

## Order & risks

- **Execution order:** T1 → T2 → T3.
- **Dependencies:** secuenciales.
- **Risks:** los cuidados son de género y no de especie (dicho en cada dato) → hallazgo para la retrospectiva y para el humano; un JSON con un carácter que rompa el cargador → se valida con `cargar_catalogo` antes de copiar.
