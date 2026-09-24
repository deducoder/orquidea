# Story s2: Derive screens from inventory — Retrospective

Estimated: una sesión, sin cifra declarada · Actual: una sesión; de `50e5a26` (00:07) a `e696ff8` (00:19) en las fechas de autor, más el tiempo de las tres pausas de decisión.

## Summary

Inventario de Orquídea leído en `c9a8ea1`: 38 entradas, de las que la confirmación quitó 4 (Sesión y lo que colgaba de ella), y quedaron 34. Conjunto de pantallas derivado por la regla A con pantallas de paso: 9 pantallas, las mismas que la aplicación ya muestra. ADR-017 abierto antes de leer, con su rojo, y `accepted`. Dos hallazgos del addon aparcados.

## Finalize

- **Gate:** `./scripts/check` salió 0 antes de cada uno de los commits de la rama.
- **Pruebas huérfanas:** no aplica; la historia no toca código (`git diff --name-only develop..HEAD` no lista ningún `.py`).
- **Criterios de aceptación (scope):**
  - ADR en `proposed` antes de leer: cumplido (`50e5a26` antes de `3021953`).
  - `inventory-sources.py` sale 0 con el inventario: `OK (34 entries: 34 read, all found at c9a8ea1; 0 declared …)`.
  - Sale 0 con el conjunto: `… 9 screens, each derived from an entry`.
  - Confirmación del dueño con fecha, y juicio de la regla firmado: cumplidos, los dos del 2026-09-24.
  - Rojo antes de producir (deducido y confirmado en el diseño): `e3c1be3`.
  - Escenario que añadió el diseño, más de cero pantallas: 9.
  - Ningún criterio retractado.
- **Survival-review:**
  - `precedence` sale PASS en el conjunto y FAIL en el inventario. Leído a mano, el FAIL viene de `6a7cadf`, que solo llenó celdas medidas; aparcado en `e696ff8`.
  - Los nueve criterios del catálogo, "no aplica" en los dos entregables, **firmados por Daniel Efraín Domínguez Urbina el 2026-09-24**.
- **quality-review:**
  - Se revisaron las citas contra el código: los modelos línea por línea con `sed`, las rutas con la salida del `grep` de decoradores.
  - A1 y P2 citan la misma línea (`catalogo.py:15`), y es correcto: el mismo `GET` es pantalla y búsqueda.
  - El hallazgo semántico está en *What to improve*.
- **security-review:** sin sujeto. El diff son siete archivos Markdown y ningún `.py`, y el binding escanea `.py` cambiados. No aplica ningún guardarraíl de seguridad (`must-security-001` es de fotos).

## What went well

- **El registro se abrió antes del diseño y no como tarea del plan.** El recorrido de `story-design` era la lectura del inventario. Con el orden de s1, esa lectura habría pasado antes del criterio.
- **El rojo destapó un hueco del instrumento.** La primera sonda de F2 usó `###` en lugar de `## The screens` y salió verde con `0 screens`. De ahí salió la guarda de F2 en ADR-017 y la entrada aparcada, en vez de un verde vacío.
- **Correr las tres reglas sacó a la luz algo que la confirmación no vio.** La regla C perdió "Mi colección", y así se supo que ninguna tarea declarada pide ver la colección aunque la visión lo nombra ("Colección al día"). El dueño decidió no agregarla y quedó escrito.

## What to improve

- **El valor del parámetro de pasos se fijó después de ver las salidas.** ADR-017 nombró "qué tareas llevan pantallas de paso" como parámetro de A, sin valor. El valor ("formulario propio o confirmación") se escribió al elegir, y A reprodujo exactamente las 9 pantallas de hoy. El resultado puede ser correcto, pero la rejilla no muestra que el valor llegó tarde. Lo mitigó que "A sin pasos" corrió igual y quedó en *What was tried and rejected*. La próxima vez, cada valor candidato va a la rejilla como opción desde el `record-open`. Guardado en memoria.
- **La confirmación juntó en una sola pregunta dos decisiones que chocaban.** "Quitar Sesión" se llevaba T8, y "tareas tal cual" la conservaba. Se resolvió aplicando la respuesta más específica y diciéndolo. La pregunta de tareas debió formularse después de la de Sesión, con T8 ya fuera.
- **La revisión de promociones del parking lot se hizo en la revisión y no en el diseño**, como pide la memoria del proyecto. No se cumplía ninguna, pero se revisaron tarde.

## Learned

1. **Sobre el sistema:** las 9 pantallas actuales de Orquídea son exactamente las que deriva la regla de objetos (Especie y Ejemplar con lista y detalle, lo demás como secciones), más tres pasos (alta sin especie, edición, baja) e Inicio y Acceso. Mi colección existe por el objeto, no por una tarea.
2. **Sobre el proceso:** con `screens`, el orden de la historia es initialize → ADR → rojo → diseño → plan. `precedence.py` no distingue el llenado de una celda `pending: measured when run` de una edición del criterio, así que el FAIL se lee a mano, como con el eslabón recalculado de s1.
3. **Capacidad ganada:** los dos primeros eslabones de `screens` están hechos. La guía de prioridad de estas 9 pantallas es la entrada del siguiente, y en ella se juzga el criterio 3 de ADR-009 (la foto como protagonista).
