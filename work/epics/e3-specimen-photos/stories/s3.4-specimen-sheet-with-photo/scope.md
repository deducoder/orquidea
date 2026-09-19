# Story s3.4: Specimen sheet with photo — Scope

## User story

As a coleccionista,
I want abrir la ficha de uno de mis ejemplares y subirle su foto,
so that reconozca la planta a simple vista sin que la imagen revele dónde se tomó.

## Acceptance criteria

```gherkin
@stated
Given un ejemplar en mi colección y una foto JPEG de 4000x3000 px con GPS en el EXIF
When la subo desde la ficha del ejemplar
Then la ficha muestra la foto, el archivo guardado mide 1600 px de ancho y no contiene EXIF ni GPS

@stated
Given un ejemplar con foto
When abro su ficha
Then veo la foto a tamaño completo junto al nombre, la especie y las notas del ejemplar

@deduced
Given un ejemplar sin foto
When abro su ficha
Then veo que aún no tiene foto y el formulario para subirla

@deduced
Given un ejemplar con foto
When subo otra
Then la ficha muestra la nueva y los archivos de la anterior desaparecen

@deduced
Given que no inicié sesión
When pido la ficha, la imagen o la subida de un ejemplar
Then me redirige al acceso y no entrega nada

@deduced
Given una subida sin el token CSRF
When se envía
Then responde 403 y no se guarda nada

@deduced
Given un archivo que no es una imagen admisible, o una petición sin archivo
When se sube
Then la ficha responde 422 con un mensaje en español y no se guarda nada

@deduced
Given un cuerpo de petición mayor al límite
When se envía
Then responde 413 sin procesar la imagen

@deduced
Given un ejemplar sin foto, o un identificador inexistente
When pido su imagen
Then responde 404
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `GET /coleccion/1` con sesión | abrir la ficha | 200 con nombre, notas, `<img src="/coleccion/1/foto">` si hay foto y el formulario de subida |
| `POST /coleccion/1/foto` con `csrf` y `foto=orquidea.jpg` (4000x3000 con GPS) | subir | 303 a `/coleccion/1`; archivos de 1600x1200 y 320x240 sin EXIF |
| `POST /coleccion/1/foto` con `foto=nota.txt` | subir | 422, "El archivo no es una imagen válida." |
| `GET /coleccion/1/foto` | pedir la imagen | 200 `image/jpeg`, `X-Content-Type-Options: nosniff` |
| `GET /coleccion/1/foto/miniatura` | pedir la miniatura | 200 `image/jpeg`, lado mayor ≤ 320 px |

## In scope

- Ficha del ejemplar `GET /coleccion/{id}` con su foto y el formulario de subida (multipart con CSRF).
- Subida `POST /coleccion/{id}/foto` que valida, procesa (s3.2) y guarda (s3.3), traduciendo los errores.
- Rutas protegidas que sirven la imagen y la miniatura desde el disco.
- Límite del tamaño del cuerpo de la petición (413), también sin `Content-Length`.
- Enlace "Ficha" en "Mi colección" para llegar a ella.

## Out of scope

- Miniaturas visibles en "Mi colección" y quitar la foto — s3.5.
- Documentar el límite y el volumen — s3.6.
- Caché del navegador de las imágenes — fuera de alcance de la épica.

## Done when

- [stated] Subir una foto con GPS en el EXIF y comprobar que la imagen guardada no tiene metadatos y mide ≤ 1600 px de ancho, por prueba de extremo a extremo por HTTP (métrica líder del brief).
- [stated] La foto se ve en la ficha del ejemplar (RF-05).
- [deduced] Sin sesión ninguna ruta de fotos entrega nada, y toda subida exige CSRF (`should-security-002`, ADR-006).
- [deduced] Los rechazos no dejan archivos ni cambian la base.
- [deduced] `./scripts/check` está en verde.

## Notes

Diseño de la épica: `design.md`, componentes `orquidea.web.rutas.coleccion`, plantillas; ADR-005 y ADR-006. Es el esqueleto funcional de la épica: cierra la métrica líder de punta a punta. Los `@stated` son la métrica líder del brief y el "la ve en su ficha" de RF-05.
