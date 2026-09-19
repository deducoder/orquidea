# Story s2.2: Login and logout — Retrospective

Estimated: M · Actual: M

## Summary

El único usuario puede iniciar y cerrar sesión. La contraseña vive como hash scrypt (N=2^16, r=8, p=2) en `ORQUIDEA_PASSWORD_HASH` y `python -m orquidea.autenticacion` lo genera; sin hash válido el acceso falla cerrado. La sesión se guarda en el servidor (`0001-sesiones.sql`, solo el SHA-256 del identificador, caducidad de 30 min de inactividad y 12 h de antigüedad); la cookie es `HttpOnly`, `SameSite=Lax`, `Secure` y con prefijo `__Host-` (sin prefijo y sin `Secure` con `ORQUIDEA_COOKIE_SEGURA=0`). Cinco fallos seguidos bloquean cinco minutos. La fixture `client` de `tests/conftest.py` sustituye a las dos copias del parking lot. Cinco commits de tarea (`feat`), uno de ellos no planeado (ver abajo).

## Finalize (reportado por story-implement)

- **Gate:** `./scripts/check` en verde, 110 pruebas (52 heredadas de e1 + 11 de s2.1 + 47 de s2.2), ruff, ruff format, mypy strict.
- **Orphaned-test check:** `tests/test_web_inicio.py` y `tests/test_web_especies.py` importan `orquidea.web.app`, que cambió: ambas se actualizaron a la fixture compartida (no huérfanas). `tests/test_datos_base.py` importa `orquidea.datos.base` (se añadió `conectar`, `check_same_thread=False`) y no se tocó: sigue pasando y `conectar` lo cubre `test_datos_sesiones.py`. Limpio.
- **Acceptance:** los diez escenarios del scope y los tres del diseño tienen prueba. Prueba manual (T5) con `uvicorn` real y `curl`: `GET /acceso` 200; contraseña mala 401; correcta 303 a `/` con `Set-Cookie` `HttpOnly; SameSite=lax; Max-Age=43200`; la base guardó el SHA-256 (no el valor de la cookie); `POST /salir` 303 y la fila desapareció; cinco fallos 401 y la contraseña correcta después 429.
- **Plan con `> Pause: none`:** sin aprobación humana por tarea; el despacho se decidió en `decisions.md`.
- **Tiempo de implementación:** sin tracker; derivable de la rama, no registrado.

## Reviews

- **quality-review:** sin críticos. Observaciones: (1) `_nombre_de_cookie()` y `_cookie_segura()` leen el entorno en cada petición: coherente con `ORQUIDEA_PASSWORD_HASH` y probable en pruebas, sin costo apreciable. (2) `samesite="lax"` explícito es un mutante equivalente hoy (Starlette lo trae por defecto), se deja a propósito por si el valor por defecto cambia. (3) El límite de intentos es global: quien lo agote bloquea al dueño cinco minutos; el diseño ya lo declaró como costo.
- **security-review:** PASS WITH FINDINGS. Bandit: 0 hallazgos en `src/`; 125 B101 (baja) en `tests/`, ya estacionados. Guardrails `should-security-002` (ASVS L2), contra lo que la historia toca: hash lento con sal (2.4) cumple; token de sesión aleatorio de 256 bits, nuevo en cada acceso (3.2) cumple; invalidación al cerrar y caducidad (3.3) cumple; atributos de cookie (3.4) cumple **tras corregir en la revisión** el prefijo `__Host-` (3.4.4); anti-automatización (2.2.1) cumple con la limitación global anotada; registro de eventos de autenticación sin secretos (7.1) cumple **tras añadirlo en la revisión**. Observaciones que **s2.3** debe cerrar: CSRF en los `POST` autenticados y cabeceras de seguridad, más proteger todas las rutas; `/salir` no lleva token CSRF hasta entonces (cerrar sesión ajena es de bajo impacto, y `SameSite=Lax` no envía la cookie en un `POST` entre sitios). Ninguna política de longitud mínima de contraseña: el humano elige la contraseña al generar el hash.

## What went well

- Hacer las mutaciones sistemáticas (cada propiedad del plan) encontró dos pruebas que no mordían: la purga de sesiones caducadas (el `obtener` posterior también borraba la fila, así que la prueba pasaba sin la purga) y el esquema del hash (el resto lo rechazaba por otro camino). Ambas se corrigieron con una aserción intermedia y una prueba con datos válidos.
- Aislar primero el código criptográfico y de sesión, sin HTTP, permitió probar cada propiedad con datos mínimos antes de tocar rutas.

## What to improve

- La comparación ASVS de la revisión mostró dos huecos (prefijo `__Host-`, registro de accesos) que estaban en la guardia y no en el diseño; costó un commit no planeado. En la próxima historia de seguridad, recorrer la lista ASVS aplicable **durante el diseño**, no en la revisión.
- `ruff format` reformatea los `.md` de la historia: correrlo antes del commit de la fase para no gastar un `style(...)`.
- El plan nombró `compare_digest` como "no observable por conducta"; se resolvió con un espía, y el mismo truco sirve para otras funciones de seguridad.

## Learned

1. About the system: FastAPI corre las dependencias síncronas y el endpoint en hilos distintos, así que una conexión SQLite abierta por petición necesita `check_same_thread=False`; Starlette ya envía `SameSite=lax` por defecto; `TestClient` con `base_url="https://testserver"` reenvía cookies `Secure`.
2. About the process: una mutación de "borrar la línea" es válida solo si otra ruta no compensa lo mismo (la purga y el `obtener`); poner la aserción entre las dos.
3. Capability gained: sesión con token CSRF ya guardado (`sesiones.csrf`), lista para que s2.3 la exija en los `POST`, y fixture `client` con base temporal para las historias que siguen.
