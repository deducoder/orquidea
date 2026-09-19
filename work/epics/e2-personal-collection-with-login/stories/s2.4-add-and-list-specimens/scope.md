# Story s2.4: Add catalog specimens and see them — Scope

## User story

As a coleccionista con sesión iniciada,
I want agregar a mi colección un ejemplar de una especie del catálogo y verlo en "Mi colección" con un enlace a los cuidados de su especie,
so that mi colección quede registrada y sus cuidados estén a un clic (RF-04).

## Acceptance criteria

```gherkin
@stated
Given una sesión iniciada y la ficha de una especie del catálogo
When pulso "Agregar a mi colección"
Then se crea un ejemplar ligado a esa especie y veo "Mi colección" con él

@stated
Given un ejemplar de la especie Epidendrum radicans en mi colección
When abro "Mi colección"
Then lo veo con el nombre científico de su especie, enlazado a la ficha de la especie

@stated
Given un ejemplar ya agregado de una especie
When agrego otro de la misma especie
Then hay dos ejemplares independientes en la lista

@stated
Given una colección vacía
When abro "Mi colección"
Then veo un mensaje que invita a agregar el primer ejemplar desde el catálogo

@stated
Given un usuario que inicia sesión, abre una ficha, agrega un ejemplar y abre "Mi colección"
When recorre esos pasos con la aplicación real
Then el ejemplar aparece (métrica líder del brief)

@deduced
Given un identificador de especie que no existe en el catálogo
When se intenta agregar un ejemplar con él
Then responde 404 y no se guarda nada

@deduced
Given un ejemplar cuya especie ya no está en el catálogo
When abro "Mi colección"
Then se lista con el identificador de la especie y un aviso, sin romper la página

@deduced
Given que no hay sesión, o el token CSRF falta
When se intenta agregar un ejemplar
Then se redirige al acceso o responde 403 y no se guarda nada

@deduced
Given que se agregó un ejemplar
When se recarga la página resultante
Then no se agrega un segundo ejemplar (POST y redirección a la lista)

@deduced
Given una base reiniciada
When abro "Mi colección"
Then los ejemplares siguen ahí (persisten)
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `POST /coleccion` con `especie_id=epidendrum-radicans` y `csrf` | agregar | 303 a `/coleccion`; una fila en `ejemplares` |
| `GET /coleccion` | ver la colección | `<li>` con `<a href="/especies/epidendrum-radicans">Epidendrum radicans</a>` y la fecha de alta |
| `POST /coleccion` con `especie_id=no-existe` | agregar | 404, sin fila nueva |

## In scope

- Migración `0002-ejemplares.sql` con la tabla completa de RF-04 (`especie_id`, `nombre`, `notas`, `creado`, con la regla de que sin especie hay nombre).
- Modelo `Ejemplar` del dominio y repositorio (`agregar`, `listar`).
- Rutas `GET /coleccion` y `POST /coleccion`; botón en la ficha; enlace "Mi colección" en la cabecera.
- Prueba de extremo a extremo de la métrica líder.

## Out of scope

- Ejemplares fuera del catálogo (nombre y notas propios) — s2.5.
- Editar y quitar — s2.6.
- Fotos, riegos y floraciones — no-go del brief (versión 0.2).
- Buscar, filtrar u ordenar la colección — **not now** (ver scope del épico).

## Done when

- [stated] El recorrido iniciar sesión, abrir una ficha, agregar el ejemplar y verlo en "Mi colección" funciona con la aplicación real.
- [stated] Varios ejemplares de la misma especie son independientes.
- [deduced] Una especie inexistente no se agrega y una desaparecida del catálogo no rompe la lista.
- [deduced] `./scripts/check` en verde y `security-review` sin críticos.

## Notes

Diseño del épico: `design.md` (componentes `orquidea.coleccion`, `orquidea.datos.ejemplares`) y ADR-003. Los `@stated` provienen de la fila de la historia y de la métrica líder del brief.
