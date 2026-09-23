---
name: redondeo-medio-hacia-arriba-no-es-round
description: round() de Python redondea al par; "medio hacia arriba" es floor(x + 0.5), y la prueba necesita un .5 con parte entera par
metadata:
  type: feedback
---

En s5.6 (2026-09-22), `derivar-medidas.py` declara "medio hacia arriba" para tamaños y alturas de línea. La mutación que cambiaba `floor(x + 0.5)` por `round()` sobrevivió a ocho casos de prueba, porque en todos el .5 caía sobre una parte entera impar (7.5 → 8 con los dos métodos). Hizo falta el caso 12 px → 1.5·12/4 = 4.5, donde `round` da 4 y medio hacia arriba da 5.

**Why:** `round` usa redondeo bancario. Una prueba con x.5 impar no distingue las dos reglas, y la mutación pasa en verde.

**How to apply:** cuando una regla declare un redondeo, la prueba lleva un caso con .5 y parte entera **par**. En s5.7 aplica a cualquier medida que se calcule. Ver [[mutacion-de-frontera-se-prueba-en-el-predicado]].
