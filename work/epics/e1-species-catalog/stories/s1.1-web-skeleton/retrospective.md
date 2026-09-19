# Story s1.1: Web skeleton — Retrospective

Estimated: S · Actual: 3 tareas, una sesión (sin tracker, sin tiempo registrado)

## Summary

Aplicación FastAPI mínima en `orquidea.web.app`: `GET /` renderiza `inicio.html` sobre `base.html` (bloques `title` y `content`), htmx 2.0.4 servido desde `/static` (50.9 KB, 16.4 KB gzip), tres pruebas. Verificada además con un servidor real (`uvicorn` ad hoc): `/` 200 `text/html` y `/static/htmx.min.js` 200.

## Acceptance

- Criterios `[stated]` (GET / → 200 HTML desde la base; la base carga htmx): confirmados por `test_inicio_responde_html` y `test_htmx_se_sirve_localmente`.
- `[deduced]` sin recursos externos: confirmado por el diseño y por `test_sin_recursos_externos` (mutación: script apuntando a un CDN pone dos pruebas en rojo). `./scripts/check` en verde: confirmado. Ninguno retractado.
- Finalize: `./scripts/check` verde (ruff, format, mypy strict, 3 pruebas); tests huérfanos: ninguno (no existían otros archivos de prueba); sin tracker, sin registro de tiempo.

## Reviews

- **quality-review — PASS.** Archivos leídos: `app.py`, `base.html`, `inicio.html`, `test_web_inicio.py`. Sin tipos deshonestos ni excepciones tragadas; las tres pruebas afirman comportamiento y fallaron bajo mutación.
- **security-review — PASS WITH FINDINGS.** Bandit 1.9.4 sobre `app.py`, `web/__init__.py` y `tests/test_web_inicio.py` (los tres, igual que la lista esperada): solo 7 × B101 (severidad baja) en las pruebas, ya ignorado por ruff en `tests/`; ninguno en código de aplicación. Estacionado en `records/parking-lot.md` ("Bandit reporta B101 en `tests/`"). Guardrails: `must-security-001` (EXIF) y `should-security-002` (ASVS L2, disparado por el inicio de sesión) no aplican todavía: la historia no tiene fotos ni sesión.

## What went well

Los tests-guardia vacuos (sin recursos externos) se validaron con una mutación real, no solo pasando en verde. El RED de T1 fue por import, el de T2 por comportamiento.

## What to improve

`test_sin_recursos_externos` pasó en verde en su RED porque protege algo que aún no existía; solo la mutación demostró que ve el defecto. Para tests-guardia, la mutación es parte de la verificación, no un extra.

## Learned

1. About the system: starlette 1.6 declara `httpx` obsoleto para `TestClient`; el paquete a usar es `httpx2` (elimina la advertencia de deprecación).
2. About the process: el id local de una historia bajo una épica sin tracker es `s{N}.{M}`, no `e{N}.{M}`; se corrigió en los artefactos de la épica tras detectarlo en `story-start`.
3. Capability gained: base web (FastAPI + Jinja + htmx estático) sobre la que s1.3 y s1.4 montan rutas. Pendiente para s1.5: comprobar que `uv_build` empaqueta `templates/` y `static/`.
