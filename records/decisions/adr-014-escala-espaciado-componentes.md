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

Las celdas medibles son lo que cada regla produce: dicen `pending: measured when run` y se llenan corriendo la regla, sin tocar criterio ni parámetro.

| Criterio | Estrato | Escala (A) 1.25 | Escala (B) 1.5 | Escala (C) 1.2, fechas abajo |
|---|---|---|---|---|
| M1 · piso y colapso | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| M3 · regeneración | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| M4 · una jerarquía | `judgement` | pendiente de la lámina | pendiente de la lámina | pendiente de la lámina |

| Criterio | Estrato | Espaciado (A) d = 3 | Espaciado (B) d = 2 | Espaciado (C) d = 6 |
|---|---|---|---|---|
| M2 · controles ≥ 44 × 44 | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| `target-size` (SC 2.5.8) | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| M3 · regeneración y `provenance` | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| `contrast` de los componentes | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| M4 · una familia | `judgement` | pendiente de la lámina | pendiente de la lámina | pendiente de la lámina |

## Decision

Sin resolver.

## Consequences

Se escriben al decidir.

## Alternatives considered

Las candidatas de arriba; las que pierdan se registran aquí con su razón.
