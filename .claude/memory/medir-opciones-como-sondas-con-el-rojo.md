---
name: medir-opciones-como-sondas-con-el-rojo
description: en un ADR de gemba-design con opciones completas, medir todas como sondas en el commit del rojo, antes de producir
metadata:
  type: feedback
---

Cuando las opciones de la rejilla están completas desde el `record-open` (ver [[parametros-de-regla-con-valor-al-abrir]]), se arman como archivos de sonda y se miden con el instrumento en la misma pasada que el rojo. Las celdas `mechanical` de la rejilla se llenan en ese `update`, antes de la pieza.

**Why:** en s4 (2026-09-24), ADR-019 cerró su rejilla medible antes de `5d3574e` y `precedence.py` dio PASS sin depender del nombre del commit. En s2, llenarla después con un `update` dio FAIL ([[precedence-py-juzga-por-creacion]]).
**How to apply:** en cada eslabón de `screens` (y en `ui` si aplica), el orden es ADR → sondas (rojo + opciones) → pieza → `accept` con solo los juicios.
