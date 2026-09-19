# Story s1.3: Species sheet — Scope

## User story

As a coleccionista de orquídeas de Chiapas,
I want ver la lista de especies del catálogo y abrir la ficha de cada una con su información general y sus cuidados de luz, riego, temperatura y sustrato,
so that sepa cómo cuidarla y de dónde viene cada dato.

## Acceptance criteria

```gherkin
@stated
Given un catálogo con especies cargadas
When abro /especies
Then veo cada especie con su nombre científico y un enlace a su ficha

@stated
Given una especie del catálogo
When abro su ficha
Then veo su nombre científico, sus nombres comunes, su descripción y sus cuidados de luz, riego, temperatura y sustrato

@stated
Given la ficha de una especie
When leo un cuidado
Then veo junto a él la fuente de ese dato

@deduced
Given un id que no está en el catálogo
When abro /especies/{id}
Then recibo 404

@deduced
Given un catálogo cuyos datos contienen HTML
When abro la lista o la ficha
Then el HTML se muestra escapado, no se ejecuta

@deduced
Given un catálogo vacío
When abro /especies
Then veo un mensaje de que no hay especies y no un error
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| catálogo con `epidendrum-radicans` (riego: "Regular", fuente "Hágsater et al. 2015") | GET /especies/epidendrum-radicans | 200; contiene "Epidendrum radicans", "Regular" y "Hágsater et al. 2015" |
| el mismo catálogo | GET /especies/no-existe | 404 |

## In scope

- Rutas `/especies` y `/especies/{id}` con sus plantillas, sobre el catálogo cargado al arrancar.
- Enlace a la lista desde la página de inicio.

## Out of scope

- Búsqueda — s1.4.
- Datos reales del catálogo — s1.6.
- Fotos de especies y edición — no-go del brief / no están en RF-03.

## Done when

- [stated] La lista y la ficha muestran lo que RF-03 pide, con la fuente de cada cuidado.
- [deduced] Un id inexistente da 404; los datos se escapan; el catálogo vacío no rompe la lista.
- [deduced] `./scripts/check` en verde.

## Notes

Fila s1.3 de `work/epics/e1-species-catalog/scope.md`; RF-03; system-design (capa Web sobre el dominio).
