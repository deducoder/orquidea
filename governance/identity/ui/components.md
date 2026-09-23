---
type: components
commission: "La identidad visual de la interfaz web de Orquídea: paleta, tipografía y la interfaz derivada de ellas"
derived-from: "governance/identity/ui/semantics.md, governance/identity/ui/type-scale.md, governance/identity/ui/spacing.md"
decision: ADR-014, ADR-016
date: 2026-09-22
---

# Orquídea — Components

## The criterion this answers

No se repite aquí: vive en `ADR-014` y en `ADR-016`, cada uno abierto antes de que existieran los valores que decide. Esta sección nombra los registros y nada más.

## The rule

Los componentes son los que usan hoy las plantillas. Cada uno es una composición de referencias: su fondo y su texto, a un rol de `semantics.md`; su tipografía, a un escalón de `type-scale.md`; su relleno y sus dimensiones, a un paso de `spacing.md`. Un control declara su alto y su ancho mínimos (`minHeight`, `minWidth`), los dos del paso de control; una forma con esquinas cita un nivel de `rounded`, y un componente con borde cita su color con `borderColor` (ADR-016). Una variante de estado es otro componente con nombre relacionado (`boton-presionado`), como pide el spec.

## The parameters

| Parameter | Value | Stratum | Alternatives it beat, and why each lost |
|-----------|-------|---------|------------------------------------------|
| conjunto de componentes | los diez de abajo | `judgement` | con `boton-secundario` y `boton-peligro` para "Quitar": ADR-010 deja un solo acento, y quitar se distingue por su texto y su página de confirmación; con `menu` o `pestañas`: las plantillas no los usan (biblioteca de componentes, rabbit hole del brief) |
| relleno de `tarjeta` y `boton` | paso 2 | `judgement` | paso 1: la tarjeta pega su texto al borde; paso 3: en 360 px el texto de la tarjeta pierde ancho |
| relleno de `campo` | paso 1 | `judgement` | paso 2: el texto del campo queda hundido y el alto de 48 no deja aire al interlineado de 24 |
| dimensiones de controles | `minHeight` y `minWidth` = paso 6 | `mechanical` | paso 4 o 5 del espaciado (C): bajo 44 y bajo 24 (ADR-014); `height`/`width` fijos: declaran un ancho que la hoja no aplica (`min-width` deja crecer el botón con su texto); los dos a la vez: la misma medida dos veces (ADR-016) |
| color de borde | `borderColor` en `campo` (`campo-borde`) | `judgement` | tokens de `colors` sin componente: era un rodeo del generador de 0.21.0, que rechazaba la columna (ADR-014); 0.23.0 la acepta con advertencia contada (ADR-016) |
| foco | el rol `foco`, sin componente | `judgement` | un componente `foco`: el formato no tiene estado de foco que componer; el anillo lo dibuja la hoja (ADR-015) |
| radio | un nivel, `recto` | `judgement` | sin token, solo en la prosa de ADR-015: la decisión no se veía en `DESIGN.md`; esquinas redondeadas: ninguna regla publicada deriva un radio, y una libreta de campo tiene esquinas rectas (ADR-015) |
| elevación | dos planos, separados solo por tono (`superficie` sobre `fondo`) | `judgement` | tono y borde, como en e5; solo borde (ADR-016, V4) |

## The corners

| Level | Value | Where |
|---|---|---|
| recto | 0px | botones, campos y tarjetas |

Un solo nivel: la decisión de ADR-015 (esquinas rectas), ahora como token. No hay regla que derive un radio de un atributo; el valor es una declaración y el generador lo sigue diciendo en sus huecos.

## The components

| Component | backgroundColor | textColor | typography | rounded | padding | borderColor | minHeight | minWidth |
|---|---|---|---|---|---|---|---|---|
| pagina | {colors.fondo} | {colors.texto} | {typography.step-0} | | | | | |
| tarjeta | {colors.superficie} | {colors.texto} | {typography.step-0} | {rounded.recto} | {spacing.step-2} | | | |
| titulo | {colors.fondo} | {colors.texto} | {typography.step-2} | | | | | |
| subtitulo | {colors.fondo} | {colors.texto} | {typography.step-1} | | | | | |
| boton | {colors.acción-fondo} | {colors.acción-texto} | {typography.step-0} | {rounded.recto} | {spacing.step-2} | | {spacing.step-6} | {spacing.step-6} |
| boton-presionado | {colors.acción-presionada} | {colors.acción-texto} | {typography.step-0} | {rounded.recto} | {spacing.step-2} | | {spacing.step-6} | {spacing.step-6} |
| campo | {colors.campo-fondo} | {colors.texto} | {typography.step-0} | {rounded.recto} | {spacing.step-1} | {colors.campo-borde} | {spacing.step-6} | {spacing.step-6} |
| enlace-navegacion | {colors.fondo} | {colors.enlace} | {typography.step-0} | | | | {spacing.step-6} | {spacing.step-6} |
| aviso | {colors.fondo} | {colors.error} | {typography.step-0} | | | | | |
| fecha | {colors.superficie} | {colors.texto-secundario} | {typography.step-0} | | | | | |

`borderColor`, `minHeight` y `minWidth` están fuera del vocabulario del formato: el generador de 0.23.0 los acepta y los cuenta en su salida, como pide el spec para una propiedad que no conoce. `error` como borde de campo se mide en `semantics.md`, pero ningún componente lo usa: ninguna plantilla marca un campo inválido (los errores son un párrafo `aviso`). `DESIGN.md` se genera de estas tablas y de las de `semantics.md`, `type-scale.md` y `spacing.md`, nunca a mano.

## The interface dimensions

Cada dimensión del catálogo de gemba-design 0.23.0 con destino `ui`, respondida (V1 de ADR-016). Las que el formato de `DESIGN.md` no lleva van también como hueco declarado en el generador.

| Dimension | Answer | Where |
|---|---|---|
| `color-ramp` | declarada: tres rampas de doce escalones, anclas en OKLCH | ADR-013, `primitives.md` |
| `color-roles` | declarada: trece roles por función, iguales en `papel` y en `hoja` | ADR-013, ADR-016, `semantics.md` |
| `type-scale` | declarada: razón 1.25 desde 16 px, tres escalones | ADR-014, `type-scale.md` |
| `spacing` | declarada: unidad de 8 px, pasos 1, 2, 3, 4 y 6 | ADR-014, `spacing.md` |
| `control-size` | declarada: mínimo de 48 × 48 (`minHeight`, `minWidth` = paso 6) | ADR-016, arriba |
| `composition` | declarada: los diez componentes de arriba | ADR-014, arriba |
| `interaction-states` | declarada: `boton-presionado` como componente; foco como anillo de 2 px del rol `foco`, que el formato no compone | ADR-014, ADR-015 |
| `corner-radius` | declarada: un nivel, `recto` | ADR-016, arriba |
| `stroke` | declarada: 1 px en el borde del campo y en los separadores de la cabecera y del historial, 2 px en el anillo de foco (WCAG 2.2 SC 2.4.13, AAA); el formato no tiene grosores | ADR-015, ADR-016 |
| `elevation` | declarada: dos planos, base (`fondo`) y elevado (la tarjeta, `superficie`), separados solo por tono; el formato no tiene elevación | ADR-016 (V4) |
| `grid` | declarada: una columna, con margen lateral de paso 2 | ADR-016 |
| `measure` | declarada: sin tope; el renglón ocupa el ancho de la página menos su margen. V3 no se cumple en escritorio y se eligió así | ADR-016 (V3) |
| `density` | no aplica, porque hay una sola densidad y ningún control baja de su mínimo | ADR-016 |
| `iconography` | no aplica, porque la interfaz no usa íconos (no-go del brief de e5) | ADR-016 |

## The components, measured

`ran:` sobre `governance/identity/ui/DESIGN.md`, regenerado con gemba-design 0.23.0 (ADR-016): `uv run python scripts/contraste-de-lectura.py` (texto a 7:1), `python3 $G/tokens.py pairs`, `targets` y `provenance`, y `uv run python scripts/comprobar-medidas.py objetivos --minimo 44`, que lee los mínimos declarados. Salidas copiadas abajo.

| Component | Text over background | Ratio and the need | Target, both dimensions | Held |
|-----------|----------------------|--------------------|-------------------------|------|
| pagina | texto sobre fondo | 15.35:1, necesita 7:1 | not declared | sí |
| tarjeta | texto sobre superficie | 17.00:1, necesita 7:1 | not declared | sí |
| titulo | texto sobre fondo | 15.35:1, necesita 7:1 | not declared | sí |
| subtitulo | texto sobre fondo | 15.35:1, necesita 7:1 | not declared | sí |
| boton | acción-texto sobre acción-fondo | 11.48:1, necesita 7:1 | mínimo 48 × 48, necesita 44 × 44 (V2, que cubre también los 24 × 24 de SC 2.5.8) | sí |
| boton-presionado | acción-texto sobre acción-presionada | 14.95:1, necesita 7:1 | 48 × 48, ídem | sí |
| campo | texto sobre campo-fondo | 17.00:1, necesita 7:1 | 48 × 48, ídem | sí |
| enlace-navegacion | enlace sobre fondo | 10.37:1, necesita 7:1 | 48 × 48, ídem | sí |
| aviso | error sobre fondo | 8.38:1, necesita 7:1 | not declared | sí |
| fecha | texto-secundario sobre superficie | 9.49:1, necesita 7:1 | not declared | sí |

**Components measured:** 10 — 8 pares distintos de texto (`contraste-de-lectura.py`: `8 par(es) de texto juzgado(s), 0 bajo el umbral`; `tokens.py pairs`: `8 pair(s) judged, 0 below threshold`), 4 objetivos por su mínimo declarado (`comprobar-medidas.py`: `4 objetivo(s) medidos, 0 bajo 44 px`), 12 tokens de medida (`provenance: 12 token(s) judged, 0 not from the declared scale`) y 14 dimensiones (`comprobar-dimensiones.py` contra `conventions/interface-dimensions.md` de 0.23.0: `14 dimensión(es) ui juzgada(s), 0 sin respuesta`).

**`tokens.py targets` no tiene sujeto:** `targets: no subject — the file declares 0 targets, so nothing was judged` (exit 2). Solo mide una caja literal (`height`/`width`), y los controles declaran su mínimo. No se reporta como pase: los objetivos los mide `comprobar-medidas.py`, a 44 px, sobre el umbral de 24 de SC 2.5.8.

**Recalculado contra e5:** las cifras de texto (8 pares, el más bajo 8.38:1), de medida (12 tokens) y de objetivos (4 a 48 × 48) son las mismas. Lo único que cambió es qué instrumento mide los objetivos.

## How it answers the survival criteria

| Criterion | How this answers it |
|-----------|---------------------|
| `platform-specs` | no aplica, porque no se entrega una marca ni un ícono de plataforma (ADR-009) |
| `minimum-size` | todo componente usa un escalón de `type-scale.md` de 16 px o más |
| `single-ink` | no aplica, porque es propiedad de una marca y este encargo no tiene marca (ADR-009) |
| `contrast` | los 8 pares de texto que `DESIGN.md` deriva de los componentes, medidos arriba contra 7:1 |
| `prior-art` | no aplica, porque no se entrega marca ni se registra nada (ADR-009) |
| `component-contrast` | los bordes, el foco y el fondo de los botones contra `fondo` y `superficie` los midió `semantics.md` (12 pares, el más bajo 3.34:1); no son pares que el formato componga |
| `target-size` | 4 controles con mínimo de 48 × 48, sobre 24 × 24; los mide `comprobar-medidas.py`, porque `tokens.py targets` no lee los mínimos (arriba) |
| `provenance` | cada celda es una referencia; `design-md.py` rechaza un literal (ADR-014) y `provenance` sobre `DESIGN.md` sale con 0 fuera de escala |

## How it answers the fitness criteria

| Criterion, as approved | From | Stratum | How this answers it |
|------------------------|------|----------|----------|
| M2 · controles ≥ 44 × 44 | concept (ADR-010) | `mechanical` | sí — arriba |
| M3 · referenciado | este eslabón | `mechanical` | sí — `provenance` arriba |
| M4 · una familia | concept (ADR-010) | `judgement` | sí, para (A)·(A) — abajo |
| V1 · catorce dimensiones respondidas | este eslabón (ADR-016) | `mechanical` | sí — 14, 0 sin respuesta (arriba) |
| V2 · mínimos ≥ 44 × 44 | ADR-014 M2 | `mechanical` | sí — 4, 0 bajo 44 px (arriba) |
| V3 · el renglón no cruza la pantalla de escritorio | concept (ADR-010, S3) | `judgement` | **no** — se eligió "sin tope" de todos modos (abajo) |
| V4 · esquinas, trazos y planos como papel y tinta | concept (ADR-010) | `judgement` | sí, para "solo tono" (abajo) |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| M4 — los componentes se leen como una familia del Cuaderno de campo | sí, para la escala (A) con el espaciado (A) | Daniel Efraín Domínguez Urbina, 2026-09-22, en elección forzada entre A·A, A·B, B·A y B·B (escala · espaciado) sobre la lámina de la ficha y el formulario de alta a 360 px |
| V3 — el renglón de la ficha no cruza la pantalla de escritorio | no se cumple con "sin tope"; se elige de todos modos | Daniel Efraín Domínguez Urbina, 2026-09-23, en elección forzada entre sin tope, 34em y 40em sobre la ficha a 1280 y a 360 px |
| V4 — esquinas, trazos y planos se leen como papel y tinta | sí, para "solo tono" | Daniel Efraín Domínguez Urbina, 2026-09-23, en elección forzada entre tono y borde, solo tono y solo borde sobre la colección a 360 px |
| Criterio 3 de ADR-009 — la foto del ejemplar es la protagonista y la paleta no compite con la flor, sobre la interfaz vestida (foto a todo el ancho en la ficha, miniatura de 96 px en la colección) | sí | Daniel Efraín Domínguez Urbina, 2026-09-23, sobre capturas a 360 px de la app con tres fotos reales de *Laelia anceps*; quedó `unsigned` en e5 |
| Decisión 5 de ADR-015 — el subtítulo de 20 px en negrita se distingue del cuerpo de 16 px | sí; no hace falta el ajuste por espacio | Daniel Efraín Domínguez Urbina, 2026-09-23, sobre la ficha a 360 px (Foto, Riegos, Floraciones); quedó `unsigned` en e5 |

## What was not measured

Los estados que solo muestra una interfaz renderizada: el anillo de `foco` sobre un `boton` del mismo azul (lo separa un espacio de fondo que fija s5.7), el `boton-presionado` en un teléfono real, el componente con el espaciado de texto del propio usuario y el zoom. Que un `aviso` no dependa solo de su color (WCAG 1.4.1): lleva texto y va antes del formulario; lo confirma s5.7 en las plantillas.

## What was tried and rejected

- **Con el espaciado (C):** los cuatro controles a 20 × 20 (M2 y `target-size` en rojo, ADR-014).
- **`campo` con relleno escrito como `10px`:** `design-md.py` lo rechaza, porque una celda es una referencia (ADR-014).
- **La escala (B) y el espaciado (B):** pasan lo medido y perdieron M4.
- **`height`/`width` fijos, o fijos más mínimos:** pasan V2; declaran un ancho que la hoja no aplica (ADR-016).
- **Medida de 34em y de 40em:** cumplen V3 (unos 68 y 80 caracteres a 1280 px); no se eligieron (ADR-016).
- **La tarjeta con tono y borde, o solo con borde:** no se eligieron en V4 (ADR-016).
