---
type: screen-pattern
commission: "Las pantallas de la interfaz web de Orquídea, derivadas de su inventario"
derived-from: "governance/identity/ui/screens/screen-set.md y governance/identity/ui/screens/priority-guide.md"
decision: ADR-019
date: 2026-09-24
source-read: "https://developer.android.com/develop/ui/compose/layouts/adaptive/canonical-layouts (actualizada el 2026-09-22), leída el 2026-09-24; m3.material.io no entregó texto a la lectura"
---

# Orquídea — Screen patterns

## The criterion this answers

No se repite aquí: vive en `ADR-019`, abierto antes de escribir cualquier patrón de abajo. Esta sección nombra el registro y nada más.

## The rule

La regla de elección es la que publica la fuente de `source-read`, citada textualmente en ADR-019. En paráfrasis:

- **list-detail** es para contenido que se organiza como una lista de elementos que revelan información adicional. A ancho compacto muestra la lista o el detalle, uno a la vez.
- **feed** es para muchos elementos de contenido equivalentes, vistos de un vistazo en una rejilla. Lo común son tarjetas y listas, y a ancho compacto se vuelve una sola columna.
- **supporting-pane** es para un contenido principal acompañado de otro que lo apoya.
- Una pantalla que no recorre contenido (un formulario de un paso) no toma ninguno: su valor es `none`, con su razón.

## The patterns

| Screen | Pattern | Content shape |
|--------|---------|---------------|
| S1 | list-detail | la lista de especies, cada una revela su ficha |
| S2 | list-detail | el detalle de una especie de la lista de S1 |
| S3 | feed | tarjetas equivalentes con la foto primero (rango 1 de la guía), en una columna a ancho compacto |
| S4 | none | la fuente no le da panel de detalle a un feed, y la ficha es una página de un solo elemento |
| S5 | none | un formulario de un paso: no recorre contenido |
| S6 | none | un formulario de un paso: no recorre contenido |
| S7 | none | una confirmación de un paso: no recorre contenido |
| S8 | none | una entrada con enlaces a las dos listas: no recorre contenido propio |
| S9 | none | un formulario de un paso: no recorre contenido |

**Screens with a pattern:** 9 de 9.

## How it answers the survival criteria

| Criterion | How this answers it |
|-----------|---------------------|
| `platform-specs` | not applicable, because no se entrega marca ni ícono de plataforma |
| `minimum-size` | not applicable, because un patrón no tiene texto dibujado |
| `single-ink` | not applicable, because no hay marca |
| `contrast` | not applicable, because no hay texto sobre un fondo |
| `prior-art` | not applicable, because no se registra ni se entrega marca |
| `component-contrast` | not applicable, because no hay componentes dibujados |
| `target-size` | not applicable, because no hay controles |
| `provenance` | not applicable, because no hay valores de escala |
| `focus-visible` | not applicable, because no hay controles |

## How it answers the fitness criteria

| Criterion, as approved | From | Stratum | How this answers it |
|------------------------|------|----------|----------|
| P1 — un solo valor de la tabla, o `none` con razón | this link | `mechanical` | `inventory-sources.py` exit 0, sin fallos de S6 |
| P2 — 9 de 9 con patrón | this link | `mechanical` | `9 of 9 screens with a pattern` |
| P3 — cada contenido en su forma según la fuente | this link | `judgement` | sí, firmado abajo |
| P4 — sostiene la guía sin pedir contenido que no carga | ADR-018 | `judgement` | sí: `feed` pone la foto primero, como el rango 1 de S3, y S4 `none` no agrega nada a su guía |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| la opción de S3 y S4 | B, `feed` y `none` | Daniel Efraín Domínguez Urbina, 2026-09-24 |
| P3: el contenido de cada pantalla, en su forma según la regla de la fuente | sí | Daniel Efraín Domínguez Urbina, 2026-09-24 |
| P4: la opción sostiene la guía firmada sin pedir contenido que no carga | sí | Daniel Efraín Domínguez Urbina, 2026-09-24 |

## What was tried and rejected

Copiadas de ADR-019 sin cambios. S1, S2 y S5 a S9 son comunes a las tres opciones.

- **A — S3 `list-detail` ("la lista de ejemplares, cada uno revela su ficha") y S4 `list-detail` ("el detalle de un ejemplar de la lista de S3").** Midió igual que B (P1 sin fallos, `9 of 9`). Es la lectura que trata la colección igual que las especies. El dueño eligió B.
- **C — S3 `list-detail` y S4 `supporting-pane` ("el ejemplar como área principal y los cuidados de su especie como apoyo").** Midió igual (`9 of 9`). A la lectura, el área de apoyo lleva los cuidados de la especie, que la guía firmada de S4 no carga (P4).
