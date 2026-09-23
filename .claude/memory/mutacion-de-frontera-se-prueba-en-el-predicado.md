---
name: mutacion-de-frontera-se-prueba-en-el-predicado
description: "`>=`→`>` sobrevive si ninguna entrada real cae justo en el umbral; probar el predicado con el valor exacto, y no predecir mutaciones sin correrlas"
metadata:
  type: feedback
---

Una mutación de frontera (`>=`→`>`, `<`→`<=`) sobrevive cuando ninguna entrada realista cae exactamente en el umbral: en s5.1 (2026-09-22) el plan daba por hecho que `#595959` sobre blanco "da 7.00:1" y rompería `>` en lugar de `>=`; da 7.0047 y la mutación sobrevivió. Ningún gris de 8 bits da 7:1 exacto.

**Why:** el plan predijo el efecto de una mutación sin correrla; la cifra redondeada a dos decimales ocultaba que no era la frontera.

**How to apply:** sacar la comparación con el umbral a un predicado (`llega_al_umbral(r)`) y probarlo con el valor exacto y uno apenas debajo; en el plan, escribir la mutación y la propiedad, pero no su resultado hasta haberla corrido. Ver [[mutation-checks-stale-bytecode]].

Reincidencia en s5.4 (mismo día): el contraejemplo de T2 en ADR-011 se escribió con la salida esperada de `fontTools` antes de correrlo; se corrió y se reemplazó con el ADR aún en `proposed`. La regla no es solo para mutaciones: **ninguna salida de comando se escribe en un registro antes de haberla visto.**
