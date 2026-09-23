---
type: adr
id: ADR-013
title: "Roles de color de la interfaz de Orquídea"
status: proposed
date: 2026-09-22
epic: e5
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-013: Roles de color de la interfaz de Orquídea

## Status

Proposed.

## Context

**La pregunta:** ¿con qué regla salen, de la paleta de ADR-012, las rampas de color (primitivas) y los roles por función de la interfaz (roles semánticos), de modo que cada valor se reproduzca corriendo la regla y cada par se mida en su valor real?

Dos eslabones de la técnica `ui` (gemba-design 0.21.0) en un solo registro: *colour primitives* y *semantic roles*. La paleta no declara variante (ADR-012), así que la relación de invariancia no tiene sujeto: se reporta como no comparada. Todo texto es normal (16 px, ADR-011). Medido con `tokens.py pairs` sobre `palette.md` antes de abrir este registro: `renglón` sobre `papel` da 3.34:1 y sobre `hoja` 3.70:1, contra 3:1 — el margen fino de la paleta.

### Criterios de la pieza

Aprobados por el humano el 2026-09-22, antes de producir ningún valor.

| # | Criterio | Eslabón | Estrato | From |
|---|----------|---------|---------|------|
| R1 | Cada par de texto de los roles semánticos, sobre `papel` y sobre `hoja`, llega a ≥ 7:1 | semántico | `mechanical` — `scripts/contraste-de-lectura.py` | commission 2 |
| R2 | Todo valor es reproducible: `scripts/derivar-primitivas.py` con los parámetros registrados regenera `primitives.md` idéntico, y cada rol semántico es un escalón de una rampa (`tokens.py provenance`, 0 fuera de escala) | ambos | `mechanical` | este eslabón |
| R3 | Los roles añadidos (botón, campo, foco, presionado) se leen como parte del Cuaderno de campo, y el azul sigue siendo una sola familia a lo largo de su rampa | ambos | `judgement` — elección forzada entre las reglas que pasen R1 y R2, sobre una lámina con el formulario de alta (campo, campo con error, botón, botón presionado, foco, enlace, texto secundario) en `papel` y en `hoja` | concept (ADR-010) |

**Del catálogo, aplicados (no propuestos):** `contrast` (subsumido por R1: 7:1 está sobre 4.5:1); `component-contrast` (`línea`, `campo-borde`, `acción-fondo`, `acción-presionada`, `foco` y `error` como borde, contra `papel` y contra `hoja`, a la cifra del catálogo leída el día que se mide, con `tokens.py pairs`); `provenance` (R2). `platform-specs`, `minimum-size`, `single-ink`, `prior-art` y `target-size` no aplican a estas piezas; el porqué va en cada entregable.

### Roles por función

Aprobados con los criterios. Cada uno es, en cada contexto (`papel`, `hoja`), una referencia al escalón que tomó su rol de identidad:

| Rol | Rol de identidad | Pares que se miden |
|-----|------------------|--------------------|
| `fondo` | `papel` | — |
| `superficie` | `hoja` | — |
| `texto` | `tinta` | text sobre `fondo` y `superficie` |
| `texto-secundario` | `tinta suave` | text sobre `fondo` y `superficie` |
| `enlace` | `acento` | text sobre `fondo` y `superficie` |
| `error` | `alerta` | text sobre `fondo` y `superficie`; component (borde de campo) sobre ambos |
| `línea` | `renglón` | component sobre `fondo` y `superficie` |
| `campo-fondo` | `hoja` | — |
| `campo-borde` | `renglón` | component sobre `fondo` y `superficie` |
| `acción-fondo` | `acento` | component sobre `fondo` y `superficie` |
| `acción-texto` | `hoja` | text sobre `acción-fondo` y sobre `acción-presionada` |
| `acción-presionada` | — no lo trae: **el escalón siguiente más oscuro** de la rampa de `acción-fondo` | component sobre `fondo` y `superficie` |
| `foco` | `acento` | component sobre `fondo` y `superficie` |

### Parámetros comunes a las tres reglas

- **Rampas:** tres. `neutro` (roles `hoja`, `papel`, `renglón`, `tinta suave`, `tinta`), `azul` (`acento`), `rojo` (`alerta`).
- **Escalones:** doce por rampa, nombrados `0, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950`; el nombre de la primitiva es `{rampa}-{escalón}` (`azul-700`).
- **Luminosidad de la rejilla:** el escalón `i` (0 a 11) tiene luminosidad `1 − i · (1 − 0.20) / 11` en la escala de la regla (L de OKLCH en A y B; L de HSL en C). El escalón 0 es blanco en las tres.
- **Gama:** un color fuera de sRGB conserva L y h y reduce su croma (bisección, tolerancia 1e-4) hasta entrar. El hex se redondea al entero de 8 bits más cercano.
- **Asignación de un rol de identidad:** al escalón de su rampa con la luminosidad más cercana a la suya; en empate, el más oscuro (no rebaja el contraste del texto). Dos roles no comparten escalón: el segundo toma el libre más cercano.
- **Respaldo:** ninguno. Un rol que en su escalón no llega a su umbral deja la regla en rojo; no se desplaza a otro escalón que cumpla, porque ese desplazamiento esconde el rojo que la regla causó.
- **Desvío:** ΔE en OKLab (distancia euclidiana) entre el valor de identidad y la primitiva a la que resolvió.

### Candidatas

- **(A) Anclas en OKLCH.** Cada rampa pasa por sus roles de identidad (las anclas) y por el blanco del escalón 0. Cada ancla reemplaza al escalón que le toca por la asignación, con su valor exacto. Entre dos anclas, L sigue la rejilla y C y h se interpolan linealmente en L (h por el arco corto; un ancla sin croma toma el h de la otra). Por debajo del ancla más oscura, C y h del ancla más oscura, con la gama recortada.
- **(B) Uniforme en OKLCH.** L de la rejilla; C y h constantes, los de la fuente de la rampa: `renglón` para `neutro`, `acento` para `azul`, `alerta` para `rojo`; gama recortada.
- **(C) Uniforme en HSL.** L de HSL de la rejilla; H y S constantes, los de la misma fuente que en (B).

### La rejilla

Las celdas medibles son lo que cada regla produce: `pending: measured when run`, se llenan corriendo la regla, sin tocar criterio ni parámetro.

| Criterio | Estrato | (A) Anclas OKLCH | (B) Uniforme OKLCH | (C) Uniforme HSL |
|---|---|---|---|---|
| R1 · texto ≥ 7:1 | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| `component-contrast` | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| R2 · reproducible y desde un escalón | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| Desvío máximo de un rol de identidad | medido, informativo | pending: measured when run | pending: measured when run | pending: measured when run |
| R3 · se lee como Cuaderno de campo | `judgement` | pendiente de la lámina | pendiente de la lámina | pendiente de la lámina |

## Decision

Sin resolver.

## Consequences

Se escriben al decidir.

## Alternatives considered

Las candidatas (A), (B) y (C) de arriba; las que pierdan se registran aquí con su razón.
