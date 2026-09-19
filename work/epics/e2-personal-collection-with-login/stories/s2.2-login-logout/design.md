# Story s2.2: Login and logout — Design

> Complexity: complex

## 1 · What & why

**Problem:** la aplicación no tiene noción de usuario: cualquiera que llegue a la URL vería la colección que e2 va a guardar.
**Value:** un solo usuario entra con su contraseña y su sesión se puede invalidar; es el cimiento de RF-08 sobre el que s2.3 cierra todas las rutas.

## 2 · Approach

Contraseña como hash scrypt en `ORQUIDEA_PASSWORD_HASH`, sesión guardada en el servidor con un identificador aleatorio en la cookie y su hash SHA-256 en la tabla, y un límite en memoria de intentos fallidos (ADR-004, sobre ADR-003). Tres capas separadas: verificación de la contraseña (`orquidea.autenticacion`), sesiones (`orquidea.datos.sesiones`), rutas y cookie (`orquidea.web`).

**Components affected:**

- `src/orquidea/autenticacion.py`: create — `hashear_contrasena`, `verificar_contrasena`, `LimiteDeIntentos`, y la orden `python -m orquidea.autenticacion`.
- `src/orquidea/datos/migraciones/0001-sesiones.sql`: create — tabla `sesiones`.
- `src/orquidea/datos/base.py`: modify — separar `conectar(ruta)` (abre con PRAGMAs) de `abrir_base` (mkdir + conectar + migrar), para abrir una conexión por petición sin volver a leer migraciones.
- `src/orquidea/datos/sesiones.py`: create — `crear`, `obtener`, `cerrar`, con caducidad.
- `src/orquidea/web/app.py`: modify — `GET`/`POST /acceso`, `POST /salir`, dependencia que abre y cierra la conexión, `lifespan` que migra, `app.state.ruta_base`.
- `src/orquidea/web/templates/acceso.html`: create.
- `tests/conftest.py`: create — fixture del catálogo y cliente `https://testserver` con base temporal (parking lot).
- `tests/test_web_inicio.py`, `tests/test_web_especies.py`: modify — usar la fixture compartida.
- `pyproject.toml`, `uv.lock`: modify — `python-multipart` (los `Form(...)` de FastAPI la exigen; el paquete es mantenido por Starlette/Encode, amplio uso, no puede hacerse en menos de 50 líneas con seguridad).

**Legacy sweep:** las dos fixtures de `app.state.catalogo` repetidas en `tests/test_web_inicio.py` y `tests/test_web_especies.py` quedan reemplazadas por la de `conftest.py` (se borran ahí mismo). Nada más se orfana. `abrir_base` mantiene su firma; solo delega en `conectar`.

**Gobernanza:** RF-08; `should-security-002` (ASVS L2: hash lento con sal, tokens aleatorios, cookie `HttpOnly`/`Secure`/`SameSite`, invalidación al cerrar, anti-automatización); system-design (la capa de datos no conoce HTTP); `must-quality-001..003`.

## 3 · Interface / examples

### Usage (API / CLI)

```bash
$ uv run python -m orquidea.autenticacion        # pide la contraseña sin eco
Contraseña: ********
scrypt$65536$8$2$Zm9v…$YmFy…                     # se pone en ORQUIDEA_PASSWORD_HASH
```

```python
from orquidea.autenticacion import hashear_contrasena, verificar_contrasena

hash_ = hashear_contrasena("orquidea-2026")
verificar_contrasena("orquidea-2026", hash_)  # True
verificar_contrasena("otra", hash_)  # False
verificar_contrasena("orquidea-2026", None)  # False  (sin configurar: cierra)
verificar_contrasena("x", "basura")  # False  (hash malformado: cierra)
```

```http
POST /acceso            contrasena=orquidea-2026       -> 303 Location: /   Set-Cookie: sesion=<43 chars>; HttpOnly; Path=/; SameSite=lax; Secure
POST /acceso            contrasena=otra                -> 401 (formulario con "Contraseña incorrecta")
POST /acceso  (6.º intento tras 5 fallos)              -> 429 "Demasiados intentos; espera unos minutos"
POST /salir   Cookie: sesion=…                         -> 303 Location: /acceso   Set-Cookie: sesion=""; Max-Age=0
```

### Key data structures (if applicable)

```sql
-- 0001-sesiones.sql
CREATE TABLE sesiones (
    id_hash TEXT PRIMARY KEY,      -- SHA-256 hex del identificador de la cookie
    csrf TEXT NOT NULL,            -- token CSRF de la sesión (lo usa s2.3)
    creada INTEGER NOT NULL,       -- segundos epoch
    ultima_actividad INTEGER NOT NULL
);
```

```python
INACTIVIDAD_MAXIMA = 30 * 60  # 30 min (ASVS 3.3.2, L2)
ANTIGUEDAD_MAXIMA = 12 * 60 * 60  # 12 h


@dataclass(frozen=True)
class Sesion:
    csrf: str


def crear(conexion, ahora: int) -> tuple[str, Sesion]: ...  # (identificador para la cookie, sesión)
def obtener(
    conexion, identificador: str, ahora: int
) -> Sesion | None: ...  # renueva ultima_actividad; borra si caducó
def cerrar(conexion, identificador: str) -> None: ...


class LimiteDeIntentos:  # 5 fallos seguidos -> bloqueo de 5 min; un acierto reinicia
    def bloqueado(self, ahora: float) -> bool: ...
    def fallo(self, ahora: float) -> None: ...
    def acierto(self) -> None: ...
```

Decisiones de diseño (dentro de ADR-004, sin ADR nuevo): parámetros scrypt N=2^16, r=8, p=2 (equivalencia OWASP, 64 MiB), guardados en la propia cadena del hash para poder subirlos; el contador de intentos es global, no por IP (un único usuario, y tras un proxy la IP no es fiable) — coste asumido: quien lo agote bloquea al dueño 5 min; `Secure` por defecto y `ORQUIDEA_COOKIE_SEGURA=0` para desarrollo local en http; tras acceder se redirige siempre a `/` (sin `siguiente`, que sería un redireccionamiento abierto). La conexión se abre por petición (SQLite con `check_same_thread`); `lifespan` migra al arrancar.

## 4 · Acceptance criteria

- **Must:** contraseña correcta crea sesión y cookie; incorrecta o sin hash configurado no; cerrar sesión borra la fila y la cookie; la base solo guarda el hash del identificador; la orden genera un hash que verifica.
- **Should:** caducidad por inactividad y por antigüedad; límite de intentos.
- **Must NOT:** guardar la contraseña ni el identificador en claro; comparar hashes con `==`; aceptar un hash con parámetros de coste absurdos en la generación; redirigir a una URL dada por el usuario; loguear la contraseña.

### Deduced criteria

- Dos hashes de la misma contraseña son distintos y ambos verifican: confirmed
- La base solo contiene el hash SHA-256 del identificador: confirmed
- Una sesión que supera inactividad o antigüedad no vale y se borra: confirmed
- Cinco fallos seguidos bloquean incluso la contraseña correcta hasta que pase el tiempo: confirmed
- La cookie es `HttpOnly`, `SameSite=Lax` y `Secure` salvo que el entorno lo desactive: confirmed
- La base no contiene la contraseña ni identificadores utilizables: confirmed
- Las sesiones caducan y los intentos se limitan: confirmed
- La fixture compartida vive en `tests/conftest.py` y las pruebas web existentes la usan: confirmed
- `./scripts/check` en verde y `security-review` sin críticos: confirmed

### Scenarios (delta over the scope)

```gherkin
Given un hash malformado en el entorno
When se envía cualquier contraseña
Then el acceso se rechaza sin lanzar una excepción

Given una cookie de sesión con un identificador que no existe
When se usa
Then no vale (sin excepción)

Given un acierto tras cuatro fallos
When se intenta de nuevo con contraseña errónea
Then el contador empezó de cero (no bloquea hasta el quinto fallo nuevo)
```
