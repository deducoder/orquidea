# Orquídea

Aplicación web personal para llevar una colección de orquídeas nativas de
Chiapas: catálogo de especies con sus cuidados, ejemplares propios con foto, y
registro de riegos y floraciones. El porqué está en
[`governance/vision.md`](governance/vision.md).

## Quick start

```bash
uv sync            # instala Python y las dependencias de desarrollo
./scripts/check    # verifica que todo esté en verde
```

Para ejecutar la aplicación en local, genera el hash de tu contraseña y pásalo por el entorno (ver
[Configuración](#configuración)):

```bash
export ORQUIDEA_PASSWORD_HASH="$(uv run python -m orquidea.autenticacion)"   # pide la contraseña
export ORQUIDEA_COOKIE_SEGURA=0        # solo en local: sin HTTPS la cookie no puede ser Secure
uv run uvicorn orquidea.web.app:app --reload
```

y abre <http://127.0.0.1:8000>. La base se crea en `data/orquidea.sqlite3` (ignorada por git).
Requisitos: [uv](https://docs.astral.sh/uv/) instalado.

## Development

Quality gates. **Run `./scripts/check` before every commit.** Nothing enforces
it — a red check will not stop a commit — so run it yourself while working:

```bash
./scripts/check              # lint · format · types · unit tests (seconds)
```

The gates above do not run a single test. A task's RED step does, so this project's
way to run one lives here too — not a gate, just the command the loop needs:

```bash
uv run pytest tests/test_modulo.py::test_nombre
```

Everything else about how work is organized (branches, commit format, where
artifacts land) is in **Conventions** below.

## Despliegue con Dokploy

La aplicación se despliega en un VPS con [Dokploy](https://dokploy.com) (Debian 13) construyendo el `Dockerfile` del repositorio. Un solo proceso (`uvicorn`) sirve la aplicación en el puerto 8000 y `/salud` responde 200 cuando está viva. Dokploy termina el HTTPS.

1. Con el código publicado en GitHub, crea en Dokploy una **Application** cuyo proveedor sea ese repositorio y la rama `main`.
2. En **Build Type** elige **Dockerfile** (ruta `Dockerfile`, contexto `.`).
3. En **Domains** añade tu dominio, puerto `8000`, y activa HTTPS con Let's Encrypt.
4. Despliega y comprueba `https://tu-dominio/salud` (debe responder `{"estado":"ok"}`) y `https://tu-dominio/especies`.

La colección vive en un archivo SQLite y las fotos en archivos junto a él: **monta un volumen en `/data`** (la imagen guarda ahí la base, `ORQUIDEA_DB=/data/orquidea.sqlite3`, y las fotos en `/data/fotos`); sin volumen, un redespliegue pierde las dos cosas. En Dokploy, añade un **Volume** al servicio con ruta de montaje `/data`. Un volumen con nombre hereda el propietario de la imagen (el usuario `app`, uid 10001); si montas una carpeta del servidor, dale ese propietario (`chown 10001 carpeta`): la aplicación crea `fotos/` al arrancar y **no arranca** si no puede escribir ahí, con un mensaje que nombra la ruta. Las migraciones del esquema se aplican solas al arrancar una versión nueva sobre el mismo volumen.

**Respalda `/data` completo**: la base y las fotos van juntas; una foto sin su fila queda huérfana en el disco y una fila sin su foto se ve como un ejemplar sin foto. Si defines `ORQUIDEA_FOTOS`, apúntala a una ruta dentro de un volumen.

Antes del primer despliegue, en **Environment** define `ORQUIDEA_PASSWORD_HASH` con el hash de tu contraseña (ver [Configuración](#configuración)). Sin él **nadie puede iniciar sesión**: la aplicación falla cerrada. El catálogo viaja dentro de la imagen. Los nombres de las opciones pueden variar según la versión de Dokploy. El `Dockerfile` no se ha construido todavía en una máquina con Docker: si el primer build falla, el error indicará qué ajustar.

## Fotos

Cada ejemplar admite una foto JPEG, PNG o WebP de hasta 10 MB. Al subirla se reduce a 1600 px de ancho, se guarda sin metadatos (sin EXIF y, por tanto, sin la ubicación GPS con que la tomó el teléfono) y se genera una miniatura de 192 px para las listas; el original no se conserva. Las fotos solo se entregan con la sesión iniciada.

Si pones un proxy o balanceador delante de la aplicación, debe permitir cuerpos de petición de al menos 11 MiB (con nginx, `client_max_body_size 11m`); la aplicación responde 413 a lo que pase de ahí, y un proxy con un límite menor cortaría la subida antes.

Para medir cuánto transfiere la primera carga de "Mi colección" con miniaturas (el presupuesto es de 200 KB, sin contar las fotos a tamaño completo):

```bash
uv run python scripts/medir-primera-carga.py                 # 25 fotos de ejemplo con detalle
uv run python scripts/medir-primera-carga.py ~/fotos/*.jpg   # con tus fotos reales
```

Sale con código 1 si pasa del presupuesto. Con fotos de ejemplo es una estimación; la medición con el perfil "Slow 3G" de las herramientas del navegador y tus fotos reales es la que vale.

## Historial de cuidados

Cada ejemplar guarda su historial de **riegos** (una fecha) y de **floraciones** (fecha de inicio y, si ya terminó, de fin). La ficha del ejemplar muestra los dos historiales, del más reciente al más antiguo, y la fecha del último riego; "Mi colección" muestra el último riego de cada planta. Las fechas son días de calendario en formato AAAA-MM-DD, sin hora ni zona; no pueden ser posteriores a hoy, y "hoy" es el del servidor en UTC (al oeste de UTC, durante unas horas se acepta el día siguiente). Un fin no puede ser anterior al inicio y una floración terminada no se reabre: para corregir un registro se quita y se vuelve a agregar.

Cada ejemplar admite hasta 500 riegos y 500 floraciones; el registro 501 se rechaza con un mensaje. El tope acota el peso de la ficha. El historial vive en la misma base SQLite que la colección, así que el respaldo de `/data` ya lo incluye y quitar un ejemplar borra su historial.

El script de medición también mide la primera carga de la ficha con 50 riegos y 50 floraciones y con el tope (500 y 500), y sale con código 1 si alguna pasa del presupuesto de 200 KB; una prueba del gate lo vigila:

```bash
uv run python scripts/medir-primera-carga.py
```

El presupuesto se cuenta en gzip, como lo serviría un proxy: la ficha con el tope pesa unos 500 KB sin comprimir y unos 14 KB en gzip. **La aplicación no comprime sus respuestas**: comprueba que el proxy de tu despliegue comprima el HTML (no está verificado en Dokploy). La medición con el perfil "Slow 3G" de las herramientas del navegador y tus datos reales sigue siendo la que vale.

## Configuración

Todo se configura por variables de entorno; ninguna vive en el repositorio ni en la imagen.

| Variable | Obligatoria | Qué hace |
|----------|:-----------:|----------|
| `ORQUIDEA_PASSWORD_HASH` | sí | Hash scrypt de la contraseña del único usuario. Sin ella (o con un valor inválido) nadie puede entrar. |
| `ORQUIDEA_DB` | no | Ruta del archivo SQLite. En la imagen es `/data/orquidea.sqlite3` (el volumen); en local, `data/orquidea.sqlite3`. |
| `ORQUIDEA_FOTOS` | no | Directorio donde se guardan las fotos de los ejemplares. Por defecto, `fotos/` junto al archivo de la base (en la imagen, dentro del volumen `/data`). |
| `ORQUIDEA_COOKIE_SEGURA` | no | La cookie de sesión es `Secure` (solo viaja por HTTPS) y se emite la cabecera HSTS. Poner `0` **solo en desarrollo local** sin HTTPS; en el VPS, Dokploy termina el HTTPS y no debe tocarse. |

Para generar el hash de la contraseña (no la guardes en ningún archivo; el hash sí puede ir en el entorno):

```bash
uv run python -m orquidea.autenticacion
```

Imprime una línea con el formato `scrypt$N$r$p$sal$hash`; pégala como valor de `ORQUIDEA_PASSWORD_HASH`. Para cambiar la contraseña, genera otro hash, cámbialo en el entorno y reinicia: no hay recuperación por correo. Las sesiones duran 12 horas como máximo y 30 minutos sin actividad; cinco intentos fallidos seguidos bloquean el acceso cinco minutos.

## Structure

| Path | What lives here |
|------|-----------------|
| `src/orquidea/` | El código de la aplicación: `catalogo/` y `coleccion/` (dominio), `autenticacion.py` (contraseña e intentos), `datos/` (SQLite con migraciones, sesiones, ejemplares, fotos y los JSON del catálogo) y `web/` (la aplicación, la sesión, un router por área en `rutas/` y las plantillas) |
| `tests/` | Pruebas unitarias |
| `scripts/` | Gate entry points (see Development) y `medir-primera-carga.py` (ver Fotos) |
| `Dockerfile` | Imagen para desplegar en Dokploy (ver Despliegue con Dokploy) |
| `governance/` | Vision, requirements, guardrails, architecture (see below) |
| `conventions/` | Bindings de esta instancia (autonomía, notificaciones, seguridad) |
| `work/` | Work in progress — one directory per epic / story / bug / spike |
| `records/decisions/` | ADRs — the decisions and their rationale |
| `records/parking-lot.md` | Hallazgos nombrados y aplazados |

## Governance

The durable answers live here, one question per document:

| Document | Answers |
|----------|---------|
| `governance/vision.md` | Why this exists, and the outcomes it aims for |
| `governance/PRD.md` | What it must do (`RF-XX` requirements) |
| `governance/guardrails.md` | The quality bars, and how each is verified |
| `governance/architecture/system-context.md` | External actors and interfaces |
| `governance/architecture/system-design.md` | Internal layers and modules |

## Conventions

This project follows the gemba method — commits, branches, work items
and gates are defined in
`CLAUDE.md` at the repo root; not repeated here.
