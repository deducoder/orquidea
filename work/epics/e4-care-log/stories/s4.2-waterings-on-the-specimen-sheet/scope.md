# Story s4.2: Waterings on the specimen sheet — Scope

## User story

As a coleccionista,
I want registrar un riego en la ficha de mi ejemplar y ver su historial y la fecha del último,
so that sepa de un vistazo cuándo regué cada planta sin acordarme.

## Acceptance criteria

```gherkin
@stated
Given la ficha de un ejemplar sin riegos
When registro un riego con una fecha válida
Then la ficha muestra ese riego en el historial y esa fecha como la del último riego

@stated
Given la ficha de un ejemplar con riegos
When la abro
Then veo el historial en orden cronológico y la fecha del último riego

@stated
Given un riego del historial
When lo quito
Then desaparece del historial y la fecha del último riego se recalcula

@stated
Given una fecha con formato inválido, inexistente o posterior a hoy
When intento registrar el riego
Then la ficha vuelve con un mensaje claro y no se guarda nada

@deduced
Given un ejemplar sin riegos
When abro su ficha
Then dice que aún no hay riegos y no muestra una fecha de último riego

@deduced
Given un ejemplar con el tope de riegos
When intento registrar uno más
Then la ficha vuelve con el mensaje del tope y no se guarda nada

@deduced
Given un visitante sin sesión
When intenta registrar o quitar un riego
Then no se guarda ni se quita nada

@deduced
Given un formulario de riego sin el token CSRF
When se envía
Then se rechaza y no cambia nada

@deduced
Given un id de ejemplar o de riego que no existe, o un riego de otro ejemplar
When intento registrar o quitar
Then responde 404 y no cambia ningún riego

@deduced
Given dos ejemplares con riegos
When registro o quito un riego en uno
Then el otro no cambia
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| ejemplar 1 sin riegos | `POST /coleccion/1/riegos` con `fecha=2026-09-15` y `csrf` | 303 a `/coleccion/1`; la ficha muestra «Último riego: 2026-09-15» |
| `fecha=2026-09-20` (mañana) | `POST /coleccion/1/riegos` | 422; la ficha con «La fecha no puede ser posterior a hoy.»; nada guardado |
| riego 5 del ejemplar 2 | `POST /coleccion/1/riegos/5/quitar` | 404; el riego 5 sigue |
| sin cookie de sesión | `POST /coleccion/1/riegos` | redirige al acceso; nada guardado |

## In scope

- Router `orquidea.web.rutas.cuidados` con `POST /coleccion/{id}/riegos` y `POST /coleccion/{id}/riegos/{riego}/quitar`, montado en la aplicación.
- La ficha (`GET /coleccion/{id}`) carga el historial y el último riego; sección «Riegos» en `ejemplar_ficha.html` con formulario y botón de quitar por riego.
- Errores de validación con 422 y el mensaje en la ficha, en español.
- Prueba de extremo a extremo de la métrica líder del brief.

## Out of scope

- Floraciones — s4.3 y s4.4.
- Último riego en «Mi colección» — s4.5.
- Medición del peso de la ficha con el historial lleno — s4.6.
- Editar un riego — **not now** (scope de e4).

## Done when

- [stated] Registrar un riego en un ejemplar y ver la fecha del último riego en su ficha (métrica líder del brief, RF-06), con una prueba de extremo a extremo y el recorrido manual con la aplicación corriendo.
- [stated] La ficha muestra el historial de riegos en orden cronológico, permite quitar cada uno y rechaza fechas inválidas con un mensaje claro (RF-06, fila s4.2 del scope de e4).
- [deduced] Sin sesión, ninguna ruta de riegos cambia nada; toda escritura exige el token CSRF; un id inexistente o ajeno da 404 (`should-security-002`).
- [deduced] El tope de riegos se rechaza con mensaje claro y sin cambiar la base.
- [deduced] El orden de rutas se mantiene (`/coleccion/nuevo` antes de `/coleccion/{id}`) y las pruebas de e1 a e3 siguen en verde sin cambiar sus aserciones.

## Notes

Diseño de la épica: `work/epics/e4-care-log/design.md`; ADR-008. `datos.riegos` y `validar_fecha` vienen de s4.1: la ruta debe validar la fecha antes de `agregar` (observación de la revisión de s4.1). Ningún criterio depende del humano: no hay stop previsible en esta historia.
