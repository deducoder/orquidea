# Story s2.2: Login and logout — Scope

## User story

As a coleccionista, único usuario de la aplicación,
I want iniciar sesión con mi contraseña y cerrar la sesión cuando termine,
so that mi colección quede protegida y solo yo pueda entrar (RF-08).

## Acceptance criteria

```gherkin
@stated
Given la contraseña configurada en el entorno como hash
When envío esa contraseña en el formulario de acceso
Then se crea una sesión, recibo una cookie de sesión y me redirige al inicio

@stated
Given una contraseña incorrecta
When la envío en el formulario de acceso
Then veo el formulario otra vez con un mensaje de error y no se crea ninguna sesión

@stated
Given una sesión iniciada
When cierro la sesión
Then la sesión deja de valer en el servidor y la cookie se borra

@stated
Given que no hay hash configurado en el entorno
When se envía cualquier contraseña
Then el acceso se rechaza (falla cerrado)

@stated
Given una contraseña
When ejecuto la orden del paquete que genera el hash
Then obtengo una cadena que puedo poner en la variable de entorno y que verifica esa contraseña

@deduced
Given un hash con sal aleatoria
When se generan dos hashes de la misma contraseña
Then son distintos y ambos verifican

@deduced
Given una sesión creada
When consulto la base
Then solo aparece el hash SHA-256 del identificador, nunca el identificador de la cookie

@deduced
Given una sesión que superó la inactividad máxima o la antigüedad máxima
When se usa
Then no vale y se borra

@deduced
Given cinco intentos fallidos seguidos
When intento entrar de nuevo, incluso con la contraseña correcta
Then el acceso se rechaza hasta que pase el tiempo de bloqueo

@deduced
Given la cookie de sesión emitida
When reviso sus atributos
Then es `HttpOnly`, `SameSite=Lax` y `Secure` (salvo que el entorno lo desactive para desarrollo local)
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `python -m orquidea.autenticacion` con la contraseña `orquidea-2026` | generar el hash | una línea `scrypt$65536$8$2$…$…` |
| `POST /acceso` con `contrasena=orquidea-2026` y ese hash en `ORQUIDEA_PASSWORD_HASH` | iniciar sesión | 303 a `/` con `Set-Cookie: sesion=…; HttpOnly; SameSite=lax; Secure` |
| `POST /acceso` con `contrasena=otra` | iniciar sesión | 401 con el formulario y "Contraseña incorrecta" |
| `POST /salir` con la cookie | cerrar sesión | 303 a `/acceso`, cookie borrada, fila borrada |

## In scope

- Hash scrypt de la contraseña, verificación en tiempo constante y orden `python -m orquidea.autenticacion` que lo genera (ADR-004).
- Migración de la tabla `sesiones` y sesiones en servidor con caducidad por inactividad y por antigüedad.
- Rutas `GET`/`POST /acceso` y `POST /salir`; cookie `HttpOnly`, `SameSite=Lax`, `Secure`.
- Límite de intentos fallidos consecutivos con bloqueo temporal.
- Mover la fixture de `app.state.catalogo` a `tests/conftest.py` (entrada del parking lot cuyo disparador es esta historia).
- Añadir `python-multipart` para los formularios.

## Out of scope

- Proteger las demás rutas, CSRF en los `POST` autenticados y cabeceras de seguridad — s2.3.
- Botón "Salir" visible en las páginas — s2.3 (necesita el token CSRF).
- Registro, varias cuentas y recuperación de contraseña — no-gos del brief.
- Cambiar la contraseña desde la interfaz — se cambia la variable de entorno (ADR-004).

## Done when

- [stated] Con el hash correcto en el entorno se puede iniciar y cerrar sesión, y con uno incorrecto o ausente no se puede entrar (RF-08).
- [deduced] La base no contiene la contraseña ni identificadores de sesión utilizables.
- [deduced] Las sesiones caducan y los intentos fallidos se limitan.
- [deduced] La fixture compartida vive en `tests/conftest.py` y las pruebas web existentes la usan.
- [deduced] `./scripts/check` está en verde y `security-review` sin críticos.

## Notes

Diseño del épico: ADR-004 y `design.md`. Los `@stated` provienen de la fila de la historia en el scope del épico y de RF-08.
