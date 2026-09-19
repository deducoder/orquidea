---
name: ids-coincidentes-ocultan-cruces-en-pruebas-idor
description: En pruebas de rutas con dos ids (ejemplar y registro), desfasar los ids con datos señuelo; si coinciden, una ruta que los cruza pasa todas las pruebas
metadata:
  type: feedback
---

Al probar rutas del tipo `/coleccion/{id}/floraciones/{floracion}/fin`, crear antes registros señuelo para que el id del registro no coincida con el del ejemplar (1 y 1 en una base recién creada).

**Why:** en s4.4 (e4) las mutaciones «pasar `floracion` en los dos argumentos de id» sobrevivieron a las pruebas de camino feliz y de IDOR porque el ejemplar 1 y su primera floración 1 coincidían; con cinco floraciones señuelo (ids desfasados) las mismas mutaciones fallaron.
**How to apply:** una función auxiliar `_desfasar_los_ids()` al inicio de las pruebas de éxito y de 404 por ajeno; y correr siempre la mutación de argumentos cruzados. Ver [[tope-atomico-en-un-insert-select]] y [[mutation-checks-stale-bytecode]].
