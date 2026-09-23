---
name: session-pointer
description: "Last session handoff for Orquídea — date, next action, and handoff path"
metadata:
  node_type: memory
  type: project
  modified: 2026-09-23
---

Last session: **2026-09-23**. La historia standalone s1 llevó la identidad al vocabulario de gemba-design 0.23.0 (ADR-016) y quedó cerrada y publicada en `origin/develop` (`d6260ff`).

Full handoff: `work/sessions/2026-09-23-s1-ui-vocabulary.md` (read it in full via
`session-start`).

Next action: **Quitar `'unsafe-inline'` de la CSP**: primero comprobar que htmx no inyecte estilos en línea, luego la prueba de la CSP (`src/orquidea/web/app.py:46`, `tests/test_web_proteccion.py:225`).

El refactor de los lectores de tablas tiene la promoción cumplida en el parking lot y espera su propia historia.

Overwritten on every `session-close`; this is a pointer, the handoff is the
source of truth.
