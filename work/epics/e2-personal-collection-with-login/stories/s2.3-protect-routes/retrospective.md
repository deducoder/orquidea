# Story s2.3: Protect all routes — Retrospective

Estimated: S · Actual: S

## Summary

Toda ruta exige sesión salvo `/acceso` y `/salud` (`/static` es un montaje, fuera de la dependencia): una dependencia global `exigir_sesion` lee la cookie, valida la sesión, la renueva y deja la sesión en `request.state`; sin sesión redirige a `/acceso` (303) o, si la petición es de htmx, responde 401 con `HX-Redirect`. Todo `POST` autenticado exige el token CSRF de la sesión (campo `csrf` o cabecera `X-CSRF-Token`, comparado con `hmac.compare_digest`). La plantilla base trae el botón "Salir" y `hx-headers` con el token. Un middleware añade `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, una CSP sin scripts en línea, `Cache-Control: no-store` fuera de `/static` y HSTS cuando la cookie es `Secure`; `/docs`, `/redoc` y `/openapi.json` no existen. La fixture `client` de `conftest.py` ahora trae sesión y `anonimo` es el cliente sin ella. Tres commits de tarea, sin ninguno no planeado.

## Finalize (reportado por story-implement)

- **Gate:** `./scripts/check` en verde, 146 pruebas (110 al cierre de s2.2 + 36), ruff, ruff format, mypy strict.
- **Orphaned-test check:** todos los archivos de prueba que importan `orquidea.web.app` (`test_web_inicio`, `test_web_especies`, `test_web_acceso`, `test_web_proteccion`, `conftest`) se tocaron o son nuevos y pasan; `test_datos_base`, `test_datos_sesiones` y `test_autenticacion` no dependen de lo que cambió. Limpio.
- **Acceptance:** los nueve escenarios del scope y los tres del diseño tienen prueba, entre ellos la que enumera `app.routes` y comprueba que sin sesión cada ruta no pública redirige, y otra que añade una ruta nueva y comprueba que nace protegida. Prueba manual (T4) con `uvicorn` real y `curl`: sin sesión `/`, `/especies` y una ficha dan 303; `/salud` y `/static` 200; `/docs` y `/openapi.json` 404; con sesión se ven las 100 especies del catálogo real; `POST /salir` sin token 403 y con token 303 y la sesión deja de valer; las cabeceras aparecen.
- **Plan con `> Pause: none`:** sin aprobación humana por tarea; el despacho se decidió en `decisions.md`.
- **Tiempo de implementación:** sin tracker; derivable de la rama, no registrado.

## Reviews

- **quality-review:** sin críticos. Observaciones: (1) `exigir_sesion` abre la conexión a la base también en rutas públicas (`/salud` la incluye): un healthcheck que exige poder abrir la base es razonable aquí y no se cambia. (2) Un `POST` con el campo `csrf` y la cabecera a la vez pasa si cualquiera de los dos es correcto; no abre nada. (3) `samesite="lax"` sigue siendo equivalente hoy (ver s2.2).
- **security-review:** PASS. Bandit: 0 hallazgos en `src/orquidea/web/app.py`; 99 B101 (baja) en `tests/`, ya estacionados. Guardrails `should-security-002`, recorridos en el diseño y confirmados: control de acceso en el servidor (V4.1.1), CSRF (V4.2.2), cabeceras (V14.4.3, .4, .6, .7), sin caché de páginas autenticadas (V8.3), sin documentación de depuración expuesta (V14.3.2). Sin `includeSubDomains` en HSTS a propósito. **Sin verificar en un navegador real:** que la CSP (sin `unsafe-eval` ni scripts en línea) no rompa htmx; la búsqueda del catálogo no usa evaluación de código, pero solo un navegador lo confirma. Se pide al humano en `epic-review`, junto con la medición de `must-perf-001`, que ya estaba prevista como stop.

## What went well

- Recorrer la lista ASVS durante el diseño (lo aprendido en s2.2, memoria `asvs-checklist-at-design`) dejó cero commits no planeados y ninguna sorpresa en la revisión.
- La prueba que enumera `app.routes` fija el contrato del system-design ("toda ruta, salvo el acceso, exige sesión") para todas las rutas que vendrán en s2.4 a s2.6: si una ruta nueva queda pública por descuido, la prueba se cae.
- Las mutaciones encontraron una aserción demasiado laxa (`hx-headers` renombrado sobrevivía): se apretó a la cadena exacta del atributo.

## What to improve

- Cometí scope, diseño y plan en un solo commit `initialize` y tuve que separarlos con un `reset` local; un commit por fase desde el principio.
- Las mutaciones de "borrar la opción" de `FastAPI(docs_url=None)` no bastan solas: `openapi_url=None` ya apaga los tres; las mutaciones deben tocar la causa real, no una de las tres redundantes.

## Learned

1. About the system: `request.scope["route"]` está disponible dentro de una dependencia global y permite declarar públicas las rutas por plantilla de ruta; un middleware `@app.middleware("http")` envuelve también las respuestas de los manejadores de excepción (303, 401, 403, 404); `app.mount` no recibe las dependencias de la aplicación.
2. About the process: escribir primero la prueba que enumera todas las rutas convierte una regla de arquitectura en un test que vigila el futuro.
3. Capability gained: toda ruta nueva nace protegida y con CSRF; s2.4 a s2.6 solo declaran sus rutas y sus formularios llevan `csrf` desde la plantilla base o su propio campo.
