# Story s1.1: Web skeleton — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · Página de inicio desde la plantilla base

- **Files:** modify `pyproject.toml`, `uv.lock` (fastapi, jinja2; dev: httpx); create `src/orquidea/web/__init__.py`, `src/orquidea/web/app.py`, `src/orquidea/web/templates/base.html`, `src/orquidea/web/templates/inicio.html`, `tests/test_web_inicio.py`
- **TDD:** RED `test_inicio_responde_html` (GET / → 200, text/html, contiene `<title>Orquídea`) falla por import → GREEN `app` con la ruta y las plantillas mínimas → REFACTOR título como bloque sobrescribible
- **Satisfies:** scenario 1 del scope (GET / → 200 HTML desde la base)
- **Mold:** none
- **Verify:** el test afirma estado 200, tipo `text/html` y el título; mutaciones que lo ponen en rojo: devolver 404 quitando la ruta; devolver texto plano en vez de HTML; quitar la plantilla `inicio.html`; luego `uv run pytest tests/test_web_inicio.py` y `./scripts/check` completo (archivo nuevo que el gate escanea)
- **Commit:** feat(web): página de inicio desde la plantilla base

### T2 · htmx servido localmente y sin recursos externos

- **Files:** create `src/orquidea/web/static/htmx.min.js`; modify `src/orquidea/web/app.py` (monta `/static`), `src/orquidea/web/templates/base.html` (script), `tests/test_web_inicio.py`
- **TDD:** RED `test_htmx_se_sirve_localmente` (GET /static/htmx.min.js → 200) y `test_sin_recursos_externos` (ningún `src=`/`href=` con `http(s)://` en el HTML de /) fallan → GREEN montar StaticFiles, descargar htmx 2.x y referenciarlo → REFACTOR ninguno previsto
- **Satisfies:** scenario 2 del scope y los deducidos (sin externos, delta de htmx estático)
- **Mold:** T1
- **Verify:** afirma que el HTML referencia `/static/htmx.min.js` y que ese path devuelve 200 con contenido no vacío; mutaciones: referenciar htmx en un CDN (debe fallar `test_sin_recursos_externos`); borrar el archivo (debe fallar el 200); quitar el `<script>` de la base; luego `./scripts/check` completo
- **Commit:** feat(web): sirve htmx desde archivo estático propio

### T3 · Manual integration test

- Arrancar la aplicación con un servidor real (`uv run --with uvicorn uvicorn orquidea.web.app:app`, sin agregar uvicorn al proyecto) y pedir `/` y `/static/htmx.min.js` con `curl`.
- **Verify:** ambos responden 200, el HTML trae "Orquídea" y el script de htmx; `./scripts/check` en verde en el checkout limpio.

## Order & risks

- **Execution order:** T1 → T2 → T3 — T1 fija el stack y las dependencias (lo más incierto: resolver e instalar); T2 se apoya en la app.
- **Dependencies:** secuenciales, acíclicas.
- **Risks:** el plugin `uv_build` puede no empaquetar `templates/` y `static/` → basta para las pruebas (corren desde el árbol) y se revisa en s1.5 al desplegar; el descargar htmx requiere red → disponible en esta sesión; si fallara, P5.
