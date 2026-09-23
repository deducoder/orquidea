---
name: excepcion-sin-capturar-sale-con-1
description: En los scripts 0/1/2 del proyecto, una excepción sin capturar sale con 1 y se lee como "falla el criterio"; cada entrada ilegible debe salir con 2
metadata:
  type: feedback
---

En s5.6 (2026-09-22), la revisión de calidad encontró que `comprobar-medidas.py` con una fila corta (`| boton | 48 |`) reventaba con `IndexError`. Python salía con 1, el mismo código que "un control bajo el mínimo". Se corrigió en `9da6948` validando el largo de la fila y saliendo con 2.

**Why:** el contrato 0/1/2 de los instrumentos (`contraste-de-lectura.py`, `derivar-*`, `comprobar-medidas.py`, `tokens.py`) separa el rojo del criterio de "nada juzgado". Un traceback se hace pasar por el primero.

**How to apply:** al escribir o revisar un script con ese contrato, alimentarlo con una fila corta, una celda vacía y un archivo sin la tabla, y comprobar que sale con 2, no con 1 ni con un traceback. Ver [[poblacion-no-cuenta-lo-que-no-es-sujeto]].
