# Story s1.5: VPS deployment — Plan

> Size: M
> Pause: none (default)

## Tasks

### T1 · Endpoint de salud y uvicorn

- **Files:** modify `src/orquidea/web/app.py`, `tests/test_web_inicio.py`, `pyproject.toml`, `uv.lock` (uvicorn)
- **TDD:** RED prueba: GET `/salud` responde 200 y `{"estado": "ok"}`, y responde igual con `app.state.catalogo` vacío → GREEN la ruta → REFACTOR
- **Satisfies:** el escenario deducido de `/salud`
- **Mold:** none
- **Verify:** afirma estado 200 y cuerpo exacto; mutaciones: quitar la ruta; devolver 200 con otro cuerpo; leer el catálogo en la ruta (con catálogo vacío debe seguir en 200); luego `./scripts/check` completo
- **Commit:** feat(web): endpoint de salud para el healthcheck

### T2 · Dockerfile, .dockerignore y guía de Dokploy

- **Files:** create `Dockerfile`, `.dockerignore`; modify `README.md`
- **TDD:** artefacto de configuración sin comportamiento de código que se pruebe con una prueba unitaria; se verifica en T3 (excepción explícita a TDD para este archivo; sin Docker local no se puede construir)
- **Satisfies:** escenario 1 del scope (a nivel de repositorio) y el delta del diseño
- **Mold:** none
- **Verify:** `./scripts/check` sigue en verde y `git ls-files` no incluye `.venv` ni `work/` en el contexto (`.dockerignore` los excluye); el resto en T3
- **Commit:** build(docker): Dockerfile y guía de despliegue en Dokploy

### T3 · Manual integration test

- `uv build` → inspeccionar el wheel (plantillas, htmx, 100 JSON) → instalarlo en un entorno limpio fuera del repositorio → arrancar `uvicorn` allí → `curl` a `/salud`, `/especies` (100 enlaces), una ficha y `/static/htmx.min.js`.
- **Verify:** todos 200; 100 enlaces; el proceso corre sin el árbol `src/`. Dejar dicho que `docker build` no se ejecutó.

## Order & risks

- **Execution order:** T1 → T2 → T3.
- **Dependencies:** secuenciales.
- **Risks:** `uv_build` puede no empaquetar los datos → se detecta en T3 y se corrige con la configuración del backend antes de cerrar; el Dockerfile no se puede construir aquí → el humano lo verá en Dokploy y la guía lo dice; versión de `uv` fijada a la instalada (0.12.7), a comprobar en el primer build.
