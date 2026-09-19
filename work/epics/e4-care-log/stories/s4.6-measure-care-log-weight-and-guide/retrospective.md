# Story s4.6: Measure care log weight and guide — Retrospective

Estimated: S · Actual: S (4 min entre el commit del plan y el último de las tareas, con tres tareas; más el diseño y la revisión)

## Summary

`scripts/medir-primera-carga.py` extrae `coleccion_temporal()` y añade `medir_ficha`, que monta un ejemplar con N riegos y N floraciones en curso y mide su ficha en gzip; `main` mide la lista y las fichas con 50+50 y con el tope 500+500 y sale con 1 si cualquiera pasa de 200 KB. `tests/test_medicion.py` protege el presupuesto en el gate. El README gana «Historial de cuidados» (qué se guarda, fechas UTC, tope, respaldo, medición y compresión) y `test_despliegue.py` ata la cifra del tope a `CUIDADOS_MAXIMO`. Tres commits de tarea: `refactor(medicion)`, `feat(medicion)` y `docs(readme)`.

## Verification (lo que reportó `story-implement`)

- Gate: `./scripts/check` en verde tras cada tarea (493 pruebas al final).
- Huérfanas: ninguna sin resolver. `test_medicion.py` y `test_despliegue.py` son las que importan lo cambiado y se ampliaron sin cambiar aserciones previas; las demás no se tocaron y pasan.
- Integración manual: `uv run python scripts/medir-primera-carga.py` mide la lista (146,5 KB), la ficha con 50+50 (18,2 KB; 50,8 KB sin comprimir) y con el tope (29,8 KB; 488,7 KB sin comprimir), todo OK y salida 0; con `--presupuesto 1` las tres dicen «PASA DEL PRESUPUESTO» y sale 1; la base real (`data/`) no cambió.
- Plan sin saltarse: no hubo aprobación de omitirlo.

## Acceptance

- `@stated` (4): ficha con 50 registros ≤ 200 KB, con el tope ≤ 200 KB, prueba del gate, sección del README — cumplidos.
- `@deduced` confirmados por el diseño (3) y cumplidos: la lista se mide como antes, la medición no toca la base real y restaura `app.state` incluso si falla, salida 1 si la ficha pasa. Escenarios añadidos (2): `--presupuesto 1` nombra las fichas, restaurado tras un fallo — cumplidos. Ninguno retractado.
- La parte de `must-perf-001` con "Slow 3G" en el navegador **no se cierra aquí**: es del humano, prevista desde el diseño de la épica como stop P4 en `epic-review` (el README lo repite).

## Quality review

Verdict: PASS. Observaciones:
- `main` repite la impresión de la lista y de la ficha con un formato casi igual; son ~10 líneas de un script de medición y unificarlas costaría más que dejarlo.
- `test_medicion.py` afirma sobre `filas` (conteo de `<li>`); depende del marcado de la ficha, pero es lo que demuestra que la medición insertó y midió todos los registros.

## Security review

Bandit sobre los tres `.py` cambiados: el script sin hallazgos; 65 × B101 en `tests/`, el ruido ya aparcado. `should-security-002` (ASVS L2): sin cambios de comportamiento de la aplicación; V14: el README no lleva secretos y la prueba existente de `test_despliegue.py` lo vigila (con la mutación de pegar un hash, falla). Verdict: PASS.

## What went well

- Diseñar desde el hallazgo medido en s4.4 (500 KB crudos, 14 KB en gzip) dio un destino claro al dato incómodo: README y entrada del parking lot (con `park`), sin añadir compresión que nadie pidió.
- Las mutaciones encontraron dos supervivientes reales (`--presupuesto 1` hacía que la lista tapara a la ficha); una prueba con `monkeypatch` que aísla la ficha las cerró.
- Atar la cifra del README a `CUIDADOS_MAXIMO` con la prueba existente de la guía evita que documentación y código se separen.

## What to improve

- Otra vez un `E501` de `ruff` en mi propio código antes del gate; y una mutación mal escrita al principio (un `sed` con saltos de línea que no aplicaba nada): comprobar con `git diff` que la mutación cambió algo antes de leer el resultado.

## Learned

1. About the system: una ficha con el tope de historial pesa ~500 KB sin comprimir; solo el proxy la lleva a ~30 KB con el JavaScript, y esa dependencia es ahora una entrada explícita del parking lot.
2. About the process: una prueba de presupuesto con un valor pequeño (`--presupuesto 1`) no prueba que cada medición cuente: hay que aislar cada medición con datos falsos donde solo una falle.
3. Capability gained: `coleccion_temporal()` sirve a cualquier medición futura de una página sobre una base temporal con sesión.
