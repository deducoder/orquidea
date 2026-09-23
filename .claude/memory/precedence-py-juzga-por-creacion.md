---
name: precedence-py-juzga-por-creacion
description: precedence.py de gemba-design 0.23.0 compara el registro con el primer commit de la pieza; un eslabón ui que se vuelve a correr siempre sale FAIL
metadata:
  type: reference
---

`skills/reviews/survival-review/scripts/precedence.py check` toma la fecha del commit que **creó** la pieza (`--diff-filter=A`) y la última edición `add`/`update` de cada ADR del `decision:`. Una pieza de e5 que cita un ADR nuevo (s1: `semantics.md` y `components.md` con ADR-016) sale `FAIL — not before the piece`, aunque el registro preceda a toda tarea de la historia. `DESIGN.md` sale `unreadable` porque el generador no escribe `decision:`.

**How to apply:** en una historia que vuelve a correr eslabones, no quitar el ADR del `decision:` para que pase; leer el orden a mano con `git log --reverse develop..HEAD` y decirlo en el ADR y en la revisión. Está aparcado como hallazgo del addon. Ver [[design-md-py-que-lee]].
