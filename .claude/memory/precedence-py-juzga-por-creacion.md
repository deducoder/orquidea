---
name: precedence-py-juzga-por-creacion
description: precedence.py compara el último add/update del ADR con el primer commit de la pieza; eslabón recalculado sale FAIL; celdas medidas se llenan en el commit accept
metadata:
  type: reference
---

`skills/reviews/survival-review/scripts/precedence.py check` toma la fecha del commit que **creó** la pieza (`--diff-filter=A`) y la última edición `add`/`update` de cada ADR del `decision:`. Una pieza de e5 que cita un ADR nuevo (s1: `semantics.md` y `components.md` con ADR-016) sale `FAIL — not before the piece`, aunque el registro preceda a toda tarea de la historia. `DESIGN.md` sale `unreadable` porque el generador no escribe `decision:`.

**How to apply:** en una historia que vuelve a correr eslabones, no quitar el ADR del `decision:` para que pase; leer el orden a mano con `git log --reverse develop..HEAD` y decirlo en el ADR y en la revisión. Está aparcado como hallazgo del addon. Ver [[design-md-py-que-lee]].

**Además (s3, 2026-09-24):** el gate toma como fecha del registro su último commit `add`/`update`; uno `accept` no cuenta. Si las celdas `pending: measured when run` se llenan en el commit que acepta el ADR, y no en un `docs(sN): update ADR-NNN` posterior a la pieza, el veredicto es PASS sin forzarlo (ADR-018: PASS; ADR-017, que usó `update`: FAIL). No es una forma de esquivar el gate: el llenado de celdas medidas no cambia el criterio.
