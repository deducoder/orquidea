# Story s4.6: Measure care log weight and guide — Scope

## User story

As a coleccionista,
I want saber que la ficha de un ejemplar sigue cargando rápido aunque acumule años de riegos y floraciones, y tener por escrito cómo funciona el historial,
so that el registro de cuidados no vuelva lenta la aplicación ni me sorprenda al desplegarla.

## Acceptance criteria

```gherkin
@stated
Given un ejemplar con 50 registros entre riegos y floraciones
When se mide la primera carga de su ficha
Then el peso transferido (HTML y JavaScript en gzip, sin fotos) es de a lo más 200 KB

@stated
Given un ejemplar con el tope de registros de cada tipo
When se mide la primera carga de su ficha
Then el peso transferido es de a lo más 200 KB

@stated
Given el presupuesto de la ficha
When el gate corre
Then una prueba automatizada falla si la ficha lo rebasa

@stated
Given el README
When se lee la sección del historial de cuidados
Then explica el historial de riegos y floraciones, su tope, sus fechas y cómo medir el peso

@deduced
Given el script de medición existente
When se corre sin argumentos
Then sigue midiendo "Mi colección" como antes y añade la ficha con historial lleno

@deduced
Given la medición de la ficha
When se corre
Then deja la aplicación como estaba y no toca la base real

@deduced
Given una ficha que pasa del presupuesto
When se corre el script
Then sale con código 1 y lo dice
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| ejemplar con 25 riegos y 25 floraciones | `medir_ficha(25, 25)` | `Medicion` con HTML y JavaScript en gzip; total ≤ 200 KB |
| ejemplar con 500 riegos y 500 floraciones | `medir_ficha(500, 500)` | ~14 KB en gzip de HTML más ~16 KB de JavaScript |
| `--presupuesto 1` | `uv run python scripts/medir-primera-carga.py` | «PASA DEL PRESUPUESTO», salida 1 |

## In scope

- Extender `scripts/medir-primera-carga.py` con la medición de la ficha con historial (50 y 50, y el tope 500 y 500), reutilizando el montaje de la colección temporal.
- Una prueba en el gate del presupuesto de la ficha en ambos casos.
- Sección «Historial de cuidados» del README: qué se guarda, fechas de calendario, tope, respaldo (la misma base) y la medición.
- Destino del hallazgo de s4.4: la aplicación no comprime y el presupuesto es en gzip (una entrada del parking lot y una línea del README).

## Out of scope

- Añadir compresión a la aplicación — **not now** (se decide con la entrada del parking lot).
- Medir con "Slow 3G" en el navegador — la hace el humano con la aplicación desplegada: **stop previsible** (P4 en `epic-review`), fuera de esta historia.
- Paginar el historial — **not now** (el tope de 500 lo acota).
- Cambios en las rutas o en la ficha — no hay.

## Done when

- [stated] La ficha con 50 registros y con el tope (500 riegos y 500 floraciones) transfiere ≤ 200 KB sin contar fotos, medido por script (métrica rezagada del brief, `must-perf-001`, en su parte de bytes) y protegido por una prueba del gate.
- [stated] El README explica el historial de cuidados y cómo medir su peso (fila s4.6 del scope de e4).
- [stated] La parte de `must-perf-001` con "Slow 3G" en el navegador no se cierra aquí: es del humano (stop previsible P4 en `epic-review`).
- [deduced] El script sigue midiendo "Mi colección" y las pruebas de `test_medicion.py` pasan sin cambiar sus aserciones.
- [deduced] La medición no deja rastro en la aplicación ni en la base real.

## Notes

Diseño de la épica: `work/epics/e4-care-log/design.md`. Medidas de s4.4: la ficha con 500 y 500 pesa 500 KB sin comprimir y 14 KB en gzip; la aplicación no comprime y depende del proxy. Sigue el patrón de e3/s3.6 (`scripts/medir-primera-carga.py`, `tests/test_medicion.py`, README). Un criterio depende del humano (Slow 3G): ya previsto como stop en `epic-review`.
