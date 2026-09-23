---
name: cifras-de-retrospectiva-de-la-salida-del-comando
description: Toda cifra de una retrospectiva (pruebas, KB, minutos) se copia de la salida de un comando ya corrido, no de memoria ni de la suma mental
metadata:
  type: feedback
---

Al escribir una retrospectiva, cada número (pruebas que pasan, pesos, tiempos) sale de la salida de un comando corrido en ese momento; si no se corrió, se corre antes de escribirlo.

**Why:** en e4 de orquidea escribí «399 pruebas» (eran 406) en s4.2 y «467» (eran 476) en s4.4 sin haberlas contado, y las corregí en un commit aparte después de verificarlas.
**How to apply:** `uv run pytest -q | tail -1` justo antes de escribir la línea de verificación; para pesos, pegar la salida del script. Ver [[prueba-con-azar-se-corre-en-bucle]] para el gate encadenado.

Lo mismo para el `Swept:` de una entrada retirada del parking lot y para toda referencia a otro archivo en un ADR: en s1 escribí un barrido sin `grep` y una ruta de comando que no existía, y costaron tres commits de corrección.
