# Story s2.1: SQLite persistence with migrations — Retrospective

Estimated: S · Actual: S

## Summary

`orquidea.datos.base` abre la base SQLite y aplica, en orden y cada una en su transacción, las migraciones `NNNN-nombre.sql` mayores que `PRAGMA user_version`; la ruta sale de `ORQUIDEA_DB` (por defecto `data/orquidea.sqlite3`), las claves foráneas quedan activas y el journal en WAL. La carpeta `datos/migraciones/` existe vacía y `.gitignore` ignora `data/` y los archivos `-wal`/`-shm`. Dos commits de tarea (`feat(datos)`), 11 pruebas nuevas.

## Finalize (reportado por story-implement)

- **Gate:** `./scripts/check` en verde (63 pruebas: 52 previas + 11 nuevas, ruff, ruff format, mypy strict).
- **Orphaned-test check:** `base.py` es un módulo nuevo que nadie más importa; ningún archivo de prueba no tocado depende de lo que la historia cambió. Limpio.
- **Acceptance:** los seis escenarios del scope y los dos del diseño (carpeta inexistente, hueco de numeración) tienen prueba; los siete criterios `[deduced]` que el diseño confirmó se cumplen. La prueba manual (T3) con la ruta por entorno, dos aperturas y una migración añadida después dio `user_version` 1, 1, 2, WAL y ambas tablas, verificado desde otro proceso.
- **Plan con `> Pause: none`:** sin aprobación humana por tarea; el despacho se decidió en `decisions.md`.
- **Tiempo de implementación:** sin tracker; derivable de la rama (`git log --author-date`), no registrado.

## Reviews

- **quality-review:** sin críticos. Observación: si la carpeta de migraciones no existe, `glob` devuelve vacío y la base queda sin esquema hasta que una consulta falle con "no such table"; con la carpeta del paquete presente no ocurre y el fallo sería ruidoso. Se deja sin abrir: el riesgo real es un empaquetado sin la carpeta, que s2.7 y la prueba manual del despliegue cubren.
- **security-review:** PASS WITH FINDINGS, solo B101 (17, severidad baja) en `tests/test_datos_base.py`, ya estacionado en `records/parking-lot.md` (Bandit reporta B101 en `tests/`). `src/orquidea/datos/base.py` salió limpio. Guardrails: ninguno de seguridad aplica a esta historia (`should-security-002` empieza en s2.2); el único SQL interpolado lleva un entero derivado de un nombre validado con `^\d{4}-`.

## What went well

- Las mutaciones (sin bytecode) mostraron que el `ROLLBACK` explícito era redundante: `abrir_base` cierra la conexión y SQLite descarta la transacción abierta. Se quitó y se dejó un comentario. La mutación real de atomicidad (ejecutar sin `BEGIN`) sí la mata cuatro pruebas.
- Probar la atomicidad desde una segunda conexión (`sqlite3.connect(ruta)`) en lugar de la que falló evitó una prueba que pasa en vacío.

## What to improve

- Una de mis mutaciones ("línea vacía") era equivalente y sobrevivió sin significar nada: antes de lanzar una mutación, comprobar que cambia el comportamiento.
- `ruff format` reformateó `design.md` (ruff formatea `.md`), lo que costó un commit `style`; escribir los artefactos ya formateados o correr el formato antes del commit de la fase.

## Learned

1. About the system: `executescript` hace `COMMIT` antes de ejecutar; con `isolation_level=None` y `BEGIN`/`COMMIT` dentro del script la migración y la versión avanzan juntas o no avanzan, y `PRAGMA user_version` es transaccional.
2. About the process: comprobar que una mutación no es equivalente antes de contarla como superviviente.
3. Capability gained: base migrada y tipada lista para las tablas de sesiones (s2.2) y ejemplares (s2.4).
