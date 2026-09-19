# Story s3.2: Image processing — Scope

## User story

As a coleccionista que sube la foto de una de sus orquídeas,
I want que la aplicación reduzca la imagen y le quite todos los metadatos antes de guardarla,
so that la foto pese poco y nunca revele dónde se tomó, y las listas puedan mostrar una miniatura.

## Acceptance criteria

```gherkin
@stated
Given una foto JPEG de 4000x3000 px con coordenadas GPS en el EXIF
When se procesa
Then la imagen resultante mide 1600 px de ancho, la miniatura tiene su lado mayor ≤ 320 px, y ninguna de las dos tiene EXIF ni GPS

@deduced
Given una imagen de 800x600 px
When se procesa
Then la imagen resultante conserva 800x600 (no se amplía)

@deduced
Given un JPEG con orientación EXIF 6 (girado 90°)
When se procesa
Then los píxeles resultantes ya están girados (el ancho y el alto se intercambian) y el resultado no lleva EXIF

@deduced
Given un PNG con canal alfa
When se procesa
Then el resultado es un JPEG con el fondo blanco donde había transparencia

@deduced
Given un archivo con metadatos XMP, comentario o perfil ICC además del EXIF
When se procesa
Then el resultado no contiene ninguno de ellos

@deduced
Given bytes que no son una imagen, o un formato que no es JPEG, PNG ni WebP (por ejemplo GIF)
When se procesa
Then se lanza un error de dominio con un mensaje en español y no se devuelve nada

@deduced
Given una imagen cuyas dimensiones exceden el tope de píxeles, o bytes que superan el tamaño máximo
When se procesa
Then se lanza el mismo error de dominio antes de decodificar los píxeles completos
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| JPEG 4000x3000 con GPS en EXIF | `procesar_foto(bytes)` | imagen JPEG 1600x1200 y miniatura 320x240, sin EXIF |
| JPEG 600x800 con orientación 6 | `procesar_foto(bytes)` | imagen 800x600 (girada), sin EXIF |
| `b"no soy una imagen"` | `procesar_foto(bytes)` | `FotoInvalida("El archivo no es una imagen válida.")` |

## In scope

- Módulo de la capa de datos con la función pura que recibe bytes y devuelve la imagen y la miniatura (ADR-005).
- Dependencia `pillow` en `pyproject.toml`.
- Límites de entrada: tamaño máximo del archivo y tope de píxeles; formatos JPEG, PNG y WebP.
- Pruebas automatizadas de `must-perf-002` y `must-security-001`.

## Out of scope

- Guardar archivos en disco y la columna en la base — s3.3.
- Rutas HTTP, formulario de subida y límite del cuerpo de la petición — s3.4 y s3.6.
- Otros tamaños o formatos de salida — rabbit hole del brief.

## Done when

- [stated] Una imagen con GPS en el EXIF sale sin metadatos y con ancho ≤ 1600 px, demostrado por prueba automatizada (métrica líder del brief; `must-perf-002`, `must-security-001`).
- [deduced] Las pruebas de los criterios anteriores pasan y `./scripts/check` está en verde.
- [deduced] La función no escribe archivos ni conoce HTTP ni SQL (system-design: la capa de datos procesa; el dominio no conoce HTTP).

## Notes

Diseño de la épica: `design.md`, componente `orquidea.datos.fotos`; ADR-005. El único criterio `@stated` es el que declara la métrica líder del brief; el resto lo dedujo quien escribió el scope.
