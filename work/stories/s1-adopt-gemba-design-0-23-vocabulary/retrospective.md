# Story s1: Adopt the gemba-design 0.23.0 vocabulary — Retrospective

Estimated: L, 8 tareas · Actual: 9 tareas (T9 por re-plan), 13 commits de tarea, 2760 s de implementación (`implementation-time.sh develop s1`)

## Summary

- **Tokens en español** (`línea`, `acción-*`) en `semantics.md`, `components.md`, `DESIGN.md` y la hoja. ADR-016 reemplaza la decisión 6 de ADR-014.
- **El vocabulario de 0.23.0 en `components.md`:** un nivel de radio `recto: 0px`, `borderColor` en el campo, `minHeight`/`minWidth` de 48 en los cuatro controles, y la tabla de las catorce dimensiones del catálogo con su respuesta. Lo que el formato no lleva (foco, trazo, elevación, retícula, medida) va como `--gap` del generador.
- **`DESIGN.md` regenerado con 0.23.0**, idéntico en dos corridas con el comando escrito en ADR-016.
- **Dos instrumentos propios:** `comprobar-medidas.py objetivos` lee los mínimos declarados; `comprobar-dimensiones.py` cuenta las dimensiones contra el catálogo del plugin.
- **Elecciones del humano** (forzadas, sobre láminas): mínimo (B), medida (A) sin tope, **con V3 no cumplido**, elevación (B) solo tono y sangría (A).
- **La hoja:** la tarjeta sin borde, los enlaces `accion` sin sangría y sin centrar, y el campo de Acceso en su propio `<p>`.
- **Los dos juicios que e5 dejó `unsigned`**, firmados sí y sí.
- **La cadena de colores atada en el gate** (T9): `primitives.md` → `semantics.md` → `DESIGN.md`.
- **Parking lot:** tres entradas retiradas (ASCII, interfaz vestida, cadena) y dos hallazgos aparcados (`precedence.py` con eslabones que se vuelven a correr, y sustitución parcial en la técnica `adr`).

**Finalize** (lo que reportó `story-implement`):
- **Gate:** `./scripts/check` verde, 658 pruebas.
- **Pruebas huérfanas:** nueve archivos tocan algo que cambió y s1 no los modificó. Ocho entran por `/acceso` solo para iniciar sesión; el marcado del formulario cambió y el comportamiento no. `test_medicion.py` mide el peso real de la hoja. Todos pasan.
- **Aceptación:** los `@stated` del scope se cumplen salvo lo dicho en *Scope* abajo. Los `@deduced` confirmados en el diseño se cumplen: la hoja verde con los nombres nuevos, `survival-review` corrido y el parking lot al día.
- **Integración manual:** uvicorn con tres ejemplares y fotos reales. Todas las páginas responden 200, la hoja se sirve igual a la del repo (`text/css; charset=utf-8`) y el log no trae errores.

**Scope verificado contra el scope:**
- **"Radio, `borderColor`, `minWidth` y roles en español en `DESIGN.md`":** cumplido.
- **"Regenerado idéntico dos veces":** cumplido (`cmp`).
- **"ADR commiteado en `proposed` antes del primer valor, y `precedence.py` lo confirma":** **parcial.**
  - `add ADR-016` precede a toda tarea.
  - `precedence.py` da FAIL en `semantics.md` y `components.md`, porque compara con la creación de la pieza en e5.
  - Leído a mano: el renombre (T3) tocó las piezas entre dos ediciones del ADR.
  - Está dicho en ADR-016 y aparcado; no se rodeó.
- **"Los dos juicios firmados, los dos ajustes decididos":** cumplido.
- **"Cada cifra que cambió, corregida":** no cambió ninguna. Cambió qué instrumento mide los objetivos (`tokens.py targets` quedó sin sujeto).

**Revisiones:**
- **`quality-review`:** dos defectos en las pruebas de T9, corregidos en `bc7901d`. `test_sin_tablas_no_hay_verde` afirmaba lo contrario de su nombre, y `_leer_cadena` escondía un tipo falso con `type: ignore`. Límites que quedan, dichos:
  - `_declaraciones(".accion")` no ve una regla con otro selector (`main .accion`);
  - la prueba de la hoja no distingue `border-radius: 0` del token (mutación corrida, sobrevive; escrito en ADR-016);
  - las poblaciones 14 y 13 están fijas en las pruebas.
- **`security-review`:** Bandit sobre los 7 `.py` cambiados. Salen 140 hallazgos, todos B101 (`assert`) en `tests/`, el caso ya aparcado. Los dos scripts salen limpios. De las guardas, `must-security-001` no se toca y de ASVS L2 solo cambió marcado. Veredicto: **PASS**.

## What went well

- **Las sondas de la survival-review sirvieron de diseño.** Correr el generador de 0.23.0 con acentos, `borderColor`, `rounded` y `minWidth` antes de abrir la historia dijo exactamente qué podía expresar el formato, y el diseño no tuvo que suponer nada.
- **El rojo antes de producir se vio en cada criterio medible** (V1, V2, `provenance`), con la salida copiada en ADR-016. Cuando el humano eligió (A) en V3, el criterio commiteado no dejó reescribirlo para que pasara: quedó "no se cumple, se elige igual", dicho por el humano.
- **Mirar el render encontró lo que la prueba no veía.** Las capturas con fotos reales mostraron que «Ficha» seguía centrada en su objetivo de 48 px. La prueba de T6 revisaba que no hubiera `padding`, no que el texto quedara alineado.
- **Reusar `_filas` en T9** evitó un quinto lector de tablas en el mismo momento en que se aparcaba el refactor de los lectores.

## What to improve

- **El diseño no revisó qué entradas del parking lot se promovían con la historia.** Dos se cumplían con s1 ("la siguiente historia que toque `governance/identity/ui/`" y "un cuarto script que lea tablas") y aparecieron recién en T7. Una terminó en T9 por re-plan; la otra va a su propia historia. El barrido de promociones es parte de la visita al código en el diseño, no del cierre.
- **Un barrido escrito sin mirar.** Al retirar la entrada de la cadena escribí que la retrospectiva de e5 la citaba sin haberlo comprobado. Luego lo "corregí" al revés con un `grep` demasiado estrecho, y lo arreglé con un tercer commit (`0281c32`, `e5890d2`). Tres commits para un párrafo: el barrido se escribe con la salida del `grep` a la vista.
- **Una afirmación falsa en un ADR recién aceptado:** "el comando completo está en el `plan.md`". No estaba, y se corrigió en `0f3a0b6` poniéndolo en el ADR. Toda referencia a otro archivo se verifica antes del `publish`.
- **La primera lámina fue una ruta `\\wsl.localhost\…` que el humano no pudo abrir.** Las láminas de juicio se publican desde el principio como página privada con las capturas dentro.
- **El plan decía un nombre de ADR con slug en español**, y la técnica `adr` pide slug en inglés. Se usó el inglés, pero el plan no lo leyó de la técnica.

## Learned

1. **About the system:**
   - `design-md.py` de 0.23.0 escribe la tabla `Target` solo con `height`/`width` literales. Un control declarado con mínimos deja a `tokens.py targets` sin sujeto, y el mínimo lo tiene que medir un script propio, leyendo la tabla `Token | Value | From`.
   - `precedence.py` juzga una pieza por su creación. Un eslabón que la técnica `ui` pide volver a correr en el mismo archivo siempre sale en FAIL contra un registro nuevo.
   - La tarjeta tenía una elevación real (tono y borde) que ningún documento declaraba. Responder el catálogo dimensión por dimensión la hizo visible.
2. **About the process:**
   - Una prueba de CSS que mira una propiedad no ve el efecto de otra: el centrado de flex sangraba igual que el relleno. Una decisión visual se verifica en el render, además de en la prueba.
   - Un juicio forzado que contradice su criterio se registra como "no se cumple, se elige igual", nunca retocando el criterio.
3. **Capability gained:**
   - `comprobar-dimensiones.py`: el gate sabe si falta responder una dimensión.
   - `comprobar-medidas.py` mide mínimos declarados.
   - La cadena de colores está atada en el gate.
   - La receta de láminas funciona: uvicorn con datos de prueba, `curl` con cookie, capturas a 360 px en un iframe y publicación privada.

## Follow-ups

- **Refactor de los lectores de tablas:** su entrada en el parking lot tiene la promoción cumplida (cuatro scripts). Va como historia propia.
- **`work/epics/e5-visual-identity/docs.md` quedó desactualizado en dos puntos:** la línea 95 (el límite ASCII) y la 93 (la cadena sin atar). Es de `epic-close` de un epic cerrado y no se reescribe desde aquí. Se aparca con promoción a la próxima vez que se genere documentación de desarrollador.
- **Quitar `'unsafe-inline'` de la CSP:** sigue siendo la historia siguiente del handoff.
