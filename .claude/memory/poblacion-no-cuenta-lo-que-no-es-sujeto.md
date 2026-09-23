---
name: poblacion-no-cuenta-lo-que-no-es-sujeto
description: Una comprobación que "cuenta su población" da verde falso si cuenta archivos que no son sujeto (`.gitkeep`)
metadata:
  type: feedback
---

"Sin población es rojo" no basta: la población tiene que ser del sujeto. En s5.1 (2026-09-22) `medir-primera-carga.py --identidad` contaba `.gitkeep` como recurso de la identidad y salía OK con "1 archivo(s), 0.0 KB" sin haber medido nada; lo encontró `quality-review`, no las mutaciones del plan.

**Why:** la forma habitual de commitear un directorio vacío es un archivo oculto, justo antes de que exista lo que se va a medir.

**How to apply:** al diseñar una comprobación que cuenta su población, preguntar qué más puede vivir donde se busca el sujeto (ocultos, cachés, archivos de relleno) y agregar esa mutación — "un sujeto falso presente" — junto a "el sujeto quitado". Ver [[afirmar-presencia-no-ve-el-lugar]].
