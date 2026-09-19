# Story s1.2: Catalog schema and loader — Scope

## User story

As a mantenedor del catálogo,
I want que las especies vivan en JSON con un esquema que exige su fuente y que la carga rechace cualquier archivo inválido diciendo cuál y en qué campo,
so that el catálogo nunca se cargue a medias ni con datos sin sustento.

## Acceptance criteria

```gherkin
@stated
Given un directorio con archivos JSON de especies que cumplen el esquema
When cargo el catálogo
Then obtengo todas las especies

@stated
Given un archivo cuya especie no cita ninguna fuente
When cargo el catálogo
Then la carga falla con un error que nombra el archivo y el campo `fuentes`

@stated
Given un archivo con un campo ausente o de tipo incorrecto
When cargo el catálogo
Then la carga falla con un error que nombra el archivo y ese campo

@deduced
Given un directorio con un archivo válido y otro inválido
When cargo el catálogo
Then la carga falla y no devuelve ninguna especie (todo o nada)

@deduced
Given un archivo que no es JSON válido
When cargo el catálogo
Then la carga falla con un error que nombra el archivo

@deduced
Given dos archivos con la misma `id` de especie
When cargo el catálogo
Then la carga falla nombrando ambos archivos
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `epidendrum-radicans.json` con todos los campos y `fuentes: ["Hágsater et al. 2015"]` | `cargar_catalogo(directorio)` | lista con una `Especie` de id `epidendrum-radicans` |
| el mismo archivo sin `fuentes` | `cargar_catalogo(directorio)` | `CatalogoInvalido`: `epidendrum-radicans.json: fuentes: Field required` |

## In scope

- Modelo de especie (información general, cuidados de luz, riego, temperatura y sustrato, fuentes) y su validación.
- Carga de un directorio de JSON, todo o nada, con errores que nombran archivo y campo.
- Directorio del catálogo dentro del paquete, inicialmente vacío de datos reales.

## Out of scope

- Mostrar las especies (s1.3) y buscarlas (s1.4).
- Los datos reales del catálogo — s1.6.
- Editar el catálogo desde la interfaz — no-go del brief.

## Done when

- [stated] Un JSON que no cumple el esquema o carece de fuente se rechaza señalando archivo y campo.
- [stated] Un catálogo válido se carga completo.
- [deduced] Nunca se devuelve un catálogo parcial.
- [deduced] `./scripts/check` en verde.

## Notes

Fila s1.2 de `work/epics/e1-species-catalog/scope.md`; RF-01, `must-data-001`, system-design (capa Datos y Dominio).
