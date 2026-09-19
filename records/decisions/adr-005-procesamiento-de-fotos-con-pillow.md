---
type: adr
id: ADR-005
title: "Procesamiento de fotos con Pillow: se reconstruye la imagen desde sus píxeles"
status: superseded by ADR-007
date: 2026-09-19
epic: e3
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-005: Procesamiento de fotos con Pillow: se reconstruye la imagen desde sus píxeles

## Status

Superseded by ADR-007 (solo cambia el tamaño y la calidad de la miniatura; el resto de la decisión se mantiene)

## Context

RF-05 pide una foto por ejemplar, visible en su ficha y en miniatura en las listas. `must-perf-002` fija un ancho máximo de 1600 px y miniaturas; `must-security-001` exige que ninguna foto llegue al disco con metadatos EXIF, incluido el GPS (una orquídea nativa con coordenadas revela dónde crecen poblaciones silvestres y dónde vive el usuario). El brief descarta una tubería con varios tamaños y formatos modernos: basta la imagen reducida y una miniatura. La biblioteca estándar de Python no decodifica ni reescala imágenes, así que hace falta una dependencia.

Fuerzas:

- **La foto es una entrada no confiable**: un archivo subido puede mentir sobre su tipo, ser enorme en píxeles (bomba de descompresión) o llevar metadatos.
- **Quitar metadatos con fiabilidad**: borrar campos EXIF de un archivo conservado es frágil (otros contenedores: XMP, IPTC, comentarios, perfiles); reconstruir el archivo solo con los píxeles no deja nada que olvidar.
- **La orientación vive en el EXIF**: si se descarta el EXIF sin aplicarla antes, las fotos del teléfono quedan giradas.
- **Un solo usuario y un solo proceso** (ADR-001): el procesamiento síncrono en el pool de hilos de las rutas basta.

Opciones:

- **(A) Pillow**, abriendo, aplicando `ImageOps.exif_transpose`, reduciendo y guardando un JPEG nuevo a partir de los píxeles.
- **(B) Borrar los metadatos del archivo original** (por ejemplo con `piexif`) y guardarlo tal cual. Conserva el archivo, pero deja pasar lo que la biblioteca no conoce.
- **(C) Herramienta externa (`exiftool`, ImageMagick).** Dependencia del sistema que no cabe en la imagen mínima y ejecuta procesos con entrada del usuario.

## Decision

Opción (A): `pillow` es dependencia de la aplicación.

1. Un módulo de la capa de datos (`orquidea.datos.fotos`, funciones puras sobre bytes) recibe los bytes subidos y devuelve **dos JPEG nuevos**: la imagen (ancho máximo 1600 px, sin ampliar las más chicas) y la miniatura (lado mayor 320 px).
2. La orientación EXIF se aplica a los píxeles **antes** de descartar los metadatos; el JPEG de salida se escribe sin `exif`, sin `icc_profile` y sin `info` alguno del original. Las imágenes con transparencia se aplanan sobre blanco.
3. Solo se aceptan JPEG, PNG y WebP; el tipo se decide por lo que Pillow decodifica, nunca por el nombre ni por el `Content-Type` enviado.
4. Límites de entrada: tamaño máximo del archivo subido y un tope de píxeles (`Image.MAX_IMAGE_PIXELS` fijado explícitamente y `DecompressionBombError` tratado como rechazo). Una entrada que no decodifica o excede un límite se rechaza con un error de dominio, sin escribir nada.
5. El formato de salida es siempre JPEG: sin formatos modernos ni varios tamaños (rabbit hole del brief).

## Consequences

**Positive:**
- Los metadatos no pueden sobrevivir porque el archivo de salida nunca los recibe; la prueba de `must-security-001` es directa (una imagen con GPS sale sin EXIF).
- Un solo camino de código para las dos salidas; sin procesos externos.

**Negative / costs:**
- Una dependencia con extensión nativa en la imagen y en el wheel; se acepta porque no hay alternativa en la biblioteca estándar.
- Se recomprime la foto: pierde algo de calidad y el original se descarta (no hay "descargar original"; asumido, RF-05 no lo pide).
- Cada subida decodifica y recodifica en un hilo del pool: con un solo usuario es despreciable, pero los límites de entrada son obligatorios.
- Pillow tendrá avisos de seguridad propios: se actualiza como cualquier dependencia.

## Alternatives considered

- **(B) Borrar campos del archivo original:** conserva la calidad, pero depende de conocer todos los contenedores de metadatos; un olvido filtra el GPS, que es exactamente el riesgo que el guardarraíl quiere excluir.
- **(C) `exiftool` o ImageMagick:** dependencia del sistema, procesos externos con archivos del usuario y más superficie que una biblioteca en proceso.
