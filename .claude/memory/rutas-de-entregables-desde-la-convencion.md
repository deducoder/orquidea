---
name: rutas-de-entregables-desde-la-convencion
description: Las piezas de interfaz de gemba-design van en governance/identity/ui/; leer conventions/deliverables antes de escribir una ruta en scope o diseño
metadata:
  type: feedback
---

En s5.5 (2026-09-22) el scope y el diseño decían `governance/identity/primitives.md`. La convención `deliverables` del addon pone las piezas de interfaz (`primitives`, `semantics`, `type-scale`, `spacing`, `components` y el `DESIGN.md` generado) un nivel más abajo, en `governance/identity/ui/`. Se vio al producir y se corrigió ahí.

**Why:** la ruta la fija la convención, no la técnica, y ninguna plantilla la repite. Copiarla de la historia anterior (`palette.md` va en la raíz) dio la ruta equivocada.

**How to apply:** en s5.6 y s5.7, `type-scale.md`, `spacing.md`, `components.md` y `DESIGN.md` van en `governance/identity/ui/`, y la hoja de s5.7 lee de ahí. Antes de escribir una ruta en un scope, leer `conventions/deliverables/convention.md` del addon. Ver [[regla-con-respaldo-no-se-ve-en-rojo]].
