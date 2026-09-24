# Story s3: Rank content of object screens — Scope

## User story

Como dueño de Orquídea,
quiero una guía de prioridad firmada para las cuatro pantallas de objeto (Especies, Ficha de especie, Mi colección, Ficha del ejemplar), con la técnica `screens` de gemba-design 0.24.0,
para que lo que carga cada pantalla y su orden sirvan a las tareas del inventario, y la composición posterior tenga contra qué medirse.

## Acceptance criteria

```gherkin
@stated
Given ningún rango escrito todavía
When se abre el ADR de esta historia en `proposed`
Then trae los nueve criterios de supervivencia aplicados, G1 a G4 aprobados el 2026-09-24 con su estrato y las opciones A, B y C con sus órdenes para S3 y S4, commiteado antes del primer rango

@stated
Given la guía escrita en `governance/identity/ui/screens/`
When corre `inventory-sources.py` con el inventario, el conjunto y la guía
Then sale 0 y cuenta 4 pantallas guiadas

@stated
Given la guía y el inventario
When corre el comando de G2 escrito en el ADR
Then cada tarea T1 a T7 queda servida por al menos un rango

@stated
Given la guía propuesta
When el dueño lee S3 y S4 frente a G3 y G4
Then elige una opción y firma la guía con nombre y fecha, o la deja `unsigned`

@deduced
Given una guía con un hueco de rango, una tarea inexistente y una firma sin fecha, y otra que deja una tarea sin servir
When corren `inventory-sources.py` y el comando de G2
Then los dos salen en rojo por su criterio antes de producir la guía real
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| S4, Ficha del ejemplar, con la opción A | se escribe el rango 1 | `\| S4 \| 1 \| la foto del ejemplar \| T5 \|` |
| una guía donde ningún rango sirve a T6 | corre el comando de G2 | rojo que nombra `T6` |

## In scope

- Guía de prioridad de S1, S2, S3 y S4.
- ADR nuevo: `proposed` con el rojo de G1 y G2, y después `accepted`.
- `survival-review` sobre la guía.

## Out of scope

- Guía de S5 a S9: se hace cuando haga falta.
- Patrón y composición: los eslabones siguientes.
- Cambiar plantillas para seguir la guía: la composición decide eso.

## Done when

- [stated] El ADR estaba commiteado en `proposed`, con su rojo, antes del commit del primer rango.
- [stated] `inventory-sources.py` sale 0 con 4 pantallas guiadas, y el comando de G2 no deja ninguna tarea sin servir.
- [stated] La guía está firmada por el dueño o dice `unsigned`, y G3 y G4 tienen su juicio.
- [deduced] El ADR queda `accepted`, en el mismo archivo y con el mismo número.
- [deduced] `./scripts/check` verde.

## Notes

- Standalone: sale por su cuenta con `integrate`.
- Entrada: `inventory.md` (`read-at` `c9a8ea1`) y `screen-set.md` de s2, con ADR-017.
- Criterios aprobados por el humano el 2026-09-24: G1 (`mechanical`), G2 (`mechanical`), G3 (`judgement`, del criterio 3 de ADR-009) y G4 (`judgement`).
