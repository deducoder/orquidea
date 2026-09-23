---
name: design-md-py-que-lee
description: Cómo se regenera governance/identity/ui/DESIGN.md y qué tablas lee design-md.py; no pasarle primitives.md
metadata:
  type: reference
---

`DESIGN.md` (spec google-labs-code/design.md, versión `alpha`) se genera con `design-md.py` del addon, que está en la caché del plugin (`skills/techniques/ui/scripts/`). El comando completo, con sus `--decision` y `--gap`, está en la *Decision* de ADR-014 (s5.6, 2026-09-22). No va en el gate porque depende del plugin: se regenera a mano y se compara con `cmp`.

Lee las tablas por las dos primeras celdas de la cabecera: `Role | Value` (colores), `Step | Size` (escala), `Step | Value` (espaciado) y `Component | {vocabulario}`. **No se le pasa `primitives.md`**, porque su `Step | Value | Ramp` lo leería como espaciado y rechazaría los hex. Tampoco `palette.md` ni `specimen.md`. Solo acepta referencias ASCII, y el vocabulario de componentes no tiene color de borde.

s5.7: la hoja de estilos lee de `governance/identity/ui/DESIGN.md`. Bordes, foco, peso y cifras tabulares están en `colors` o en `specimen.md`, no en `components`. Ver [[rutas-de-entregables-desde-la-convencion]].
