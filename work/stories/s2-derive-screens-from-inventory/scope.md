# Story s2: Derive screens from inventory — Scope

## User story

Como dueño de Orquídea,
quiero que las pantallas de la interfaz web se deriven de un inventario del producto leído del código y confirmado por mí, con la técnica `screens` de gemba-design 0.24.0,
para que cada pantalla que tenga o le falte a la aplicación salga de un objeto o de una tarea con cita, y no de una referencia ni de lo que ya estaba dibujado.

## Acceptance criteria

```gherkin
@stated
Given ninguna entrada del inventario leída todavía
When se abre el ADR de esta historia en `proposed`
Then trae los criterios de supervivencia aplicados, los cuatro de fitness aprobados el 2026-09-24 con su estrato, y las reglas A, B y C en la rejilla, commiteado antes de leer la primera entrada

@stated
Given el inventario escrito en `governance/identity/ui/screens/`
When corre `inventory-sources.py` con el inventario
Then cada entrada cita un `archivo:línea` que existe en su `read-at`, o dice `declared — quién, fecha`, y el script sale 0 con la población contada

@stated
Given el conjunto de pantallas derivado del inventario confirmado
When corre `inventory-sources.py` con el inventario y el conjunto
Then cada pantalla nombra entradas que el inventario tiene, y el script sale 0

@stated
Given el inventario leído
When el humano lo confirma
Then declara las tareas, quita con razón lo que no merece pantalla y firma con nombre y fecha

@stated
Given el conjunto derivado por la regla elegida
When el humano lo lee lado a lado con las tareas y con las pantallas que la aplicación ya muestra
Then firma si la regla fue la correcta, o lo deja `unsigned`

@deduced
Given un inventario con una cita a una línea que no existe en `read-at`, y un conjunto con una pantalla que nombra un `Id` inexistente
When corre `inventory-sources.py`
Then sale en rojo por el criterio, antes de producir los entregables reales
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| un modelo de ejemplar en el código de la aplicación | se lee como objeto | fila `O{n}` con `src/orquidea/…:línea` y `Within` `—` |
| la bitácora de cuidados de un ejemplar | el humano decide si vive dentro del ejemplar | `Within` = el `Id` del ejemplar, y el conjunto no le da pantalla propia sino una sección del detalle |
| "registrar un riego desde el campo" | el humano la declara como tarea | fila `T{n}` con `declared — Daniel Efraín Domínguez Urbina, 2026-09-24` y sus acciones |

## In scope

- Eslabón inventario: objetos, acciones, pantallas existentes y tareas, con cita o declaración, leídos en un commit nombrado.
- Eslabón conjunto de pantallas: derivado del inventario confirmado por la regla que el ADR elija entre A (catálogo, ORCA), B (solo las existentes) y C (solo por tarea).
- Un ADR nuevo, abierto en `proposed` y completado a `accepted` en el mismo archivo.
- El rojo de los criterios medibles visto antes de producir.
- `survival-review` sobre los dos entregables.

## Out of scope

- Guía de prioridad, patrón y composición: los otros tres eslabones de la cadena. Se deciden cuando exista el conjunto.
- Cambiar rutas o plantillas de la aplicación para que muestren pantallas que la regla deriva y hoy no existen: lo que salga del conjunto es insumo para historias futuras.
- Quitar `'unsafe-inline'` de la CSP y el refactor de los lectores de tablas: sus propias historias.

## Done when

- [stated] El ADR estaba commiteado en `proposed` antes del commit que escribe la primera entrada del inventario.
- [stated] `inventory-sources.py` sale 0 sobre el inventario y el conjunto, con la población contada.
- [stated] El inventario lleva la confirmación del humano con fecha, y el conjunto el juicio sobre la regla, firmado o `unsigned`.
- [deduced] El rojo de los criterios 1 y 2 escrito en el ADR antes de producir.
- [deduced] El ADR queda `accepted`, mismo archivo y mismo número.
- [deduced] `./scripts/check` verde.

## Notes

- Standalone: e5 está cerrada. Sale por su cuenta con `integrate` al cerrar.
- Parte de la identidad que dejó e5 y s1 (`governance/identity/ui/`), pero estos dos eslabones no leen `DESIGN.md`: eso empieza en la composición.
- Criterios de fitness aprobados por el humano en la sesión del 2026-09-24: (1) cita o declaración en cada entrada, `mechanical`; (2) cada pantalla nombra entradas existentes, `mechanical`; (3) el inventario confirmado es el producto, `judgement`; (4) el conjunto cubre todas las tareas declaradas, `judgement`.
