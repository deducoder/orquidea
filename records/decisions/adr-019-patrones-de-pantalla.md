---
type: adr
id: ADR-019
title: "El patrón de cada pantalla de Orquídea"
status: proposed
date: 2026-09-24
epic: —
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-019: El patrón de cada pantalla de Orquídea

## Status

Proposed.

## Context

**La pregunta:** ¿qué forma toma cada una de las 9 pantallas del conjunto de ADR-017, según la forma de su contenido?

Historia s4, standalone, con el cuarto eslabón de la técnica `screens` de gemba-design 0.24.0. Entrada: `screen-set.md` (ADR-017) y `priority-guide.md` (ADR-018, que guía S1 a S4). La dimensión es `screen-pattern` (`conventional`, `derived`): una tabla cerrada de layouts canónicos con su regla de elección, sin medición.

### La fuente, leída el 2026-09-24

Android Developers, "Canonical layouts", `https://developer.android.com/develop/ui/compose/layouts/adaptive/canonical-layouts`, con fecha de actualización 2026-09-22. m3.material.io, la página que nombra el catálogo, se arma con JavaScript y no entregó texto a la lectura. Android es una de las tres fuentes de la misma familia que el catálogo da por equivalentes. La regla de elección, citada de la fuente:

- **list-detail:** "ideal for … any app where the content can be organized as a list of items that reveal additional information". A ancho compacto, "show either the list or the detail, depending on user interaction".
- **feed:** "arranges equivalent content elements in a configurable grid for quick, convenient viewing of a large amount of content … Cards and lists are common components of feed layouts"; "especially well suited for news and social media apps". A ancho compacto, "a single, scrolling column".
- **supporting-pane:** "organizes app content into primary and secondary display areas … a pane that … presents content that supports the main content". A ancho compacto, lo secundario puede ir "in a bottom or side sheet".

### Criterios de supervivencia, aplicados

| Criterio | Cómo responde |
|---|---|
| `platform-specs` | no aplica: no se entrega marca ni ícono de plataforma |
| `minimum-size` | no aplica: un patrón no tiene texto dibujado |
| `single-ink` | no aplica: no hay marca |
| `contrast` | no aplica: todavía no hay texto sobre un fondo |
| `prior-art` | no aplica: no se registra ni se entrega marca |
| `component-contrast` | no aplica: todavía no hay componentes dibujados |
| `target-size` | no aplica: todavía no hay controles |
| `provenance` | no aplica: no hay valores de escala |
| `focus-visible` | no aplica: todavía no hay controles |

### Criterios de fitness, aprobados

Aprobados por Daniel Efraín Domínguez Urbina el 2026-09-24.

| # | Criterio | De dónde | Estrato | Qué lo decide |
|---|---|---|---|---|
| P1 | Cada pantalla toma un solo valor de la tabla (`list-detail`, `supporting-pane`, `feed`), o `none` con su razón | de este eslabón | `mechanical` | `inventory-sources.py` con los patrones como cuarto archivo (cláusula S6) |
| P2 | Las 9 pantallas del conjunto tienen patrón | de este eslabón | `mechanical` | la cuenta `N of 9 screens with a pattern` en la salida del mismo comando. El script no sale en rojo si faltan pantallas, así que P2 se cumple solo con `9 of 9` |
| P3 | El contenido de cada pantalla se leyó con la forma correcta según la regla de la fuente citada arriba | de este eslabón | `judgement` | la firma del dueño |
| P4 | El patrón sostiene la guía firmada de S1 a S4 sin pedir contenido que la guía no carga | ADR-018 | `judgement` | la lectura del dueño de S1 a S4 frente a la guía |

### Las opciones

Las tres coinciden en S1, S2 y S5 a S9:

| Pantalla | Patrón | Forma del contenido |
|---|---|---|
| S1 Especies | `list-detail` | la lista de especies, cada una revela su ficha |
| S2 Ficha de especie | `list-detail` | el detalle de una especie de la lista de S1 |
| S5 Nuevo ejemplar sin especie | `none` | un formulario de un paso: no recorre contenido |
| S6 Editar ejemplar | `none` | un formulario de un paso: no recorre contenido |
| S7 Confirmar la baja | `none` | una confirmación de un paso: no recorre contenido |
| S8 Inicio | `none` | una entrada con enlaces a las dos listas: no recorre contenido propio |
| S9 Acceso | `none` | un formulario de un paso: no recorre contenido |

Difieren en S3 y S4:

| Pantalla | A | B | C |
|---|---|---|---|
| S3 Mi colección | `list-detail` — la lista de ejemplares, cada uno revela su ficha | `feed` — tarjetas equivalentes con la foto primero (rango 1 de la guía), en una columna a ancho compacto | `list-detail` — como en A |
| S4 Ficha del ejemplar | `list-detail` — el detalle de un ejemplar de la lista de S3 | `none` — la fuente no le da panel de detalle a un feed, y la ficha es una página de un solo elemento | `supporting-pane` — el ejemplar como área principal y los cuidados de su especie como apoyo, en una hoja a ancho compacto |

### La rejilla

| Criterio | Estrato | A | B | C |
|---|---|---|---|---|
| P1 — un valor de la tabla, o `none` con razón | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| P2 — 9 de 9 con patrón | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| P3 — cada contenido en su forma, según la fuente | `judgement` | pendiente del dueño | pendiente del dueño | pendiente del dueño |
| P4 — sostiene la guía sin pedir contenido que no carga | `judgement` | pendiente del dueño | pendiente del dueño; a la lectura, S4 `none` no pide nada fuera de la guía | pendiente del dueño; a la lectura, el área de apoyo de S4 lleva los cuidados de la especie, que la guía de S4 no carga |

### El rojo de los criterios medibles

- P1: pendiente.
- P2: pendiente.

## Decision

Sin resolver.

## Consequences

Sin resolver.

## Alternatives considered

Sin resolver: las opciones A, B y C de arriba.
