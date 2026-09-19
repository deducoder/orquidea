# Story s4.5: Last watering in my collection — Scope

## User story

As a coleccionista,
I want ver la fecha del último riego de cada planta en "Mi colección",
so that sepa cuáles regar sin abrir la ficha de cada una.

## Acceptance criteria

```gherkin
@stated
Given un ejemplar con riegos
When abro "Mi colección"
Then su fila muestra la fecha de su último riego

@stated
Given una colección con varios ejemplares
When abro "Mi colección"
Then la lista pide los últimos riegos con una sola consulta, sin una por ejemplar

@deduced
Given un ejemplar sin riegos
When abro "Mi colección"
Then su fila dice que aún no tiene riegos

@deduced
Given un ejemplar con varios riegos
When abro "Mi colección"
Then la fila muestra el de mayor fecha, el mismo que muestra su ficha

@deduced
Given dos ejemplares con riegos distintos
When abro "Mi colección"
Then cada fila muestra el último de su propio ejemplar

@deduced
Given un riego que se quita en la ficha
When vuelvo a "Mi colección"
Then la fila muestra el nuevo último riego, o que no tiene riegos
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| ejemplar 1 con riegos `2026-09-01` y `2026-09-15`; ejemplar 2 sin riegos | `GET /coleccion` | fila 1: «Último riego: 2026-09-15»; fila 2: «Sin riegos» |
| tres ejemplares | `ultimos(conexion)` | `{1: "2026-09-15", 3: "2026-08-30"}` con una sola sentencia SQL |

## In scope

- `orquidea.datos.riegos.ultimos`: el último riego de todos los ejemplares en una sola consulta.
- La ruta de la lista lo carga una vez y la plantilla lo muestra en cada fila.

## Out of scope

- Fecha del último riego en otras vistas (ficha de especie, inicio) — **not now**.
- Floraciones en la lista — **not now** (RF-07 habla de la ficha).
- Ordenar o filtrar la lista por riego — **not now**.

## Done when

- [stated] La lista de "Mi colección" muestra la fecha del último riego de cada ejemplar (RF-06, fila s4.5 del scope de e4).
- [stated] Se obtiene con una sola consulta para toda la lista, no una por ejemplar (fila s4.5 del scope de e4), demostrado por una prueba que cuenta las consultas.
- [deduced] Coincide con la fecha que muestra la ficha del mismo ejemplar.
- [deduced] Las pruebas de la lista, de las fotos y de la medición siguen en verde sin cambiar sus aserciones.

## Notes

Diseño de la épica: `work/epics/e4-care-log/design.md`. Solo lectura: no añade entrada del usuario. Ningún criterio depende del humano: no hay stop previsible en esta historia.
