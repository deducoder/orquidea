---
type: adr
id: ADR-014
title: "Escala tipográfica, espaciado y componentes de Orquídea"
status: proposed
date: 2026-09-22
epic: e5
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-014: Escala tipográfica, espaciado y componentes de Orquídea

## Status

Proposed.

## Context

**La pregunta:** ¿con qué reglas salen los tamaños de letra, los espacios y la composición de cada componente de la interfaz, sobre el espécimen (ADR-011) y los roles de color (ADR-013), para que s5.7 vista las plantillas desde un `DESIGN.md` generado y verificado?

Tres eslabones de la técnica `ui` (gemba-design 0.21.0) en un solo registro: *type scale*, *spacing* y *components*. El formato de `DESIGN.md` es el spec de google-labs-code/design.md, versión `alpha`, leído el 2026-09-22 (`docs/spec.md`). El generador es `skills/techniques/ui/scripts/design-md.py` del addon, invocado por su ruta.

Todo texto tiene un piso de 16 px (ADR-011), y la jerarquía la marcan peso, color y espacio más que tamaño. ADR-010 pide acciones grandes y navegación al pulgar.

### Identificadores de token en ASCII

`design-md.py` acepta solo referencias `^\{([a-z][A-Za-z0-9.-]*)\}$`. El spec no pone ese límite. Cuatro roles de `semantics.md` (s5.5) llevan acento, y un componente con `{colors.acción-fondo}` sale `refused` (exit 1).

**Decisión (aprobada por el humano el 2026-09-22 con el diseño):** los identificadores de token se escriben en ASCII: `linea`, `accion-fondo`, `accion-texto` y `accion-presionada`. `semantics.md` se re-deriva con esos nombres. Los roles, sus valores y ADR-013 no cambian: ADR-013 no cambia de opinión, solo de grafía de identificador. La prosa sigue en español con acentos.

Opciones rechazadas:
- **Mantener los acentos:** ni el botón ni la línea entrarían en `DESIGN.md`.
- **Copiar el generador y cambiar su expresión regular:** una segunda copia de un instrumento del addon, que el addon prohíbe.

El límite del generador va al parking lot como hallazgo del addon.

### Criterios de la pieza

Aprobados por el humano el 2026-09-22, antes de producir ningún valor.

| # | Criterio | Eslabón | Estrato | From |
|---|----------|---------|---------|------|
| M1 | Ningún escalón asignado a un rol de lectura (`text`, `binomial`, `date`) queda bajo 16 px, y ningún par de escalones colapsa en uno al redondear | escala | `mechanical` — `scripts/comprobar-medidas.py piso` | specimen (ADR-011) |
| M2 | Cada control declarado (`boton`, `boton-presionado`, `campo`, `enlace-navegacion`) mide al menos 44 × 44 px CSS. Fuente: WCAG 2.2 SC 2.5.5 Target Size (Enhanced), AAA | espaciado | `mechanical` — `scripts/comprobar-medidas.py objetivos --minimo 44` | concept (ADR-010) |
| M3 | Todo valor es reproducible y referenciado: `scripts/derivar-medidas.py` regenera las tablas de escala y de espaciado idénticas, y en `DESIGN.md` `tokens.py provenance` sale con 0 fuera de escala | los tres | `mechanical` | este eslabón |
| M4 | La escala se lee como una sola jerarquía con peso y espacio, y los componentes como una familia del Cuaderno de campo | escala, componentes | `judgement` — elección forzada sobre una lámina a 360 px con la ficha de un ejemplar y el formulario de alta | concept (ADR-010) |

**Del catálogo, aplicados (no propuestos):**
- `minimum-size`: el piso de 16 px del espécimen; lo comprueba M1.
- `contrast`: los pares `text` que `DESIGN.md` deriva de cada componente, con `tokens.py pairs` y `contraste-de-lectura.py` a 7:1 (commission 2).
- `component-contrast`: medido en s5.5 sobre los mismos roles; aquí se cita.
- `target-size`: WCAG 2.2 SC 2.5.8, con la cifra leída de la fuente el día que se mide y `tokens.py targets` sobre `DESIGN.md`.
- `provenance`: lo comprueba M3.

`platform-specs`, `single-ink` y `prior-art` no aplican; el porqué va en cada entregable.

### Componentes

Aprobados con los criterios. Cada celda es una referencia; `u` es la unidad del espaciado y `C` el tamaño de control de la candidata:

| Componente | backgroundColor | textColor | typography | padding | height | width |
|---|---|---|---|---|---|---|
| `pagina` | `fondo` | `texto` | cuerpo | — | — | — |
| `tarjeta` | `superficie` | `texto` | cuerpo | 2u | — | — |
| `titulo` | `fondo` | `texto` | escalón de `titulo` | — | — | — |
| `subtitulo` | `fondo` | `texto` | escalón de `subtitulo` | — | — | — |
| `boton` | `accion-fondo` | `accion-texto` | cuerpo | 2u | C | C |
| `boton-presionado` | `accion-presionada` | `accion-texto` | cuerpo | 2u | C | C |
| `campo` | `campo-fondo` | `texto` | cuerpo | 1u | C | C |
| `enlace-navegacion` | `fondo` | `enlace` | cuerpo | — | C | C |
| `aviso` | `fondo` | `error` | cuerpo | — | — | — |
| `fecha` | `superficie` | `texto-secundario` | cuerpo | — | — | — |

`width` es el ancho mínimo del objetivo. `rounded` no se compone: el generador lo declara no derivado. Los bordes (`campo-borde`, `linea`, `foco`, `error` como borde) son tokens de `colors` sin componente, porque el vocabulario del formato no tiene color de borde, y van como `--gap`. Los enlaces dentro de un párrafo quedan en la excepción *inline* de SC 2.5.8 y 2.5.5: se dice, no se supone.

### Parámetros comunes

- **Escala:**
  - El tamaño del escalón `n` es `16 · razón^n`, redondeado al entero de px más cercano (medio hacia arriba).
  - La altura de línea es el múltiplo de 4 px más cercano a `1.5 · tamaño` (medio hacia arriba).
  - Un escalón negativo se nombra `-1`.
  - Roles: `text`, `binomial` y `date` son de lectura; `titulo` (`h1`) y `subtitulo` (`h2`) son de énfasis (700).
- **Espaciado:**
  - La unidad `u` es la altura de línea del escalón 0 dividida entre `d`.
  - Los pasos son `m · u` para cada multiplicador `m` declarado, y se nombran por `m` (`6` es `6u`).
  - El tamaño de control `C` es `k · u`, y tiene que ser uno de los pasos.
- **Respaldo:** ninguno. Un escalón bajo el piso, dos escalones colapsados o un control bajo su mínimo dejan la regla en rojo; nada se desplaza a otro valor que cumpla.

### Candidatas

**Escala:**
- **(A) Razón 1.25:** escalones `0, 1, 2`. `text`, `binomial` y `date` van a `0`; `subtitulo` a `1`; `titulo` a `2`.
- **(B) Razón 1.5:** mismos escalones y misma asignación.
- **(C) Razón 1.2 con fechas un escalón abajo:** escalones `-1, 0, 1, 2`. `text` y `binomial` van a `0`, `date` a `-1`, `subtitulo` a `1` y `titulo` a `2`.

**Espaciado** (sobre la altura de línea del escalón 0, que es la misma en las tres escalas porque sale de 16 px):
- **(A)** `d = 3`, multiplicadores `1, 2, 3, 4, 6`, `C = 6u`.
- **(B)** `d = 2`, multiplicadores `1, 2, 3, 4`, `C = 4u`.
- **(C) Compacto:** `d = 6`, multiplicadores `1, 2, 3, 4, 5, 6`, `C = 5u`.

### La rejilla

Corridas el 2026-09-22 hacia el scratchpad (`$S`):
- Escala: `uv run python scripts/derivar-medidas.py escala --base 16 --razon {1.25|1.5|1.2} --escalones {0,1,2|-1,0,1,2} --roles …`.
- Espaciado: `… espaciado --base 16 --divisor {3|2|6} --multiplicadores … --control {6|4|5}`.
- Componentes: la tabla de arriba con esos pasos, y un `DESIGN.md` por espaciado, generado con `python3 $D/design-md.py --spec-version alpha --name Orquídea governance/identity/ui/semantics.md $S/escala-A.md $S/espaciado-{A|B|C}.md $S/componentes-{A|B|C}.md`.

Medidas con `scripts/comprobar-medidas.py`, `tokens.py targets`, `pairs` y `provenance` y `scripts/contraste-de-lectura.py`. Las cifras se copiaron de la salida vista, y los criterios y parámetros no se tocaron desde el commit que abrió este registro.

| Criterio | Estrato | Escala (A) 1.25 | Escala (B) 1.5 | Escala (C) 1.2, fechas abajo |
|---|---|---|---|---|
| Tamaños (px) y altura de línea | medido | 16/24, 20/32, 25/36 | 16/24, 24/36, 36/56 | 13/20, 16/24, 19/28, 23/36 |
| M1 · piso y colapso | `mechanical` | sí — 3 escalones y 3 roles de lectura medidos, 0 bajo el piso, 0 colapsados (`ran:`) | sí — 3 y 3, 0 y 0 (`ran:`) | **no** — 4 escalones y 3 roles medidos, 1 bajo el piso: `date` en el escalón -1 = 13px (`ran:`) |
| M3 · regeneración | `mechanical` | sí — la misma tabla al correr otra vez (`cmp`, `ran:`), y la prueba del script | sí — ídem, prueba del script | sí — ídem, prueba del script |
| M4 · una jerarquía | `judgement` | pendiente de la lámina | pendiente de la lámina | no se lleva a la lámina: falla M1 |

| Criterio | Estrato | Espaciado (A) d = 3 | Espaciado (B) d = 2 | Espaciado (C) d = 6 |
|---|---|---|---|---|
| Unidad, pasos y control | medido | 8px; 8, 16, 24, 32, 48; control 48 | 12px; 12, 24, 36, 48; control 48 | 4px; 4 a 24; control 20 |
| M2 · controles ≥ 44 × 44 | `mechanical` | sí — 4 objetivos, 0 bajo 44 px (`ran:`) | sí — 4, 0 bajo 44 px (`ran:`) | **no** — 4 objetivos, 4 bajo 44 px: todos 20×20 (`ran:`) |
| `target-size` (SC 2.5.8) | `mechanical` | sí — `targets`: 4 judged, 0 below 24x24 (`ran:`) | sí — 4, 0 (`ran:`) | **no** — 4 judged, 4 below 24x24 (`ran:`) |
| M3 · `provenance` | `mechanical` | sí — 12 tokens, 0 fuera de escala (`ran:`) | sí — 12, 0 (`ran:`) | sí — 12, 0 (`ran:`) |
| `contrast` de los componentes | `mechanical` | sí — 8 pares, 0 bajo 7:1; el más bajo, `error` sobre `fondo` 8.38:1 (`ran:`) | sí — los mismos 8 pares (`ran:`) | sí — los mismos 8 pares (`ran:`) |
| M4 · una familia | `judgement` | pendiente de la lámina | pendiente de la lámina | no se lleva a la lámina: falla M2 |

`design-md.py` sobre las tres combinaciones: 10 componentes, 8 pares, 4 objetivos, 0 literales en la prosa y 0 tablas `Component` ignoradas. Los tokens son 21, 20 y 22 (13 colores, 3 escalones y 5, 4 o 6 pasos).

### Contraejemplos

- **M1: rojo, visto, sobre la escala (C).**

```
$ uv run python scripts/comprobar-medidas.py piso $S/escala-C.md --piso 16 --lectura text,binomial,date
…
date: escalón -1 = 13px  piso 16px  NO
4 escalón(es) y 3 rol(es) de lectura medidos, 1 bajo el piso, 0 colapsado(s)
exit=1
```

- **M2 y `target-size`: rojo, visto, sobre el espaciado (C).**

```
$ uv run python scripts/comprobar-medidas.py objetivos $S/DESIGN-C.md --minimo 44
…
enlace-navegacion 20×20  necesita 44×44  NO — enlace-navegacion: ancho bajo 44, enlace-navegacion: alto bajo 44
4 objetivo(s) medidos, 4 bajo 44 px
exit=1
$ python3 $G/tokens.py targets $S/DESIGN-C.md
targets: 4 target(s) judged, 4 below 24x24
  boton 20x20  FAIL
…
exit=1
```

- **M3 (`provenance`): rojo, visto, dos veces.**
  - Sobre una muestra construida: el `campo` de (A) con `padding` escrito como el literal `10px`. El generador la rechaza antes de escribir nada:

```
$ python3 $D/design-md.py … $S/componentes-literal.md
refused: campo.padding is '10px': a component cell is a reference like {colors.text}
exit=1
```

  - Sobre un `DESIGN.md` de (A) editado a mano (la altura de `boton` a 40px):

```
$ python3 $G/tokens.py provenance $S/DESIGN-amano.md
provenance: 12 token(s) judged, 1 not from the declared scale
  components.boton.height 40px names spacing.step-6 = 48px  FAIL
exit=1
```

- **M3 (regeneración de las tablas):** su rojo es el de la prueba que compara `type-scale.md` y `spacing.md` con la salida del script. Esos archivos no existen antes de elegir, así que se ve al escribir la prueba en T4.
- **M4: no aplica, no hay oráculo.** Se juzga en elección forzada entre las combinaciones de (A) y (B) sobre la lámina.

## Decision

Sin resolver.

## Consequences

Se escriben al decidir.

## Alternatives considered

Las candidatas de arriba; las que pierdan se registran aquí con su razón.
