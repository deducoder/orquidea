# Story s2.1: SQLite persistence with migrations — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · Aplicar migraciones numeradas, en orden y atómicas

- **Files:** create `src/orquidea/datos/base.py`, `tests/test_datos_base.py`
- **TDD:** RED pruebas con `tmp_path`: dos migraciones aplican en orden y `user_version` = 2; reabrir no reaplica y conserva datos; base en versión 1 aplica solo la 2; una migración que falla a la mitad no deja la tabla ni avanza la versión y lanza `MigracionFallida` con el nombre del archivo; un hueco de numeración (0001 y 0003) lanza el error sin aplicar ninguna → GREEN `abrir_base`, `MigracionFallida`, `MIGRACIONES` → REFACTOR
- **Satisfies:** scenarios 1 a 4 del scope y el delta del hueco de numeración
- **Mold:** `src/orquidea/datos/catalogo.py` (excepción propia que nombra el archivo, todo o nada) y ADR-003
- **Verify:** cada prueba se pone en rojo con su mutación: aplicar sin ordenar por número; no filtrar por `user_version` (reaplica y falla por tabla existente); escribir `user_version` fuera de la transacción de la migración (queda avanzado tras el fallo); quitar el `ROLLBACK` (queda la tabla parcial); aceptar el hueco de numeración; luego `uv run pytest tests/test_datos_base.py` y `./scripts/check` completo (archivo nuevo)
- **Commit:** feat(datos): abrir la base SQLite y aplicar migraciones numeradas

### T2 · Ruta por `ORQUIDEA_DB`, carpeta, claves foráneas y WAL

- **Files:** modify `src/orquidea/datos/base.py`, `tests/test_datos_base.py`, `.gitignore`; create `src/orquidea/datos/migraciones/.gitkeep`
- **TDD:** RED pruebas con `monkeypatch`: con `ORQUIDEA_DB` devuelve esa ruta y sin ella `data/orquidea.sqlite3`; una ruta con carpeta inexistente se crea; `PRAGMA foreign_keys` = 1 y `journal_mode` = `wal` en una conexión nueva → GREEN `ruta_de_la_base`, `mkdir(parents=True)`, PRAGMAs → REFACTOR
- **Satisfies:** scenarios 5 y 6 del scope y el delta de la carpeta
- **Mold:** T1
- **Verify:** quitar `PRAGMA foreign_keys = ON` (rojo); no crear la carpeta (rojo: `OperationalError`); ignorar la variable de entorno (rojo); leer `ORQUIDEA_DB` vacía como ruta válida en vez de usar el defecto (rojo, con la variable puesta a `""`); luego `./scripts/check` completo
- **Commit:** feat(datos): ruta de la base por entorno, claves foráneas y WAL

### T3 · Manual integration test

- Con la base real por defecto: `ORQUIDEA_DB=$TMPDIR/o.sqlite3 uv run python -c` que abra la base con la carpeta de migraciones vacía, dos veces, y luego con una migración temporal; comprobar con `sqlite3`/`PRAGMA` fuera del proceso.
- **Verify:** `user_version` avanza solo con migraciones nuevas, el archivo se crea con su carpeta, `git status` no muestra archivos de base (ignorados) y `./scripts/check` está en verde.

## Order & risks

- **Execution order:** T1 → T2 → T3 — la atomicidad de las migraciones es lo que puede fallar en silencio; la ruta y los PRAGMAs son triviales.
- **Dependencies:** secuenciales, acíclicas.
- **Risks:** `executescript` hace `COMMIT` implícito antes de ejecutar → se envuelve el script con su propio `BEGIN`/`COMMIT` y la conexión en `isolation_level=None`; las pruebas de fallo a mitad lo demuestran. Bandit puede marcar el SQL interpolado del `user_version` (B608) → el número es un entero derivado de un nombre validado; si marca, se documenta con `# nosec` y su razón.
