# Story s1.2: Catalog schema and loader — Plan

> Size: M
> Pause: none (default)

## Tasks

### T1 · Modelo de especie con fuente obligatoria

- **Files:** modify `pyproject.toml`, `uv.lock` (pydantic); create `src/orquidea/catalogo/__init__.py`, `src/orquidea/catalogo/modelo.py`, `tests/test_catalogo_modelo.py`
- **TDD:** RED pruebas: una especie completa valida; sin `fuentes`, con `fuentes=[]`, con un `Cuidado` sin `fuente`, con campo desconocido y con `id` no-slug lanzan `ValidationError` → GREEN modelos pydantic con `extra="forbid"` y restricciones → REFACTOR
- **Satisfies:** scenarios 1 a 3 del scope (a nivel de modelo)
- **Mold:** none
- **Verify:** cada prueba de rechazo pone en rojo si se relaja la restricción: `min_length=1` de `fuentes` quitado; `extra="forbid"` quitado; `fuente` de `Cuidado` con valor por defecto `""`; el patrón del `id` quitado; luego `uv run pytest tests/test_catalogo_modelo.py` y `./scripts/check` completo (archivos nuevos)
- **Commit:** feat(catalogo): modelo de especie con fuente obligatoria

### T2 · Carga de un directorio, todo o nada, con archivo y campo

- **Files:** create `src/orquidea/datos/__init__.py`, `src/orquidea/datos/catalogo.py`, `src/orquidea/datos/catalogo/.gitkeep`, `tests/test_catalogo_carga.py`
- **TDD:** RED pruebas con `tmp_path`: válido → lista ordenada por id; sin `fuentes` → error `x.json: fuentes: ...`; campo anidado → `cuidados.riego.fuente`; JSON roto → nombra el archivo; válido + inválido → excepción, sin lista; varios errores → todos reunidos; directorio vacío → `[]` → GREEN `cargar_catalogo` y `CatalogoInvalido` → REFACTOR
- **Satisfies:** scenarios 1 a 5 del scope y los deltas del diseño
- **Mold:** T1
- **Verify:** los errores contienen el nombre del archivo y la ruta del campo (mutaciones: omitir el nombre del archivo del mensaje; devolver las especies válidas ignorando la inválida; capturar y saltar el JSON roto con `except`; devolver solo el primer error); luego pruebas del archivo y `./scripts/check` completo
- **Commit:** feat(datos): carga del catálogo desde JSON, todo o nada

### T3 · Ids duplicadas y directorio inexistente

- **Files:** modify `src/orquidea/datos/catalogo.py`, `tests/test_catalogo_carga.py`
- **TDD:** RED dos archivos con la misma `id` → error que nombra ambos; directorio inexistente → `CatalogoInvalido` nombrando el directorio → GREEN comprobaciones → REFACTOR
- **Satisfies:** scenario 6 del scope y el delta del diseño
- **Mold:** T2
- **Verify:** quitar la comprobación de duplicadas pone en rojo la prueba; `Path.iterdir` sobre directorio inexistente sin capturar debe dar `FileNotFoundError` en vez de `CatalogoInvalido` (rojo); luego `./scripts/check`
- **Commit:** feat(datos): rechaza ids duplicadas y directorio inexistente

### T4 · Manual integration test

- Con un directorio real de dos JSON (uno válido, uno sin fuentes) ejecutar `uv run python -c` que llame `cargar_catalogo` y muestre el resultado y el mensaje de error.
- **Verify:** el error nombra el archivo y `fuentes`; con solo el válido se carga la lista; `./scripts/check` en verde.

## Order & risks

- **Execution order:** T1 → T2 → T3 — el modelo es el contrato; la carga lo usa; los casos extremos al final.
- **Dependencies:** secuenciales, acíclicas.
- **Risks:** el mapeo de `loc` de pydantic a "campo.anidado" puede no ser obvio en listas (p. ej. `fuentes.0`) → se prueba con un elemento vacío en la lista de fuentes; el directorio `datos/catalogo/` solo con `.gitkeep` debe seguir cargando como `[]`.
