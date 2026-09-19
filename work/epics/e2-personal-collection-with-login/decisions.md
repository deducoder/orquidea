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

### 2026-09-19 · story-implement step 1 · s2.3: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s2.3 ella misma; con `> Pause: none` la reformulación va en el reporte.
**Why:** `plan.md` de la épica, `## Delegation`, fila s2.3: `—`; y `delegate`: "never delegate on your own initiative without asking first". Plan de la historia: `> Pause: none (default)`.
**Would have stopped:** una fila de Delegation con bloque para s2.3, o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · story-implement step 1 · s2.4: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s2.4 ella misma; con `> Pause: none` la reformulación va en el reporte.
**Why:** `plan.md` de la épica, `## Delegation`, fila s2.4: `—`; y `delegate`: "never delegate on your own initiative without asking first". Plan de la historia: `> Pause: none (default)`.
**Would have stopped:** una fila de Delegation con bloque para s2.4, o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · story-implement step 1 · s2.5: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s2.5 ella misma; con `> Pause: none` la reformulación va en el reporte.
**Why:** `plan.md` de la épica, `## Delegation`, fila s2.5: `—`; y `delegate`: "never delegate on your own initiative without asking first". Plan de la historia: `> Pause: none (default)`.
**Would have stopped:** una fila de Delegation con bloque para s2.5, o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · story-implement step 1 · s2.6: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s2.6 ella misma; con `> Pause: none` la reformulación va en el reporte.
**Why:** `plan.md` de la épica, `## Delegation`, fila s2.6: `—`; y `delegate`: "never delegate on your own initiative without asking first". Plan de la historia: `> Pause: none (default)`.
**Would have stopped:** una fila de Delegation con bloque para s2.6, o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · story-implement step 1 · s2.7: ofrecer el despacho del bloque
**Decided:** no despachar; la sesión de épica implementa s2.7 ella misma; con `> Pause: none` la reformulación va en el reporte.
**Why:** `plan.md` de la épica, `## Delegation`, fila s2.7: `—`; y `delegate`: "never delegate on your own initiative without asking first". Plan de la historia: `> Pause: none (default)`.
**Would have stopped:** una fila de Delegation con bloque para s2.7, o un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · epic-review step 3 · Stopped at P4
**Question:** un criterio `[stated]` del `## Done when` de la épica no se puede demostrar con lo que el código hace, y solo tú puedes soltarlo: "El usuario registra toda su colección real, incluidas plantas fuera del catálogo, sin otra herramienta" (métrica rezagada del brief). Necesita la aplicación desplegada en tu VPS (nunca se ha construido la imagen: aquí no hay daemon de Docker) y tus plantas reales. Aparte, la guardia `must-perf-001` pide medir con las herramientas del navegador en cada `epic-review`, y no puedo hacerlo: el tiempo con "Slow 3G" y comprobar que la CSP (sin scripts en línea ni `eval`) no rompe htmx (la búsqueda del catálogo). Lo que sí medí: la primera carga es `/acceso` (351 B con gzip) más htmx (16,352 B con gzip), muy por debajo de 200 KB; `/especies` con las 100 especies pesa 2,055 B con gzip. ¿Difieres estas verificaciones (las haces tú tras el primer despliegue) para que la épica cierre con `epic-close` (integración a `develop` y push, sin tocar `main`), o prefieres que no cierre hasta que existan?
**State:** develop · no stash · s2.1 a s2.7 hechas y mergeadas localmente, plan.md con las siete filas en `done`, sin push · `epic-review` pasos 1 a 3 hechos: quality-review y security-review a escala de épica encontraron dos defectos entre historias y los corrigieron con prueba antes de parar (`fix(web)`: el registro `acceso correcto` no salía con la configuración por defecto de uvicorn; y las verificaciones de contraseña scrypt, 64 MiB cada una, podían correr en paralelo en una ráfaga y el contador de intentos no era atómico); Bandit sin hallazgos en `src/`; un hallazgo estacionado en el parking lot (tamaño de `app.py`). Alcance re-leído: RF-04 y RF-08 completos, ruta protegida por defecto (probado enumerando `app.routes`), métrica líder demostrada de punta a punta (`test_recorrido_coleccion.py`) y los criterios `[deduced]` cumplidos; no demostrable: el criterio rezagado `[stated]` de arriba. Falta el paso 4 (retrospectiva y memoria), que se escribe con tu respuesta.

### 2026-09-19 · epic-review step 3 · Answered (P4 above)
**Decided:** el criterio `[stated]` rezagado del brief y las verificaciones de `must-perf-001` con navegador (tiempo con Slow 3G y CSP frente a htmx) se difieren: la épica cierra y el humano las verifica tras el primer despliegue.
**Why:** answer from the supervisor, verbatim: "a — diferir todo y dejar que e2 cierre"

### 2026-09-19 · epic-close step 4 · Preguntar al humano qué le faltaría a un desarrollador nuevo
**Decided:** no se pregunta y se sigue; `docs.md` incluye como modos de fallo los tropiezos reales de la épica (los dos defectos de `epic-review`, el bytecode obsoleto de las mutaciones, el formato de `.md` por `ruff`, la conexión SQLite por hilo, la CSP frente a htmx y el primer `docker build`, estos dos últimos marcados como no verificados).
**Why:** `epic-close | Then ask the human what a developer new to the code would still find` está clasificado `decision`; el humano lo revisa después en `docs.md`. El supervisor ya respondió lo relevante: "a — diferir todo y dejar que e2 cierre".
**Would have stopped:** un stop añadido en el binding (`Added stops: none`).

### 2026-09-19 · epic-close step 4 · Revisión humana de docs.md antes del paso 5
**Decided:** `docs.md` se da por revisada por el humano a posteriori y se continúa; el humano la leerá tras el cierre.
**Why:** gates `epic-close | missing — added failure modes are the most valuable. Human-reviewed before` y `epic-close | Human reviewed docs.md before shipping.`, ambos `decision`; y el supervisor dijo: "a — diferir todo y dejar que e2 cierre".
**Would have stopped:** que `docs.md` afirmara algo no verificado; se cuidó que cada módulo, prueba y ruta nombrados existan (comprobados con `grep`); lo no verificado (CSP con htmx, `docker build`) se dice como tal.

### 2026-09-19 · epic-close step 5 · Deriva del README
**Decided:** se corrige en `README.md` solo la fila de Structure `src/orquidea/` (faltaban `coleccion/`, `autenticacion.py` y el nuevo contenido de `datos/`); el resto de Structure coincide con la raíz del repositorio y el Quick start coincide con `scripts/check` y con el arranque local que s2.7 ya actualizó, y no se tocan.
**Why:** gates `epic-close | nothing has drifted, say so and change nothing. Human-reviewed before` y `epic-close | sections only — human-reviewed, never any other section`, `decision`; la comparación fue entre la tabla y los primeros niveles del repositorio y `src/orquidea/`.
**Would have stopped:** cambiar una sección distinta de Quick start o Structure.
