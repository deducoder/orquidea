---
type: adr
id: ADR-012
title: "Paleta de Orquídea"
status: accepted
date: 2026-09-22
epic: e5
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-012: Paleta de Orquídea

## Status

Accepted.

## Context

**La pregunta:** ¿qué valores toman los roles de color de Orquídea, dentro de la dirección Cuaderno de campo (ADR-010), con todo texto a 16 px (ADR-011) y cada par de texto a ≥ 7:1 (ADR-009)?

Como ADR-011 pone todo texto a 16 px, ningún texto es "grande": todo par de texto de la paleta, incluida la tinta suave de fechas y fuentes, necesita 7:1. Con una tinta casi negra y un acento oscuro a 7:1 sobre el papel, el acento contra la tinta queda muy por debajo de 3:1, así que los enlaces no pueden distinguirse solo por color: se subrayan (consecuencia para s5.6 y s5.7). La identidad no declara variante (sin tema oscuro, rabbit hole del brief de e5).

### Criterios de la pieza

Aprobados por el humano el 2026-09-22, antes de fijar ningún color.

| # | Criterio | Estrato | From |
|---|-----------|---------|------|
| P1 | Cada par de texto de la paleta (tinta, tinta suave, acento como texto, alerta como texto, sobre papel y sobre hoja) llega a ≥ 7:1 | `mechanical` | commission 2 |
| P2 | Junto a fotos reales de orquídeas de colores fuertes, ningún color de la paleta compite con la flor | `judgement` | commission 3 (y S1 de ADR-010) |
| P3 | Se lee como papel y tinta: fondo neutro cálido, tinta casi negra, un solo acento; nada de marca | `judgement` | concept (ADR-010) |

**Roles:** `papel`, `hoja`, `tinta`, `tinta suave`, `renglón`, `acento`, `alerta`. Sin rol de éxito: la aplicación confirma redirigiendo.

### Candidatas

Tres, descritas antes de fijar valores:

- **(A) Papel cálido, acento azul tinta** — papel ligeramente crema, hoja blanca, acento de tinta azul-negra.
- **(B) Papel blanco, acento sepia** — papel blanco, hoja apenas cálida, acento sepia oscuro.
- **(C) Papel gris frío, acento verde bosque** — papel gris muy claro, hoja blanca, acento verde oscuro.

### Valores y mediciones

Fijados el 2026-09-22 en el scratchpad (`$S`), cada candidata en su mejor versión, y medidos con `scripts/contraste-de-lectura.py` (salida vista; cifras copiadas de ella). Los pares declarados son los ocho de texto (tinta, tinta suave, acento y alerta, sobre papel y sobre hoja) y `renglón` sobre `papel` y sobre `hoja` como `component` (s5.5 los mide contra 3:1; aquí no se juzgan).

| Role | (A) Papel cálido, azul tinta | (B) Papel blanco, sepia | (C) Gris frío, verde bosque |
|---|---|---|---|
| papel | `#F7F3EA` | `#FFFFFF` | `#F1F3F1` |
| hoja | `#FFFFFF` | `#F8F6F1` | `#FFFFFF` |
| tinta | `#1E1C19` | `#141414` | `#1B1F1C` |
| tinta suave | `#4A453E` | `#474747` | `#444B46` |
| renglón | `#8C8475` | `#8A8A8A` | `#848C86` |
| acento | `#1F3A5F` | `#6B4420` | `#24503A` |
| alerta | `#8A1C1C` | `#8E1B1B` | `#8A1C1C` |

### La rejilla

| Criterio | Estrato | (A) | (B) | (C) |
|---|---|---|---|---|
| P1 · texto ≥ 7:1 | `mechanical` | sí — 8 pares, 0 bajo el umbral; el más bajo, alerta sobre papel 8.38:1 (`ran:`) | sí — 8 pares, 0 bajo; el más bajo, acento sobre hoja 7.86:1 (`ran:`) | sí — 8 pares, 0 bajo; el más bajo, tinta suave sobre papel 8.04:1 (`ran:`) |
| P2 · no compite con la flor | `judgement` | sí — el azul tinta no está en ninguna flor ni follaje | sí | **no** — el acento verde queda junto al follaje de las plantas |
| P3 · papel y tinta | `judgement` | sí | **no** — hoja crema sobre blanco y acento sepia se leen como lámina de herbario (descartada en ADR-010) | sí |

### Contraejemplos

- **P1 — rojo, visto.** Sujeto: la candidata (A) con el gris habitual de texto secundario, `#767676`, como tinta suave.

```
$ uv run python scripts/contraste-de-lectura.py $S/candidata-roja.md
…
tinta suave sobre papel (texto): 4.10:1  necesita 7:1  NO
tinta suave sobre hoja (texto): 4.54:1  necesita 7:1  NO
…
8 par(es) de texto juzgado(s), 2 bajo el umbral
exit=1
```

- **P2 y P3 — no aplica: no hay oráculo.** Se juzgan en elección forzada sobre una lámina de tres pantallas de teléfono (una por candidata) con fotos reales de orquídeas del catálogo, compuesta con Roboto a 16 px y 3× en el scratchpad (`$S/lamina-paletas.jpg`). Fotos, solo en el scratchpad: *Barkeria spectabilis* (Wikimedia Commons, «Barkeria spectabilis.jpg», Brett Francis (Oort), CC BY-SA 2.5), *Cuitlauzina pulchella* (Commons, «Cuitlauzina pulchella (7533856656).jpg», Mitch, CC BY 2.0) y *Brassia verrucosa* (Commons, «BrassiaVerrucosa.jpg», Chhe, dominio público).

Las celdas de P2 y P3 las propuso el agente sobre la lámina y las confirmó el humano con su elección.

## Decision

**Option (A) Papel cálido, azul tinta**, elegida y firmada por Daniel Efraín Domínguez Urbina el 2026-09-22 en elección forzada entre las tres, sobre la lámina con fotos.

1. Roles y valores: `papel` `#F7F3EA`, `hoja` `#FFFFFF`, `tinta` `#1E1C19`, `tinta suave` `#4A453E`, `renglón` `#8C8475`, `acento` `#1F3A5F`, `alerta` `#8A1C1C`.
2. Ocho pares de texto declarados (cuatro tintas sobre papel y sobre hoja), todos ≥ 7:1 — el más bajo 8.38:1; `renglón` declarado como `component` para s5.5.
3. Variante: ninguna; la relación de invariancia no se compara, y s5.5 lo dice así.
4. El entregable es `palette.md` en `governance/identity/`, legible por `contraste-de-lectura.py` y por `tokens.py pairs`.

## Consequences

**Positive:**
- Todo texto, incluido el secundario, pasa 7:1 con margen (≥ 8.38:1), así que s5.5 puede derivar escalones sin caer bajo el umbral a la primera.
- El único color vivo de la pantalla es la foto, y el acento no se confunde con ninguna flor del catálogo probada.

**Negative / costs:**
- El acento contra la tinta da 1.48:1: los enlaces no se distinguen por color y tienen que ir subrayados (s5.6, s5.7).
- No hay rol de éxito ni de aviso; si un día la aplicación muestra confirmaciones, la paleta crece con un ADR nuevo.
- `renglón` a 3.34:1 sobre papel es una línea visible; si s5.6 quiere renglones más tenues para decoración, necesitará un rol aparte que no se use en bordes de campos.
- El juicio de P2 se hizo con tres fotos de tres especies; una flor azul (no hay en el catálogo probado) podría acercarse al acento.

## Alternatives considered

- **(B) Papel blanco, acento sepia:** pasa P1 (7.86:1), falla P3 — se lee como la lámina de herbario que ADR-010 descartó.
- **(C) Gris frío, verde bosque:** pasa P1 (8.04:1), falla P2 — el acento verde compite con el follaje.
