# Story s2.3: Protect all routes — Scope

## User story

As a coleccionista, único usuario de la aplicación,
I want que toda la aplicación exija mi sesión, que las acciones que cambian datos vengan de mis propias páginas y que las respuestas lleven cabeceras de seguridad,
so that nadie sin mi contraseña vea o cambie mi colección (RF-08, ASVS L2).

## Acceptance criteria

```gherkin
@stated
Given que no hay sesión
When pido cualquier ruta salvo el formulario de acceso, /salud y /static
Then me redirige al formulario de acceso (303) y no veo contenido

@stated
Given una sesión iniciada
When pido el inicio, la lista de especies o una ficha
Then los veo como antes

@stated
Given una sesión iniciada
When envío un POST sin el token CSRF de mi sesión, o con otro
Then recibo 403 y nada cambia

@stated
Given una sesión iniciada
When envío un POST con el token CSRF de mi sesión
Then se procesa

@deduced
Given una petición de htmx sin sesión
When pide una ruta protegida
Then recibe 401 con la cabecera `HX-Redirect: /acceso` en vez de un fragmento con el formulario

@deduced
Given una página autenticada
When la abro
Then trae un botón "Salir" (POST con el token CSRF) y las peticiones de htmx llevan el token en la cabecera

@deduced
Given cualquier respuesta
When reviso sus cabeceras
Then trae `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, `Content-Security-Policy`; y las páginas (no `/static`) traen `Cache-Control: no-store`

@deduced
Given la documentación automática de FastAPI
When pido `/docs`, `/redoc` o `/openapi.json`
Then no existen

@deduced
Given una ruta nueva añadida sin declararla pública
When se pide sin sesión
Then queda protegida (seguro por defecto)
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `GET /especies` sin cookie | pedir la lista | 303 a `/acceso` |
| `GET /especies` con `HX-Request: true` sin cookie | pedir la lista desde htmx | 401 y `HX-Redirect: /acceso` |
| `POST /salir` con sesión y sin token | cerrar sesión | 403, la sesión sigue |
| `POST /salir` con sesión y `csrf=<token>` | cerrar sesión | 303 a `/acceso`, sesión borrada |
| `GET /salud` sin sesión | healthcheck | 200 `{"estado":"ok"}` |

## In scope

- Dependencia global de sesión con lista explícita de rutas públicas (`/acceso`, `/salud`); `/static` queda fuera por ser un montaje.
- Token CSRF exigido en todo `POST` autenticado (campo de formulario o cabecera `X-CSRF-Token`).
- Botón "Salir" en la plantilla base y token en las peticiones de htmx.
- Cabeceras de seguridad en todas las respuestas; `no-store` en las páginas.
- Desactivar `/docs`, `/redoc` y `/openapi.json`.
- Actualizar las pruebas web de e1 para que usen una sesión.

## Out of scope

- Rutas de la colección — s2.4 a s2.6 (nacerán ya protegidas).
- CSRF en el propio `POST /acceso` (no hay sesión que suplantar; `SameSite=Lax`) — decisión de ADR-004.
- HSTS más allá de emitirlo cuando la cookie es `Secure`; el HTTPS lo termina Dokploy.

## Done when

- [stated] Ninguna ruta salvo `/acceso`, `/salud` y `/static` responde contenido sin sesión (RF-08), demostrado enumerando `app.routes`.
- [stated] Todo `POST` autenticado sin token CSRF válido da 403.
- [deduced] Las respuestas llevan las cabeceras de seguridad y las páginas `no-store`.
- [deduced] Las pruebas web de e1 pasan con sesión y `./scripts/check` está en verde.

## Notes

Diseño del épico: ADR-004 puntos 3, 5 y 6. Los `@stated` provienen de la fila de la historia y del contrato del system-design ("toda ruta, salvo el inicio de sesión, exige la sesión").
