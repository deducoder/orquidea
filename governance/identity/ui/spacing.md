---
type: spacing
commission: "La identidad visual de la interfaz web de Orquídea: paleta, tipografía y la interfaz derivada de ellas"
derived-from: "governance/identity/ui/type-scale.md"
decision: ADR-014
date: 2026-09-22
---

# Orquídea — Spacing

## The criterion this answers

No se repite aquí: vive en `ADR-014`, abierto antes de que existiera cualquiera de los valores de abajo. Esta sección nombra el registro y nada más.

## The rule

La unidad es la altura de línea del escalón 0 de la escala entre un divisor declarado, y tiene que ser entera. Cada paso es un multiplicador declarado por la unidad y se nombra por su multiplicador. El tamaño de control es uno de esos pasos, y cada control declarado se compone de él en sus dos dimensiones. La regla la corre `scripts/derivar-medidas.py espaciado`; la tabla de abajo es su salida sin editar, y la prueba de regeneración la compara con este archivo.

## The parameters

| Parameter | Value | Stratum | Alternatives it beat, and why each lost |
|-----------|-------|---------|------------------------------------------|
| base | `16` | `judgement` | es la base de `type-scale.md`, no otra: la unidad sale del cuerpo de texto |
| divisor | `3` | `judgement` | `2` (unidad de 12 px): pasa M2, pero los márgenes de 24 px en la tarjeta separan de más en 360 px; perdió M4. `6` (unidad de 4 px): los controles salen de 20 px (M2 y `target-size` en rojo, ADR-014) |
| multiplicadores | `1,2,3,4,6` | `judgement` | con medios (`0.5`): el nombre `step-0.5` rompe la ruta de la referencia en `DESIGN.md`; con `5`: ningún componente lo usa |
| control | `6` | `judgement` | `4` (32 px): bajo el 44 de M2; `5` (40 px): ídem |
| composición de cada control | alto y ancho mínimo = paso `6` | `judgement` | alto de control con ancho libre: el ancho no se declara y `targets` no lo mide |

## The spacing

| Step | Value | Where it is used |
|---|---|---|
| 1 | 8px | 1 unidad |
| 2 | 16px | 2 unidades |
| 3 | 24px | 3 unidades |
| 4 | 32px | 4 unidades |
| 6 | 48px | 6 unidades; tamaño de control |

Cada valor se reproduce: correr la regla con los parámetros de arriba lo devuelve.

## The controls, measured

`ran:` `uv run python scripts/comprobar-medidas.py objetivos governance/identity/ui/DESIGN.md --minimo 44` y `ran:` `python3 $G/tokens.py targets governance/identity/ui/DESIGN.md` — salidas copiadas abajo.

| Control | Composition | Width | Height | Target minimum and its source | Held | Exception leaned on |
|---------|-------------|-------|--------|-------------------------------|------|---------------------|
| boton | paso 6 × paso 6 | 48 | 48 | 44 (M2, WCAG 2.2 SC 2.5.5, AAA) y 24 (SC 2.5.8, `target-size`), leídos el 2026-09-22 | sí | ninguna |
| boton-presionado | paso 6 × paso 6 | 48 | 48 | ídem | sí | ninguna |
| campo | paso 6 × paso 6 | 48 | 48 | ídem | sí | ninguna |
| enlace-navegacion | paso 6 × paso 6 | 48 | 48 | ídem | sí | ninguna |
| enlace dentro de un párrafo | — | not declared | not declared | ídem | no se mide | *inline* de SC 2.5.8 y 2.5.5: el tamaño lo fija la línea de texto |

**Dimensions measured:** 8

## How it answers the survival criteria

| Criterion | How this answers it |
|-----------|---------------------|
| `platform-specs` | no aplica, porque no se entrega una marca ni un ícono de plataforma (ADR-009) |
| `minimum-size` | no aplica, porque un espaciado no fija tamaños de texto; lo resolvió `type-scale.md` |
| `single-ink` | no aplica, porque es propiedad de una marca y este encargo no tiene marca (ADR-009) |
| `contrast` | no aplica, porque un espaciado no fija colores |
| `prior-art` | no aplica, porque no se entrega marca ni se registra nada (ADR-009) |
| `component-contrast` | no aplica, porque un espaciado no fija colores |
| `target-size` | 4 controles declarados, 48 × 48, sobre el 24 × 24 de SC 2.5.8: `targets: 4 target(s) judged, 0 below 24x24` |
| `provenance` | cada paso sale de la regla (prueba de regeneración) y cada medida de un componente nombra un paso: `provenance` sobre `DESIGN.md`, 12 tokens, 0 fuera de escala |

## How it answers the fitness criteria

| Criterion, as approved | From | Stratum | How this answers it |
|------------------------|------|----------|----------|
| M2 · controles ≥ 44 × 44 | concept (ADR-010) | `mechanical` | sí — 4 objetivos medidos, 0 bajo 44 px; también en el gate (`tests/test_identidad_ui.py`) |
| M3 · reproducible | este eslabón | `mechanical` | sí — la prueba de regeneración y `provenance` |
| M4 · una familia | concept (ADR-010) | `judgement` | sí, para (A) — abajo |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| M4 — el ritmo de la unidad de 8 px conviene al Cuaderno de campo | sí, para el espaciado (A) con la escala (A) | Daniel Efraín Domínguez Urbina, 2026-09-22, en elección forzada entre A·A, A·B, B·A y B·B (escala · espaciado) sobre la lámina de la ficha y el formulario de alta a 360 px |

## What was not measured

El espaciado con el tamaño de texto o el interlineado del propio usuario, el reflujo, y si 48 × 48 cabe en fila en los formularios en línea de la ficha a 360 px (quitar un riego, terminar una floración): eso lo ve s5.7 al vestir las plantillas. Los enlaces dentro de un párrafo no se miden: se apoyan en la excepción *inline*, dicha arriba.

## What was tried and rejected

- **(B) d = 2:** unidad de 12 px, control de 48; pasa M2 y perdió M4.
- **(C) d = 6:** unidad de 4 px, control de 20; M2 y `target-size` en rojo — 4 objetivos de 20 × 20 (ADR-014).
