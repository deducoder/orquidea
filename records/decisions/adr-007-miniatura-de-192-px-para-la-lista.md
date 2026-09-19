---
type: adr
id: ADR-007
title: "Miniatura de 192 px de lado mayor y calidad 75, medida contra el presupuesto de la lista"
status: accepted
date: 2026-09-19
epic: e3
supersedes: ADR-005
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-007: Miniatura de 192 px de lado mayor y calidad 75, medida contra el presupuesto de la lista

## Status

Accepted. Sustituye a ADR-005.

## Context

ADR-005 eligió Pillow, reconstruir la imagen desde sus píxeles y dos salidas JPEG: la imagen (ancho máximo 1600 px) y una miniatura de lado mayor 320 px (calidad 80). Esa cifra de 320 px no salió de ninguna medida: fue una elección razonable antes de tener la lista.

Con la lista hecha (s3.5) apareció el dato que faltaba. "Mi colección" muestra cada miniatura a 96x96 px, y `must-perf-001` cuenta las miniaturas dentro de los 200 KB de la primera carga, porque un JPEG no se comprime más con gzip. Una foto con detalle a 320 px, medida con un proxy de foto (ruido fractal reducido con el mismo procesamiento), pesa unos 15 KB con calidad 80; con 192 px y calidad 75 pesa unos 5 KB. La colección de un aficionado puede tener decenas de plantas con foto.

Fuerzas:

- **Presupuesto**: 200 KB para HTML, JavaScript y miniaturas; el HTML y `htmx` ya gastan ~20 KB.
- **Nitidez**: en una pantalla de doble densidad, 96 px CSS son 192 px físicos; más píxeles no se ven.
- **La miniatura solo sirve a la lista**: la ficha usa la imagen de 1600 px.
- **Cambiar de idea sobre un ADR aceptado** se hace con otro ADR que lo sustituya.

Opciones:

- **(A) Mantener 320 px y confiar en `loading="lazy"`.** Solo cuentan las visibles en la primera carga, pero cuántas son depende de la pantalla y lo decide el navegador; el presupuesto quedaría sujeto a algo que no controlamos.
- **(B) 192 px y calidad 75** (2x del tamaño mostrado).
- **(C) 128 px, 1x.** La más ligera, pero borrosa en pantallas de doble densidad, que son las de los teléfonos donde más se mira una colección.

## Decision

Opción (B). Las cinco decisiones de ADR-005 se mantienen tal como están (Pillow; reconstruir desde píxeles y aplicar antes la orientación; JPEG, PNG y WebP como entradas; límites de tamaño y de píxeles; salida siempre JPEG) salvo el punto 1, que cambia: la miniatura mide como máximo **192 px** de lado mayor y se guarda con calidad **75**. La imagen sigue en 1600 px de ancho máximo y calidad 85.

## Consequences

**Positive:**
- Cada miniatura pesa un tercio; la lista cabe en el presupuesto con margen aunque haya decenas de fotos, sin depender del `lazy`.
- Menos bytes en el disco y en la red por cada foto.

**Negative / costs:**
- La miniatura pierde nitidez si algún día se muestra más grande de 96 px; habría que regenerarlas o servir la imagen de 1600 px.
- Las miniaturas ya guardadas con el tamaño anterior (ninguna en producción: e3 aún no se despliega) seguirían siendo de 320 px hasta volver a subir la foto.
- ADR-005 queda sustituido: quien busque la razón de Pillow debe leer los dos.

## Alternatives considered

- **(A) 320 px con `loading="lazy"`:** deja el presupuesto en manos del navegador y de la pantalla; con el proxy, 13 miniaturas ya pasan de 200 KB.
- **(C) 128 px:** ahorra poco más que (B) y se ve borrosa a 2x.
