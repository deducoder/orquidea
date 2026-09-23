---
name: revisar-promociones-del-parking-lot-al-disenar
description: En story-design, buscar en el parking lot las entradas cuya promoción se cumple con esta historia (archivos o áreas que toca), no descubrirlas en el cierre
metadata:
  type: feedback
---

Al diseñar una historia, leer las promociones de `records/parking-lot.md` contra lo que la historia va a tocar: rutas (`governance/identity/ui/`), scripts nuevos ("un cuarto script que lea tablas"), momentos ("la siguiente historia que…"). Las que se cumplen entran al scope o se dicen fuera de él con su razón.

**Why:** en s1 (2026-09-23) dos promociones se cumplían con la propia historia y aparecieron recién en T7; una costó un re-plan (T9) y la otra quedó para una historia aparte sin haberse decidido en el diseño.
**How to apply:** `grep -n "Promotion" records/parking-lot.md` en la visita al código de `story-design`, y una línea por entrada que se cumple en `design.md`. Ver [[survival-review-es-tarea-del-plan]].
