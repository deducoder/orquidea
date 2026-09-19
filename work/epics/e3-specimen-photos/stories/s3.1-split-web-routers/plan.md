# Story s3.1: Split web routers — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · Fijar el mapa de rutas y el orden antes de mover nada

- **Files:** create `tests/test_web_rutas.py`
- **TDD:** RED no aplica a un refactor: la prueba se escribe contra el código de hoy y debe pasar; se prueba que detecta (mutación) antes de mover → GREEN pasa con el código actual → REFACTOR
- **Satisfies:** escenario `@stated` (rutas idénticas) y el del orden de `/coleccion/nuevo`
- **Mold:** `tests/test_web_proteccion.py` (`rutas_de_la_aplicacion`)
- **Verify:** la prueba compara `(método, ruta)` con la lista literal de hoy y el orden de `nuevo` — forced mutations, each of which must turn it red: quitar una ruta (comentar `/salir`); cambiar una ruta de nombre (equivalent form); registrar `/coleccion/{id}` sin sufijo antes de `nuevo`; then `uv run pytest tests/test_web_rutas.py -q` y `./scripts/check`
- **Commit:** test(web): fijar el mapa de rutas y el orden de la colección

### T2 · Dividir en sesión, plantillas y routers

- **Files:** create `web/sesion.py`, `web/plantillas.py`, `web/rutas/__init__.py`, `web/rutas/acceso.py`, `web/rutas/catalogo.py`, `web/rutas/coleccion.py`; modify `web/app.py`, `tests/test_web_acceso.py`, `tests/test_web_proteccion.py`
- **TDD:** RED las pruebas que apuntan a nombres movidos (destino del `monkeypatch`, `RUTAS_PUBLICAS`) se actualizan primero y fallan → GREEN mover el código sin tocar cuerpos → REFACTOR quitar imports sobrantes
- **Satisfies:** todos los escenarios del scope
- **Mold:** `orquidea.datos` y `orquidea.catalogo` (paquetes por área)
- **Verify:** el mapa de rutas de T1 y la suite completa siguen en verde con `app.py` sin rutas salvo `/salud` — forced mutations: no incluir un router (T1 debe fallar); quitar `dependencies=[Depends(exigir_sesion)]` (`test_web_proteccion` debe fallar); apuntar el `monkeypatch` al módulo viejo (la prueba de concurrencia de acceso debe fallar); then `./scripts/check` completo (archivos nuevos escaneados por el gate)
- **Commit:** refactor(web): dividir app.py en sesión, plantillas y routers por área

### T3 · Manual integration test

- Arrancar `uvicorn orquidea.web.app:app` con una base temporal, iniciar sesión con un hash real y recorrer inicio, catálogo, agregar, editar y quitar con `curl`.
- **Verify:** las respuestas coinciden con las de `develop` (mismos códigos y redirecciones) y `/coleccion/nuevo` responde 200.

## Order & risks

- **Execution order:** T1 → T2 → T3 — el mapa se fija antes de mover para que la división se pruebe contra el estado anterior.
- **Dependencies:** secuencial.
- **Risks:** un import circular entre `sesion`, `plantillas` y los routers → ninguno importa a `app.py`; la aplicación es lo único que los junta.
