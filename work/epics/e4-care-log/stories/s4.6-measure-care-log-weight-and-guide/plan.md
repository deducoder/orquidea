# Story s4.6: Measure care log weight and guide — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · El montaje de la colección temporal, en un administrador de contexto

- **Files:** modify `scripts/medir-primera-carga.py`
- **TDD:** refactor sin comportamiento nuevo: la red es `tests/test_medicion.py` (`medir` conserva su firma, su resultado y el restaurado de `app.state`); se extrae `coleccion_temporal()` que monta la base y las fotos temporales, inicia una sesión y devuelve cliente y conexión, y restaura al salir → REFACTOR
- **Satisfies:** `@deduced` de que la medición de la lista sigue igual y de que no deja rastro
- **Mold:** `scripts/medir-primera-carga.py::medir` (el montaje actual)
- **Verify:** las cuatro pruebas de `test_medicion.py` pasan sin editarse — forced mutations: no restaurar `app.state` en el `finally` (`test_medir_deja_la_aplicacion_como_estaba` falla); no cerrar la conexión antes de pedir la lista (la lectura ve una base bloqueada o incompleta: `test_la_coleccion_de_ejemplo_cabe...` falla); then `uv run pytest tests/test_medicion.py -q` y `./scripts/check`
- **Commit:** refactor(medicion): el montaje de la colección temporal, aparte

### T2 · Medir la ficha con el historial lleno y protegerla en el gate

- **Files:** modify `scripts/medir-primera-carga.py`, `tests/test_medicion.py`
- **TDD:** RED pruebas: `medir_ficha(50, 50)` y `medir_ficha(500, 500)` cuentan HTML y JavaScript en gzip (mayores que 0, gzip menor que el HTML sin comprimir), caben en `PRESUPUESTO`, y dejan `app.state` como estaba (también si falla a la mitad); `main` con `--presupuesto 1` sale con 1 y nombra la ficha; sin argumentos sale con 0 e imprime la lista y las dos fichas → GREEN `MedicionDeFicha`, `medir_ficha` (inserta por SQL en lotes) y `main` → REFACTOR
- **Satisfies:** los tres primeros `@stated` (50 y 50, el tope, la prueba del gate) y los `@deduced` del script; escenarios añadidos del código de salida y del restaurado tras un fallo
- **Mold:** `scripts/medir-primera-carga.py::medir` y `tests/test_medicion.py`
- **Verify:** la prueba falla si la ficha pasa del presupuesto y el script lo dice — forced mutations: medir el HTML sin comprimir en lugar de gzip (la ficha llena pasa de 200 KB: la prueba del tope falla); comparar contra `PRESUPUESTO * 10` (el caso `--presupuesto 1` deja de dar 1); insertar solo la mitad de los registros (una aserción sobre el número de filas insertadas o sobre `<li>` en la ficha falla); no restaurar `app.state` tras una excepción (la prueba del fallo falla); then `uv run pytest tests/test_medicion.py -q` y `./scripts/check`
- **Commit:** feat(medicion): medir el peso de la ficha con el historial de cuidados lleno

### T3 · README, prueba de la guía y el hallazgo de la compresión

- **Files:** modify `README.md`, `tests/test_despliegue.py`, `records/parking-lot.md` (con la técnica `park`: el hallazgo de s4.4 fue nombrado y no se abre; su trigger, «whenever something is named and not opened», se cumple)
- **TDD:** RED en `test_cada_cifra_de_la_guia_es_la_de_su_constante`: añadir la cifra del tope (`CUIDADOS_MAXIMO` riegos y floraciones) y una prueba de que la guía menciona el historial de cuidados, `medir-primera-carga` y que la aplicación no comprime → GREEN sección «Historial de cuidados» del README → REFACTOR
- **Satisfies:** el `@stated` del README
- **Mold:** la sección «Fotos» del README y `test_cada_cifra_de_la_guia_es_la_de_su_constante`
- **Verify:** la guía y el código no se separan y el README no lleva secretos — forced mutations: cambiar `CUIDADOS_MAXIMO` a 400 sin tocar el README (la prueba de la cifra falla); quitar la línea de la compresión (la prueba nueva falla); pegar un hash de contraseña en el README (`test_el_readme_no_contiene_un_hash_real` falla); then `uv run pytest tests/test_despliegue.py -q` y `./scripts/check`
- **Commit:** docs(readme): el historial de cuidados y el peso de la ficha

### T4 · Manual integration test

- Correr `uv run python scripts/medir-primera-carga.py` y ver las tres mediciones y el código de salida 0; correrlo con `--presupuesto 1` y ver el código 1; leer la sección nueva del README como quien despliega por primera vez; confirmar que la base real (`data/`) no cambió.
- **Verify:** las tres mediciones salen con OK, el código es 0 (y 1 con el presupuesto de 1 KB) y el README se entiende sin abrir el código.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 — T1 deja el terreno; T2 es lo que protege el peso (el criterio `[stated]`); T3 es documentación.
- **Dependencies:** secuencial.
- **Risks:** tocar `medir` rompe la medición de la lista de e3 → T1 aparte con `test_medicion.py` como red; una medición que falla deja `app.state` cambiado → `finally` y prueba con excepción; una guía que dice una cifra que el código ya cambió → la cifra del tope sale de la constante y la prueba de la guía la comprueba; el hallazgo de la compresión se queda sin destino → entrada del parking lot con su condición de promoción.
