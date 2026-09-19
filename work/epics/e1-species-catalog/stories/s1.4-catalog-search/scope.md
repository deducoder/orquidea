# Story s1.4: Catalog search — Scope

## User story

As a coleccionista de orquídeas de Chiapas,
I want buscar especies por su nombre científico o por un nombre común,
so that llegue a su ficha sin recorrer todo el catálogo.

## Acceptance criteria

```gherkin
@stated
Given un catálogo con especies
When busco por parte del nombre científico
Then veo solo las especies cuyo nombre científico lo contiene

@stated
Given una especie con nombres comunes
When busco por parte de uno de sus nombres comunes
Then veo esa especie

@stated
Given una búsqueda escrita con otras mayúsculas o sin acentos
When busco
Then obtengo las mismas especies que con la escritura original

@deduced
Given una búsqueda vacía o en blanco
When busco
Then veo todas las especies

@deduced
Given una búsqueda sin coincidencias
When busco
Then veo un mensaje de que no hay resultados y no un error

@deduced
Given la lista de especies en el navegador
When escribo en el campo de búsqueda
Then los resultados se actualizan sin recargar la página (htmx), y sin JavaScript el formulario sigue funcionando
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| catálogo con "Epidendrum radicans" (común: "orquídea de fuego") | GET /especies?q=ORQUIDEA | 200; lista con Epidendrum radicans |
| el mismo catálogo | GET /especies?q=zzz | 200; "No hay especies que coincidan con la búsqueda." |

## In scope

- Función de búsqueda del dominio que ignora mayúsculas y acentos.
- Parámetro `q` en `/especies`, campo de búsqueda con htmx y formulario que funciona sin JavaScript.

## Out of scope

- Búsqueda difusa o por relevancia — rabbit hole del brief.
- Búsqueda por otros campos (descripción, cuidados) — RF-02 pide nombre científico o común.

## Done when

- [stated] Se busca por nombre científico o común sin distinguir mayúsculas ni acentos.
- [deduced] Vacío da todas, sin coincidencias da mensaje.
- [deduced] `./scripts/check` en verde.

## Notes

Fila s1.4 de `work/epics/e1-species-catalog/scope.md`; RF-02.
