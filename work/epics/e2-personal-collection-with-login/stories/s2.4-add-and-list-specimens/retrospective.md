# Story s2.4: Add catalog specimens and see them — Retrospective

Estimated: M · Actual: M

## Summary

El usuario agrega desde la ficha de una especie un ejemplar a su colección ("Agregar a mi colección", un formulario `POST` sin JavaScript) y lo ve en "Mi colección" (`GET /coleccion`) con el nombre científico enlazado a la ficha y la fecha de alta en UTC. La migración `0002-ejemplares.sql` crea la tabla completa de RF-04 (`especie_id`, `nombre`, `notas`, `creado`, con un `CHECK` que exige nombre si no hay especie); el dominio `orquidea.coleccion` (`Ejemplar`, `resolver`) no conoce HTTP ni SQL y `orquidea.datos.ejemplares` guarda y lista con SQL parametrizado. Una especie inexistente da 404; una desaparecida del catálogo se lista con aviso; recargar no duplica (POST-303-GET). La cabecera trae "Catálogo" y "Mi colección" y el campo CSRF vive en un parcial `_csrf.html`. Cuatro commits de tarea (más uno de preparación de fábricas de prueba dentro del primero).

## Finalize (reportado por story-implement)

- **Gate:** `./scripts/check` en verde, 172 pruebas (146 al cierre de s2.3 + 26), ruff, ruff format, mypy strict.
- **Orphaned-test check:** los archivos que importan `orquidea.web.app` o las migraciones (`test_web_inicio`, `test_web_especies`, `test_web_acceso`, `test_web_proteccion`, `test_datos_base`, `test_datos_sesiones`) o se tocaron o siguen pasando sin cambios (`test_web_proteccion` enumera `app.routes` y cubre las rutas nuevas sin editarlo; `test_datos_sesiones` migra la base real y ahora aplica también `0002`). `tests/fabricas.py` sustituye a la copia de `especie()` que vivía en `test_web_especies.py`. Limpio.
- **Acceptance:** los cinco escenarios `@stated`, los cinco `@deduced` y los tres del diseño tienen prueba; `test_recorrido_coleccion.py` recorre la métrica líder del brief sin atajos (contraseña real, ficha del catálogo real, token extraído del propio formulario, colección, reabrir la base). Prueba manual (T4) con `uvicorn` real y `curl`: tres altas (dos de la misma especie), 404 con una especie inexistente, tres entradas enlazadas a su ficha y las tres siguen tras reiniciar el proceso.
- **Plan con `> Pause: none`:** sin aprobación humana por tarea; el despacho se decidió en `decisions.md`.
- **Tiempo de implementación:** sin tracker; derivable de la rama, no registrado.

## Reviews

- **quality-review:** sin críticos. Observaciones: (1) `creado` se muestra en UTC; una alta cerca de la medianoche de México aparece con el día siguiente. Está dicho en el diseño y probado; si molesta, la zona horaria del usuario sería una decisión nueva, no un defecto. (2) La tabla trae `nombre` y `notas` que s2.4 no usa: adelanto deliberado, declarado en el plan. (3) La ruta valida la especie contra `app.state.catalogo` en lugar de que el dominio lo haga; con una sola ruta que agrega, no hay duplicación que justificar otra capa.
- **security-review:** PASS. Bandit: 0 hallazgos en `src/`; 83 B101 (baja) en `tests/`, ya estacionados. Guardrails `should-security-002`, recorridos en el diseño: entrada validada (V5: el `especie_id` solo se guarda si está en el catálogo), consultas parametrizadas (probado con un identificador con comillas), salida escapada (probado con HTML en el nombre científico), CSRF y sesión heredados de la dependencia global (probados para esta ruta). Sin acceso a un ejemplar por identificador todavía: el control de acceso a nivel de objeto (V4.2.1) se revisa en s2.6, que introduce esas rutas.

## What went well

- Las mutaciones encontraron dos pruebas que no mordían, ambas por compartir un valor con otro elemento de la página: el token del botón de la ficha coincidía con el de la cabecera, y la fecha en UTC coincidía con la local porque el entorno de pruebas está en UTC. Se arreglaron aislando el formulario con una expresión regular y forzando `TZ=America/Mexico_City` con una alta cerca de la medianoche UTC.
- La prueba de extremo a extremo (T3) pasó a la primera porque T2 ya se había escrito contra el HTML real; funcionó como red de seguridad de cara a s2.5 y s2.6.
- La enumeración de `app.routes` de s2.3 cubrió las rutas nuevas sin cambiarla.

## What to improve

- `ruff` (S608) rechazó el SQL con f-string que usé para no repetir la lista de columnas; la lista repetida en una sola consulta es más simple que la abstracción. Escribir el SQL literal desde el principio.
- Dos aserciones de plantilla necesitaron un segundo intento: cuando dos partes de la página comparten un valor, acotar la aserción al elemento (el `<form>` concreto).

## Learned

1. About the system: la fecha de un ejemplar guardada como segundos epoch se formatea en UTC con un filtro Jinja; `time.tzset()` con `monkeypatch.setenv("TZ", …)` permite probar la zona horaria (hay que restaurar con `monkeypatch.undo()` y otro `tzset()`); el `TestClient` sigue redirecciones con `follow_redirects=True` y expone la URL final.
2. About the process: para probar un elemento de una página que comparte valores con otro, extraerlo primero (regex sobre el `<form>`) y afirmar sobre el extracto.
3. Capability gained: colección persistente con dominio, repositorio y vista; s2.5 y s2.6 solo añaden campos y rutas sobre la misma tabla y la misma plantilla.
