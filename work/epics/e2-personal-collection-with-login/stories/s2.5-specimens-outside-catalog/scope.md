# Story s2.5: Specimens outside the catalog — Scope

## User story

As a coleccionista con sesión iniciada,
I want agregar a mi colección una planta que no está en el catálogo, con su propio nombre y notas,
so that toda mi colección real quede en un solo lugar, incluso lo que el catálogo aún no cubre (RF-04).

## Acceptance criteria

```gherkin
@stated
Given una sesión iniciada
When abro "Mi colección"
Then veo un enlace para agregar una planta que no está en el catálogo

@stated
Given el formulario de planta fuera del catálogo
When envío el nombre "Cattleya de mi abuela" y las notas "Regalo de 2019; florece en enero"
Then se crea un ejemplar sin especie de catálogo y lo veo en "Mi colección" con ese nombre y esas notas

@stated
Given un ejemplar sin especie de catálogo
When lo veo en la lista
Then no lleva enlace a una ficha de especie

@deduced
Given el formulario con el nombre vacío o solo espacios
When lo envío
Then veo el formulario otra vez con un mensaje de error, conservando lo escrito, y no se guarda nada

@deduced
Given un nombre de más de 120 caracteres o notas de más de 2000
When envío el formulario
Then se rechaza con un mensaje y no se guarda nada

@deduced
Given un nombre con espacios al inicio y al final
When lo envío
Then se guarda sin ellos

@deduced
Given nombre o notas con HTML
When se listan
Then aparecen escapados

@deduced
Given que no hay sesión o falta el token CSRF
When envío el formulario
Then se redirige al acceso o responde 403 y no se guarda nada

@deduced
Given notas con saltos de línea
When se listan
Then se conservan los saltos de línea
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `POST /coleccion/nuevo` con `nombre=Cattleya de mi abuela`, `notas=Regalo de 2019` y `csrf` | agregar | 303 a `/coleccion`; fila con `especie_id` NULL |
| `POST /coleccion/nuevo` con `nombre=   ` | agregar | 422 con el formulario y "El nombre es obligatorio." |
| `GET /coleccion` | ver la colección | entrada "Cattleya de mi abuela" sin enlace, con sus notas |

## In scope

- Validación del ejemplar propio en el dominio (nombre obligatorio y acotado, notas acotadas).
- Repositorio: alta sin especie de catálogo.
- Rutas `GET`/`POST /coleccion/nuevo`, formulario, enlace desde "Mi colección" y presentación en la lista.

## Out of scope

- Editar y quitar — s2.6.
- Promover una planta propia a una especie del catálogo — **not now**: el catálogo lo mantiene el equipo desde el repositorio.
- Fotos, riegos y floraciones — no-go del brief (versión 0.2).

## Done when

- [stated] Se puede registrar una planta que no está en el catálogo, con nombre y notas, y verla en la colección (métrica rezagada del brief, la parte que una sesión puede demostrar).
- [deduced] Nombre vacío o excesivo se rechaza sin guardar; la salida se escapa.
- [deduced] `./scripts/check` en verde y `security-review` sin críticos.

## Notes

Tabla y `CHECK` de s2.4 (`0002-ejemplares.sql`): no hay migración nueva. Los `@stated` provienen de la fila de la historia y del brief ("incluidas plantas fuera del catálogo").
