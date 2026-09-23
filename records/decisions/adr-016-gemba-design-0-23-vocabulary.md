---
type: adr
id: ADR-016
title: "La identidad de Orquídea en el vocabulario de gemba-design 0.23.0"
status: proposed
date: 2026-09-23
epic: —
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-016: La identidad de Orquídea en el vocabulario de gemba-design 0.23.0

## Status

Proposed.

## Context

**La pregunta:** con el vocabulario de gemba-design 0.23.0, ¿cómo declara la identidad de Orquídea cada dimensión del catálogo de interfaz, qué valor toma cada una que la hoja ya usa sin declarar, y qué cambia al recalcular la cadena?

Historia s1, standalone. La técnica `ui` de 0.23.0 añade tres cosas:

- el catálogo cerrado de dimensiones (`conventions/interface-dimensions.md`), que pide responder cada una: declarada, o "no aplica, porque…";
- un generador (`skills/techniques/ui/scripts/design-md.py`) que acepta identificadores con letras de cualquier escritura, una tabla de radio `Level | Value` y propiedades de componente fuera del vocabulario, estas con advertencia contada;
- el formato `decision: ADR-{NNN}` en las piezas, que lee `precedence.py`.

Leído en la historia (sondas de la survival-review del 2026-09-23 y recorrido de `identidad.css`):

- `{stroke.*}` sale `refused`: el formato no tiene grupo de grosores;
- el generador dice "Radius, elevation and motion are not derived" y pone la iconografía en sus Known Gaps;
- `tokens.py targets` solo mide objetivos con `height`/`width` literales, y su umbral está fijo en 24 px;
- la hoja ya decide radio (`border-radius: 0`), trazo (1 y 2 px), elevación (la tarjeta es `superficie` con borde sobre `fondo`), retícula (una columna) y densidad (una sola), y no pone tope a la medida.

### Lo que este registro reemplaza

ADR-013, ADR-014 y ADR-015 siguen `accepted`. Este registro no los sustituye enteros: la técnica `adr` solo sabe sustituir un registro completo, y el resto de cada uno sigue en pie (decidido por el humano el 2026-09-23; el hueco del método va al parking lot). Reemplaza solo estas decisiones:

- **ADR-014, decisión 6** — los identificadores de token en ASCII;
- **ADR-014, el `--gap` de bordes** — "los bordes son tokens de `colors` sin componente";
- **ADR-014, decisión 3, en lo que toca a `height`/`width` como ancho mínimo** — según la opción de mínimo de control que se elija abajo;
- **ADR-015, decisión 3** — esquinas rectas sin token: la decisión se mantiene, y deja de vivir solo en la prosa.

### Tokens en español

El generador de 0.23.0 acepta `{colors.acción-fondo}` (sonda: exit 0; `pairs` 8, 0 bajo; `targets` 4, 0 bajo; `provenance` 12, 0 fuera). La lengua declarada del proyecto es el español de México.

**Decisión (aprobada por el humano el 2026-09-23 con el alcance):** los roles se nombran `línea`, `acción-fondo`, `acción-texto` y `acción-presionada`, en `semantics.md`, `components.md`, `DESIGN.md` y la hoja (`--colors-línea`, …). Los valores no cambian.

Opciones rechazadas:
- **Conservar el ASCII:** el único motivo era el límite del generador, que ya no existe.
- **Renombrar también la clase HTML `accion`:** es un selector, no un token; renombrarla toca quince enlaces sin mover nada de la identidad.

### Criterios de la pieza

Aprobados por el humano el 2026-09-23, antes de producir ningún valor.

| # | Criterio | Dimensión | Estrato | From |
|---|----------|-----------|---------|------|
| V1 | Las catorce dimensiones del catálogo con destino `ui` tienen respuesta en un entregable: declarada (con referencia a un token, o con su valor y su fuente), o "no aplica, porque…". Un script las cuenta y sale en rojo con una sin respuesta o con población cero | todas | `mechanical` — `scripts/comprobar-dimensiones.py` | este eslabón |
| V2 | Cada control declarado llega a 44 × 44 px CSS en su mínimo, medido recalculando desde lo que declara `DESIGN.md` (`minWidth`/`minHeight`, o la tabla `Target`). Fuente: WCAG 2.2 SC 2.5.5 Target Size (Enhanced), AAA | `control-size` | `mechanical` — `scripts/comprobar-medidas.py objetivos --minimo 44` | ADR-014 M2 |
| V3 | El texto corrido de una ficha se lee sin que el renglón cruce la pantalla de escritorio, y a 360 px no cambia nada | `measure` | `judgement` — elección forzada entre las candidatas de medida, renderizadas a 1280 y a 360 px con la ficha de un ejemplar con notas largas | concept (ADR-010, S3) |
| V4 | Esquinas, trazos y planos se leen como el Cuaderno de campo: papel y tinta, sin sombra de pantalla | `corner-radius`, `stroke`, `elevation` | `judgement` — elección forzada entre las candidatas de elevación, sobre la colección con tres tarjetas a 360 px | concept (ADR-010) |

**Del catálogo, aplicados (no propuestos):**
- `contrast` y `component-contrast`: recalculados sobre los roles renombrados, con `contraste-de-lectura.py` (7:1, commission 2) y `tokens.py pairs`.
- `target-size`: WCAG 2.2 SC 2.5.8, con `tokens.py targets` si queda tabla `Target`. Si no queda, se dice y lo cubre V2, que es más estricto.
- `provenance`: `tokens.py provenance` sobre `DESIGN.md`.
- `minimum-size`: el piso de 16 px (M1 de ADR-014), sin cambio.

`platform-specs`, `single-ink` y `prior-art` no aplican, igual que en e5.

### Las catorce dimensiones

Respuesta propuesta. Una dimensión que el formato de `DESIGN.md` no lleva se declara en `components.md` y va como `--gap` en el generador.

| Dimensión | Respuesta propuesta | Dónde |
|---|---|---|
| `color-ramp` | declarada: la regla de anclas en OKLCH | ADR-013, `primitives.md` |
| `color-roles` | declarada: trece roles, ahora en español | ADR-013 y este, `semantics.md` |
| `type-scale` | declarada: razón 1.25, 16/20/25 | ADR-014, `type-scale.md` |
| `spacing` | declarada: unidad de 8 px, pasos 1, 2, 3, 4, 6 | ADR-014, `spacing.md` |
| `control-size` | declarada: mínimo de 48 × 48, según la opción elegida abajo | este, `components.md` |
| `composition` | declarada: diez componentes | ADR-014, `components.md` |
| `interaction-states` | declarada: `boton-presionado` como componente; foco como anillo de 2 px de `foco` (sin componente en el formato) | ADR-014, ADR-015, `components.md` |
| `corner-radius` | declarada: un nivel, `recto: 0px`, citado por `boton`, `boton-presionado`, `campo` y `tarjeta` | este, `components.md` |
| `stroke` | declarada: 1 px en bordes y separadores, 2 px en el anillo de foco (SC 2.4.13, AAA), con su valor; `--gap` | ADR-015, este, `components.md` |
| `elevation` | declarada: dos planos, base (`fondo`) y elevado (tarjeta), según la opción elegida abajo; `--gap` | este, `components.md` |
| `grid` | declarada: una columna, margen lateral de `spacing.step-2`; `--gap` | este, `components.md` |
| `measure` | declarada según la opción elegida abajo; `--gap` | este, `components.md` |
| `density` | no aplica, porque hay una sola densidad y ningún control baja de su mínimo | `components.md` |
| `iconography` | no aplica, porque la interfaz no usa íconos (no-go del brief de e5) | `components.md` |

### Parámetros fijados

- **Radio:** tabla `Level | Value | Where` con una fila, `recto | 0px`. La hoja la usa como `var(--rounded-recto)`.
- **Color de borde:** columna `borderColor` en `campo` (`{colors.campo-borde}`) y en `tarjeta` (`{colors.línea}`). `error` como borde se sigue midiendo en `semantics.md`, y `components.md` dice que ningún componente lo usa: ninguna plantilla marca un campo inválido.
- **Respaldo:** ninguno. Un control bajo su mínimo, una dimensión sin respuesta o un valor fuera de escala dejan la regla en rojo.

### Candidatas

**Mínimo de control** (`boton`, `boton-presionado`, `campo`, `enlace-navegacion`):
- **(A) Fijo, como hoy:** `height` y `width` = `{spacing.step-6}`.
- **(B) Solo mínimo:** `minHeight` y `minWidth` = `{spacing.step-6}`, sin `height`/`width`.
- **(C) Los dos:** `height`/`width` y `minHeight`/`minWidth`, todos `{spacing.step-6}`.

**Medida** (el `max-width` de `main`):
- **(A) Sin tope, como hoy.**
- **(B) `34em`.**
- **(C) `40em`.**

**Elevación** (cómo se aparta la tarjeta del papel):
- **(A) Tono y borde, como hoy:** `superficie` sobre `fondo`, con borde de 1 px `línea`.
- **(B) Solo tono:** `superficie` sobre `fondo`, sin borde.
- **(C) Solo borde:** fondo `fondo`, con borde de 1 px `línea`.

**Sangría de los enlaces `accion`** (parking lot de e5):
- **(A)** sin relleno horizontal fuera de la cabecera; el objetivo sigue en 48 por `min-width`.
- **(B)** como está: 8 px de relleno a cada lado.

**El botón de Acceso:** los controles se envuelven en `<p>`, como en el resto de los formularios (`ejemplar.html`). Sin candidatas: es la forma que ya usa el código.

### La rejilla

Corridas el 2026-09-23 hacia el scratchpad (`$S`), con los nombres de e5 (el renombre es posterior y no cambia valores):
- Componentes de cada candidata de mínimo en `$S/comp-{A|B|C}.md`, y su `DESIGN.md` generado con `python3 $D/design-md.py --spec-version alpha --name Orquídea governance/identity/ui/semantics.md governance/identity/ui/type-scale.md governance/identity/ui/spacing.md $S/comp-{A|B|C}.md` (gemba-design 0.23.0).
- Medidas con `scripts/comprobar-medidas.py objetivos --minimo 44`, `tokens.py targets` y `provenance`. Las cifras se copiaron de la salida vista; criterios y parámetros sin tocar desde el commit que abrió este registro.

| Criterio | Estrato | Mínimo (A) fijo | Mínimo (B) solo mínimo | Mínimo (C) los dos |
|---|---|---|---|---|
| V2 · ≥ 44 × 44 | `mechanical` | sí — 4 objetivos, 0 bajo 44 px (`ran:`) | sí — 4 objetivos (los mínimos), 0 bajo 44 px (`ran:`) | sí — 8 objetivos (4 cajas y 4 mínimos), 0 bajo 44 px (`ran:`) |
| `target-size` (SC 2.5.8) | `mechanical` | sí — `targets: 4 target(s) judged, 0 below 24x24` (`ran:`) | **sin sujeto** — `targets: no subject — the file declares 0 targets`, exit 2 (`ran:`); lo cubre V2 | sí — 4, 0 (`ran:`) |
| `provenance` | `mechanical` | sí — 12 tokens, 0 fuera de escala (`ran:`) | sí — 12, 0 (`ran:`) | sí — 20, 0 (`ran:`) |
| Propiedades fuera del vocabulario (stderr del generador) | medido | 0 | 8 | 8 |

La (A) declara un ancho fijo de 48 px que la hoja no aplica: `min-width` deja crecer el botón con su texto ("Agregar una planta…"). La (C) declara dos veces lo mismo.

| Criterio | Estrato | Medida (A) sin tope | Medida (B) 34em | Medida (C) 40em |
|---|---|---|---|---|
| Caracteres por renglón a 1280 px (estimado: ancho del texto entre 8 px, el ancho medio de 0.5 em a 16 px; el texto mide 1280 − 2 × 16 px de margen) | medido, informativo | 156 | 68 | 80 |
| Caracteres por renglón a 360 px (mismo estimado; 328 px de texto) | medido, informativo | 41 | 41 | 41 |
| V3 · el renglón no cruza la pantalla | `judgement` | pending | pending | pending |

| Criterio | Estrato | Elevación (A) tono y borde | Elevación (B) solo tono | Elevación (C) solo borde |
|---|---|---|---|---|
| Contraste del borde `línea` sobre el plano vecino (`contrast.py`) | medido, informativo | 3.34:1 sobre `fondo`, 3.70:1 sobre `superficie` | — sin borde | 3.34:1 sobre `fondo` |
| Contraste `superficie` sobre `fondo` (`contrast.py`) | medido, informativo | 1.11:1 | 1.11:1 | — sin tono |
| V4 · papel y tinta | `judgement` | pending | pending | pending |

La tarjeta no es un componente interactivo, así que `component-contrast` (SC 1.4.11) no la obliga. Las cifras dicen lo que aparta cada plano, no un umbral. Con la (B), 1.11:1 es todo lo que separa la hoja del papel.

| Criterio | Estrato | V1 · catorce dimensiones |
|---|---|---|
| Respondidas / sin respuesta | `mechanical` | 14 juzgadas, 0 sin respuesta, sobre la tabla propuesta en `$S/dimensiones.md` contra `conventions/interface-dimensions.md` de 0.23.0 (`ran:`) |

### Contraejemplos

- **V2 — rojo, visto, sobre la (B) con el mínimo de ancho de `enlace-navegacion` bajado a `{spacing.step-4}`:**

```
$ uv run python scripts/comprobar-medidas.py objetivos $S/DESIGN-B-bajo.md --minimo 44
…
enlace-navegacion mínimo 32×48  necesita 44×44  NO — enlace-navegacion: ancho bajo 44
4 objetivo(s) medidos, 1 bajo 44 px
exit=1
```

- **`provenance` — rojo, visto, sobre un `DESIGN.md` de la (B) editado a mano (`boton.minWidth` a 40px):**

```
$ python3 $G/tokens.py provenance $S/DESIGN-amano.md
provenance: 12 token(s) judged, 1 not from the declared scale
  components.boton.minWidth 40px names spacing.step-6 = 48px  FAIL
exit=1
```

- **V1 — rojo, visto, sobre la tabla propuesta sin la fila de `measure`:**

```
$ uv run python scripts/comprobar-dimensiones.py …/conventions/interface-dimensions.md $S/dimensiones-sin-measure.md
measure: sin respuesta  NO
14 dimensión(es) ui juzgada(s), 1 sin respuesta
exit=1
```

- **V3 y V4 — no aplica: no hay oráculo.** Se juzgan en elección forzada sobre las láminas.

## Decision

Sin resolver.

## Consequences

Se escriben al decidir.

## Alternatives considered

Se escriben al decidir.
