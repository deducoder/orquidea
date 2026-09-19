---
name: aos-genus-care-cards
description: Fuente de cuidados por género de orquídeas (AOS) usada en el catálogo semilla, y trampas al investigar
metadata:
  type: reference
---

Cuidados por género: `https://www.aos.org/explore/{género}` (sección "Care and Culture Card": luz, temperatura, riego, sustrato) y hojas `https://www.aos.org/orchid-care/care-sheets/{género}-culture-sheet`. Popularidad/nativas de Chiapas: API de iNaturalist (lugar 97003, `native=true`, `captive=false`). Kew POWO está detrás de un desafío anti-bots (no eludir).

**Why:** base de las 100 fichas de s1.6; los cuidados son de género, no de especie.
**How to apply:** para ampliar el catálogo (p. ej. más especies), reutilizar estas fuentes y declarar siempre que el dato es del género. Al escribir Markdown con backticks desde la shell, usar `<<'EOF'`.
