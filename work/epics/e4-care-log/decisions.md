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

### 2026-09-19 · story-implement (s4.1) step 5 · Acuse del humano tras cada tarea
**Decided:** se continúa con la tarea siguiente en cuanto el gate está en verde y el commit existe, para T1 a T3.
**Why:** `stories/s4.1-*/plan.md` línea `> Pause: none (default)`; story-implement paso 5: «unless the plan declares `> Pause: none`, in which case continue to the next task once the gate is green».
**Would have stopped:** P3 si el gate estuviera en rojo y no supiera arreglarlo.

### 2026-09-19 · story-implement (s4.2) step 1 · Ofrecer el envío a un ejecutor
**Decided:** no se envía; la sesión implementa s4.2 ella misma.
**Why:** `plan.md` del épico, `## Delegation`, fila s4.2: Block `—`, Mode `—`; orchestrate paso 6: una fila con `—` → esta sesión corre las skills de la historia.
**Would have stopped:** P5 si la fila designara un bloque y `delegate` no pudiera correrlo.

### 2026-09-19 · story-implement (s4.2) step 2 · Confirmar con el humano la intención del diseño
**Decided:** no se espera confirmación; la intención va en el reporte: s4.2 añade el router `cuidados` con dos POST (registrar y quitar un riego), valida la fecha con `validar_fecha` antes de `agregar`, y la ficha carga el historial (más reciente primero) y el último riego, con 422 y mensaje ante fechas inválidas o el tope.
**Why:** `stories/s4.2-*/plan.md` línea `> Pause: none (default)` y la propia skill: «in which case there is no human in the loop and the restatement goes in your report instead».
**Would have stopped:** P5 si el plan declarara `per task`.

### 2026-09-19 · story-implement (s4.2) step 5 · Acuse del humano tras cada tarea
**Decided:** se continúa con la tarea siguiente en cuanto el gate está en verde y el commit existe, para T1 a T4.
**Why:** `stories/s4.2-*/plan.md` línea `> Pause: none (default)`; story-implement paso 5: «in which case continue to the next task once the gate is green».
**Would have stopped:** P3 si el gate estuviera en rojo y no supiera arreglarlo.

### 2026-09-19 · story-implement (s4.3) step 1 · Ofrecer el envío a un ejecutor
**Decided:** no se envía; la sesión implementa s4.3 ella misma.
**Why:** `plan.md` del épico, `## Delegation`, fila s4.3: Block `—`, Mode `—`; orchestrate paso 6: una fila con `—` → esta sesión corre las skills de la historia.
**Would have stopped:** P5 si la fila designara un bloque y `delegate` no pudiera correrlo.

### 2026-09-19 · story-implement (s4.3) step 2 · Confirmar con el humano la intención del diseño
**Decided:** no se espera confirmación; la intención va en el reporte: s4.3 añade la tabla `floraciones` (cascada, `CHECK` de forma y de orden), `validar_floracion` y `datos.floraciones` con `agregar`, `terminar` (una sola sentencia condicionada a propia, en curso y con inicio no posterior), `listar` y `quitar`, con tope de 500 atómico.
**Why:** `stories/s4.3-*/plan.md` línea `> Pause: none (default)` y la propia skill: «in which case there is no human in the loop and the restatement goes in your report instead».
**Would have stopped:** P5 si el plan declarara `per task`.

### 2026-09-19 · story-implement (s4.3) step 5 · Acuse del humano tras cada tarea
**Decided:** se continúa con la tarea siguiente en cuanto el gate está en verde y el commit existe, para T1 a T3.
**Why:** `stories/s4.3-*/plan.md` línea `> Pause: none (default)`; story-implement paso 5: «in which case continue to the next task once the gate is green».
**Would have stopped:** P3 si el gate estuviera en rojo y no supiera arreglarlo.

### 2026-09-19 · story-implement (s4.4) step 1 · Ofrecer el envío a un ejecutor
**Decided:** no se envía; la sesión implementa s4.4 ella misma.
**Why:** `plan.md` del épico, `## Delegation`, fila s4.4: Block `—`, Mode `—`; orchestrate paso 6: una fila con `—` → esta sesión corre las skills de la historia.
**Would have stopped:** P5 si la fila designara un bloque y `delegate` no pudiera correrlo.

### 2026-09-19 · story-implement (s4.4) step 2 · Confirmar con el humano la intención del diseño
**Decided:** no se espera confirmación; la intención va en el reporte: s4.4 añade tres POST al router `cuidados` (registrar, fijar el fin y quitar una floración), validando con `validar_floracion` y `validar_fecha` antes de tocar `datos.floraciones`; la ficha carga el historial (más reciente primero), ofrece «Terminar» solo en las que están en curso y `ficha()` recibe `valores` en lugar de `fecha`.
**Why:** `stories/s4.4-*/plan.md` línea `> Pause: none (default)` y la propia skill: «in which case there is no human in the loop and the restatement goes in your report instead».
**Would have stopped:** P5 si el plan declarara `per task`.

### 2026-09-19 · story-implement (s4.4) step 5 · Acuse del humano tras cada tarea
**Decided:** se continúa con la tarea siguiente en cuanto el gate está en verde y el commit existe, para T1 a T3.
**Why:** `stories/s4.4-*/plan.md` línea `> Pause: none (default)`; story-implement paso 5: «in which case continue to the next task once the gate is green».
**Would have stopped:** P3 si el gate estuviera en rojo y no supiera arreglarlo.

### 2026-09-19 · story-implement (s4.5) step 1 · Ofrecer el envío a un ejecutor
**Decided:** no se envía; la sesión implementa s4.5 ella misma.
**Why:** `plan.md` del épico, `## Delegation`, fila s4.5: Block `—`, Mode `—`; orchestrate paso 6: una fila con `—` → esta sesión corre las skills de la historia.
**Would have stopped:** P5 si la fila designara un bloque y `delegate` no pudiera correrlo.

### 2026-09-19 · story-implement (s4.5) step 2 · Confirmar con el humano la intención del diseño
**Decided:** no se espera confirmación; la intención va en el reporte: s4.5 añade `datos.riegos.ultimos` (un `MAX(fecha) … GROUP BY ejemplar_id`) y la lista de "Mi colección" lo carga una vez y muestra «Último riego» o «Sin riegos» en cada fila.
**Why:** `stories/s4.5-*/plan.md` línea `> Pause: none (default)` y la propia skill: «in which case there is no human in the loop and the restatement goes in your report instead».
**Would have stopped:** P5 si el plan declarara `per task`.

### 2026-09-19 · story-implement (s4.5) step 5 · Acuse del humano tras cada tarea
**Decided:** se continúa con la tarea siguiente en cuanto el gate está en verde y el commit existe, para T1 y T2.
**Why:** `stories/s4.5-*/plan.md` línea `> Pause: none (default)`; story-implement paso 5: «in which case continue to the next task once the gate is green».
**Would have stopped:** P3 si el gate estuviera en rojo y no supiera arreglarlo.

### 2026-09-19 · story-implement (s4.6) step 1 · Ofrecer el envío a un ejecutor
**Decided:** no se envía; la sesión implementa s4.6 ella misma.
**Why:** `plan.md` del épico, `## Delegation`, fila s4.6: Block `—`, Mode `—`; orchestrate paso 6: una fila con `—` → esta sesión corre las skills de la historia.
**Would have stopped:** P5 si la fila designara un bloque y `delegate` no pudiera correrlo.

### 2026-09-19 · story-implement (s4.6) step 2 · Confirmar con el humano la intención del diseño
**Decided:** no se espera confirmación; la intención va en el reporte: s4.6 saca el montaje de la colección temporal del script de medición, añade la medición de la ficha con 50+50 y con el tope 500+500 (y una prueba del gate que protege el presupuesto de 200 KB en gzip), y documenta el historial de cuidados en el README con su hallazgo de compresión en el parking lot.
**Why:** `stories/s4.6-*/plan.md` línea `> Pause: none (default)` y la propia skill: «in which case there is no human in the loop and the restatement goes in your report instead».
**Would have stopped:** P5 si el plan declarara `per task`.

### 2026-09-19 · story-implement (s4.6) step 5 · Acuse del humano tras cada tarea
**Decided:** se continúa con la tarea siguiente en cuanto el gate está en verde y el commit existe, para T1 a T3.
**Why:** `stories/s4.6-*/plan.md` línea `> Pause: none (default)`; story-implement paso 5: «in which case continue to the next task once the gate is green».
**Would have stopped:** P3 si el gate estuviera en rojo y no supiera arreglarlo.

### 2026-09-19 · epic-review step 3 · Stopped at P4
**Question:** el criterio `[stated]` del brief y del scope, «la ficha con 50 registros entre riegos y floraciones los muestra en orden cronológico y su primera carga transfiere ≤ 200 KB (`must-perf-001`)», no se puede dar por cumplido sin ti en dos puntos. (1) Peso: los bytes están medidos y protegidos por el gate (`scripts/medir-primera-carga.py`, gzip sin fotos: ficha con 50+50 = 18,2 KB; con el tope 500+500 = 29,8 KB, contra 200 KB), pero la medición con el perfil "Slow 3G" del navegador con la aplicación desplegada solo la puedes hacer tú: ¿la haces y me dices el resultado, la das por cumplida con la medición por script, o la difieres? (2) Orden: la ficha muestra **dos listas separadas** (riegos y floraciones), cada una **del más reciente al más antiguo**; no hay una línea de tiempo mezclada ni orden ascendente. ¿Es eso lo que pedías con «orden cronológico», o quieres orden ascendente o una sola lista mezclada (eso sería una historia nueva)?
**State:** develop · no stash · las seis historias (s4.1 a s4.6) están mergeadas y `done` en `plan.md`; sin retrospectiva ni `docs.md` todavía; revisión de calidad y de seguridad a escala de épica hecha (Bandit sin hallazgos fuera de `tests/`; un hallazgo, `datos.riegos.ultimo` sin llamadores, quitado en `refactor(datos): quitar ultimo…`); el resto del alcance (MUST, SHOULD y `[deduced]`) re-cotejado como cumplido, sin compromisos de eliminación.

### 2026-09-19 · epic-review step 3 · Answered (P4 above)
**Decided:** el peso se da por cumplido con la medición por script (ficha 50+50 = 18,2 KB y con el tope = 29,8 KB en gzip, contra 200 KB); la medición con "Slow 3G" en el navegador queda **pendiente del humano** y se anota así en la retrospectiva; las dos listas (riegos y floraciones), cada una del más reciente al más antiguo, cumplen «orden cronológico».
**Why:** answer from the supervisor, verbatim: "(1) el peso se da por cumplido con la medición por script y la de Slow 3G queda pendiente del humano; (2) las dos listas del más reciente al más antiguo cumplen «orden cronológico»."

### 2026-09-19 · epic-close step 4 · Preguntar al humano qué le faltaría a un desarrollador nuevo
**Decided:** no se pregunta; `docs.md` se escribe con los modos de fallo de las retrospectivas de las historias y de `epic-review`, y el humano puede añadir los que falten al leerlo.
**Why:** el gate `epic-close | Then ask the human what a developer new to the code would still find` está clasificado `decision` en `### The gates`; las fuentes que la habilidad manda usar (retrospectivas de las seis historias y de la épica) cubren cada módulo mayor (dominio, datos, rutas, plantilla, medición) con al menos un modo de fallo y su diagnóstico. Precedente: la misma decisión de e3 en este mismo archivo de la épica anterior.
**Would have stopped:** un módulo mayor sin ningún modo de fallo documentado, o un stop añadido en el binding (`Added stops: none`); ninguno ocurre.

### 2026-09-19 · epic-close step 4 · Revisión humana de `docs.md` antes de seguir
**Decided:** `docs.md` se da por revisado con lo escrito y sigue el cierre; el humano lo lee después junto con este registro.
**Why:** los gates `epic-close | missing — added failure modes are the most valuable. Human-reviewed before` y `epic-close | Human reviewed docs.md before shipping.` están clasificados `decision`; todos los módulos, funciones, tipos y pruebas nombrados en `docs.md` existen (comprobado con `grep` sobre `src/`, `scripts/` y `tests/`), las cifras salen de las mediciones de las retrospectivas y cada módulo mayor lleva al menos un modo de fallo con su diagnóstico.
**Would have stopped:** un nombre en `docs.md` que no exista en el código, o un stop añadido en el binding; ninguno ocurre.

### 2026-09-19 · epic-close step 5 · Revisión humana de la deriva del README
**Decided:** se corrigen dos celdas de la tabla Structure del README: `datos/` nombra también riegos y floraciones, y `scripts/` dice que `medir-primera-carga.py` se explica en Fotos y en Historial de cuidados; Quick start no cambia (`uv sync`, `./scripts/check` y la orden de `uvicorn` siguen siendo las de hoy; `scripts/check-integration` no existe) y se sigue sin espera.
**Why:** los gates `epic-close | nothing has drifted, say so and change nothing. Human-reviewed before` y `epic-close | sections only — human-reviewed, never any other section` están clasificados `decision`; la edición es mínima, dentro de Structure, y la puede revertir el humano al leer el diff. Las filas de primer nivel del repositorio (`src/`, `tests/`, `scripts/`, `Dockerfile`, `governance/`, `conventions/`, `work/`, `records/`) siguen nombradas en la tabla.
**Would have stopped:** un cambio en una sección que no sea Quick start o Structure, o un stop añadido en el binding; ninguno ocurre.
