---
name: pillow-guarda-comentario-jpeg
description: "Pillow copia el comentario JPEG de Image.info al guardar; para quitar metadatos hay que reconstruir la imagen desde los bytes de sus píxeles"
metadata:
  type: project
---

Al guardar un JPEG, Pillow toma el `comment` de `Image.info` aunque no se pase a `save()`; `copy()`, `resize()` y `thumbnail()` conservan `info`. Quitar `exif`/`icc_profile` de los argumentos no basta.

**Why:** descubierto en s3.2 de orquidea (`must-security-001`): la prueba que buscaba los bytes del comentario en la salida falló aunque `getexif()` salía vacío. Una prueba que solo mira la API de EXIF no ve XMP ni comentarios.
**How to apply:** reconstruir con `Image.frombytes(modo, tamaño, imagen.tobytes())` antes de guardar y probar la ausencia de metadatos buscando los bytes en la salida (`Exif`, `ns.adobe.com/xap`, el comentario, `ICC_PROFILE`). Ver [[mutation-checks-stale-bytecode]] para las mutaciones.
