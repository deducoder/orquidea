# Epic e2: Personal collection with login — Design

## Gemba findings

- `src/orquidea/web/app.py`: una sola aplicación FastAPI con rutas `/`, `/especies`, `/especies/{id}` y `/salud`; el catálogo se carga al importar y vive en `app.state.catalogo`. Sin sesión, sin base de datos, sin POST alguno. **Extender**, siguiendo el patrón (rutas simples, `Jinja2Templates`, HTML del servidor).
- `src/orquidea/catalogo/` (dominio) no conoce HTTP; `src/orquidea/datos/catalogo.py` carga los JSON. **Seguir el patrón de capas** del system-design: dominio de la colección en `orquidea.coleccion`, persistencia en `orquidea.datos`, autenticación en la capa web.
- `Especie.id` (`^[a-z0-9]+(-[a-z0-9]+)*$`) es el contrato de enlace que e1 dejó para e2; un ejemplar lo guarda como texto (ADR-003 punto 5).
- No hay dependencias de sesión ni de contraseñas: `pyproject.toml` solo trae fastapi, jinja2, pydantic y uvicorn. Todo lo de e2 sale de la biblioteca estándar (`sqlite3`, `hashlib.scrypt`, `secrets`, `hmac`) — sin duplicar nada existente.
- Los formularios `POST` de FastAPI necesitan `python-multipart`, que no está instalado. **Decisión de diseño:** s2.2 la añade como única dependencia nueva (formularios HTML clásicos; htmx solo para confirmaciones parciales).
- Pruebas: `tests/test_web_inicio.py` y `tests/test_web_especies.py` sustituyen y restauran `app.state.catalogo` cada una por su lado, y ninguna tiene sesión. Ambas se ven afectadas por s2.2 (fixture) y s2.3 (todas las rutas exigen sesión): un test que se queda sin actualizar es huérfano.
- `Dockerfile`: usuario `app` (uid 10001), sin directorio de datos escribible ni volumen; el README dice "no hay variables de entorno ni secretos" — deja de ser cierto con e2 (s2.7).
- Parking lot: la fixture repetida de `app.state.catalogo` promueve en "la primera historia de e2 que añada pruebas web" → s2.2, a `tests/conftest.py`. El homónimo `orquidea.datos.catalogo` (módulo) / `datos/catalogo/` (directorio) no cambia: e2 añade módulos de datos con otros nombres, no lo agrava.
- Sin conflictos de ADR: ADR-001 punto 4 difirió exactamente estas piezas; ADR-003 y ADR-004 las resuelven.

## Target components

| Component | Change | Purpose |
|-----------|--------|---------|
| `orquidea.datos.base` (conexión y migraciones) | create | Abrir SQLite, aplicar migraciones numeradas por `user_version`, ruta por `ORQUIDEA_DB` (`s2.1`) |
| `orquidea/datos/migraciones/*.sql` | create | `0001` sesiones (`s2.2`), `0002` ejemplares (`s2.4`), ampliada por `s2.5`/`s2.6` solo con migraciones nuevas |
| `orquidea.autenticacion` (hash scrypt, verificación, orden `python -m orquidea.autenticacion`) | create | Contraseña única, hash en `ORQUIDEA_PASSWORD_HASH` (`s2.2`) |
| `orquidea.datos.sesiones` | create | Sesiones en servidor con hash SHA-256 del identificador, caducidad y token CSRF (`s2.2`) |
| `orquidea.web.app` | modify | Rutas de acceso y cierre (`s2.2`), dependencia de sesión, CSRF y cabeceras (`s2.3`), rutas de la colección (`s2.4`, `s2.5`, `s2.6`) |
| `orquidea.coleccion` (modelo `Ejemplar` y reglas) | create | Ejemplar con especie de catálogo o nombre propio y notas; el dominio no conoce HTTP ni SQL (`s2.4`, `s2.5`, `s2.6`) |
| `orquidea.datos.ejemplares` | create | Persistencia de ejemplares (`s2.4`, `s2.6`) |
| `orquidea/web/templates/` (`acceso`, `coleccion`, `ejemplar`, ficha con botón) | create/modify | Vistas de acceso, "Mi colección", formulario de ejemplar y botón en `especie.html` (`s2.2`, `s2.4`, `s2.5`, `s2.6`) |
| `tests/conftest.py` | create | Fixture de catálogo y cliente autenticado compartida (`s2.2`) |
| `tests/test_web_inicio.py`, `tests/test_web_especies.py` | modify | Usar la fixture compartida y la sesión (`s2.2`, `s2.3`) |
| `Dockerfile`, `README.md` | modify | Directorio y volumen de datos, variables de entorno, orden del hash (`s2.7`) |
| `pyproject.toml` | modify | `python-multipart` (`s2.2`) |

## Key contracts

- Un solo usuario, sin nombre de usuario: el formulario de acceso pide solo la contraseña (RF-08).
- Sin `ORQUIDEA_PASSWORD_HASH` válido no se puede iniciar sesión: falla cerrado (ADR-004).
- Toda ruta, salvo el formulario de acceso, `/salud` y `/static`, exige sesión válida; sin ella redirige al acceso (303) o responde 401 a las peticiones de htmx.
- Todo `POST` exige el token CSRF de la sesión; sin él, 403 y nada cambia.
- El identificador de sesión viaja en la cookie; en la base solo su hash SHA-256; cerrar sesión borra la fila.
- Un ejemplar tiene `id` propio, `especie_id` opcional (texto, sin clave foránea), `nombre` y `notas`; sin `especie_id`, `nombre` es obligatorio; con `especie_id`, debe existir en el catálogo al guardar.
- Un ejemplar cuyo `especie_id` ya no está en el catálogo se muestra sin romperse.
- Toda consulta es parametrizada; ninguna cadena del usuario entra en el SQL (ADR-003).
- Las migraciones se aplican en orden y una aplicada nunca se edita.
- Los mensajes de la interfaz van en español.

## Decisions (ADRs)

- ADR-003: La colección se guarda con sqlite3 de la biblioteca estándar y migraciones numeradas propias — sin ORM para dos tablas; `records/decisions/adr-003-persistencia-con-sqlite3-y-migraciones-propias.md`.
- ADR-004: Autenticación de un solo usuario: contraseña con scrypt en el entorno y sesión guardada en el servidor — sin dependencias de seguridad; `records/decisions/adr-004-autenticacion-de-un-solo-usuario-con-sesion-en-servidor.md`.

## Legacy sweep

Nada se elimina. Cambian de contrato: las pruebas web de e1 (`test_web_inicio.py`, `test_web_especies.py`) dejan de funcionar sin sesión y se actualizan en s2.2 y s2.3; la frase del README "No hay variables de entorno ni secretos" queda falsa y la corrige s2.7. El `Dockerfile` de e1 (sin directorio de datos ni volumen) se amplía en s2.7.
