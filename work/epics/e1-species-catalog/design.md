# Epic e1: Species catalog — Design

## Gemba findings

- `src/orquidea/__init__.py` está vacío, `tests/` solo tiene `__init__.py` y `pyproject.toml` declara `dependencies = []`: no hay código que reutilizar ni duplicar; todo es nuevo.
- `scripts/check` corre ruff, ruff format, mypy strict y pytest con `uv run`; cada historia debe dejarlo en verde antes de cada commit.
- ADR-001 fija el stack (FastAPI, Jinja, htmx, SQLite, uv) y difiere a la historia que lo necesite por primera vez la elección de las piezas que FastAPI no trae. En e1 solo el esquema/validación (s1.2) y el despliegue (s1.5) caen en ese caso.
- `governance/architecture/system-design.md` fija las capas (Web, Dominio, Datos) y que el dominio no conoce HTTP ni SQL: el catálogo se implementa respetándolo.
- El catálogo de e1 no usa SQLite: se carga desde los JSON del repositorio (RF-01); la persistencia entra con e2.

## Target components

| Component | Change | Purpose |
|-----------|--------|---------|
| `src/orquidea/web/` (app, rutas, plantillas, base) | create | Aplicación FastAPI, plantilla base con htmx, rutas de inicio, lista, ficha y búsqueda (`s1.1`, `s1.3`, `s1.4`) |
| `src/orquidea/catalogo/` (modelo y búsqueda) | create | Dominio: especie y búsqueda insensible a mayúsculas y acentos, sin HTTP (`s1.2`, `s1.3`, `s1.4`) |
| `src/orquidea/datos/` (carga del catálogo) | create | Lee y valida los JSON contra el esquema; error con archivo y campo (`s1.2`) |
| `catalogo/*.json` y su esquema | create | Datos versionados de las especies y su esquema (`s1.2`, `s1.6`) |
| Configuración de despliegue | create | Lo necesario para correr en el VPS (`s1.5`) |
| `pyproject.toml` | modify | Dependencias de ejecución: FastAPI, Jinja y las que decidan s1.2 y s1.5 (`s1.1`, `s1.2`, `s1.5`) |

## Key contracts

- El catálogo se carga completo y válido o no se carga; un JSON inválido detiene la carga con un error que nombra archivo y campo (RF-01).
- Toda especie cita al menos una fuente (`must-data-001`); la ficha muestra la fuente de cada dato (RF-03).
- La búsqueda ignora mayúsculas y acentos (RF-02).
- El dominio del catálogo no importa la capa web ni SQL (system-design).
- El catálogo es de solo lectura desde la interfaz (no-go del brief).
- Primera carga ≤ 5 s en "Slow 3G" y ≤ 200 KB gzip (`must-perf-001`): un solo script (htmx) y HTML del servidor.

## Decisions (ADRs)

- Ninguno a nivel de épica. El stack está decidido en ADR-001; la elección del mecanismo de validación del esquema (s1.2) y de la forma de despliegue (s1.5) se decide dentro de esas historias, con su propio ADR si hay más de una opción razonable, como ADR-001 punto 4 lo pide.

## Legacy sweep

Nada — net-new. El `__init__.py` vacío se conserva como paquete raíz.
