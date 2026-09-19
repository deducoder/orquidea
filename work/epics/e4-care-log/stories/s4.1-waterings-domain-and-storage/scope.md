# Story s4.1: Waterings domain and storage — Scope

## User story

As a coleccionista,
I want que cada riego de un ejemplar se guarde con su fecha y desaparezca con él,
so that el historial de mis riegos y la fecha del último sean confiables cuando la ficha los muestre.

## Acceptance criteria

```gherkin
@stated
Given un ejemplar
When se agrega un riego con una fecha válida y no futura
Then el riego queda guardado y aparece en el historial de ese ejemplar

@stated
Given un ejemplar con varios riegos
When se pide el último
Then se obtiene el de mayor fecha

@stated
Given una fecha con formato inválido, inexistente o posterior a hoy
When se valida
Then se rechaza con un mensaje claro en español

@deduced
Given un ejemplar con riegos
When se lista su historial
Then salen ordenados por fecha y, a igual fecha, por id

@deduced
Given un riego de un ejemplar
When se quita pasando el ejemplar y el riego
Then desaparece y no se toca ningún otro riego

@deduced
Given dos ejemplares y un riego del segundo
When se intenta quitar ese riego con el id del primero
Then no se quita nada y el riego sigue

@deduced
Given un ejemplar con riegos
When se quita el ejemplar
Then sus riegos desaparecen

@deduced
Given un ejemplar que ya tiene el tope de riegos
When se intenta agregar uno más
Then se rechaza con un mensaje claro y no se guarda

@deduced
Given un id de ejemplar que no existe
When se intenta agregar un riego
Then no se guarda nada

@deduced
Given una base migrada a la versión 3 con ejemplares y fotos
When se aplica la migración 0004
Then los ejemplares y sus fotos siguen y no hay riegos
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| ejemplar 1, `"2026-09-19"` | `agregar(conexion, 1, fecha)` | riego con id, `ejemplar_id=1`, `fecha="2026-09-19"` |
| riegos `2026-09-01` y `2026-09-15` del ejemplar 1 | `ultimo(conexion, 1)` | el del `2026-09-15` |
| `"19/09/2026"`, `"2026-02-30"`, mañana | `validar_fecha(texto, hoy)` | `CuidadoInvalido` con mensaje |
| 500 riegos del ejemplar 1 | agregar el 501.º | `CuidadoInvalido`; siguen 500 |
| riego 7 del ejemplar 2 | `quitar(conexion, 1, 7)` | `False`; el riego 7 sigue |

## In scope

- Migración `0004-riegos.sql`: tabla `riegos` con `ejemplar_id` en cascada e índice por `(ejemplar_id, fecha)` (ADR-008).
- Dominio en `orquidea.coleccion.modelo`: `Riego`, validación de la fecha (ISO, existente, no posterior a hoy) y el tope de 500 riegos por ejemplar.
- `orquidea.datos.riegos`: agregar, listar, último y quitar, siempre filtrando por ejemplar y riego.
- Medición del tamaño del historial lleno (500 riegos) desde el diseño, según la memoria del proyecto.

## Out of scope

- Rutas, formularios y ficha — s4.2.
- Último riego de toda la lista en una consulta — s4.5.
- Floraciones y su migración `0005` — s4.3.
- Editar un riego, hora del riego o zona horaria — **not now** (scope de e4).

## Done when

- [stated] Se agrega un riego con fecha válida y no futura, se lista y se obtiene el último (RF-06, fila s4.1 del scope de e4).
- [stated] Una fecha con formato inválido, inexistente o posterior a hoy se rechaza con un mensaje claro y no cambia la base (scope de e4).
- [deduced] Quitar un ejemplar borra sus riegos; quitar un riego no toca los de otros ejemplares aunque se pase un id ajeno (ADR-008).
- [deduced] El ejemplar con 500 riegos rechaza el 501.º (tope de e4) y su historial se lee sin sorpresas de tamaño.
- [deduced] La migración `0004` se aplica sobre una base de e3 con datos sin perderlos (ADR-003).

## Notes

Diseño de la épica: `work/epics/e4-care-log/design.md`; ADR-008. Los módulos siguen el patrón de `orquidea.datos.ejemplares`. Ningún criterio depende del humano: no hay stop previsible en esta historia.
