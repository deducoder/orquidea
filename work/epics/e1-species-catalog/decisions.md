# Epic e1: Species catalog — Decisions

Written by the epic session alone, newest last, one entry per gate answered in
the human's place, per stop, and per answer to a stop. An entry is never
rewritten or removed: a later decision that reverses one is a new entry that
names it.

### 2026-09-19 · epic-plan step 4 · Presentar el plan al humano antes de la primera historia
**Decided:** el plan se da por presentado con `plan.md` commiteado y sin esperar aprobación; se sigue a la primera historia (e1.1). Delegación: `—` en todas las filas, este mismo session corre cada historia.
**Why:** el gate `epic-plan | Present it to the human before starting the first story.` está clasificado `decision` en `### The gates` de la convención de autonomía; el humano lo leerá después aquí y en `plan.md`. Delegación `—` porque `delegate` dice "never delegate on your own initiative without asking first" y nada escrito pide delegar.
**Would have stopped:** una historia con un stop añadido en el binding (`Added stops: none`, no aplica) o un plan que contradijera un criterio `[stated]` del brief (P4); ninguno ocurre.

### 2026-09-19 · story-implement step 1 · s1.1: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s1.1 ella misma. (Nota: las entradas anteriores de este archivo escribieron "e1.1"; el id correcto es `s1.1`, corregido en scope, design y plan por `chore(e1): use local story ids s1.n`.)
**Why:** `plan.md` de la épica, `## Delegation`, fila s1.1: `—`; y `delegate`: "never delegate on your own initiative without asking first". El único mold de T2 es la tarea T1 de la misma historia, no un patrón externo.
**Would have stopped:** una fila de Delegation con bloque para s1.1 (entonces corre `delegate`), o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · story-implement step 1 · s1.2: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s1.2 ella misma.
**Why:** `plan.md` de la épica, `## Delegation`, fila s1.2: `—`; y `delegate`: "never delegate on your own initiative without asking first". Los moldes T1/T2 son tareas de la propia historia.
**Would have stopped:** una fila de Delegation con bloque para s1.2, o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · story-implement step 1 · s1.3: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s1.3 ella misma.
**Why:** `plan.md` de la épica, `## Delegation`, fila s1.3: `—`; y `delegate`: "never delegate on your own initiative without asking first". El mold T1 de T2 es una tarea de la propia historia.
**Would have stopped:** una fila de Delegation con bloque para s1.3, o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · epic-plan step 2 · Re-plan: s1.4 antes que s1.5, s1.5 depende de s1.6
**Decided:** el orden de la secuencia pasa a s1.4, s1.5, s1.6 con s1.5 dependiendo de s1.6 (que a su vez espera datos del humano); `plan.md` re-escrito por `chore(e1): re-plan`.
**Why:** `plan.md`, "Sequencing risks": los datos del VPS y los datos botánicos con fuentes no están escritos en ningún artefacto; y `scope.md`, criterio `[stated]` del brief: "una especie de ejemplo se ve en su ficha, desplegada en el VPS", que necesita una especie real con fuentes (`must-data-001`), inventarla violaría la guardia. Ordenar así deja s1.4 hecha antes del stop.
**Would have stopped:** que el reorden contradijera un criterio `[stated]` del brief (P4): no lo hace, el orden no es un criterio.

### 2026-09-19 · epic-plan step 2 · Corrección del re-plan: el orden es s1.4, s1.6, s1.5
**Decided:** corrige la entrada anterior ("Re-plan: s1.4 antes que s1.5, s1.5 depende de s1.6"): la secuencia queda s1.4, s1.6, s1.5, porque s1.5 depende de s1.6 y no puede ir antes; la tabla de Progress sigue el mismo orden.
**Why:** `plan.md`, columna `Depends on` de s1.5: `s1.6 (hard)`; una dependencia dura no puede quedar después de lo que depende de ella. Reversa la parte del orden de la entrada anterior; su razón (agotar primero lo que no espera al humano) sigue en pie.
**Would have stopped:** nada: es una corrección de coherencia interna del plan.

### 2026-09-19 · story-implement step 1 · s1.4: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s1.4 ella misma.
**Why:** `plan.md` de la épica, `## Delegation`, fila s1.4: `—`; y `delegate`: "never delegate on your own initiative without asking first". El mold T1 de T2 es una tarea de la propia historia.
**Would have stopped:** una fila de Delegation con bloque para s1.4, o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · story-start step 4 · Stopped at P5 (s1.6)
**Question:** s1.6 necesita las especies semilla reales: cuáles (nombre científico y comunes), y para cada una los cuidados de luz, riego, temperatura y sustrato con la fuente de cada dato (`must-data-001`); ningún artefacto los contiene y inventarlos violaría la guardia. Y para s1.5 (despliegue al VPS): host y acceso (SSH), sistema operativo, cómo se debe correr la aplicación (systemd, contenedor, proxy inverso) y dominio o puerto expuesto. ¿Me los das, o me indicas dónde están escritos? Alternativa: decir que s1.5 y s1.6 se difieran y cerrar la épica con s1.1 a s1.4.
**State:** develop · no stash · s1.1, s1.2, s1.3 y s1.4 mergeadas localmente en `develop` (sin push, como manda el modo de la épica); s1.5 y s1.6 sin empezar, sin rama.
