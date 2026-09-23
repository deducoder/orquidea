---
type: components
commission: "La identidad visual de la interfaz web de Orquídea: paleta, tipografía y la interfaz derivada de ellas"
derived-from: "governance/identity/ui/semantics.md, governance/identity/ui/type-scale.md, governance/identity/ui/spacing.md"
decision: ADR-014, ADR-016
date: 2026-09-22
---

# Orquídea — Components

## The criterion this answers

No se repite aquí: vive en `ADR-014`, abierto antes de que existiera cualquiera de los valores de abajo. Esta sección nombra el registro y nada más.

## The rule

Los componentes son los que usan hoy las plantillas. Cada uno es una composición de referencias: su fondo y su texto, a un rol de `semantics.md`; su tipografía, a un escalón de `type-scale.md`; su relleno y sus dimensiones, a un paso de `spacing.md`. Un control declara alto y ancho mínimo, los dos del paso de control. Una variante de estado es otro componente con nombre relacionado (`boton-presionado`), como pide el spec.

## The parameters

| Parameter | Value | Stratum | Alternatives it beat, and why each lost |
|-----------|-------|---------|------------------------------------------|
| conjunto de componentes | los diez de abajo | `judgement` | con `boton-secundario` y `boton-peligro` para "Quitar": ADR-010 deja un solo acento, y quitar se distingue por su texto y su página de confirmación; con `menu` o `pestañas`: las plantillas no los usan (biblioteca de componentes, rabbit hole del brief) |
| relleno de `tarjeta` y `boton` | paso 2 | `judgement` | paso 1: la tarjeta pega su texto al borde; paso 3: en 360 px el texto de la tarjeta pierde ancho |
| relleno de `campo` | paso 1 | `judgement` | paso 2: el texto del campo queda hundido y el alto de 48 no deja aire al interlineado de 24 |
| dimensiones de controles | alto y ancho mínimo = paso 6 | `mechanical` | paso 4 o 5 del espaciado (C): bajo 44 y bajo 24 (ADR-014) |
| bordes y foco | tokens de `colors` sin componente | `judgement` | `borderColor` en la tabla: el generador lo rechaza (fuera del vocabulario) y el spec solo lo acepta con advertencia |

## The components

| Component | backgroundColor | textColor | typography | padding | height | width |
|---|---|---|---|---|---|---|
| pagina | {colors.fondo} | {colors.texto} | {typography.step-0} | | | |
| tarjeta | {colors.superficie} | {colors.texto} | {typography.step-0} | {spacing.step-2} | | |
| titulo | {colors.fondo} | {colors.texto} | {typography.step-2} | | | |
| subtitulo | {colors.fondo} | {colors.texto} | {typography.step-1} | | | |
| boton | {colors.acción-fondo} | {colors.acción-texto} | {typography.step-0} | {spacing.step-2} | {spacing.step-6} | {spacing.step-6} |
| boton-presionado | {colors.acción-presionada} | {colors.acción-texto} | {typography.step-0} | {spacing.step-2} | {spacing.step-6} | {spacing.step-6} |
| campo | {colors.campo-fondo} | {colors.texto} | {typography.step-0} | {spacing.step-1} | {spacing.step-6} | {spacing.step-6} |
| enlace-navegacion | {colors.fondo} | {colors.enlace} | {typography.step-0} | | {spacing.step-6} | {spacing.step-6} |
| aviso | {colors.fondo} | {colors.error} | {typography.step-0} | | | |
| fecha | {colors.superficie} | {colors.texto-secundario} | {typography.step-0} | | | |

`rounded` no se compone: el generador lo declara no derivado. `DESIGN.md` se genera de esta tabla y de las de `semantics.md`, `type-scale.md` y `spacing.md`, nunca a mano.

## The components, measured

`ran:` sobre `governance/identity/ui/DESIGN.md`: `uv run python scripts/contraste-de-lectura.py` (texto a 7:1), `python3 $G/tokens.py pairs`, `targets` y `provenance`, y `uv run python scripts/comprobar-medidas.py objetivos --minimo 44`. Salidas copiadas abajo.

| Component | Text over background | Ratio and the need | Target, both dimensions | Held |
|-----------|----------------------|--------------------|-------------------------|------|
| pagina | texto sobre fondo | 15.35:1, necesita 7:1 | not declared | sí |
| tarjeta | texto sobre superficie | 17.00:1, necesita 7:1 | not declared | sí |
| titulo | texto sobre fondo | 15.35:1, necesita 7:1 | not declared | sí |
| subtitulo | texto sobre fondo | 15.35:1, necesita 7:1 | not declared | sí |
| boton | acción-texto sobre acción-fondo | 11.48:1, necesita 7:1 | 48 × 48, necesita 44 × 44 (M2) y 24 × 24 (SC 2.5.8) | sí |
| boton-presionado | acción-texto sobre acción-presionada | 14.95:1, necesita 7:1 | 48 × 48, ídem | sí |
| campo | texto sobre campo-fondo | 17.00:1, necesita 7:1 | 48 × 48, ídem | sí |
| enlace-navegacion | enlace sobre fondo | 10.37:1, necesita 7:1 | 48 × 48, ídem | sí |
| aviso | error sobre fondo | 8.38:1, necesita 7:1 | not declared | sí |
| fecha | texto-secundario sobre superficie | 9.49:1, necesita 7:1 | not declared | sí |

**Components measured:** 10 — 8 pares distintos de texto (`contraste-de-lectura.py`: `8 par(es) de texto juzgado(s), 0 bajo el umbral`; `tokens.py pairs`: `8 pair(s) judged, 0 below threshold`), 4 objetivos (`targets: 4 target(s) judged, 0 below 24x24`; `comprobar-medidas.py`: `4 objetivo(s) medidos, 0 bajo 44 px`), 12 tokens de medida (`provenance: 12 token(s) judged, 0 not from the declared scale`).

## How it answers the survival criteria

| Criterion | How this answers it |
|-----------|---------------------|
| `platform-specs` | no aplica, porque no se entrega una marca ni un ícono de plataforma (ADR-009) |
| `minimum-size` | todo componente usa un escalón de `type-scale.md` de 16 px o más |
| `single-ink` | no aplica, porque es propiedad de una marca y este encargo no tiene marca (ADR-009) |
| `contrast` | los 8 pares de texto que `DESIGN.md` deriva de los componentes, medidos arriba contra 7:1 |
| `prior-art` | no aplica, porque no se entrega marca ni se registra nada (ADR-009) |
| `component-contrast` | los bordes, el foco y el fondo de los botones contra `fondo` y `superficie` los midió `semantics.md` (12 pares, el más bajo 3.34:1); no son pares que el formato componga |
| `target-size` | 4 controles, 48 × 48, sobre 24 × 24 (arriba) |
| `provenance` | cada celda es una referencia; `design-md.py` rechaza un literal (ADR-014) y `provenance` sobre `DESIGN.md` sale con 0 fuera de escala |

## How it answers the fitness criteria

| Criterion, as approved | From | Stratum | How this answers it |
|------------------------|------|----------|----------|
| M2 · controles ≥ 44 × 44 | concept (ADR-010) | `mechanical` | sí — arriba |
| M3 · referenciado | este eslabón | `mechanical` | sí — `provenance` arriba |
| M4 · una familia | concept (ADR-010) | `judgement` | sí, para (A)·(A) — abajo |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| M4 — los componentes se leen como una familia del Cuaderno de campo | sí, para la escala (A) con el espaciado (A) | Daniel Efraín Domínguez Urbina, 2026-09-22, en elección forzada entre A·A, A·B, B·A y B·B (escala · espaciado) sobre la lámina de la ficha y el formulario de alta a 360 px |

## What was not measured

Los estados que solo muestra una interfaz renderizada: el anillo de `foco` sobre un `boton` del mismo azul (lo separa un espacio de fondo que fija s5.7), el `boton-presionado` en un teléfono real, el componente con el espaciado de texto del propio usuario y el zoom. Que un `aviso` no dependa solo de su color (WCAG 1.4.1): lleva texto y va antes del formulario; lo confirma s5.7 en las plantillas.

## What was tried and rejected

- **Con el espaciado (C):** los cuatro controles a 20 × 20 (M2 y `target-size` en rojo, ADR-014).
- **`campo` con relleno escrito como `10px`:** `design-md.py` lo rechaza, porque una celda es una referencia (ADR-014).
- **La escala (B) y el espaciado (B):** pasan lo medido y perdieron M4.
