# Story s4.4: Blooms on the specimen sheet — Scope

## User story

As a coleccionista,
I want registrar cuándo floreció un ejemplar, cerrar la floración cuando termina y ver su historial en la ficha,
so that sepa cuándo floreció cada planta y si lo está haciendo ahora.

## Acceptance criteria

```gherkin
@stated
Given la ficha de un ejemplar
When registro una floración con fecha de inicio y sin fin
Then aparece en el historial como en curso

@stated
Given la ficha de un ejemplar
When registro una floración con inicio y fin
Then aparece en el historial con las dos fechas

@stated
Given una floración en curso en la ficha
When le fijo la fecha de fin
Then el historial la muestra terminada con esa fecha

@stated
Given una floración del historial
When la quito
Then desaparece del historial

@stated
Given una fecha inválida, inexistente o posterior a hoy, o un fin anterior al inicio
When intento registrar o terminar una floración
Then la ficha vuelve con un mensaje claro y no cambia nada

@deduced
Given un ejemplar sin floraciones
When abro su ficha
Then dice que aún no hay floraciones

@deduced
Given un ejemplar con floraciones terminadas y en curso
When abro su ficha
Then las veo de la más reciente a la más antigua y solo las que están en curso ofrecen fijar el fin

@deduced
Given un ejemplar con el tope de floraciones
When intento registrar una más
Then la ficha vuelve con el mensaje del tope y no cambia nada

@deduced
Given un visitante sin sesión
When intenta registrar, terminar o quitar una floración
Then no cambia nada

@deduced
Given un formulario de floración sin el token CSRF
When se envía
Then se rechaza y no cambia nada

@deduced
Given un id de ejemplar o de floración que no existe, o una floración de otro ejemplar
When intento terminar o quitar
Then responde 404 y no cambia ninguna floración

@deduced
Given un ejemplar con riegos y floraciones
When registro, termino o quito una floración
Then los riegos y la foto siguen igual
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| ejemplar 1 sin floraciones | `POST /coleccion/1/floraciones` con `inicio=2026-03-01`, `fin=` y `csrf` | 303 a `/coleccion/1`; la ficha muestra «2026-03-01 — en curso» |
| la floración 4 en curso | `POST /coleccion/1/floraciones/4/fin` con `fin=2026-03-20` | 303; la ficha muestra «2026-03-01 — 2026-03-20» |
| `fin=2026-02-01` sobre esa misma | `POST /coleccion/1/floraciones/4/fin` | 422; «El fin no puede ser anterior al inicio.»; sigue en curso |
| floración 5 del ejemplar 2 | `POST /coleccion/1/floraciones/5/quitar` | 404; la floración 5 sigue |
| sin cookie de sesión | `POST /coleccion/1/floraciones` | redirige al acceso; nada guardado |

## In scope

- Tres rutas POST en el router `cuidados`: registrar (`/coleccion/{id}/floraciones`), fijar el fin (`.../{floracion}/fin`) y quitar (`.../{floracion}/quitar`).
- La ficha carga el historial de floraciones (más reciente primero) y muestra la sección «Floraciones» con su formulario, «Terminar» solo en las que están en curso y «Quitar» en todas.
- Errores de validación y del tope con 422 y el mensaje, en español, conservando lo escrito en los campos (escapado).
- Prueba de extremo a extremo del historial de floración y medición de la ficha con los dos historiales en el tope (solo se anota; el presupuesto es de s4.6).

## Out of scope

- Último riego en «Mi colección» — s4.5.
- Presupuesto de peso y guía — s4.6.
- Editar las fechas de una floración o reabrirla — **not now** (scope de e4): se quita y se vuelve a registrar.
- Estadísticas o gráficas de floración — **never** (no-go del brief).

## Done when

- [stated] Registrar una floración con inicio y fin opcional, fijarle el fin después, quitarla y ver el historial en la ficha (RF-07, fila s4.4 del scope de e4), con una prueba de extremo a extremo y el recorrido manual con la aplicación corriendo.
- [stated] Una fecha inválida o un fin anterior al inicio se rechaza con un mensaje claro y no cambia la base (scope de e4).
- [deduced] Sin sesión, ninguna ruta de floraciones cambia nada; toda escritura exige el token CSRF; un id inexistente o ajeno da 404 (`should-security-002`).
- [deduced] El tope de floraciones se rechaza con mensaje claro y sin cambiar la base.
- [deduced] Las pruebas de riegos, fotos y e1 a e3 siguen en verde sin cambiar sus aserciones, salvo las que enumeran las rutas.

## Notes

Diseño de la épica: `work/epics/e4-care-log/design.md`; ADR-008. Sigue el patrón de s4.2 (`web/rutas/cuidados.py`). Observación de s4.3: la ruta debe llamar a `validar_floracion`/`validar_fecha` antes de `agregar` y `terminar`. Ningún criterio depende del humano: no hay stop previsible en esta historia.
