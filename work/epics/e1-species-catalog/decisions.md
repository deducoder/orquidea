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

### 2026-09-19 · story-start step 4 · Answered (P5 above)
**Decided:** s1.6 obtiene los datos por investigación (`research`), con las 100 especies nativas de Chiapas más conocidas y populares; s1.5 despliega a un VPS con Dokploy sobre Debian 13.
**Why:** answer from the supervisor, verbatim: "Debemos hacer un research para buscar los datos. Tengo un VPS Dokploy debian 13. Pongamos las 100 más conocidas y populares"

### 2026-09-19 · story-implement step 1 · s1.6: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s1.6 ella misma.
**Why:** `plan.md` de la épica, `## Delegation`, fila s1.6: `—`; y `delegate`: "never delegate on your own initiative without asking first". El mold T1 de T2 es una tarea de la propia historia.
**Would have stopped:** una fila de Delegation con bloque para s1.6, o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · story-design step 3 · s1.6: regla de "más conocidas y populares" y datos de género
**Decided:** "más conocidas y populares" se operacionaliza como las especies nativas de Chiapas con más observaciones de grado de investigación en iNaturalist que además tienen una fuente de cuidados utilizable; los cuidados citan la AOS a nivel de género y lo declaran en cada dato.
**Why:** answer del supervisor: "Pongamos las 100 más conocidas y populares"; ninguna medida de popularidad comercial es accesible y `must-data-001` exige una fuente real por dato, así que se eligió la medida objetiva y reproducible descrita en `work/research/chiapas-orchid-seed/report.md`. No contradice ningún criterio `[stated]`: el 100 se cumple.
**Would have stopped:** P4 si no hubiera 100 con fuente; no fue el caso (100 con fuente). Queda para revisión del humano: la regla de popularidad y que los cuidados sean de género, ambos marcados en la retrospectiva de s1.6.

### 2026-09-19 · story-implement step 1 · s1.5: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s1.5 ella misma.
**Why:** `plan.md` de la épica, `## Delegation`, fila s1.5: `—`; y `delegate`: "never delegate on your own initiative without asking first".
**Would have stopped:** una fila de Delegation con bloque para s1.5, o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · story-start step 4 · s1.5: el despliegue real queda fuera de la historia
**Decided:** s1.5 entrega Dockerfile, healthcheck y guía; la ejecución del despliegue en el VPS no forma parte de la historia y el criterio `[stated]` de la épica ("desplegada en el VPS") se verifica con el humano en `epic-review`.
**Why:** `scope.md` de la épica y regla de la épica ("A story under an epic merges locally... defers the push to `epic-close`"): sin push a GitHub, Dokploy no puede construir, y el acceso al Dokploy es del humano; publicar antes sería un push que el modo prohíbe hasta el cierre. Tampoco hay Docker utilizable en esta máquina.
**Would have stopped:** P1 si el despliegue apuntara a `main`; no aplica. El criterio `[stated]` queda sin cumplir hasta que el humano despliegue: es el punto de P4 para `epic-review`.

### 2026-09-19 · epic-review step 3 · Stopped at P4
**Question:** dos criterios `[stated]` del `## Done when` de la épica no se cumplen con lo que el código puede demostrar, y solo tú puedes soltarlos. (1) "El catálogo se carga desde JSON validado y una especie de ejemplo se ve en su ficha, desplegada en el VPS": el repositorio está listo (Dockerfile, `/salud`, guía de Dokploy) y el catálogo real carga, pero no está desplegado: eso necesita el push a GitHub (que hace `epic-close`) y tu acceso a Dokploy, y aquí no hay Docker para construir la imagen. (2) "Primera carga usable en ≤ 5 s con Slow 3G y ≤ 200 KB, medida sobre el catálogo real": el peso se midió (lista 1,884 B, ficha 1,035 B, htmx 16,356 B con gzip, muy por debajo de 200 KB), pero el tiempo con "Slow 3G" necesita un navegador con las herramientas de desarrollo y no lo medí. ¿Difieres estos dos criterios (los verificas tú tras el despliegue) para que cierre la épica con `epic-review` y `epic-close` (push a `develop`, sin tocar `main`), o prefieres que la épica no cierre hasta que existan?
**State:** develop · no stash · s1.1 a s1.6 hechas y mergeadas localmente, plan.md con las seis filas en `done`, sin push · `epic-review` pasos 1 a 3 hechos (rango completo: quality-review sin críticos, security-review PASS WITH FINDINGS solo B101 en `tests/` ya estacionado, sin hallazgos fuera de tests); falta el paso 4 (retrospectiva), que se escribe con tu respuesta. Alcance re-leído: RF-01, ficha con fuente por dato, búsqueda, conjunto semilla de 100 y los criterios `[deduced]` cumplidos; no cumplidos: los dos `[stated]` de arriba. Para tu revisión aparte (no son stops): la regla de popularidad (observaciones en iNaturalist) y que los cuidados de las 100 fichas son de género, ambos dichos en cada ficha y en la retrospectiva de s1.6.

### 2026-09-19 · epic-review step 3 · Answered (P4 above)
**Decided:** los dos criterios `[stated]` (despliegue en el VPS y tiempo con Slow 3G) se difieren: la épica cierra y el humano los verifica tras dar acceso de Dokploy al repositorio.
**Why:** answer from the supervisor, verbatim: "Dile que lo cierre, regreso para darle acceso a dokploy al repo y continuar la e2"

### 2026-09-19 · epic-close step 4 · Preguntar al humano qué le faltaría a un desarrollador nuevo
**Decided:** no se pregunta y se sigue; `docs.md` incluye como modos de fallo los tropiezos reales de la épica (bytecode obsoleto, formato de `.md`, `httpx2`, fixture compartida, empaquetado, primer `docker build`, cuidados de género).
**Why:** `epic-close | Then ask the human what a developer new to the code would still find` está clasificado `decision`; el humano lo revisa después en `docs.md`. El supervisor ya dio la respuesta relevante: "Dile que lo cierre".
**Would have stopped:** un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · epic-close step 4 · Revisión humana de docs.md antes del paso 5
**Decided:** `docs.md` se da por revisada por el humano a posteriori y se continúa; el humano la leerá tras el cierre.
**Why:** gates `epic-close | missing — added failure modes are the most valuable. Human-reviewed before` y `epic-close | Human reviewed docs.md before shipping.`, ambos `decision`; y el supervisor dijo: "Dile que lo cierre".
**Would have stopped:** que `docs.md` afirmara algo no verificado; se cuidó que cada módulo, prueba y ruta nombrados existan (comprobados con `grep` y ejecución).

### 2026-09-19 · epic-close step 5 · Deriva del README
**Decided:** se corrigen en `README.md` solo las filas de Structure (`src/orquidea/`, `conventions/`, `Dockerfile`); el Quick start ya coincide con `scripts/check` y con el arranque local, y no se toca.
**Why:** gates `epic-close | nothing has drifted, say so and change nothing. Human-reviewed before` y `epic-close | sections only — human-reviewed, never any other section`, `decision`; la comparación fue entre la tabla y los primeros niveles del repositorio (`Dockerfile` faltaba; `conventions/` describía solo notificaciones).
**Would have stopped:** cambiar una sección distinta de Quick start o Structure.
