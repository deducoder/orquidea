# Story s3.4: Specimen sheet with photo — Design

> Complexity: complex

## 1 · What & why

**Problem:** hay funciones para procesar y guardar fotos, pero ninguna ruta las usa, y no existe una ficha del ejemplar donde mostrarlas.
**Value:** el usuario sube y ve la foto de su ejemplar por HTTP y la métrica líder del brief queda demostrada de punta a punta.

## 2 · Approach

Cuatro rutas nuevas en el router de la colección (`GET /coleccion/{id}`, `POST /coleccion/{id}/foto`, `GET /coleccion/{id}/foto` y `.../foto/miniatura`) y un middleware ASGI mínimo que limita el cuerpo. La ficha es una plantilla nueva; la subida reutiliza `procesar_foto` y `poner_foto`; las imágenes salen con `FileResponse` desde una ruta formada solo con el nombre guardado (ADR-006). Todo nace protegido por la dependencia global.

**Components affected:**

- `orquidea/web/limite.py`: create — `LimiteDeCuerpo` (ASGI): 413 si `Content-Length` excede o si los bytes recibidos exceden, también sin cabecera.
- `orquidea/web/app.py`: modify — `app.add_middleware(LimiteDeCuerpo, maximo=...)`.
- `orquidea/web/rutas/coleccion.py`: modify — la ficha, la subida y el servicio de imágenes.
- `orquidea/web/templates/ejemplar_ficha.html`: create; `coleccion.html`: modify (enlace "Ficha").
- `tests/test_web_fotos.py`, `tests/test_web_limite.py`: create.

**Legacy sweep:** nothing — net-new (el enlace "Ficha" se añade junto a "Editar" y "Quitar"). `test_web_rutas.py` se actualiza con las cuatro rutas nuevas y su prueba de orden deja de ser vacía. Orphaned tests: `test_web_proteccion.py` enumera las rutas y recorre las nuevas sin cambios; `test_web_coleccion.py` prueba el HTML de la lista (una aserción sobre el enlace nuevo no rompe las existentes).

## 3 · Interface / examples

```
GET  /coleccion/1                 -> 200 ficha: nombre, especie, notas, <img src="/coleccion/1/foto"> si hay foto, formulario
POST /coleccion/1/foto            multipart: csrf=<token>, foto=<archivo>   -> 303 /coleccion/1
GET  /coleccion/1/foto            -> 200 image/jpeg (≤ 1600 px)
GET  /coleccion/1/foto/miniatura  -> 200 image/jpeg (≤ 320 px)
```

```
POST sin csrf                      -> 403 (exigir_sesion)
POST sin archivo elegido           -> 422 "Elige una foto."
POST nota.txt                      -> 422 "El archivo no es una imagen válida."
POST gif                           -> 422 "Solo se admiten fotos JPEG, PNG o WebP."
POST > 11 MiB                      -> 413 (el cuerpo no se procesa)
GET  /coleccion/1/foto sin foto    -> 404
GET  /coleccion/1/foto con la fila apuntando a un archivo borrado -> 404 (no 500)
disco lleno al guardar             -> 500 controlado: ficha 500 "No se pudo guardar la foto."
```

```python
LIMITE_DE_CUERPO = TAMANO_MAXIMO + 1024 * 1024  # foto máxima más el resto del formulario
```

## 4 · Acceptance criteria

**Must:**

- Métrica líder por HTTP: una foto 4000x3000 con GPS sube y el archivo guardado mide 1600 px y no contiene `Exif`, XMP ni el GPS.
- Sin sesión, ficha, imagen y subida redirigen al acceso (o 401 con htmx); sin CSRF, 403 y nada se guarda.
- Todo rechazo (no imagen, formato, tamaño, sin archivo) deja la base y el directorio como estaban.
- El cuerpo excedido responde 413 antes de decodificar, con `Content-Length` y sin él.
- La ruta de la imagen se forma solo con el nombre guardado; un nombre inválido en la base da 404, no una lectura fuera del directorio.

**Should:** la ficha lleva `alt` con el nombre del ejemplar; los errores se muestran con `role="alert"` como el resto de la app.

**Must NOT:** servir el directorio como estático; usar el nombre del archivo subido; dejar escapar un 500 por `FotoInvalida`; cachear la foto en el navegador (`no-store` del middleware se mantiene).

### ASVS L2 recorrido al diseñar (subida y entrega de archivos)

- V12.1.1 tamaño: cubierto en dos capas — `LimiteDeCuerpo` (413, cuerpo entero) y `TAMANO_MAXIMO` en `procesar_foto`.
- V12.2.1 tipo verificado: cubierto por `procesar_foto` (s3.2); el `Content-Type` y el nombre subidos se ignoran.
- V12.3 nombre de archivo: cubierto — el nombre subido no se usa; ruta desde el nombre guardado (s3.3).
- V12.4 almacenamiento: cubierto — el directorio no se monta en `/static`.
- V12.5 entrega: `FileResponse` con `image/jpeg` fijo (el archivo siempre lo genera la app), `X-Content-Type-Options: nosniff` del middleware, sin `Content-Disposition` con datos del usuario.
- V4.2 control de acceso a objetos: cubierto — un solo usuario; la dependencia global exige la sesión antes de cualquier lectura; la imagen se busca por el id del ejemplar y el nombre sale de la base.
- V4.3 / V3 CSRF: cubierto por `exigir_sesion` (campo `csrf` del formulario multipart); prueba sin token.
- V5.1 entrada: `id` entero validado por FastAPI; `foto` como `UploadFile`.
- V7 registro: un fallo al guardar se registra en `orquidea.fotos` sin datos del usuario.
- Concurrencia (memoria del proyecto): el cerrojo de s3.3 protege el reemplazo; la prueba manual sube en paralelo bajo `uvicorn` real.
- DoS por recursos: límite de cuerpo, de bytes y de píxeles; el procesamiento corre en el pool de hilos de las rutas síncronas.

### Deduced criteria

- Ejemplar sin foto → mensaje y formulario: confirmed
- Reemplazar borra lo anterior: confirmed — `poner_foto` (s3.3)
- Sin sesión no entrega nada: confirmed
- Sin CSRF, 403 y nada guardado: confirmed — la dependencia se resuelve antes del cuerpo del handler
- Archivo inválido o sin archivo → 422 en español: confirmed
- Cuerpo excedido → 413 sin procesar: confirmed — el middleware corta antes del multipart
- Sin foto o id inexistente → 404: confirmed

### Scenarios (delta over the scope)

```gherkin
Given un ejemplar cuya fila apunta a un archivo que ya no existe en el disco
When pido su imagen
Then responde 404 y no 500

Given un cuerpo chunked sin Content-Length que excede el límite
When se envía
Then responde 413

Given "/coleccion/nuevo" y "/coleccion/1"
When se piden
Then el primero muestra el formulario de alta y el segundo la ficha (el orden de registro los distingue)

Given un fallo de escritura (disco lleno) al guardar
When se sube una foto válida
Then la ficha responde 500 con un mensaje controlado y no queda ningún archivo
```
