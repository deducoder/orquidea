---
type: semantics
commission: "La identidad visual de la interfaz web de Orquídea: paleta, tipografía y la interfaz derivada de ellas"
derived-from: "governance/identity/ui/primitives.md"
decision: ADR-013
date: 2026-09-22
---

# Orquídea — Semantic roles

## The criterion this answers

No se repite aquí: vive en `ADR-013`, abierto antes de que existiera cualquiera de los valores de abajo. Esta sección nombra el registro y nada más.

## The rule

Cada rol por función es, en cada contexto, una referencia al escalón que tomó un rol de la paleta en `primitives.md`. El único rol que la paleta no trae, `acción-presionada`, se resuelve relativo a uno que sí: el escalón siguiente más oscuro de la rampa de `acción-fondo`. Los contextos son los dos fondos de la aplicación, `papel` y `hoja`, y en los dos cada rol resuelve al mismo escalón. Ningún rol está fijado a su valor exacto: con la regla de anclas, cada rol de la paleta ya resuelve a él (desvío 0.000), así que fijarlo no cambiaría nada.

## The parameters

| Parameter | Value | Stratum | Alternatives it beat, and why each lost |
|-----------|-------|---------|------------------------------------------|
| conjunto de roles | los trece de la tabla de abajo | `judgement` | con éxito, aviso y deshabilitado: la interfaz no los usa (la aplicación confirma redirigiendo, no tiene controles deshabilitados); con un rol de acción destructiva en `alerta`: "Sí, quitar" ya se distingue por su texto y su página de confirmación, y ADR-010 deja un solo acento |
| contextos | `papel` y `hoja`, mismo escalón en los dos | `judgement` | un escalón distinto por fondo: ningún par lo necesita — el más bajo sobre `papel` pasa (3.34:1 en componente, 8.38:1 en texto) |
| resolución de `acción-presionada` | el escalón siguiente más oscuro de `acción-fondo` | `judgement` | el siguiente más claro: bajaría el contraste de `acción-texto` encima; un color distinto (la tinta): el botón presionado dejaría de ser azul |
| roles fijados | ninguno | `judgement` | fijar los siete de la paleta: con la regla de anclas el desvío ya es 0.000, y fijar escondería que la regla los reproduce |

## The roles

La tabla va en la forma de paleta que lee el instrumento de invariancia (`Role`, `Value`), con las columnas de este eslabón a la derecha. La variante: **ninguna declarada** (ADR-012), y por eso la tabla **no lleva columna `Variant`**: con la columna llena de `—`, `invariance.py` sale con 2 por un valor ilegible, no por falta de sujeto; sin ella, reporta lo que es cierto — no hay segundo lado que comparar.

| Role | Value | Resolves to | Identity value | Drift |
|------|-------|-------------|----------------|-------|
| fondo | #F7F3EA | `neutro-50` en `papel` y en `hoja` | `#F7F3EA` (papel) | 0.000 — el valor exacto |
| superficie | #FFFFFF | `neutro-0` en `papel` y en `hoja` | `#FFFFFF` (hoja) | 0.000 — el valor exacto |
| texto | #1E1C19 | `neutro-950` en `papel` y en `hoja` | `#1E1C19` (tinta) | 0.000 — el valor exacto |
| texto-secundario | #4A453E | `neutro-700` en `papel` y en `hoja` | `#4A453E` (tinta suave) | 0.000 — el valor exacto |
| enlace | #1F3A5F | `azul-800` en `papel` y en `hoja` | `#1F3A5F` (acento) | 0.000 — el valor exacto |
| error | #8A1C1C | `rojo-700` en `papel` y en `hoja` | `#8A1C1C` (alerta) | 0.000 — el valor exacto |
| línea | #8C8475 | `neutro-400` en `papel` y en `hoja` | `#8C8475` (renglón) | 0.000 — el valor exacto |
| campo-fondo | #FFFFFF | `neutro-0` en `papel` y en `hoja` | `#FFFFFF` (hoja) | 0.000 — el valor exacto |
| campo-borde | #8C8475 | `neutro-400` en `papel` y en `hoja` | `#8C8475` (renglón) | 0.000 — el valor exacto |
| acción-fondo | #1F3A5F | `azul-800` en `papel` y en `hoja` | `#1F3A5F` (acento) | 0.000 — el valor exacto |
| acción-texto | #FFFFFF | `neutro-0` en `papel` y en `hoja` | `#FFFFFF` (hoja) | 0.000 — el valor exacto |
| acción-presionada | #0C274A | `azul-900` en `papel` y en `hoja` | un rol que la identidad no trae | — (el escalón siguiente más oscuro de `acción-fondo`) |
| foco | #1F3A5F | `azul-800` en `papel` y en `hoja` | `#1F3A5F` (acento) | 0.000 — el valor exacto |

Cada valor es una referencia que resuelve a una primitiva: `tokens.py provenance` lo comprueba sobre esta tabla y la escala de `primitives.md`:

| Token | Value | From |
|---|---|---|
| fondo | #F7F3EA | neutro-50 |
| superficie | #FFFFFF | neutro-0 |
| texto | #1E1C19 | neutro-950 |
| texto-secundario | #4A453E | neutro-700 |
| enlace | #1F3A5F | azul-800 |
| error | #8A1C1C | rojo-700 |
| línea | #8C8475 | neutro-400 |
| campo-fondo | #FFFFFF | neutro-0 |
| campo-borde | #8C8475 | neutro-400 |
| acción-fondo | #1F3A5F | azul-800 |
| acción-texto | #FFFFFF | neutro-0 |
| acción-presionada | #0C274A | azul-900 |
| foco | #1F3A5F | azul-800 |

Los pares que declaran estos roles, en el formato que leen `scripts/contraste-de-lectura.py` y `tokens.py pairs`:

| Foreground | Ground | Kind |
|---|---|---|
| texto | fondo | text |
| texto | superficie | text |
| texto-secundario | fondo | text |
| texto-secundario | superficie | text |
| enlace | fondo | text |
| enlace | superficie | text |
| error | fondo | text |
| error | superficie | text |
| acción-texto | acción-fondo | text |
| acción-texto | acción-presionada | text |
| error | fondo | component |
| error | superficie | component |
| línea | fondo | component |
| línea | superficie | component |
| campo-borde | fondo | component |
| campo-borde | superficie | component |
| acción-fondo | fondo | component |
| acción-fondo | superficie | component |
| acción-presionada | fondo | component |
| acción-presionada | superficie | component |
| foco | fondo | component |
| foco | superficie | component |

## The pairs, measured

La cuenta de pares y de relaciones comparadas se dice, y cero es rojo. Cifras copiadas de `ran:` `uv run python scripts/contraste-de-lectura.py governance/identity/ui/semantics.md` (10 pares de texto, 0 bajo 7:1, exit 0) y `ran:` `python3 $G/tokens.py pairs governance/identity/ui/semantics.md` (22 pares, 0 bajo su umbral, exit 0), con `$G` = `conventions/mechanical/instruments/` de gemba-design 0.21.0.

| Pair | Ground | Base case | Variant | Relation |
|------|--------|-----------|---------|----------|
| texto | fondo | 15.35:1 (texto, contra 7:1) | — | no comparada: sin variante |
| texto | superficie | 17.00:1 (texto, contra 7:1) | — | no comparada: sin variante |
| texto-secundario | fondo | 8.57:1 (texto, contra 7:1) | — | no comparada: sin variante |
| texto-secundario | superficie | 9.49:1 (texto, contra 7:1) | — | no comparada: sin variante |
| enlace | fondo | 10.37:1 (texto, contra 7:1) | — | no comparada: sin variante |
| enlace | superficie | 11.48:1 (texto, contra 7:1) | — | no comparada: sin variante |
| error | fondo | 8.38:1 (texto, contra 7:1) | — | no comparada: sin variante |
| error | superficie | 9.28:1 (texto, contra 7:1) | — | no comparada: sin variante |
| acción-texto | acción-fondo | 11.48:1 (texto, contra 7:1) | — | no comparada: sin variante |
| acción-texto | acción-presionada | 14.95:1 (texto, contra 7:1) | — | no comparada: sin variante |
| error | fondo | 8.38:1 (componente, contra 3:1) | — | no comparada: sin variante |
| error | superficie | 9.28:1 (componente, contra 3:1) | — | no comparada: sin variante |
| línea | fondo | 3.34:1 (componente, contra 3:1) | — | no comparada: sin variante |
| línea | superficie | 3.70:1 (componente, contra 3:1) | — | no comparada: sin variante |
| campo-borde | fondo | 3.34:1 (componente, contra 3:1) | — | no comparada: sin variante |
| campo-borde | superficie | 3.70:1 (componente, contra 3:1) | — | no comparada: sin variante |
| acción-fondo | fondo | 10.37:1 (componente, contra 3:1) | — | no comparada: sin variante |
| acción-fondo | superficie | 11.48:1 (componente, contra 3:1) | — | no comparada: sin variante |
| acción-presionada | fondo | 13.50:1 (componente, contra 3:1) | — | no comparada: sin variante |
| acción-presionada | superficie | 14.95:1 (componente, contra 3:1) | — | no comparada: sin variante |
| foco | fondo | 10.37:1 (componente, contra 3:1) | — | no comparada: sin variante |
| foco | superficie | 11.48:1 (componente, contra 3:1) | — | no comparada: sin variante |

**Pairs measured:** 22 (10 de texto, 12 de componente) · **Relations compared:** 0 — `ran:` `python3 invariance.py governance/identity/ui/semantics.md texto fondo` → `no subject: the palette declares no variant column, so the relation has no second side and nothing was compared.`, exit 2. La relación **no se comparó**; no pasó.

## How it answers the survival criteria

| Criterion | How this answers it |
|-----------|---------------------|
| `platform-specs` | no aplica, porque no se entrega una marca ni un ícono de plataforma (ADR-009) |
| `minimum-size` | no aplica, porque un conjunto de roles de color no fija tamaños; lo resolvió `specimen.md` (16 px) |
| `single-ink` | no aplica, porque es propiedad de una marca y este encargo no tiene marca (ADR-009) |
| `contrast` | los diez pares de texto, medidos arriba; el más bajo, 8.38:1, sobre 4.5:1 |
| `prior-art` | no aplica, porque no se entrega marca ni se registra nada (ADR-009) |
| `component-contrast` | los doce pares de componente (`error` como borde, `línea`, `campo-borde`, `acción-fondo`, `acción-presionada`, `foco`, sobre `papel` y sobre `hoja`), medidos arriba contra 3:1, la cifra del catálogo (WCAG 2.2 SC 1.4.11) leída hoy; el más bajo, 3.34:1 |
| `target-size` | no aplica, porque un rol de color no declara objetivos interactivos; lo resuelve s5.6 |
| `provenance` | los trece roles vienen de un escalón de `primitives.md`: `tokens.py provenance`, arriba |

## How it answers the fitness criteria

| Criterion, as approved | From | Stratum | How this answers it |
|------------------------|------|----------|----------|
| R1 · texto ≥ 7:1 | commission 2 | `mechanical` | sí — 10 pares de texto, 0 bajo 7:1; el más bajo, `error` sobre `fondo` 8.38:1 (`ran:` arriba) |
| R2 · reproducible y desde un escalón | este eslabón | `mechanical` | sí — `ran:` `tokens.py provenance` sobre `primitives.md` + este archivo: `provenance: 13 token(s) judged, 0 not from the declared scale`, exit 0; `primitives.md` lo regenera la prueba del gate |
| R3 · los roles añadidos se leen como Cuaderno de campo | concept (ADR-010) | `judgement` | sí, para (A) — abajo |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| R3 — botón, campo, foco y presionado se leen como parte del Cuaderno de campo | sí, para (A); no, para (C) | Daniel Efraín Domínguez Urbina, 2026-09-22, en elección forzada entre (A) y (C) sobre la lámina del formulario de alta |

## What was not measured

Lo que solo una interfaz renderizada muestra: el anillo de foco sobre un botón del mismo azul (el anillo se separa con un espacio de fondo; que ese espacio exista es de los componentes, s5.6), el estado presionado en un teléfono real, zoom, reflujo. Que un error no se distinga **solo** por su color (WCAG 1.4.1) tampoco se mide aquí: con un solo acento oscuro (ADR-010), el error lleva texto y posición, y eso es de los componentes. La relación de invariancia **no se comparó**: la identidad no declara variante, y el instrumento lo dice (arriba).

## What was tried and rejected

- **(B) Uniforme en OKLCH:** `texto-secundario` sobre `fondo` 6.86:1; `línea` y `campo-borde` sobre `fondo` 2.76:1 — sus primitivas se alejan de la paleta.
- **(C) Uniforme en HSL:** pasa (mínimos 7.40:1 y 3.30:1), pero la tinta y el papel de los roles dejan de ser los de la paleta; perdió R3.
- **`acción-presionada` como literal** (`#1A3050`): `provenance` en rojo — no es escalón de ninguna rampa (ADR-013).
