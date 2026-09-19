# Epic e4: Care log — Decisions

Written by the epic session alone, newest last, one entry per gate answered in
the human's place, per stop, and per answer to a stop. An entry is never
rewritten or removed: a later decision that reverses one is a new entry that
names it.

### 2026-09-19 · epic-plan step 4 · Presentar el plan al humano antes de la primera historia
**Decided:** el plan se da por presentado con este registro y con el reporte final del supervisor; la sesión sigue con s4.1 sin esperar una respuesta.
**Why:** `conventions/autonomy` (`### The gates`): epic-plan «Present it to the human before starting the first story.» → `decision`; el plan está en `plan.md` (commit `chore(e4): plan`) y el humano lo lee después aquí y allá.
**Would have stopped:** P5 si el plan no pudiera escribirse por falta de `scope.md` o `design.md`; P4 si un criterio `[stated]` del brief lo contradijera (ninguno lo hace: la medición con "Slow 3G" queda prevista como stop P4 en `epic-review`).

### 2026-09-19 · story-implement (s4.1) step 1 · Ofrecer el envío a un ejecutor
**Decided:** no se envía; la sesión implementa s4.1 ella misma.
**Why:** `plan.md` del épico, `## Delegation`, fila s4.1: Block `—`, Mode `—` («The designation is the plan's, never the executor's»); orchestrate paso 6: una fila con `—` → esta sesión corre las skills de la historia.
**Would have stopped:** P5 si la fila designara un bloque y `delegate` no pudiera correrlo.

### 2026-09-19 · story-implement (s4.1) step 2 · Confirmar con el humano la intención del diseño
**Decided:** no se espera confirmación; la intención va en el reporte: s4.1 añade la tabla `riegos` (cascada, `CHECK` de forma), la validación estricta de la fecha, el tope de 500 comprobado en el mismo `INSERT` y las funciones `agregar/listar/ultimo/quitar` filtradas por ejemplar y registro.
**Why:** `stories/s4.1-*/plan.md` línea `> Pause: none (default)` y la propia skill: «unless the plan declares `> Pause: none`, in which case there is no human in the loop and the restatement goes in your report instead».
**Would have stopped:** P5 si el plan declarara `per task`.
