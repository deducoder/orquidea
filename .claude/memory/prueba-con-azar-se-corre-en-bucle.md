---
name: prueba-con-azar-se-corre-en-bucle
description: "Una prueba que depende de valores aleatorios o de hilos se corre en bucle antes de commitear; y el gate se encadena al commit"
metadata:
  type: feedback
---

Antes de commitear una prueba que usa nombres aleatorios (`token_urlsafe`) o hilos, correrla 10-15 veces. Y encadenar siempre `./scripts/check && git commit`, sin leer solo la cola de la salida. Desde 2026-09-22 el hook `pre-commit` de Gemba corre el gate en cada commit de orquidea, así que encadenarlo a mano es redundante aquí, pero sigue valiendo donde los hooks no estén cableados (un clon nuevo).

**Why:** en s3.3 de orquidea una prueba que comprobaba que el dígito del id no aparecía en un nombre aleatorio falló 6 de 8 corridas, y dos commits salieron con el gate en rojo porque el código de salida no se encadenó.
**How to apply:** `for i in $(seq 15); do pytest -q archivo; done | sort | uniq -c`; para carreras, ensanchar la ventana (`sleep` en el paso intermedio) y comprobar que quitar el cerrojo pone rojo. Ver [[mutation-checks-stale-bytecode]].
