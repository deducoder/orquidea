# Story s4.1: Waterings domain and storage — Retrospective

Estimated: S · Actual: S (3 min entre el commit del plan y el último de las tareas; más el diseño y la revisión)

## Summary

Migración `0004-riegos.sql` (cascada, `CHECK` de forma de la fecha, índice), `validar_fecha` estricta en el dominio, el tope de 500 riegos por ejemplar y `datos.riegos` con `agregar`, `listar`, `ultimo` y `quitar`, siempre filtrados por ejemplar y registro. Tres commits de tarea: `feat(coleccion)`, `feat(datos)` y `test(datos)`.

## Verification (lo que reportó `story-implement`)

- Gate: `./scripts/check` en verde tras cada tarea (385 pruebas al final).
- Huérfanas: ninguna. Las pruebas que importan `coleccion.modelo`, `datos.base` o `datos.ejemplares` y no se tocaron (`test_datos_base`, `test_datos_ejemplares`, `test_web_coleccion`, `test_recorrido_coleccion`, `test_web_fotos`, `test_datos_almacen_fotos`, `test_datos_sesiones`) pasan; ninguna asume un número fijo de migraciones.
- Integración manual (proceso aparte, base real): una base en la versión 3 con ejemplar y foto migra a la 4 sin perder nada; tres riegos dan por último el de mayor fecha; quitar el ejemplar deja `riegos` vacía.
- Plan sin saltarse: no hubo aprobación de omitirlo.

## Acceptance

- `@stated` (3): agregar y listar, último de mayor fecha, fecha inválida rechazada con mensaje — cumplidos.
- `@deduced` confirmados por el diseño (7) y cumplidos: orden por fecha e id, quitar solo el propio, id ajeno no quita nada, cascada, tope, ejemplar inexistente, migración sobre la versión 3.
- Escenarios añadidos por el diseño (3): formatos que `fromisoformat` aceptaría, altas simultáneas, `CHECK` de la tabla — cumplidos. Ninguno retractado.

## Quality review

Verdict: PASS. Observaciones sin acción:
- `agregar` confía en que la fecha ya viene validada; el `CHECK` solo comprueba la forma (`2026-13-45` la pasaría). Es intencional (dos capas, el dominio valida la existencia): s4.2 debe llamar a `validar_fecha` antes de `agregar`, y su prueba de ruta lo cubre. Destino: s4.2.
- `CUIDADOS_MAXIMO` es común a riegos y floraciones; el mensaje de `agregar` nombra «riegos», y s4.3 pondrá el suyo. Destino: s4.3.

## Security review

Bandit sobre los cuatro `.py` cambiados: `src/` limpio (0 hallazgos); 42 × B101 (`assert`) en `tests/`, el ruido ya aparcado en el parking lot (entrada «Bandit reporta B101 en `tests/`»). Guardrail `should-security-002` (ASVS L2), recorrido: V5 validación (cubierto: regex ASCII, `fromisoformat`, `CHECK`, SQL parametrizado), V4 IDOR (cubierto a nivel de datos: `quitar` filtra por ejemplar y registro, con prueba), V11 lógica de negocio (cubierto: tope atómico y fecha no futura). Sesión y CSRF de las rutas: s4.2. Verdict: PASS.

## What went well

- Medir con el tamaño máximo desde el diseño (memoria del proyecto): 500 riegos, 97 KB de HTML sin comprimir, 7 ms de altas; no hubo sorpresas después.
- Las mutaciones planeadas se corrieron todas (4 en T1, 6 en T2, 2 en T3) y todas pusieron rojo la prueba; la de "contar y luego insertar" falló 15 de 15.

## What to improve

- Dos veces el gate salió rojo por cosas mías fuera del código: una línea de 101 caracteres y el `design.md` sin formatear (`ruff format` también formatea los `.md` del work log, ya en la memoria). Correr `./scripts/check` al escribir un artefacto, no solo al escribir código.
- La prueba de altas simultáneas pasó en verde de entrada (T2 ya era atómico); el RED de T3 no existe como tal. Se compensó con la mutación, pero un plan honesto la habría marcado como prueba de caracterización desde el principio.

## Learned

1. About the system: `abrir_base`/`conectar` dan una conexión por petición con `foreign_keys = ON`, así que una cascada en la migración basta para la baja del ejemplar sin tocar `almacen_fotos`.
2. About the process: un tope por ejemplar solo es honesto si se prueba con conexiones distintas; con una compartida SQLite serializa y la carrera no aparece.
3. Capability gained: patrón de tabla de cuidados (migración con cascada + `CHECK` + módulo de funciones filtradas por ejemplar y registro) que s4.3 repite.
