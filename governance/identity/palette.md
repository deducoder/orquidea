---
type: palette
commission: "La identidad visual de la interfaz web de Orquídea: paleta, tipografía y la interfaz derivada de ellas"
decision: ADR-012
date: 2026-09-22
---

# Orquídea — Palette

## The criterion this answers

No se repite aquí: vive en `ADR-012`, abierto antes de que existiera cualquiera de los colores de abajo. Esta sección nombra el registro y nada más.

## The palette

**Papel cálido, azul tinta.** La variante que esta identidad promete sobrevivir: **ninguna** — no hay tema oscuro ni aplicación invertida (rabbit hole del brief de e5). Por eso la columna de variante queda vacía y la relación de invariancia **no se compara**: el eslabón de roles de s5.5 la reporta como no comparada, nunca como pasada.

| Role | Value | Variant (ninguna declarada) | Where it is used |
|------|-------|-----------------------------|------------------|
| papel | `#F7F3EA` | — | el fondo de toda la aplicación |
| hoja | `#FFFFFF` | — | la tarjeta de cada ejemplar y de cada especie, sobre el papel |
| tinta | `#1E1C19` | — | todo el texto: títulos, cuerpo, binomios |
| tinta suave | `#4A453E` | — | fechas, fuentes citadas, etiquetas, texto secundario |
| renglón | `#8C8475` | — | líneas, bordes de la hoja y de los campos |
| acento | `#1F3A5F` | — | enlaces (subrayados) y acciones |
| alerta | `#8A1C1C` | — | mensajes de error |

Los pares que la paleta declara, en el formato que leen `scripts/contraste-de-lectura.py` y `tokens.py pairs`:

| Role | Value |
|---|---|
| papel | #F7F3EA |
| hoja | #FFFFFF |
| tinta | #1E1C19 |
| tinta suave | #4A453E |
| renglón | #8C8475 |
| acento | #1F3A5F |
| alerta | #8A1C1C |

| Foreground | Ground | Kind |
|---|---|---|
| tinta | papel | text |
| tinta | hoja | text |
| tinta suave | papel | text |
| tinta suave | hoja | text |
| acento | papel | text |
| acento | hoja | text |
| alerta | papel | text |
| alerta | hoja | text |
| renglón | papel | component |
| renglón | hoja | component |

## How it answers the survival criteria

| Criterion | How this palette answers it |
|-----------|-----------------------------|
| `platform-specs` | no aplica, porque no se entrega una marca ni un ícono de plataforma (ADR-009) |
| `minimum-size` | no aplica a una paleta, porque no fija tamaños; lo resolvió `specimen.md` (16 px) |
| `single-ink` | no aplica, porque es propiedad de una marca y este encargo no tiene marca (ADR-009) |
| `contrast` | los ocho pares de texto, medidos (abajo): el más bajo es 8.38:1, sobre el piso de 4.5:1 y sobre el 7:1 del encargo; todo texto es normal (16 px, ADR-011) |
| `prior-art` | no aplica, porque no se entrega marca ni se registra nada (ADR-009) |
| `component-contrast` | declarado para s5.5: `renglón` sobre `papel` y sobre `hoja` como `component`; esta paleta no tiene componentes y no lo juzga |
| `target-size` | no aplica, porque una paleta no declara objetivos interactivos; lo resuelve s5.6 |
| `provenance` | cada valor es un rol de la tabla de arriba; s5.5 deriva de aquí sus rampas y declara la diferencia con estos valores |

## How it answers the fitness criteria

| Criterion, as approved | From | How this palette answers it |
|------------------------|------|-------------------------|
| P1 · cada par de texto ≥ 7:1 | commission 2 | sí — `ran:` `uv run python scripts/contraste-de-lectura.py governance/identity/palette.md` → 8 pares de texto, 0 bajo el umbral; tinta 15.35 y 17.00, tinta suave 8.57 y 9.49, acento 10.37 y 11.48, alerta 8.38 y 9.28 (sobre papel y sobre hoja) |
| P2 · no compite con la flor | commission 3 | sí — juzgado sobre fotos reales de *Barkeria spectabilis*, *Cuitlauzina pulchella* y *Brassia verrucosa*: el azul tinta no está en ninguna de las flores ni del follaje |
| P3 · papel y tinta | concept (ADR-010) | sí — papel crema cálido, hoja blanca, tinta casi negra, un solo acento; nada de marca |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| P2 — ningún color compite con la flor | sí, para (A); (C) compite con el follaje | Daniel Efraín Domínguez Urbina, 2026-09-22, en elección forzada entre (A), (B) y (C) sobre la lámina con fotos |
| P3 — se lee como papel y tinta | sí, para (A); (B) se lee como herbario | Daniel Efraín Domínguez Urbina, 2026-09-22, en la misma elección |

## What was tried and rejected

- **(B) Papel blanco, acento sepia** (`#FFFFFF`, `#F8F6F1`, `#6B4420`): pasa P1 (par más bajo 7.86:1), pero la hoja crema sobre blanco y el acento sepia se leen como lámina de herbario, la dirección que ADR-010 descartó (P3).
- **(C) Papel gris frío, acento verde bosque** (`#F1F3F1`, `#FFFFFF`, `#24503A`): pasa P1 (8.04:1), pero el acento verde queda junto al follaje de las propias plantas (P2).
- **Tinta suave `#767676`** (el gris habitual de texto secundario): falla P1 — 4.10:1 sobre papel y 4.54:1 sobre hoja.
