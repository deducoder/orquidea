# Story s4: Choose screen patterns — Scope

## User story

Como dueño de Orquídea,
quiero que cada una de las 9 pantallas del conjunto tome la forma que pide su contenido, elegida de la tabla cerrada de layouts canónicos con la técnica `screens` de gemba-design 0.24.0,
para que la composición parta de una forma decidida contra una fuente, y no de la plantilla de hoy.

## Acceptance criteria

```gherkin
@stated
Given ningún patrón escrito todavía
When se abre el ADR de esta historia en `proposed`
Then trae los nueve criterios de supervivencia aplicados, P1 a P4 aprobados el 2026-09-24 con su estrato, la regla de elección de la fuente leída ese día y las opciones A, B y C pantalla por pantalla, commiteado antes del primer patrón

@stated
Given los patrones escritos en `governance/identity/ui/screens/`
When corre `inventory-sources.py` con el inventario, el conjunto, la guía y los patrones
Then sale 0 y cuenta `9 of 9 screens with a pattern`

@stated
Given los patrones propuestos
When el dueño lee cada pantalla frente a la regla de la fuente y a la guía firmada
Then elige una opción y firma P3 y P4 con nombre y fecha, o los deja `unsigned`

@deduced
Given una tabla con un valor fuera de la tabla canónica, un `none` sin razón, una pantalla con dos patrones y otra con una pantalla que falta
When corre `inventory-sources.py`
Then sale en rojo por S6, o cuenta menos de 9, antes de producir los patrones reales
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| S5, Nuevo ejemplar sin especie | se elige el patrón | `\| S5 \| none \| un formulario de un paso: no recorre contenido \|` |
| S1, Especies | se elige el patrón | `\| S1 \| list-detail \| una lista de especies que revelan su ficha \|` |

## In scope

- Patrón de las 9 pantallas del conjunto de ADR-017.
- ADR nuevo: `proposed` con su rojo y las opciones medidas antes de producir, y después `accepted`.
- `survival-review` sobre los patrones.

## Out of scope

- La composición y la página generada.
- La guía de S5 a S9.
- Cambiar plantillas.

## Done when

- [stated] El ADR estaba commiteado en `proposed`, con su rojo, antes del commit del primer patrón.
- [stated] `inventory-sources.py` sale 0 con `9 of 9 screens with a pattern`.
- [stated] P3 y P4 tienen el juicio del dueño con fecha, o dicen `unsigned`.
- [deduced] El ADR queda `accepted`, en el mismo archivo y con el mismo número.
- [deduced] `./scripts/check` verde.

## Notes

- Standalone: sale por su cuenta con `integrate`.
- Fuente: Android Developers, "Canonical layouts" (`developer.android.com/develop/ui/compose/layouts/adaptive/canonical-layouts`), actualizada el 2026-09-22 y leída el 2026-09-24. m3.material.io se arma con JavaScript y no entregó texto. Android es una de las tres fuentes de la misma familia que nombra el catálogo.
- Criterios aprobados por el humano el 2026-09-24: P1 y P2 (`mechanical`), P3 y P4 (`judgement`; P4 viene de ADR-018).
