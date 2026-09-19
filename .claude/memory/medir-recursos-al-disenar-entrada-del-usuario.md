---
name: medir-recursos-al-disenar-entrada-del-usuario
description: "En historias que procesan entrada del usuario (imágenes, archivos) medir memoria, tiempo y peso con el tamaño máximo permitido desde el diseño, no en el epic-review"
metadata:
  type: feedback
---

Medir el pico de memoria y el tiempo del procesamiento con la entrada del tamaño máximo permitido (proceso aparte, bytes por stdin), y el peso de lo que se sirve, al diseñar la historia.

**Why:** en e3 de orquidea el pico de ~1 GB de `procesar_foto` con una foto de 48 MP apareció recién en el `epic-review` (s3.2 pasó todas sus pruebas), y el peso de las miniaturas en s3.6.
**How to apply:** una prueba con `subprocess` que mide `ru_maxrss` con topes ~30 % sobre lo medido, y una prueba de presupuesto de peso en el gate. Ver [[prueba-con-azar-se-corre-en-bucle]] y [[fastapi-cuerpo-excedido-por-senal]].
