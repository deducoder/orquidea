# Story s1.3: Species sheet — Plan

> Size: M
> Pause: none (default)

## Tasks

### T1 · Lista de especies

- **Files:** modify `src/orquidea/web/app.py`, `src/orquidea/web/templates/inicio.html`; create `src/orquidea/web/templates/especies.html`, `tests/test_web_especies.py`
- **TDD:** RED pruebas: lista con dos especies muestra nombre y enlace; catálogo vacío muestra el mensaje con 200; nombre con HTML sale escapado → GREEN carga en `app.state.catalogo` y ruta `/especies` → REFACTOR
- **Satisfies:** scenario 1, y los deducidos de vacío y escape
- **Mold:** none
- **Verify:** afirma el enlace `/especies/{id}`, el mensaje de vacío y la ausencia de la etiqueta cruda; mutaciones que lo ponen en rojo: quitar el enlace; renderizar con `|safe`; cargar el catálogo dentro de la ruta a partir de un directorio distinto; luego `./scripts/check` completo (archivos nuevos)
- **Commit:** feat(web): lista de especies del catálogo

### T2 · Ficha de especie con la fuente de cada cuidado

- **Files:** modify `src/orquidea/web/app.py`; create `src/orquidea/web/templates/especie.html`; modify `tests/test_web_especies.py`
- **TDD:** RED pruebas: la ficha contiene nombre, nombres comunes, descripción, los cuatro cuidados con su fuente y las fuentes; id inexistente da 404 → GREEN ruta `/especies/{id}` y plantilla → REFACTOR
- **Satisfies:** scenarios 2 a 4 del scope
- **Mold:** T1
- **Verify:** una fuente distinta por cuidado en la fixture (mutación: renderizar la misma fuente en todos, o quitar `Fuente:` de un cuidado, pone en rojo); 404 verificado (mutación: devolver 200 con ficha vacía); luego `./scripts/check`
- **Commit:** feat(web): ficha de especie con la fuente de cada cuidado

### T3 · El catálogo inválido detiene el arranque

- **Files:** modify `tests/test_web_especies.py`
- **TDD:** RED prueba que recarga el módulo `orquidea.web.app` con `DIRECTORIO_CATALOGO` apuntando a un directorio con JSON inválido y espera `CatalogoInvalido` → GREEN ya debería pasar por T1; si pasa de inmediato, se demuestra su valor con la mutación (capturar el error en la carga) → REFACTOR
- **Satisfies:** el delta del diseño
- **Mold:** none
- **Verify:** mutación: envolver la carga en `try/except CatalogoInvalido` y seguir con lista vacía pone en rojo la prueba; luego `./scripts/check`
- **Commit:** test(web): el catálogo inválido detiene el arranque

### T4 · Manual integration test

- Arrancar la aplicación con `uvicorn` ad hoc sobre un directorio de catálogo con una especie (variable temporal apuntando a un directorio de prueba) y pedir `/especies` y la ficha con `curl`; con el catálogo real (vacío) pedir `/especies`.
- **Verify:** la ficha muestra cuidados con fuente; `/especies` con el catálogo real responde 200 con el mensaje de vacío; `./scripts/check` en verde.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 — la lista fija cómo se carga y se prueba el catálogo; la ficha se apoya en ello.
- **Dependencies:** secuenciales.
- **Risks:** recargar el módulo en T3 puede dejar `app` duplicado para otras pruebas → la prueba restaura el módulo; el arranque para la prueba manual necesita apuntar a otro directorio → se hace con un enlace temporal o con una variable de entorno solo si hace falta; si no, se prueba con un script que asigne `app.state.catalogo`.
