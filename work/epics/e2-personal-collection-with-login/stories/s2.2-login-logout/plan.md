# Story s2.2: Login and logout — Plan

> Size: M
> Pause: none (default)

## Tasks

### T1 · Hash scrypt, verificación y orden que lo genera

- **Files:** create `src/orquidea/autenticacion.py`, `tests/test_autenticacion.py`
- **TDD:** RED pruebas: el hash verifica su contraseña y rechaza otra; dos hashes de la misma contraseña difieren; `None`, cadena vacía, `"basura"`, parámetros no numéricos y un hash con longitud de sal/hash incorrecta devuelven `False` sin excepción; `main()` (con `getpass` sustituido) imprime un hash que verifica → GREEN `hashear_contrasena(contrasena, n=2**16)`, `verificar_contrasena`, `main` → REFACTOR
- **Satisfies:** scenarios de hash y generación del scope y el delta del hash malformado
- **Mold:** none
- **Verify:** cada mutación pone en rojo su prueba: sal fija (los dos hashes coinciden); comparar con `==` en vez de `hmac.compare_digest` (no detectable por conducta: se fija con una prueba que inspecciona que se llama `compare_digest`, o se declara en la revisión); ignorar los parámetros guardados y usar los constantes (rojo con un hash de `n` distinto); devolver `True` cuando `hash` es `None`; dejar escapar `ValueError` con un hash malformado; luego `./scripts/check` completo (archivo nuevo)
- **Commit:** feat(autenticacion): hash scrypt de la contraseña y orden que lo genera

### T2 · Límite de intentos fallidos

- **Files:** modify `src/orquidea/autenticacion.py`, `tests/test_autenticacion.py`
- **TDD:** RED con reloj inyectado: 4 fallos no bloquean; el 5.º bloquea durante 5 min y desbloquea al pasar el tiempo; un acierto reinicia el contador → GREEN `LimiteDeIntentos` → REFACTOR
- **Satisfies:** scenario del límite y el delta del contador
- **Mold:** T1
- **Verify:** umbral 5→6 (rojo), bloqueo que nunca expira (rojo), `acierto` que no reinicia (rojo), bloqueo por `>` en vez de `>=` en el borde de expiración (rojo); luego `./scripts/check`
- **Commit:** feat(autenticacion): límite de intentos fallidos consecutivos

### T3 · Tabla de sesiones, sesiones en servidor y `conectar`

- **Files:** create `src/orquidea/datos/migraciones/0001-sesiones.sql`, `src/orquidea/datos/sesiones.py`, `tests/test_datos_sesiones.py`; modify `src/orquidea/datos/base.py` (extraer `conectar`), `tests/test_datos_base.py`
- **TDD:** RED pruebas con base temporal migrada con la migración real: `crear` devuelve un identificador de ≥ 32 bytes de entropía y la base solo guarda su SHA-256 (el identificador no aparece en ninguna columna); `obtener` devuelve la sesión y renueva `ultima_actividad`; identificador inexistente → `None`; supera inactividad o antigüedad → `None` y la fila desaparece; `cerrar` borra; `conectar` abre con FK y WAL sin migrar → GREEN → REFACTOR
- **Satisfies:** scenarios de sesión, caducidad, hash del identificador y delta de identificador inexistente
- **Mold:** `src/orquidea/datos/base.py` (T1 de s2.1, consultas parametrizadas)
- **Verify:** guardar el identificador en claro (rojo); no comprobar inactividad (rojo); no comprobar antigüedad aunque haya actividad reciente (rojo); `<` por `<=` en los bordes con la prueba en el límite exacto (rojo); `cerrar` que no borra (rojo); `obtener` que no renueva (rojo); luego `./scripts/check` completo
- **Commit:** feat(datos): sesiones en el servidor con caducidad

### T4 · Rutas de acceso y cierre, cookie y fixture compartida

- **Files:** modify `pyproject.toml`, `uv.lock` (`python-multipart`), `src/orquidea/web/app.py`, `tests/test_web_inicio.py`, `tests/test_web_especies.py`; create `src/orquidea/web/templates/acceso.html`, `tests/conftest.py`, `tests/test_web_acceso.py`
- **TDD:** RED con el cliente `https://testserver`: contraseña correcta → 303 a `/`, cookie `HttpOnly`/`SameSite=lax`/`Secure`, una fila en la base con el SHA-256 del valor de la cookie; incorrecta → 401 con mensaje y sin fila ni cookie; sin `ORQUIDEA_PASSWORD_HASH` o con hash malformado → 401; `POST /salir` con cookie → 303 a `/acceso`, cookie borrada y fila borrada; 5 fallos → 429 y ni la contraseña correcta entra; con `ORQUIDEA_COOKIE_SEGURA=0` la cookie no lleva `Secure`; `GET /acceso` muestra el formulario; las pruebas web existentes pasan a la fixture del `conftest.py` → GREEN → REFACTOR
- **Satisfies:** scenarios de acceso, cierre, fallo cerrado, cookie, límite, y la fixture
- **Mold:** rutas y plantillas de `src/orquidea/web/app.py` (s1.3); T1 a T3
- **Verify:** cookie sin `httponly` (rojo); sin `secure` (rojo); crear la sesión aunque la contraseña sea incorrecta (rojo); aceptar el acceso cuando el hash es `None` (rojo); `POST /salir` que borra la cookie pero no la fila (rojo); no consultar el límite antes de verificar (rojo con la contraseña correcta tras 5 fallos); no registrar el fallo (rojo); luego `./scripts/check` completo
- **Commit:** feat(web): inicio y cierre de sesión con cookie segura

### T5 · Manual integration test

- Con `ORQUIDEA_DB` temporal, `ORQUIDEA_PASSWORD_HASH` generado con la orden real y `ORQUIDEA_COOKIE_SEGURA=0`, arrancar `uvicorn` y recorrer con `curl`: `GET /acceso`, acceso correcto e incorrecto, cierre, y cinco fallos.
- **Verify:** la cookie aparece con sus atributos, `sqlite3` muestra una fila que no contiene el valor de la cookie y desaparece al cerrar, el sexto intento da 429, y `./scripts/check` está en verde.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 → T5 — primero el código criptográfico y de sesión (el riesgo de la épica), aislado y sin HTTP; las rutas al final lo juntan.
- **Dependencies:** T4 depende de T1 a T3; el resto, secuenciales, acíclicas.
- **Risks:** `compare_digest` no es observable por conducta → se comprueba con una prueba que sustituye `hmac.compare_digest` y verifica que se invoca; scrypt con N=2^16 hace lentas las pruebas → `hashear_contrasena` acepta `n` y las pruebas usan un `n` bajo, con una sola prueba con los parámetros reales; `python-multipart` instalado por `uv add` necesita red (disponible); Bandit puede marcar el hash o `hashlib` (B324) → se revisa, no se silencia sin razón.
