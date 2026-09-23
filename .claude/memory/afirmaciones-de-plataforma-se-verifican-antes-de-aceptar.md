---
name: afirmaciones-de-plataforma-se-verifican-antes-de-aceptar
description: Lo que trae una plataforma (fuentes del sistema, soportes) es `read:` hasta comprobarlo; verificarlo antes de pasar un ADR a accepted
metadata:
  type: feedback
---

En ADR-010 (s5.2, 2026-09-22) una celda que descartaba la "lámina de herbario" afirmó que "las serif del sistema en Android no dan" itálica real; Noto Serif sí la trae. El veredicto se sostuvo por el otro motivo de la celda, pero la frase quedó en un registro ya `accepted`, que no se reescribe.

**Why:** en una rejilla de juicio las afirmaciones de hecho se cuelan con la confianza de los juicios que las rodean, y al aceptar el ADR quedan inmóviles.

**How to apply:** en una rejilla de ADR, separar lo que es juicio de lo que es un hecho sobre una plataforma o un producto; el hecho se comprueba (o se marca `read: unverified`) mientras el registro sigue en `proposed`. En e5 aplica sobre todo a s5.4 (qué fuentes trae cada sistema). Ver [[mutacion-de-frontera-se-prueba-en-el-predicado]].
