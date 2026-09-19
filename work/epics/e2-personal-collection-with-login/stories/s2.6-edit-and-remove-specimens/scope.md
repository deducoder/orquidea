# Story s2.6: Edit and remove specimens — Scope

## User story

As a coleccionista con sesión iniciada,
I want editar el nombre y las notas de un ejemplar y quitarlo de mi colección,
so that mi registro se mantenga al día cuando una planta cambia, se corrige un dato o deja de estar conmigo (RF-04).

## Acceptance criteria

```gherkin
@stated
Given un ejemplar en "Mi colección"
When lo edito cambiando sus notas
Then la lista muestra las notas nuevas y los demás ejemplares no cambian

@stated
Given un ejemplar sin especie de catálogo
When cambio su nombre y sus notas
Then la lista muestra el nombre y las notas nuevos

@stated
Given un ejemplar en "Mi colección"
When pido quitarlo
Then veo una página de confirmación y el ejemplar sigue ahí hasta que confirme

@stated
Given la página de confirmación
When confirmo
Then el ejemplar desaparece de la lista y los demás siguen

@stated
Given dos ejemplares de la misma especie
When edito o quito uno
Then el otro no se altera

@deduced
Given un ejemplar sin especie de catálogo
When intento dejar el nombre vacío o pasar de 120 caracteres, o las notas de 2000
Then veo el formulario con un mensaje, conservando lo escrito, y no se guarda nada

@deduced
Given un ejemplar del catálogo
When dejo el nombre vacío
Then se guarda sin nombre propio (el nombre es opcional cuando hay especie)

@deduced
Given un identificador que no existe o no es un número
When pido editar o quitar
Then responde 404 (o 422 si no es número) y no cambia nada

@deduced
Given que no hay sesión o falta el token CSRF
When envío una edición o una baja
Then se redirige al acceso o responde 403 y no cambia nada

@deduced
Given la página de confirmación pedida con GET
When la abro
Then no quita nada (solo el POST quita)
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `GET /coleccion/3/editar` | abrir la edición | formulario con el nombre y las notas actuales |
| `POST /coleccion/3/editar` con `nombre=Mi rara`, `notas=Florece en marzo`, `csrf` | guardar | 303 a `/coleccion`; la fila 3 cambió |
| `GET /coleccion/3/quitar` | pedir la baja | confirmación con el nombre; nada cambia |
| `POST /coleccion/3/quitar` con `csrf` | confirmar | 303 a `/coleccion`; la fila 3 ya no existe |
| `POST /coleccion/99/quitar` con `csrf` | confirmar | 404 |

## In scope

- Repositorio: `obtener`, `actualizar`, `quitar`.
- Validación de ejemplar generalizada (nombre opcional si hay especie de catálogo).
- Rutas de edición y de baja con confirmación sin JavaScript; enlaces "Editar" y "Quitar" en la lista; el formulario compartido con el de s2.5.
- Mostrar el nombre propio de un ejemplar del catálogo cuando lo tiene.

## Out of scope

- Cambiar la especie de un ejemplar — se quita y se vuelve a agregar — **not now**.
- Deshacer una baja o papelera — **not now**.
- Fotos, riegos y floraciones — no-go del brief (versión 0.2).

## Done when

- [stated] Se puede editar y quitar cualquier ejemplar (con o sin especie de catálogo) sin afectar a los demás (RF-04).
- [stated] Quitar pide confirmación.
- [deduced] Un identificador inexistente no cambia nada y no rompe la aplicación.
- [deduced] `./scripts/check` en verde y `security-review` sin críticos.

## Notes

Cierra RF-04 junto con s2.4 y s2.5. Los `@stated` provienen de la fila de la historia ("con confirmación") y de RF-04 ("lo edita y lo quita … cada uno es independiente").
