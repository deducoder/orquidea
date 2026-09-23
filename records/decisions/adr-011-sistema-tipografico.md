---
type: adr
id: ADR-011
title: "Sistema tipográfico de Orquídea"
status: proposed
date: 2026-09-22
epic: e5
published: pendiente — se resuelve al completar el registro
---

# ADR-011: Sistema tipográfico de Orquídea

## Status

Proposed.

## Context

**La pregunta:** ¿con qué familia (o familias) se escribe Orquídea, dentro de la dirección Cuaderno de campo (ADR-010) y del criterio del encargo (ADR-009)?

Hoy ninguna plantilla enlaza una fuente: el navegador usa su serif por defecto. La CSP (`default-src 'self'`) obliga a servir una fuente web desde `/static`. El texto que más exige es de consulta: 100 binomios en itálica, nombres comunes en otras lenguas, citas largas con URL, fechas `AAAA-MM-DD` en listas de hasta 500 registros, y `<small>` para fechas y fuentes.

### Criterios de la pieza

Aprobados por el humano el 2026-09-22, antes de medir ninguna opción.

| # | Criterio | Estrato | From |
|---|-----------|---------|------|
| T1 | Las fuentes de la identidad pesan ≤ 40 KB en gzip, lo que deja ≥ 10 KB de los 50 para el CSS | `mechanical` | commission 1 |
| T2 | Los nombres científicos se ven en itálica verdadera y todos los glifos del español de México (á é í ó ú ü ñ ¿ ¡ « » — y sus mayúsculas) existen en el estilo que los usa | `mechanical` (web) · `read:` (sistema) | esta pieza (criterio 4 que ADR-009 dejó a `typography`) |
| T3 | Las fechas se alinean en columna: la familia trae cifras tabulares | `mechanical` (web) · `read:` (sistema) | concept (ADR-010) |
| T4 | La licencia permite servirla desde el propio servidor y recortarla, sin costo | `read:` | esta pieza |

Criterios del catálogo que esta pieza ejerce (resueltos en ADR-009): `minimum-size` (el piso se lee de su fuente al producir y se prueba renderizando), `contrast` (lo resuelven s5.3 y s5.5 con los pares; aquí solo se declara qué texto es normal y cuál grande), `provenance` (cada tamaño del espécimen sale de su escala).

### Opciones

- **(A) Pila de fuentes del sistema** (`system-ui`: San Francisco, Roboto, Segoe UI…).
- **(B) Atkinson Hyperlegible.**
- **(C) IBM Plex Sans.**
- **(D) Source Sans 3.**

### Cómo se midió

Medido el 2026-09-22 en el scratchpad de la sesión (`$S`), nunca en el repositorio. Archivos: subconjunto latino `woff2` de Fontsource 5.3.0 (`cdn.jsdelivr.net/npm/@fontsource/{familia}/files/{familia}-latin-{peso}-{estilo}.woff2`, y `@fontsource-variable/…-latin-wght-{estilo}.woff2` para las variables). Peso con `scripts/medir-primera-carga.py --identidad` (gzip por archivo). Glifos, bit de itálica, ángulo, rasgos `tnum`/`pnum` y anchos de avance de 0–9 con `fontTools` (`uv run --with fonttools --with brotli`), leídos del archivo. Licencia leída del `package.json` de cada paquete.

### La rejilla

| Criterio | Estrato | (A) Sistema | (B) Atkinson Hyperlegible | (C) IBM Plex Sans | (D) Source Sans 3 |
|---|---|---|---|---|---|
| T1 · fuentes ≤ 40 KB gzip | `mechanical` | sí — 0 archivos (`ran:`) | 4 estilos 69.9 KB **no**; regular + itálica 34.7 KB sí; variable 70.0 KB **no** (`ran:`) | 4 estilos 92.3 KB **no**; regular + itálica 45.8 KB **no**; variable 93.4 KB **no** (`ran:`) | 4 estilos 61.5 KB **no**; regular + itálica 30.8 KB sí; variable 56.0 KB **no** (`ran:`) |
| T2 · itálica verdadera y glifos es-MX | `mechanical` / `read:` | sí — Roboto, San Francisco y Segoe UI traen itálicas propias (`read:` abajo) | sí — archivo itálico propio (bit de itálica, −12°), ningún glifo es-MX falta en regular ni itálica (`ran:`) | sí — itálico propio (−11.3°), ningún glifo falta (`ran:`) | sí — itálico propio (−11°), ningún glifo falta (`ran:`) |
| T3 · cifras tabulares | `mechanical` / `read:` | sí — Roboto las trae por defecto; San Francisco y Segoe UI por `tnum` (`read:` abajo) | sí — por defecto son proporcionales (9 anchos), pero trae `tnum`, activable con `font-variant-numeric` (`ran:`) | sí — por defecto, un solo ancho (600) en regular e itálica (`ran:`) | sí — por defecto en la regular (un ancho, 497); la itálica varía en 1 unidad (479/480) y las fechas no van en itálica (`ran:`) |
| T4 · licencia libre para servir y recortar | `read:` | no aplica — no se sirve ningún archivo; el navegador usa la fuente instalada | sí — OFL-1.1 | sí — OFL-1.1 | sí — OFL-1.1 |
| Negrita propia dentro de T1 | — | sí | no — la negrita la sintetiza el navegador | no | no — la negrita la sintetiza el navegador |
| Lo que se ve es igual en todos los teléfonos | — | no — cambia con el sistema | sí | sí | sí |

`read:` de (A), consultados el 2026-09-22 (fuentes secundarias): Roboto — [Wikipedia, «Roboto»](https://en.wikipedia.org/wiki/Roboto) y [Tachyons, Roboto](https://tachyons.io/docs/typography/font-family/roboto/); San Francisco — [Wikipedia, «San Francisco (sans-serif typeface)»](https://en.wikipedia.org/wiki/San_Francisco_(sans-serif_typeface)) y [Apple Developer, Fonts](https://developer.apple.com/fonts/); Segoe UI — [Microsoft Learn, Segoe UI font family](https://learn.microsoft.com/en-us/typography/font-list/segoe-ui) y [«Segoe UI, tabular figures and DirectWrite»](https://blog.yuo.be/2024/07/20/segoe-ui-tabular-figures-and-directwrite/). La cobertura es-MX de las tres es `read:` por su cobertura Latin-1 publicada, no comprobada glifo por glifo.

Nota sobre ADR-010: la celda (B) × S2 de ese registro dice que las serif del sistema en Android no dan itálica real. Lo que se verificó aquí es otra cosa (las sans del sistema), así que esa frase sigue sin comprobar; el hallazgo está en la retrospectiva de s5.2.

### El piso de legibilidad (`minimum-size`)

Leído el 2026-09-22: Legge, G. E. y Bigelow, C. A. (2011), «Does print size matter for reading? A review of findings from vision science and typography», *Journal of Vision* 11(5):8, https://doi.org/10.1167/11.5.8 (texto en PMC3428264). El consenso para lectores con visión normal es un **tamaño crítico de 0.2° de altura de x**; el intervalo fluido va de 0.2° a 2°.

Parámetros declarados (no medidos): el teléfono a **35 cm** del ojo (brazo flexionado, en campo) y **160 px CSS por pulgada**. Con ellos, 0.2° son 1.22 mm = **7.7 px CSS de altura de x**, y el tamaño de fuente mínimo es 15.5 px (B), 14.9 px (C) y 15.8 px (D), según la altura de x de cada familia (`sxHeight`/`unitsPerEm`: 0.496, 0.516, 0.486). A 30 cm serían unos 13–14 px: la distancia es el parámetro que más mueve la cifra.

Prueba: renderizado con Pillow a 3 px físicos por px CSS, a 16 px y a 14 px, con un binomio en itálica, una fecha y una cita, para (B) y (D) (`$S/prueba-*.png`). En papel no aplica: la aplicación no se imprime. (A) no se pudo renderizar en esta máquina (no tiene fuentes instaladas); se prueba en el teléfono en s5.7.

### Contraejemplos

- **T1 — rojo, visto:** las tres opciones web con sus cuatro estilos pasan de 40 KB (69.9, 92.3 y 61.5 KB), y también en su versión variable (70.0, 93.4 y 56.0 KB). (C) pasa incluso con solo regular e itálica (45.8 KB). Salida del instrumento: `Total 61.5 KB tope 50 KB PASA DEL TOPE` (D, 4 estilos), `Total 45.8 KB tope 50 KB OK` (C, 2 estilos: bajo el tope del encargo, sobre el de T1).
- **T2 — ningún sujeto lo viola** entre las opciones: todas traen itálica propia y los glifos. Sujeto construido para verlo en rojo: el subconjunto regular de (D) sin su archivo itálico — el navegador sintetizaría una oblicua; el criterio pide el archivo, y `fontTools` sobre ese sujeto no encuentra ningún archivo con el bit de itálica.
- **T3 — rojo, visto en el archivo:** los anchos de 0–9 de (B) por defecto son 9 distintos; sin `tnum` las fechas no se alinean. Se cumple solo activando el rasgo.
- **T4 — no aplica: `read:`**, no hay comprobación que ver fallar; la licencia se lee.

## Decision

Sin resolver.
