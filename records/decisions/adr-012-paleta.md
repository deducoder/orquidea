---
type: adr
id: ADR-012
title: "Paleta de Orquídea"
status: proposed
date: 2026-09-22
epic: e5
published: pendiente — se resuelve al completar el registro
---

# ADR-012: Paleta de Orquídea

## Status

Proposed.

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

Valores, mediciones y contraejemplos: por escribir, antes de elegir.

## Decision

Sin resolver.
