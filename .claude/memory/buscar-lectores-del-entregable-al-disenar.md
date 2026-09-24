---
name: buscar-lectores-del-entregable-al-disenar
description: al diseñar un cambio a un entregable de identidad, buscar qué scripts y pruebas lo leen antes de decir "ningún código cambia"
metadata:
  type: feedback
---

Antes de escribir "ningún código cambia" en el diseño de una historia que toca un entregable de `governance/identity/`, hacer `grep -rln {nombre-del-entregable} scripts tests`. Las pruebas del proyecto atan los entregables a su regla (`test_el_entregable_es_lo_que_la_regla_registrada_produce`) y a la hoja (`test_identidad_hoja.py`), y los scripts los leen por posición.

**Why:** en s5 (2026-09-24), agregar `Font weight` a `type-scale.md` rompió `derivar-medidas.py`, `comprobar-medidas.py piso` (leía `Roles` por posición) y dos pruebas. El diseño decía que no cambiaba código.
**How to apply:** en el recorrido de `story-design`, junto con [[revisar-promociones-del-parking-lot-al-disenar]]. También correr el generador con una sonda antes de proponer criterios (ver [[verificar-el-efecto-en-el-render]]).
