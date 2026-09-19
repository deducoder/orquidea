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

La colección vive en un archivo SQLite: **monta un volumen en `/data`** (la imagen guarda ahí la base, `ORQUIDEA_DB=/data/orquidea.sqlite3`); sin volumen, un redespliegue la pierde. En Dokploy, añade un **Volume** al servicio con ruta de montaje `/data`. Un volumen con nombre hereda el propietario de la imagen (el usuario `app`, uid 10001); si montas una carpeta del servidor, dale ese propietario (`chown 10001 carpeta`). Las migraciones del esquema se aplican solas al arrancar una versión nueva sobre el mismo volumen.

Antes del primer despliegue, en **Environment** define `ORQUIDEA_PASSWORD_HASH` con el hash de tu contraseña (ver [Configuración](#configuración)). Sin él **nadie puede iniciar sesión**: la aplicación falla cerrada. El catálogo viaja dentro de la imagen. Los nombres de las opciones pueden variar según la versión de Dokploy. El `Dockerfile` no se ha construido todavía en una máquina con Docker: si el primer build falla, el error indicará qué ajustar.

## Configuración

Todo se configura por variables de entorno; ninguna vive en el repositorio ni en la imagen.

| Variable | Obligatoria | Qué hace |
|----------|:-----------:|----------|
| `ORQUIDEA_PASSWORD_HASH` | sí | Hash scrypt de la contraseña del único usuario. Sin ella (o con un valor inválido) nadie puede entrar. |
| `ORQUIDEA_DB` | no | Ruta del archivo SQLite. En la imagen es `/data/orquidea.sqlite3` (el volumen); en local, `data/orquidea.sqlite3`. |
| `ORQUIDEA_COOKIE_SEGURA` | no | La cookie de sesión es `Secure` (solo viaja por HTTPS) y se emite la cabecera HSTS. Poner `0` **solo en desarrollo local** sin HTTPS; en el VPS, Dokploy termina el HTTPS y no debe tocarse. |

Para generar el hash de la contraseña (no la guardes en ningún archivo; el hash sí puede ir en el entorno):

```bash
uv run python -m orquidea.autenticacion
```

Imprime una línea con el formato `scrypt$N$r$p$sal$hash`; pégala como valor de `ORQUIDEA_PASSWORD_HASH`. Para cambiar la contraseña, genera otro hash, cámbialo en el entorno y reinicia: no hay recuperación por correo. Las sesiones duran 12 horas como máximo y 30 minutos sin actividad; cinco intentos fallidos seguidos bloquean el acceso cinco minutos.

## Structure

| Path | What lives here |
|------|-----------------|
| `src/orquidea/` | El código de la aplicación: `catalogo/` y `coleccion/` (dominio), `autenticacion.py` (contraseña e intentos), `datos/` (SQLite con migraciones, sesiones, ejemplares y los JSON del catálogo) y `web/` (rutas y plantillas) |
| `tests/` | Pruebas unitarias |
| `scripts/` | Gate entry points (see Development) |
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
