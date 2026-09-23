---
type: commission
commission: "La identidad visual de la interfaz web de Orquídea: paleta, tipografía y la interfaz derivada de ellas"
decision: ADR-009
date: 2026-09-22
---

# Orquídea — Contra qué se juzga esta identidad

## The criterion this answers

No se repite aquí: vive en `ADR-009`, abierto y commiteado antes de que existiera cualquier pieza de este encargo. Esta sección nombra el registro y nada más.

## The fitness criteria of this commission

| # | Criterion | Stratum | Expected to bear on |
|---|-----------|---------|---------------------|
| 1 | Los recursos de la identidad (CSS y fuentes, en `src/orquidea/web/static/identidad/`, gzip) pesan ≤ 50 KB | `mechanical` | `typography` (fuente web o del sistema), `ui` |
| 2 | Todo texto de tamaño normal tiene contraste ≥ 7:1 con su fondo; el texto grande queda en el piso de `contrast` | `mechanical` | `color` (los pares), `ui` (qué par usa cada texto) |
| 3 | La foto del ejemplar es la protagonista: la paleta no compite con los colores de las flores | `judgement` | `color`, `ui` |

**`Expected to bear on` is an expectation, never a contract.**

Instrumentos del proyecto para los medibles: `scripts/medir-primera-carga.py --identidad DIR` (criterio 1) y `scripts/contraste-de-lectura.py SUJETO.md` (criterio 2), ambos con salida 0 (pasa), 1 (rojo del criterio) y 2 (nada juzgado).

## The survival catalogue, resolved once

| Entry | This commission | Because |
|-------|-----------------|---------|
| `platform-specs` | no aplica | no se entrega ninguna marca ni ícono de plataforma |
| `minimum-size` | aplica a `typography` | el texto más pequeño (fechas, fuentes de los cuidados) se prueba en el teléfono |
| `single-ink` | no aplica | es propiedad de una marca y este encargo no tiene marca |
| `contrast` | aplica a `color` (pares de texto) y a `ui` (plantillas) | son las aplicaciones de la identidad; no hay logotipo al que alcance su exención |
| `prior-art` | no aplica | no se entrega marca ni se registra nada; el uso es personal y no comercial |
| `component-contrast` | aplica a `ui` | botones, campos y estados de foco de los formularios |
| `target-size` | aplica a `ui` | los botones y enlaces se tocan con el dedo en campo |
| `provenance` | aplica a `color`, `typography` y `ui` | todo valor sale de la escala que declara su entregable |

## What was measured, and what was judged

- **Measured:** que las comprobaciones de los criterios 1 y 2 existen y se ponen en rojo con un sujeto que los viola — un archivo de 60 KB que no comprime (60.0 KB, tope 50 KB, salida 1) y `#767676` sobre `#ffffff` (4.54:1, necesita 7:1, salida 1) —, con sus controles de población vacía (salida 2) y de un par que cumple (7.00:1, salida 0). Salida literal en ADR-009. Nada de la identidad se midió todavía: no existe.
- **Judged:** los criterios mismos — el perímetro (`concept`, `color`, `typography`, `ui`; `logo` fuera), la opción (A) de ADR-009 (catálogo + criterios 1, 2 y 3) y el alcance del criterio 2 (todo el texto de tamaño normal) —, por **Daniel Efraín Domínguez Urbina**, el 2026-09-22.

## What this commission is not asking for

- Logotipo, favicon o ícono de plataforma: no-go del brief de e5.
- Un tema oscuro o varios temas: una sola paleta.
- Cambios de comportamiento: la identidad viste lo que la aplicación ya hace (RF-01 a RF-08).
- Efecto en el mercado o en la memoria del usuario: no se puede consultar al juzgar una pieza.

## Rejected directions

- **Solo el catálogo, sin criterios de adecuación** — nada diría qué debe lograr esta identidad para este uso; el peso de las fuentes quedaría sin tope propio dentro de los 200 KB de `must-perf-001`.
- **Sin el criterio 2** — el texto pequeño (fechas, fuentes, último riego) se quedaría en 4.5:1, que es justo el que se lee bajo el sol.
- **Itálica verdadera y glifos es-MX** — solo la pieza `typography` podría cumplirlo; queda como criterio propio de esa pieza.
- **"Evoca la naturaleza de Chiapas"** — nadie podría responderlo con un sí o un no al juzgar una pieza.
