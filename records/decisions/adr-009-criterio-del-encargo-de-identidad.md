---
type: adr
id: ADR-009
title: "Criterio del encargo de identidad visual de Orquídea"
status: proposed
date: 2026-09-22
epic: e5
published: pendiente — se resuelve al completar el registro
---

# ADR-009: Criterio del encargo de identidad visual de Orquídea

## Status

Proposed.

## Context

**La pregunta:** ¿contra qué se juzgará toda la identidad visual de Orquídea (concepto, paleta, tipografía y la interfaz derivada), antes de que exista cualquiera de sus piezas?

Hoy no hay identidad que extraer: la aplicación no enlaza una sola hoja de estilos y `base.html` no tiene estilos (recorrido de e5). El criterio entra, por tanto, **propuesto**, por la técnica `commission` de gemba-design 0.21.0, y este registro se abre y se commitea antes de producir nada: cualquier cambio posterior al criterio queda como un diff visible.

Fuerzas:

- **Uso en campo.** El resultado *Usable en campo* de la visión: teléfono, sol directo y redes de baja calidad en Chiapas. `must-perf-001` fija la primera carga en ≤ 200 KB gzip y ≤ 5 s en "Slow 3G", y hoy ya gasta parte de ese presupuesto en HTML, htmx y miniaturas.
- **La planta es lo que importa.** *Colección al día*: el coleccionista reconoce cada ejemplar por su foto, y las orquídeas traen sus propios magentas, púrpuras y amarillos.
- **Una sola persona usa y juzga.** App personal de un solo usuario (RF-08); nadie más firma los juicios, y firmar demasiados lleva a firmar en automático.
- **El coste de captura** es lo que mata esta notación: dos a cuatro criterios de adecuación, no diez.

Perímetro aprobado por el humano el 2026-09-22: `concept`, `color`, `typography` y `ui`. `logo` queda fuera (no-go del brief de e5).

### El catálogo de supervivencia, resuelto una vez

| Entrada | Este encargo | Por qué |
|---|---|---|
| `platform-specs` | no aplica | no se entrega ninguna marca ni ícono de plataforma |
| `minimum-size` | aplica a `typography` | el texto más pequeño (fechas, fuentes de los cuidados) se prueba en el teléfono |
| `single-ink` | no aplica | es propiedad de una marca y este encargo no tiene marca |
| `contrast` | aplica a `color` (pares de texto) y a `ui` (plantillas) | son las aplicaciones de la identidad; la exención del logotipo no se usa porque no hay logotipo |
| `prior-art` | no aplica | no se entrega marca ni se registra nada; el uso es personal y no comercial |
| `component-contrast` | aplica a `ui` | botones, campos y estados de foco de los formularios (acceso, alta de ejemplar, riegos) |
| `target-size` | aplica a `ui` | los botones y enlaces se tocan con el dedo en campo |
| `provenance` | aplica a `color`, `typography` y `ui` | todo valor sale de la escala que declara su entregable |

### Los criterios de adecuación candidatos

| # | Criterio | Estrato | Se espera que toque |
|---|---|---|---|
| 1 | Los recursos de la identidad (CSS y fuentes, en `src/orquidea/web/static/identidad/`, gzip) pesan ≤ 50 KB | `mechanical` | `typography`, `ui` |
| 2 | Todo texto de tamaño normal (`Kind = text`: cuerpo, fechas, fuentes, etiquetas) tiene contraste ≥ 7:1 con su fondo; el texto grande queda en el piso de `contrast` | `mechanical` | `color`, `ui` |
| 3 | La foto del ejemplar es la protagonista: la paleta no compite con los colores de las flores | `judgement` | `color`, `ui` |
| 4 | La tipografía distingue el nombre científico con itálica verdadera y cubre los glifos es-MX | `mechanical` | `typography` |
| 5 | La identidad evoca la naturaleza de Chiapas | `judgement` | todas |

El alcance del criterio 2 (todo el texto de tamaño normal y no solo los párrafos) lo decidió el humano el 2026-09-22, al diseñar s5.1: el texto pequeño es justo el que se lee bajo el sol.

### Opciones

- **(A) Catálogo + criterios 1, 2 y 3** — lo que el humano aprobó el 2026-09-22.
- **(B) Solo el catálogo** — sin criterios de adecuación; las piezas se juzgan solo por lo que sobrevive.
- **(C) Catálogo + criterios 1 y 3** — sin el 2, el texto pequeño se queda en el 4.5:1 de `contrast`.
- **(D) Catálogo + criterios 1 a 5** — todo lo que se consideró.

| Criterio | Estrato | (A) | (B) | (C) | (D) |
|---|---|---|---|---|---|
| Catálogo (8 entradas, arriba) | según la entrada | sí | sí | sí | sí |
| 1 · Peso ≤ 50 KB | `mechanical` | sí | no — el peso de las fuentes queda sin tope propio dentro de los 200 KB | sí | sí |
| 2 · Texto normal ≥ 7:1 | `mechanical` | sí | no | no — el texto pequeño queda en 4.5:1 bajo el sol | sí |
| 3 · La foto es la protagonista | `judgement` | sí | no — nada dice qué debe lograr la paleta | sí | sí |
| 4 · Itálica verdadera y glifos es-MX | `mechanical` | no — es de la pieza `typography` | no | no | sí — pero solo una pieza podría cumplirlo |
| 5 · Evoca Chiapas | `judgement` | no | no | no | sí — pero nadie puede responderlo con sí o no |
| Firmas del humano que pide | — | 1 | 0 | 1 | 2 |
| Cabe en una pantalla | — | sí | sí | sí | al límite |

### Contraejemplos (se escriben antes de producir)

- Criterio 1: pendiente — la comprobación se escribe en s5.1 y se corre sobre un sujeto que viola el tope.
- Criterio 2: pendiente — ídem, sobre un par de texto bajo 7:1.
- Criterio 3: no aplica — no hay oráculo; es juicio, y se instrumenta como elección forzada firmada, nunca como comprobación inventada.

## Decision

Sin resolver. Se completa, en este mismo archivo, cuando existan los rojos de los criterios medibles y el entregable `commission.md`.
