# Story s2: Derive screens from inventory — Plan

La historia no escribe código. La verificación de cada tarea es `inventory-sources.py` (ya visto en rojo en ADR-017) y `./scripts/check` antes de cada commit.

| # | Tarea | Verificación | Commit |
|---|-------|--------------|--------|
| T1 | Inventario leído: objetos, acciones y pantallas existentes con cita en `read-at`; tareas propuestas desde el PRD; `Within` y removidos propuestos, **sin confirmar** | `inventory-sources.py` exit 0 | `docs(identity): read the screens inventory` |
| T2 | Confirmación del dueño: tareas, `Within`, removidos y firma de F3 | exit 0; `confirmed-by` con nombre y fecha | `docs(identity): confirm the screens inventory` |
| T3 | Conjunto de pantallas: correr A, B y C sobre el inventario confirmado; llenar la rejilla de ADR-017; escribir `screen-set.md` con la regla que el dueño elija | exit 0 con más de cero pantallas | `docs(identity): derive the screen set` |
| T4 | Juicio F4 del dueño sobre la regla (firmado o `unsigned`); ADR-017 `accepted` | rejilla sin celdas `pending` | `docs(s2): accept ADR-017` |
| T5 | `survival-review` sobre los dos entregables | población contada | `docs(identity): review the screens deliverables` |

Prueba manual de integración: leer lado a lado `screen-set.md` y las rutas de `web/rutas/`. Cada pantalla marcada `Exists in code` corresponde a un `GET` que dibuja plantilla.
