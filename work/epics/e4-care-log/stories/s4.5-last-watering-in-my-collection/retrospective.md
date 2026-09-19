# Story s4.5: Last watering in my collection — Retrospective

Estimated: S · Actual: S (1 min entre el commit del plan y el último de las tareas, con dos tareas; más el diseño y la revisión)

## Summary

`datos.riegos.ultimos` (un `MAX(fecha) … GROUP BY ejemplar_id` sobre el índice de s4.1) y la lista de "Mi colección" que lo carga una vez y muestra «Último riego: AAAA-MM-DD» o «Sin riegos» en cada fila. Dos commits de tarea: `feat(datos)` y `feat(coleccion)`.

## Verification (lo que reportó `story-implement`)

- Gate: `./scripts/check` en verde tras cada tarea (484 pruebas al final).
- Huérfanas: ninguna. Las pruebas que pasan por `coleccion.html` o la ruta y no se tocaron (`test_web_coleccion`, `test_web_fotos`, `test_medicion`, `test_datos_floraciones`) pasan sin cambiar una aserción.
- Integración manual con `uvicorn` real y `curl`: tres ejemplares, riegos en dos; la lista muestra «Último riego: 2026-09-15», «Sin riegos» y «Último riego: 2026-08-30»; quitar el último riego del primero en su ficha deja «2026-09-01» en la lista; sin trazas; servidor apagado por PID. `scripts/medir-primera-carga.py`: 146,5 KB de 200 KB, sale con 0.
- Plan sin saltarse: no hubo aprobación de omitirlo.

## Acceptance

- `@stated` (2): la fila muestra el último riego; se pide con una sola consulta — cumplidos (una prueba cuenta las sentencias SQL de `ultimos` y otra las llamadas desde la ruta).
- `@deduced` confirmados por el diseño (4) y cumplidos: «Sin riegos», el de mayor fecha igual al de la ficha, cada fila el suyo, la lista se actualiza al quitar. Escenario añadido (una sola sentencia con cinco ejemplares) — cumplido. Ninguno retractado.

## Quality review

Verdict: PASS. Sin observaciones: una función de datos de cuatro líneas y una línea de plantilla por caso; nada especulativo ni sin uso.

## Security review

Bandit sobre los cuatro `.py` cambiados: `src/` limpio; 145 × B101 en `tests/`, el ruido ya aparcado. `should-security-002` (ASVS L2): solo lectura por una ruta que ya exige sesión; V4 sin cambios (la dependencia global y sus pruebas cubren `/coleccion`); V5 de salida cubierto (la fecha sale con el escape de la plantilla); V7, V8 y V11 no aplican. Verdict: PASS.

## What went well

- Las pruebas usaron ids desfasados desde el principio (memoria de s4.4) y la mutación «riego de otra fila» falló a la primera.
- Contar sentencias con `set_trace_callback` demuestra la «consulta única» en vez de afirmarla.

## What to improve

- Otra vez dos errores de `mypy` en pruebas recién escritas (un `re.findall` que devuelve `Any` y una expresión con `append` dentro de un `lambda`); correr `mypy` al terminar el archivo de pruebas, no en el gate.

## Learned

1. About the system: la lista ya tenía toda la colección en Python; el costo de cualquier dato por ejemplar es cuántas consultas, no cuántas filas, y un agregado con el índice de la tabla lo deja en una.
2. About the process: una historia S con un molde claro (`ultimo`, `mi_coleccion`) cabe en dos tareas y el diseño puede ser corto sin dejar de medir.
3. Capability gained: prueba de «consulta única» con `set_trace_callback` y `monkeypatch` que cuenta llamadas.
