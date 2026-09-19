# Story s2.1: SQLite persistence with migrations — Design

> Complexity: simple

## 1 · What & why

**Problem:** la aplicación no tiene dónde guardar nada; sesiones (s2.2) y ejemplares (s2.4) necesitan una base con un esquema que evolucione sin perder datos.
**Value:** una sola función abre la base ya migrada; cada historia posterior solo añade un archivo `NNNN-nombre.sql`, y el esquema de producción avanza sin intervención manual (ADR-003).

## 2 · Approach

Un módulo `orquidea.datos.base` con `abrir_base(ruta, migraciones)` que abre `sqlite3`, activa claves foráneas y WAL, y aplica en orden, cada una en su transacción, las migraciones `NNNN-*.sql` cuyo número sea mayor que `PRAGMA user_version`. La ruta sale de `ORQUIDEA_DB` (ADR-003).

**Components affected:**

- `src/orquidea/datos/base.py`: create — `abrir_base`, `ruta_de_la_base`, `MigracionFallida`, `MIGRACIONES` (carpeta por defecto).
- `src/orquidea/datos/migraciones/`: create — carpeta del paquete, vacía por ahora (`.gitkeep`); s2.2 pone la primera migración real.
- `.gitignore`: modify — ignorar `data/` y los archivos `-wal`/`-shm` de SQLite (la base de desarrollo por defecto vive en `data/orquidea.sqlite3`).
- `tests/test_datos_base.py`: create.

**Legacy sweep:** nada — net-new. Gobernanza: ADR-003 (sqlite3 estándar, migraciones por `user_version`, consultas parametrizadas, claves foráneas y WAL), system-design (capa de datos, sin HTTP), `must-quality-001..003` (mypy strict: la conexión se tipa como `sqlite3.Connection`). Sin dependencias nuevas. El nombre `datos/base.py` no choca con `datos/catalogo.py`.

## 3 · Interface / examples

### Usage (API / CLI)

```python
from pathlib import Path
from orquidea.datos.base import abrir_base, ruta_de_la_base

conexion = abrir_base(ruta_de_la_base())  # ORQUIDEA_DB o data/orquidea.sqlite3
conexion.execute("INSERT INTO a (x) VALUES (?)", ("uno",))  # siempre parametrizado
```

### Expected output (success + error)

```
# migraciones/0001-a.sql: CREATE TABLE a (x TEXT);   0002-b.sql: CREATE TABLE b (y TEXT);
abrir_base(tmp / "o.sqlite3", migraciones)  -> conexión; PRAGMA user_version = 2; tablas a y b
abrir_base(...) otra vez                    -> sin cambios; user_version = 2

# migraciones/0002-rota.sql: CREATE TABLE b (y TEXT); INSERT INTO no_existe VALUES (1);
abrir_base(...)                             -> MigracionFallida("0002-rota.sql: ...")
                                               user_version = 1; la tabla b no existe

ORQUIDEA_DB=/datos/o.sqlite3                -> ruta_de_la_base() == Path("/datos/o.sqlite3")
(sin ORQUIDEA_DB)                           -> Path("data/orquidea.sqlite3")
```

### Key data structures (if applicable)

```python
RUTA_POR_DEFECTO = Path("data/orquidea.sqlite3")
MIGRACIONES = Path(__file__).parent / "migraciones"


class MigracionFallida(Exception): ...


def ruta_de_la_base() -> Path: ...
def abrir_base(ruta: Path, migraciones: Path = MIGRACIONES) -> sqlite3.Connection: ...
```

Cada migración se ejecuta con `executescript` envuelta en `BEGIN; … PRAGMA user_version = N; COMMIT;` (el número se toma del nombre del archivo, que se valida con `^\d{4}-.+\.sql$`, y se inserta como entero); si falla, `ROLLBACK` y `MigracionFallida` que nombra el archivo. Las migraciones se ordenan por su número y un hueco o un duplicado de número es un error.

## 4 · Acceptance criteria

- **Must:** aplicar migraciones pendientes en orden; idempotente al reabrir; atómico por migración; ruta por `ORQUIDEA_DB` con valor por defecto; claves foráneas activas y WAL en cada conexión.
- **Should:** crear la carpeta contenedora de la base si no existe (la ruta por defecto vive en `data/`).
- **Must NOT:** editar migraciones ya aplicadas ni tener migraciones hacia atrás (ADR-003); armar SQL con texto externo; importar nada de `orquidea.web` o `orquidea.catalogo`.

### Deduced criteria

- Una base ya migrada a la versión 2 no vuelve a aplicar migraciones y conserva sus datos: confirmed
- Una base en la versión 1 aplica solo la migración 2: confirmed
- Una migración que falla a la mitad no deja cambios parciales ni avanza la versión, y el error nombra el archivo: confirmed
- `ORQUIDEA_DB` fija la ruta, con valor por defecto sin ella: confirmed
- Una conexión nueva tiene `foreign_keys = 1` y journal WAL: confirmed
- Las pruebas de los criterios pasan y `./scripts/check` está en verde: confirmed
- Ningún SQL de este módulo se arma con texto externo: confirmed — el único SQL interpolado lleva un entero derivado del nombre validado del archivo

### Scenarios (delta over the scope)

```gherkin
Given una ruta de base cuya carpeta no existe
When abro la base
Then la carpeta se crea y la base se abre migrada

Given una carpeta de migraciones con un hueco de numeración (0001 y 0003)
When abro la base
Then falla con MigracionFallida que nombra el hueco y no aplica ninguna
```
