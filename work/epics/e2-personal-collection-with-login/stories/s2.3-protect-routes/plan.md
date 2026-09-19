# Story s2.3: Protect all routes — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · Toda ruta exige sesión, salvo las públicas

- **Files:** modify `src/orquidea/web/app.py`, `tests/conftest.py`, `tests/test_web_inicio.py`, `tests/test_web_especies.py`, `tests/test_web_acceso.py`; create `tests/test_web_proteccion.py`
- **TDD:** RED pruebas: enumerar `app.routes` (rutas con `path` y método, sustituyendo parámetros) y comprobar que sin cookie todas salvo `/acceso`, `/salud` responden 303 a `/acceso` (y las de `/static` quedan fuera); con htmx 401 + `HX-Redirect`; con sesión válida `/`, `/especies` y una ficha responden 200; sesión caducada redirige; `/docs`, `/redoc`, `/openapi.json` dan 404; una ruta añadida en la prueba sin declarar pública queda protegida → GREEN `exigir_sesion` global, `SesionRequerida` y manejador, `RUTAS_PUBLICAS`, docs apagadas; las pruebas de e1 pasan a `client_autenticado` → REFACTOR
- **Satisfies:** scenarios 1, 2, 5, 8, 9 del scope y los deltas de caducidad y renovación
- **Mold:** `src/orquidea/web/app.py` de s2.2 (dependencia `Base`, cookie por entorno)
- **Verify:** quitar la dependencia global (rojo en la enumeración); agregar `/especies` a las públicas (rojo); ignorar la caducidad (rojo con la sesión vencida); no renovar (rojo); dejar `/docs` (rojo); responder 200 al htmx sin sesión (rojo); luego `./scripts/check` completo
- **Commit:** feat(web): toda ruta exige sesión salvo el acceso y la salud

### T2 · CSRF en los POST autenticados y botón "Salir"

- **Files:** modify `src/orquidea/web/app.py`, `src/orquidea/web/templates/base.html`, `tests/test_web_proteccion.py`, `tests/test_web_acceso.py`
- **TDD:** RED pruebas: `POST /salir` sin token, con token de otra sesión y vacío → 403 y la sesión sigue; con el campo `csrf` o la cabecera `X-CSRF-Token` correctos → 303 y sesión borrada; una página autenticada trae el formulario de "Salir" con el token de su sesión y `hx-headers`; una página anónima (`/acceso`) no trae token → GREEN verificación con `hmac.compare_digest` en `exigir_sesion`, plantilla → REFACTOR
- **Satisfies:** scenarios 3, 4 y 6 del scope
- **Mold:** T1 y `orquidea.autenticacion` (`compare_digest`, espía de s2.2)
- **Verify:** no exigir token (rojo); aceptar token vacío o `None == None` (rojo); comparar con `==` (rojo con el espía); exigir el token también en GET (rojo: las páginas dejan de abrir); aceptar el token de otra sesión (rojo); quitar el botón o el token del botón (rojo); luego `./scripts/check`
- **Commit:** feat(web): token CSRF en los POST autenticados y botón de salir

### T3 · Cabeceras de seguridad

- **Files:** modify `src/orquidea/web/app.py`, `tests/test_web_proteccion.py`
- **TDD:** RED pruebas: toda respuesta (página, 303, 401, 404, `/static`, `/salud`) trae las cuatro cabeceras; las páginas y las redirecciones traen `Cache-Control: no-store` y `/static` no; HSTS solo con cookie `Secure` → GREEN middleware → REFACTOR
- **Satisfies:** scenario 7 del scope
- **Mold:** none
- **Verify:** quitar cada cabecera (rojo, una prueba por cabecera); `no-store` también en `/static` (rojo); HSTS con `ORQUIDEA_COOKIE_SEGURA=0` (rojo); permitir `script-src` inline en la CSP (rojo: se comprueba que la CSP no contiene `unsafe-inline` fuera de `style-src`); luego `./scripts/check`
- **Commit:** feat(web): cabeceras de seguridad en todas las respuestas

### T4 · Manual integration test

- Con `uvicorn` real, hash generado por la orden y `ORQUIDEA_COOKIE_SEGURA=0`: `curl` sin sesión a `/`, `/especies`, `/especies/epidendrum-radicans`, `/salud`, `/static/htmx.min.js`, `/docs`; acceso; las mismas rutas con cookie; `POST /salir` sin y con token; cabeceras con `curl -I`.
- **Verify:** lo público responde, lo demás redirige, con sesión se ve el catálogo real (100 especies), el 403 sin token, y `./scripts/check` en verde.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 — primero el control de acceso (lo que abre la colección), luego CSRF, las cabeceras al final.
- **Dependencies:** secuenciales, acíclicas.
- **Risks:** declarar `Form` y `Header` en una dependencia global puede interferir con rutas que declaran sus propios campos de formulario (s2.4 en adelante) → T2 lo prueba con `/salir` y s2.4 lo vuelve a ejercitar; el `scope["route"]` puede no estar en peticiones sin ruta (404) → se ignora la dependencia allí, que no corre.
