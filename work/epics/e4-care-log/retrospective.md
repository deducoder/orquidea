# Epic e4: Care log — Retrospective

## Summary

El coleccionista registra los riegos y las floraciones de cada ejemplar desde su ficha (`/coleccion/{id}`) y ve dos historiales, cada uno del más reciente al más antiguo, con la fecha del último riego; "Mi colección" muestra el último riego de cada planta con una sola consulta. Las fechas son días de calendario (`AAAA-MM-DD`, sin hora ni zona) validados en el dominio, no posteriores a hoy, con un tope de 500 registros por ejemplar y tipo que se comprueba dentro del mismo `INSERT`. Una floración es un intervalo abierto: se registra en curso o terminada, se cierra con una sola sentencia condicionada y no se reabre. Quitar un ejemplar borra su historial por cascada. Seis historias, un ADR (008: dos tablas con fechas en texto ISO) y una guía con la medición del peso de la ficha.

## Metrics

- Stories: 6 (s4.1 a s4.6) · Estimated: S, M, S, M, S, S · Actual: S, M, S, M, S, S (ninguna cambió de talla).
- 490 pruebas (unas 350 heredadas de e3), `./scripts/check` en verde; 19 commits de tarea (18 de las historias y el retiro de `ultimo`), ninguna dependencia nueva, 1 ADR, 21 entradas en `decisions.md` (18 gates, 1 stop y su respuesta), 1 entrada nueva en el parking lot (la compresión).
- Código: 467 líneas nuevas de aplicación y scripts (11 archivos) y 1 543 de pruebas (8 archivos): unas tres líneas de prueba por cada una de código.
- Mediciones (gzip, sin fotos): ficha con 50 riegos y 50 floraciones, 18,2 KB; con el tope (500 y 500), 29,8 KB, aunque sin comprimir pesa 488,7 KB; "Mi colección" con 25 fotos, 146,5 KB; presupuesto 200 KB.
- Surgió a mitad de la épica y no estaba planeado: la prueba de migración de s4.1 rompió con `0005` (versión fija), dos mutaciones supervivientes en s4.4 (ids que coinciden, valores de un formulario en otro), el hallazgo de que la aplicación no comprime, y, en este review, una función pública sin llamadores.
- Sin despachos: ninguna historia llevó `dispatch.md` ("none dispatched").

## Scope verification

- **MUST — registrar y quitar riegos con fecha de calendario no futura** → **Fulfilled**: `coleccion/modelo.py` (`validar_fecha`), `datos/riegos.py`, `web/rutas/cuidados.py` (`registrar_riego`, `quitar_riego`); `test_coleccion_modelo.py`, `test_datos_riegos.py`, `test_web_cuidados.py`.
- **MUST — ver el historial de riegos y la fecha del último en la ficha (RF-06)** → **Fulfilled**: `ejemplar_ficha.html`, `web/rutas/coleccion.py` (`ficha`).
- **MUST — registrar floraciones con inicio y fin opcional, fijar el fin después, quitarlas y ver su historial (RF-07)** → **Fulfilled**: `datos/floraciones.py` (`agregar`, `terminar`, `quitar`), `cuidados.py`; `test_datos_floraciones.py`, `test_web_cuidados.py`, `test_recorrido_coleccion.py`.
- **MUST — ambos historiales en orden cronológico** → **Fulfilled**: dos listas, cada una del más reciente al más antiguo (`listar` ascendente por fecha o inicio y la ficha lo invierte); el humano confirmó que eso cumple «orden cronológico» (`decisions.md`, `Answered` de `epic-review`).
- **MUST — quitar un ejemplar borra su historial** → **Fulfilled**: `ON DELETE CASCADE` en `0004` y `0005` con `foreign_keys = ON`; pruebas de datos y el recorrido de riegos por HTTP.
- **MUST — toda ruta nueva exige sesión y, las que escriben, el token CSRF; un tope de registros por ejemplar y tipo** → **Fulfilled**: dependencia global `exigir_sesion` con pruebas explícitas por ruta (`test_web_cuidados.py`, `test_web_proteccion.py`); tope de 500 atómico (`test_altas_simultaneas…`, 15 corridas).
- **SHOULD — último riego en "Mi colección"; mensajes claros; medición del peso de la ficha** → **Fulfilled**: `datos.riegos.ultimos` (una sola sentencia, probada con `set_trace_callback`), mensajes del dominio en español, `scripts/medir-primera-carga.py` con `medir_ficha`.
- **[stated] registrar un riego y ver la fecha del último riego en su ficha** → **Fulfilled**: `test_registrar_un_riego_y_ver_el_ultimo_en_la_ficha_del_ejemplar` y las pruebas manuales con `uvicorn` en s4.2 y s4.5.
- **[stated] la ficha con 50 registros los muestra en orden cronológico y transfiere ≤ 200 KB (`must-perf-001`)** → **Fulfilled por script, con reserva aceptada por el humano**: 18,2 KB con 50+50 y 29,8 KB con el tope, protegidos por `test_medicion.py`; la medición con "Slow 3G" en el navegador con la aplicación desplegada queda **pendiente del humano** (`decisions.md`, `Answered` de `epic-review`: "el peso se da por cumplido con la medición por script y la de Slow 3G queda pendiente del humano").
- **[deduced] fechas inválidas, inexistentes, futuras o fin anterior rechazadas sin cambiar la base; tope con mensaje; borrado en cascada y por registro; sesión, CSRF y 404 por ajeno; texto del formulario escapado; migraciones `0004` y `0005` sobre una base de e3 con datos** → **Fulfilled**: `test_coleccion_modelo.py`, `test_datos_riegos.py`, `test_datos_floraciones.py` (incluye las migraciones sobre bases en las versiones 3 y 4), `test_web_cuidados.py` (payload `"><script>` en cada campo).
- **[stated] all stories complete · docs updated · retrospective done** → historias y retrospectiva hechas; `docs.md` lo escribe `epic-close`.

No hay compromisos de eliminación en el alcance.

## Reviews a escala de épica

**Quality review — PASS WITH RECOMMENDATIONS.** Rango `1ca0592..HEAD` (desde el commit previo al diseño de e4; el brief se escribió antes de e3), 15 `.py`. Lo que solo se ve entre historias: `datos.riegos.ultimo` (s4.1) quedó sin ningún llamador cuando s4.2 leyó la ficha con `listar()[-1]` y s4.5 creó `ultimos`; solo lo ejercitaban pruebas. Quitado en `refactor(datos): quitar ultimo, que ningún código de la aplicación llamaba`. Recomendaciones sin acción: `datos.riegos` y `datos.floraciones` y las cinco rutas de `cuidados.py` tienen la misma forma (el costo que ADR-008 declaró al preferir dos tablas a un genérico; no se une mientras solo haya dos cuidados, y la fertilización aparcada decidiría); `cuidados.py` importa `ficha`, `hoy` y `ejemplar_o_404` de `coleccion.py`, una dependencia entre módulos de rutas aceptable mientras `coleccion.py` (276 líneas) no crezca más. Sin tipos deshonestos ni pruebas sin valor nuevas.
**Security review — PASS.** Bandit sobre el mismo rango: 0 hallazgos fuera de `tests/`; 287 × B101 en `tests/` (ruido ya registrado). Composición de guardarraíles (`should-security-002`, ASVS L2): las cinco rutas de escritura heredan sesión y CSRF de la dependencia global y cada una filtra por ejemplar y registro (IDOR probado con ids desfasados); la fecha se valida en el dominio y en el `CHECK` de la tabla, y lo que vuelve al formulario sale escapado; el tope y `terminar` son atómicos ante hilos. Limitación: análisis estático; la concurrencia se probó con hilos y conexiones propias y las rutas con `uvicorn` real en cada historia.

## What went well

- Hacer primero la capa de datos con sus reglas (s4.1, s4.3) y después las rutas (s4.2, s4.4) dejó a las historias de la ficha apoyándose en contratos ya probados; s4.3 y s4.5 fueron casi mecánicas por el molde de s4.1.
- Las mutaciones sistemáticas cerraron huecos que las pruebas en verde no veían (ids que coinciden, valores mezclados entre formularios, la ficha tapada por la lista en el presupuesto) y las de concurrencia fallaron 15 de 15.
- Medir con el tamaño máximo desde el diseño (lección de e3) no dio sorpresas: 500 registros caben en milisegundos y en 30 KB de gzip; la única novedad, que la aplicación no comprime, quedó documentada y aparcada con su condición.
- El criterio rezagado se previó desde el diseño como stop P4 (lección de e1 a e3) y esta vez la pregunta llegó ya con la evidencia y con la ambigüedad del «orden cronológico» separada de la del peso.

## What to improve

- Escribí en dos retrospectivas de historia una cifra de pruebas sin comprobarla (399 en lugar de 406 en s4.2, 467 en lugar de 476 en s4.4) y las corregí después; toda cifra de una retrospectiva se copia de la salida de un comando.
- Dos avisos de `ruff` (`E501`) y dos de `mypy` por historia costaron un ciclo cada uno; pasar `ruff check` y `mypy` al terminar cada archivo de pruebas, no en el gate.
- Una función pública pasó tres revisiones de historia sin llamadores (`ultimo`) porque cada historia miraba solo su diff; al planear una función "para la historia siguiente", anotar en el plan de esa historia que debe usarla.
- La medición con "Slow 3G" sigue sin hacerse en las cuatro épicas; deja de ser una sorpresa, pero sigue siendo una deuda del humano.

## Learned

1. About the system: la ficha es una sola página con tres formularios que pueden volver con error, y el patrón que funciona es un diccionario de valores por formulario; el historial cabe en una tabla por tipo con el tope y la transición de estado dentro de una sola sentencia SQL, y "hoy" del servidor (UTC) es una decisión visible (ADR-008 y README).
2. About the process: las pruebas de IDOR necesitan ids desfasados; el rango de revisión de una épica se toma desde el commit previo a su diseño y no desde su brief cuando este se escribió antes; y una prueba de presupuesto solo cuenta si aísla cada medición.
3. Capability gained: historial de cuidados por ejemplar con garantías probadas (fechas de calendario, tope atómico, transición de floración, cascada), `coleccion_temporal()` para medir cualquier página sobre una base temporal, y un patrón de fila con acciones condicionales para futuros cuidados (fertilización aparcada).
