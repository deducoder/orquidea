---
type: composition
commission: "Las pantallas de la interfaz web de Orquídea, derivadas de su inventario"
derived-from: "governance/identity/ui/screens/priority-guide.md, governance/identity/ui/screens/screen-pattern.md y governance/identity/ui/DESIGN.md"
decision: ADR-020
date: 2026-09-24
screen: S1
page: pagina
lang: es-MX
---

# Orquídea — Composition of S1

## The criterion this answers

No se repite aquí: vive en `ADR-020`, abierto antes de escribir cualquier fila de abajo. Esta sección nombra el registro y nada más.

## The rule

El rango 1 de la guía (la búsqueda) lleva el título de la pantalla con `titulo`, el campo con `campo` y el botón con `boton`. El rango 2 (las especies que coinciden) es un enlace `enlace-navegacion` por especie. Todo va directo sobre la página, sin cajas: el fondo de `pagina` es el suelo de todas las filas. Es el candidato A de ADR-020, el que eligió el dueño.

## The composition

| Id | Rank | Element | Component | Content | From | Within |
|----|------|---------|-----------|---------|------|--------|
| C1 | 1 | h1 | titulo | Especies | src/orquidea/web/templates/especies.html:4 | — |
| C2 | 1 | input | campo | Buscar especies | src/orquidea/web/templates/especies.html:7 | — |
| C3 | 1 | button | boton | Buscar | src/orquidea/web/templates/especies.html:10 | — |
| C4 | 2 | a | enlace-navegacion | Arpophyllum giganteum | src/orquidea/datos/catalogo/arpophyllum-giganteum.json:3 | — |
| C5 | 2 | a | enlace-navegacion | Aulosepalum hemichrea | src/orquidea/datos/catalogo/aulosepalum-hemichrea.json:3 | — |
| C6 | 2 | a | enlace-navegacion | Barkeria skinneri | src/orquidea/datos/catalogo/barkeria-skinneri.json:3 | — |

## The parameters

| Parameter | Value |
|-----------|-------|
| gap | {spacing.step-2} |
| margin | {spacing.step-2} |
| border-width | 1px |

## The page, measured

**Generated:** `page: S1 (list-detail), 6 rows in 2 ranks, 4 components, 0 representative, 3 parameters, 0 literals outside a token; ranks 25 ≥ 16 px; 7 texts on their ground, all ≥ 4.5:1; 5 focusable, 0 ring on its ground ≥ 3.0:1, 5 on the browser's focus, not measured`

K1, el comando de ADR-020 sobre esta composición: `7 par(es) de texto juzgado(s), 0 bajo el umbral` (7:1), exit 0.

## How it answers the survival criteria

| Criterion | How this answers it |
|-----------|---------------------|
| `platform-specs` | not applicable, because no hay marca |
| `minimum-size` | not applicable, because la página usa los pasos de la escala, cuyo piso de 16 px midió el espécimen |
| `single-ink` | not applicable, because no hay marca |
| `contrast` | 7 textos sobre su suelo, todos ≥ 4.5:1 según `page.py`, y ≥ 7:1 según K1 |
| `prior-art` | not applicable, because no se registra ni se entrega marca |
| `component-contrast` | el borde del campo (`campo-borde` sobre `fondo`) es el par de componente medido en s1; esta página no agrega ninguno |
| `target-size` | campo, botón y enlaces declaran un mínimo de 48 × 48 (`spacing.step-6`); `comprobar-medidas.py objetivos` los mide sobre `DESIGN.md` |
| `provenance` | `0 literals outside a token`: todo valor sale de un token o de un parámetro declarado |
| `focus-visible` | sin mitad con script: los 5 controles quedan al foco del navegador (censo). Al tabular, el foco se ve y nada lo tapa (juicio, abajo) |

## How it answers the fitness criteria

| Criterion, as approved | From | Stratum | How this answers it |
|------------------------|------|----------|----------|
| W1 — peso y familia del espécimen; la página los escribe | commission 2, vía el espécimen | `mechanical` | sí: ningún rechazo por `fontWeight`, y la página escribe la pila de sistema de `specimen.md:19` |
| K1 — 7:1 en cada texto | commission 2 | `mechanical` | sí: 7 de 7 |
| K2 — `page.py` exit 0 | this link | `mechanical` | sí: el censo de arriba |
| K3 — lo más importante es la búsqueda; elección contra S1–S3 del concepto | concepto (ADR-010) | `judgement` | sí, firmado abajo |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| ¿Qué es lo más importante aquí?, en cada candidato, antes de mostrar el rango 1 | la búsqueda, en los dos candidatos. Es el rango 1, así que ninguno sale. Quien respondió firmó la guía y ya conocía la respuesta | Daniel Efraín Domínguez Urbina, 2026-09-24 |
| La elección forzada entre los dos, contra S1, S2 y S3 de `concept.md` | el candidato 1 (A). S1: sin tarjetas blancas, la firma queda en fondo, tinta y estructura. S2: los dos lo cumplen igual. S3: a 360 px la búsqueda y la lista usan todo el ancho, sin marcos que encogen. Las razones las redactó el agente y el dueño las eligió | Daniel Efraín Domínguez Urbina, 2026-09-24 |
| Si el foco se ve al tabular por la página y nada lo tapa | sí | Daniel Efraín Domínguez Urbina, 2026-09-24 |

## What was not measured

- Otros anchos: el patrón `list-detail` a ancho medio y expandido, con la lista y el detalle lado a lado, no se generó. `page.py` dibuja una sola columna.
- Reflujo, zoom y espaciado de texto.
- El anillo de foco: ningún componente tiene variante `-focus`, así que los 5 controles quedan al foco del navegador y nada lo mide. El juicio de arriba es lo único que lo cubre.
- La búsqueda en vivo con htmx y el resultado vacío: la página es una composición estática.

## What was tried and rejected

**Candidato B, en tarjetas.** Se puede generar otra vez con esta composición cambiando:

- `gap` a `{spacing.step-1}`;
- una fila `section` / `tarjeta` de rango 1 que contiene al campo y al botón;
- otra `section` / `tarjeta` de rango 2 que contiene las tres especies.

Censo: `8 rows in 2 ranks, 5 components`; K1 7 de 7. Pasó la pregunta 1 (la búsqueda) y perdió en la elección forzada. Contra S1, sus tarjetas blancas ponen un plano más entre el fondo y la tinta. Contra S3, a 360 px las tarjetas se ajustan a su contenido y no usan todo el ancho.
