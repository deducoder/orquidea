# Story s4.3: Blooms domain and storage — Scope

## User story

As a coleccionista,
I want que cada floración de un ejemplar se guarde con su fecha de inicio y, si ya terminó, su fecha de fin, y desaparezca con él,
so that el historial de floración de cada planta sea confiable cuando la ficha lo muestre.

## Acceptance criteria

```gherkin
@stated
Given un ejemplar
When se agrega una floración con fecha de inicio válida y sin fin
Then queda guardada como en curso y aparece en su historial

@stated
Given un ejemplar
When se agrega una floración con inicio y fin válidos
Then queda guardada con las dos fechas

@stated
Given una floración en curso
When se fija su fin
Then la floración queda terminada con esa fecha

@stated
Given una fecha con formato inválido, inexistente o posterior a hoy, o un fin anterior al inicio
When se valida
Then se rechaza con un mensaje claro en español

@deduced
Given un ejemplar con floraciones
When se lista su historial
Then salen ordenadas por inicio y, a igual inicio, por id

@deduced
Given una floración ya terminada
When se intenta fijar otro fin
Then se rechaza con un mensaje claro y no cambia

@deduced
Given una floración en curso con inicio posterior al fin propuesto
When se intenta fijar ese fin
Then se rechaza con un mensaje claro y sigue en curso

@deduced
Given una floración de un ejemplar
When se quita o se termina pasando el ejemplar y la floración
Then solo cambia esa floración

@deduced
Given dos ejemplares y una floración del segundo
When se intenta quitar o terminar con el id del primero
Then no cambia nada

@deduced
Given un ejemplar con floraciones
When se quita el ejemplar
Then sus floraciones desaparecen

@deduced
Given un ejemplar que ya tiene el tope de floraciones
When se intenta agregar una más
Then se rechaza con un mensaje claro que nombra las floraciones

@deduced
Given una base migrada a la versión 4 con ejemplares, fotos y riegos
When se aplica la migración 0005
Then todo sigue y no hay floraciones
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| ejemplar 1, `"2026-03-01"` | `agregar(conexion, 1, inicio)` | floración con `fin=None` (en curso) |
| ejemplar 1, `"2026-03-01"`, `"2026-03-20"` | `agregar(conexion, 1, inicio, fin)` | floración con las dos fechas |
| floración 4 en curso desde `2026-03-01` | `terminar(conexion, 1, 4, "2026-03-20")` | `True`; `fin="2026-03-20"` |
| la misma con fin `"2026-02-01"` | `terminar(...)` | `CuidadoInvalido("El fin no puede ser anterior al inicio.")` |
| floración 4 ya terminada | `terminar(...)` | `CuidadoInvalido("Esa floración ya terminó.")` |
| floración 9 del ejemplar 2 | `terminar(conexion, 1, 9, fin)` o `quitar(conexion, 1, 9)` | `False`; sigue igual |

## In scope

- Migración `0005-floraciones.sql`: tabla `floraciones` con `ejemplar_id` en cascada, `CHECK` de forma de las fechas y de `fin >= inicio`, e índice (ADR-008).
- Dominio en `orquidea.coleccion.modelo`: `Floracion` y la validación del intervalo (inicio obligatorio, fin opcional, ninguna posterior a hoy, fin no anterior al inicio).
- `orquidea.datos.floraciones`: agregar, terminar, listar y quitar, filtrando siempre por ejemplar y floración, con el tope de 500 en la misma sentencia.
- Medición del tamaño del historial lleno desde el diseño.

## Out of scope

- Rutas, formularios y ficha — s4.4.
- Editar las fechas de una floración ya guardada — **not now** (scope de e4): se quita y se vuelve a registrar.
- Reabrir una floración terminada — **not now**.
- Riegos — ya hechos en s4.1 y s4.2.

## Done when

- [stated] Se agrega una floración con inicio y fin opcional, se lista y se fija el fin de una en curso (RF-07, fila s4.3 del scope de e4).
- [stated] Una fecha inválida, inexistente o posterior a hoy, o un fin anterior al inicio, se rechaza con un mensaje claro y no cambia la base (scope de e4).
- [deduced] Quitar el ejemplar borra sus floraciones; quitar o terminar una floración no toca las de otros ejemplares aunque se pase un id ajeno (ADR-008).
- [deduced] El ejemplar con 500 floraciones rechaza la 501.ª con un mensaje que nombra las floraciones (tope de e4), también con altas simultáneas.
- [deduced] La migración `0005` se aplica sobre una base de e3 más `0004` con datos sin perderlos (ADR-003).

## Notes

Diseño de la épica: `work/epics/e4-care-log/design.md`; ADR-008. Sigue el patrón de s4.1 (`datos.riegos`). Ningún criterio depende del humano: no hay stop previsible en esta historia.
