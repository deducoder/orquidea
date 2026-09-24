# Story s5: Compose species list — Plan

| # | Tarea | Verificación | Commit |
|---|-------|--------------|--------|
| T1 | `Font weight` en `type-scale.md` y `DESIGN.md` regenerado (dos corridas idénticas) | `page.py` sobre el candidato A sin rechazos de `fontWeight`; `./scripts/check` | `docs(identity): declare the weight of each type step` |
| T2 | Medir los dos candidatos (`page.py` y K1) y llenar las celdas medidas de ADR-020 antes de producir la composición | exit 0 en los dos | `docs(s5): update ADR-020` |
| T3 | Juicio del dueño sobre las dos páginas: pregunta 1 por candidato, elección contra S1–S3 y foco al tabular; `composition-s1.md` y su página con el elegido | `page.py` exit 0; K1 exit 0 | `docs(identity): compose the species screen` |
| T4 | ADR-020 `accepted` con los juicios | ninguna celda pendiente | `docs(s5): accept ADR-020` |
| T5 | `survival-review` de la página y de la escala | censo copiado; `precedence` leído | en `chore(s5): review` |
