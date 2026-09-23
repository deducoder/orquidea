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

### La rejilla

Por llenar al medir: peso (T1), glifos e itálica (T2), `tnum` (T3), licencia (T4), por opción, cada celda marcada `ran:` o `read:`.

### Contraejemplos

Por correr, antes de elegir.

## Decision

Sin resolver.
