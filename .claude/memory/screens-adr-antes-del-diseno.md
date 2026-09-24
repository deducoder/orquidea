---
name: screens-adr-antes-del-diseno
description: con la técnica screens, el ADR se abre antes de story-design, porque el recorrido del diseño es la lectura del inventario
metadata:
  type: feedback
---

En una historia que corre `screens` (gemba-design), el registro se commitea en `proposed` **antes** de `story-design`, no como primera tarea del plan como hizo s1 con ADR-016. El recorrido del diseño (modelos, rutas, plantillas) es la lectura del inventario, y la técnica exige el registro antes de la primera entrada leída.

**Why:** s2 (2026-09-24) lo hizo así: ADR-017 en `50e5a26`, su rojo en `e3c1be3` y después el diseño. Con el orden de s1, el diseño habría leído el inventario sin criterio.
**How to apply:** en historias de `screens`, el orden es initialize → ADR `proposed` → rojo → diseño → plan. Ver [[parametros-de-regla-con-valor-al-abrir]].
