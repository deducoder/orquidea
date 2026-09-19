# Story s4.4: Blooms on the specimen sheet — Retrospective

Estimated: M · Actual: M (5 min entre el commit del plan y el último de las tareas, con tres tareas; más el diseño y la revisión)

## Summary

Tres POST en el router `cuidados` (registrar, fijar el fin y quitar una floración) que validan con `validar_floracion` y `validar_fecha` antes de tocar `datos.floraciones`; la ficha carga el historial (más reciente primero), muestra «en curso» o las dos fechas, ofrece «Terminar» solo en las que están en curso y «Quitar» en todas; `ficha()` recibe `valores` en lugar de `fecha`. Tres commits de tarea: `feat(cuidados)` ×2 y `test(cuidados)`.

## Verification (lo que reportó `story-implement`)

- Gate: `./scripts/check` en verde tras cada tarea (476 pruebas al final).
- Huérfanas: `test_web_rutas.py` (mapa de rutas declarado) se actualizó en T1 y T2. Las demás pruebas que importan `web.app`, `rutas.coleccion` o la ficha y no se tocaron pasan (`test_web_coleccion`, `test_web_fotos`, `test_web_proteccion`, `test_web_acceso`, `test_web_especies`, `test_web_inicio`, `test_web_limite`, `test_medicion`, `test_despliegue`).
- Integración manual con `uvicorn` real y `curl`: acceso, alta del ejemplar, floración en curso y terminada (303), fecha futura y fin anterior (422 con su mensaje), payload `"><script>` devuelto escapado, terminar (303) y terminar de nuevo («ya terminó», 422), `Cache-Control: no-store` y CSP presentes, quitar (303), sin sesión redirige (303), sin trazas; servidor apagado por PID.
- Medición anotada para s4.6: la ficha con 500 riegos y 500 floraciones en curso pesa 500 476 bytes sin comprimir y 14 459 en gzip, y responde en 12 ms.
- Plan sin saltarse: no hubo aprobación de omitirlo.

## Acceptance

- `@stated` (5): registrar sin fin y con fin, fijar el fin, quitar, fechas inválidas o fin anterior con mensaje — cumplidos.
- `@deduced` confirmados por el diseño (7) y cumplidos: ficha vacía, orden y «Terminar» solo en curso, tope, sin sesión, sin CSRF, 404 por ajeno o inexistente, riegos y foto intactos. Escenarios añadidos (4): escape, orden, terminada sin «Terminar», valores por defecto de los otros formularios — cumplidos. Ninguno retractado.
- Un punto del alcance no cumplido y dicho en voz alta: «conservando lo escrito en los campos» vale para registrar (floración y riego), no para «Terminar»: tras un fin rechazado el campo vuelve vacío, porque el formulario de cada fila solo tiene un selector de fecha. No lo pide ningún criterio `[stated]`; se deja.

## Quality review

Verdict: PASS. Observaciones:
- `cuidados.py` tiene ya cinco rutas con la misma forma para riegos y floraciones (validar, escribir, 303 o 422, 404 por filtro). Es la duplicación que ADR-008 aceptó; el `epic-review` decide si se unifica. Destino: `epic-review`.
- `ficha()` carga riegos y floraciones en cada respuesta de ficha, incluida la de un error de foto (dos consultas indexadas): se acepta.
- La ficha sin compresión pesa 500 KB con los dos historiales llenos; la aplicación no comprime y depende del proxy (el presupuesto es en gzip, 14 KB). Destino: s4.6 (mide el peso y decide si el presupuesto o la guía deben decirlo).

## Security review

Bandit sobre los cinco `.py` cambiados: `src/` limpio; 130 × B101 en `tests/`, el ruido ya aparcado. `should-security-002` (ASVS L2): V4 (sesión y CSRF por la dependencia global con pruebas explícitas de las tres rutas; IDOR: floración ajena da 404 en `fin` y `quitar`, con ids desfasados para que un cruce se note) cubierto; V5 (dominio antes de la base, campos devueltos escapados con `"><script>` en `inicio` y en `fin`) cubierto; V11 (tope, fecha no futura, fin no anterior, no terminar dos veces) cubierto; V7 y V2/V3 no aplican. Verdict: PASS.

## What went well

- Las mutaciones encontraron dos pruebas débiles que las pruebas en verde no mostraban: «valores mezclados» (faltaba el sentido inverso) y los ids que coinciden. Ambas se cerraron antes del commit.
- El recorrido de extremo a extremo usa el token y la acción del propio formulario de cada fila (`_formulario`), así que la mutación «formulario sin token» lo pone rojo; la primera versión usaba el token de otra página y no lo veía.
- Medir la ficha llena dio la cifra real en la propia historia, no en la revisión de la épica.

## What to improve

- Otra vez dos avisos de `ruff` por líneas largas de docstrings y comentarios; y un `python3` de edición que falló en silencio porque `ruff format` había cambiado el texto que buscaba. Verificar que una edición por script se aplicó (`git diff --stat`) antes de seguir.
- La prueba del recorrido para riegos (s4.2) todavía toma el token de la ficha con una expresión propia; podría usar `_formulario`. Es un retoque de prueba, sin defecto; no se abre.

## Learned

1. About the system: la ficha es una sola página con tres formularios que pueden volver con error; un diccionario `valores` por formulario evita que uno pise los campos de otro.
2. About the process: una prueba de IDOR con ids que coinciden no prueba nada; hay que desfasar los ids y correr la mutación de argumentos cruzados (memoria nueva).
3. Capability gained: patrón de fila con acciones condicionales («Terminar» solo en curso) y de recorrido por los formularios reales de la página.
