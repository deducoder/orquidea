# Story s1.6: Seed catalog — Scope

## User story

As a coleccionista de orquídeas de Chiapas,
I want que el catálogo traiga las especies nativas más conocidas y populares con sus cuidados y sus fuentes,
so that pueda consultar desde el primer día cómo cuidarlas y de dónde viene cada dato.

## Acceptance criteria

```gherkin
@stated
Given el directorio del catálogo de la aplicación
When cargo el catálogo
Then obtengo 100 especies y ninguna falla la validación

@stated
Given cualquiera de las especies
When leo sus datos
Then cada dato de cuidado y la especie citan una fuente real consultada durante la investigación

@stated
Given la lista de especies
When reviso su procedencia
Then todas son nativas de Chiapas y están entre las más conocidas y populares

@deduced
Given una fuente que cubre un género y no la especie
When se cita para un cuidado
Then el dato lo dice (cuidado del género) en lugar de presentarse como propio de la especie

@deduced
Given la primera carga de la lista y de una ficha con el catálogo completo
When se mide con "Slow 3G"
Then cumple must-perf-001 (medición en epic-review)
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `src/orquidea/datos/catalogo/*.json` con 100 archivos | `cargar_catalogo(DIRECTORIO_CATALOGO)` | lista de 100 `Especie`, sin `CatalogoInvalido` |

## In scope

- Un informe de investigación (`work/research/`) que fundamenta la lista, su carácter nativo de Chiapas, su popularidad y las fuentes de cuidados.
- 100 archivos JSON de especie, uno por especie, con fuentes.
- Una prueba de que el catálogo real carga y cumple un mínimo de calidad de datos.

## Out of scope

- El resto de las ~700 especies — rabbit hole del brief, sin épica asignada.
- Fotos de las especies.
- Datos que no pida el esquema (distribución detallada, floración).

## Done when

- [stated] El catálogo real carga 100 especies válidas.
- [stated] Cada especie y cada cuidado cita una fuente realmente consultada; ninguna cita se inventa.
- [deduced] Si la investigación no sostiene las 100 con fuentes reales, la historia se detiene y lo pregunta (el 100 es del humano) en vez de completar con datos no respaldados.
- [deduced] `./scripts/check` en verde.

## Notes

Respuesta del humano al stop P5: "Debemos hacer un research para buscar los datos... Pongamos las 100 más conocidas y populares". Fila s1.6 de `work/epics/e1-species-catalog/scope.md`; RF-01, RF-03, `must-data-001`; brief: la épica entrega "un conjunto semilla".
