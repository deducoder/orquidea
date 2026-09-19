# Epic e4: Care log — Brief

## Hypothesis

Para el coleccionista que hoy no recuerda cuándo regó cada planta ni cuándo floreció,
el registro de cuidados de Orquídea es una bitácora por ejemplar
que acumula riegos y floraciones con fecha.
A diferencia de la memoria o de notas sueltas, responde de inmediato cuándo fue
el último riego y cuál es el historial de floración de cada planta.

## Success metrics

- **Leading:** registrar un riego en un ejemplar y ver la fecha del último riego en su ficha (RF-06).
- **Lagging:** el historial de un ejemplar muestra 50 registros (riegos y floraciones) en orden cronológico y su ficha carga en ≤ 200 KB (`must-perf-001`).

## Appetite

M — 5-7 historias.

## Scope boundaries

What the design may not do. **What it will build is not decided here** — the
in-scope list belongs to `scope.md`, written by `epic-design` after the
decomposition.

### No-gos
- Fertilización y notas por fecha — la entrada del parking lot se queda aparcada por decisión del humano al declarar v0.2.0.
- Recordatorios o avisos de riego — no hay sistemas externos ni notificaciones al usuario (system-context).
- Estadísticas o gráficas de cuidados.

### Rabbit holes
- Un modelo genérico de eventos que anticipe la fertilización: basta con riegos y floraciones.
- Registrar riegos de varios ejemplares a la vez.
