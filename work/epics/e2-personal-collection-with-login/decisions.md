# Epic e2: Personal collection with login — Decisions

Written by the epic session alone, newest last, one entry per gate answered in
the human's place, per stop, and per answer to a stop. An entry is never
rewritten or removed: a later decision that reverses one is a new entry that
names it.

### 2026-09-19 · epic-plan step 4 · Presentar el plan al humano antes de la primera historia
**Decided:** el plan se da por presentado con `plan.md` commiteado y sin esperar aprobación; se sigue a la primera historia (s2.1). Delegación: `—` en todas las filas, esta misma sesión corre cada historia.
**Why:** el gate `epic-plan | Present it to the human before starting the first story.` está clasificado `decision` en `### The gates` de la convención de autonomía; el humano lo leerá después aquí y en `plan.md`. Delegación `—` porque `delegate` dice "never delegate on your own initiative without asking first" y nada escrito pide delegar.
**Would have stopped:** un plan que contradijera un criterio `[stated]` del brief (P4) o un stop añadido en el binding (`Added stops: none`, no aplica); ninguno ocurre.

### 2026-09-19 · story-implement step 1 · s2.1: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s2.1 ella misma. Con `> Pause: none` en el plan, la reformulación del diseño y la confirmación tras cada tarea no esperan al humano: la reformulación va en el reporte y cada tarea continúa con el gate en verde y el commit hecho.
**Why:** `plan.md` de la épica, `## Delegation`, fila s2.1: `—`; y `delegate`: "never delegate on your own initiative without asking first". El mold de T1 (`datos/catalogo.py`, ADR-003) es un patrón de código existente, no una orden de despachar. Plan de la historia: `> Pause: none (default)`.
**Would have stopped:** una fila de Delegation con bloque para s2.1 (entonces corre `delegate`), o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · story-implement step 1 · s2.2: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s2.2 ella misma; con `> Pause: none` la reformulación va en el reporte y las tareas siguen con el gate en verde y el commit hecho.
**Why:** `plan.md` de la épica, `## Delegation`, fila s2.2: `—`; y `delegate`: "never delegate on your own initiative without asking first". Los moldes de T2 a T4 son tareas de la propia historia o código existente. Plan de la historia: `> Pause: none (default)`.
**Would have stopped:** una fila de Delegation con bloque para s2.2, o un stop añadido en el binding (`Added stops: none`).
