---
name: rango-de-epic-review-desde-el-disenio
description: El rango de merge de un epic-review se toma desde el commit previo al diseño de la épica; el brief puede ser anterior a otras épicas
metadata:
  type: feedback
---

Para la revisión a escala de épica, el límite bajo del rango es el commit previo a `chore({epic}): design`, no el del `brief.md`.

**Why:** en e4 el brief se escribió al declarar la versión, antes de que e3 se construyera; usarlo como base metía el código de e3 (1 403 líneas, 735 B101) en la revisión, y el rango correcto eran 12 archivos de aplicación.
**How to apply:** `git log --grep='^chore(eN): design$'` y usar su padre; comprobar con `git diff --stat` que solo aparece lo de la épica.
