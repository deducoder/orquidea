# Story s2.3: Protect all routes — Design

> Complexity: moderate

## 1 · What & why

**Problem:** tras s2.2 hay sesión pero ninguna ruta la exige; cualquiera ve el catálogo y, desde s2.4, la colección. Tampoco hay protección CSRF ni cabeceras de seguridad.
**Value:** RF-08 queda cumplido de punta a punta y toda ruta futura nace protegida.

## 2 · Approach

Una dependencia global `exigir_sesion` (seguro por defecto): valida la cookie, deja la sesión en `request.state.sesion` y, en métodos que cambian datos, exige el token CSRF. Las rutas públicas son una lista explícita. Un middleware añade las cabeceras. Sin dependencias nuevas.

**Components affected:**

- `src/orquidea/web/app.py`: modify — `exigir_sesion` como `dependencies=[...]` de la aplicación, `SesionRequerida` y su manejador (303 o 401 con `HX-Redirect`), `RUTAS_PUBLICAS`, middleware de cabeceras, `docs_url`/`redoc_url`/`openapi_url` en `None`.
- `src/orquidea/web/templates/base.html`: modify — botón "Salir" y `hx-headers` con el token cuando hay sesión.
- `tests/conftest.py`: modify — fixture `client_autenticado` (crea la sesión con `datos.sesiones.crear` y pone la cookie).
- `tests/test_web_inicio.py`, `tests/test_web_especies.py`, `tests/test_web_acceso.py`: modify — usar `client_autenticado` donde corresponde; `/salir` con token.
- `tests/test_web_proteccion.py`: create — enumeración de rutas, htmx, CSRF, cabeceras, docs apagadas.

**Legacy sweep:** las pruebas web de e1 que llaman rutas sin sesión pasan a `client_autenticado` (en este mismo cambio, sin huérfanas). El test de s2.2 de cierre de sesión pasa a enviar el token. Nada más se orfana.

**Gobernanza:** RF-08; ADR-004 (puntos 3, 5 y 6); `should-security-002` — ASVS V4 (control de acceso, 4.1.1 y 4.2.2 CSRF), V14.4 (cabeceras: 14.4.3 CSP, 14.4.4 nosniff, 14.4.6 Referrer-Policy, 14.4.7 anti-framing), V8.3 (`no-store`), V14.3.2 (sin documentación de depuración expuesta). Recorrido hecho ahora, en diseño, según la memoria `asvs-checklist-at-design`.

## 3 · Interface / examples

### Usage (API / CLI)

```python
RUTAS_PUBLICAS = {"/acceso", "/salud"}  # rutas con plantilla de ruta (scope["route"].path)


def exigir_sesion(
    request,
    conexion,
    csrf: Annotated[str | None, Form()] = None,
    x_csrf_token: Annotated[str | None, Header()] = None,
) -> None: ...
```

```http
GET  /especies                     (sin cookie)               -> 303 Location: /acceso
GET  /especies  HX-Request: true   (sin cookie)               -> 401 HX-Redirect: /acceso
POST /salir     Cookie válida, sin token                      -> 403
POST /salir     Cookie válida, csrf=<token de la sesión>      -> 303 Location: /acceso
GET  /docs                                                    -> 404
GET  /salud                        (sin cookie)               -> 200
```

Cabeceras: `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin`, `X-Frame-Options: DENY`, `Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'` (el `unsafe-inline` solo en estilos: htmx inserta un `<style>` para sus indicadores), `Cache-Control: no-store` fuera de `/static`, `Strict-Transport-Security: max-age=31536000` cuando la cookie es `Secure`.

### Key data structures (if applicable)

```html
<!-- base.html, con sesión -->
<body hx-headers='{"X-CSRF-Token": "{{ request.state.sesion.csrf }}"}'>
<form method="post" action="/salir"><input type="hidden" name="csrf" value="{{ request.state.sesion.csrf }}"><button>Salir</button></form>
```

## 4 · Acceptance criteria

- **Must:** toda ruta salvo las públicas exige sesión (probado enumerando `app.routes`); `POST` sin token válido → 403; con token se procesa; respuestas con las cabeceras.
- **Should:** htmx sin sesión → 401 + `HX-Redirect`; `no-store` en páginas; docs apagadas.
- **Must NOT:** comparar el token con `==`; dejar rutas públicas por omisión; poner el token en la URL; abrir `unsafe-inline` en scripts.

### Deduced criteria

- Petición htmx sin sesión → 401 con `HX-Redirect`: confirmed
- Botón "Salir" con token y `hx-headers`: confirmed
- Cabeceras de seguridad en toda respuesta y `no-store` en páginas: confirmed
- `/docs`, `/redoc`, `/openapi.json` no existen: confirmed
- Una ruta nueva sin declarar pública queda protegida: confirmed — la dependencia es global y la excepción es una lista explícita
- Las pruebas web de e1 pasan con sesión y el gate en verde: confirmed

### Scenarios (delta over the scope)

```gherkin
Given una sesión caducada por inactividad
When pido una ruta protegida
Then me redirige a /acceso como si no hubiera sesión

Given una petición autenticada
When llega cualquier ruta protegida
Then la actividad de la sesión se renueva (deslizante)

Given una ruta pública (/acceso) pedida con una sesión válida
When la abro
Then se muestra el formulario (no se fuerza nada más)
```
