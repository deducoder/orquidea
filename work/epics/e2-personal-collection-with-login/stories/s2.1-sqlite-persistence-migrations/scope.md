# Story s2.1: SQLite persistence with migrations — Scope

## User story

As a desarrollador de la aplicación,
I want un módulo de datos que abra la base SQLite y aplique migraciones numeradas en orden,
so that las sesiones y los ejemplares de e2 (y las tablas de 0.2) tengan dónde guardarse y el esquema pueda evolucionar sin perder datos.

## Acceptance criteria

```gherkin
@stated
Given una base nueva y dos migraciones numeradas
When abro la base
Then ambas se aplican en orden y `PRAGMA user_version` queda en 2

@deduced
Given una base ya migrada a la versión 2
When la abro otra vez
Then no se vuelve a aplicar ninguna migración y los datos siguen ahí

@deduced
Given una base en la versión 1 y una migración nueva número 2
When abro la base
Then se aplica solo la 2

@deduced
Given una migración cuyo SQL falla a la mitad
When abro la base
Then esa migración no deja cambios parciales, la versión no avanza y se lanza un error que nombra el archivo

@deduced
Given la variable de entorno `ORQUIDEA_DB` con una ruta
When se pide la ruta de la base
Then se devuelve esa ruta; sin la variable, se devuelve la ruta por defecto de desarrollo

@deduced
Given una conexión recién abierta
When consulto `PRAGMA foreign_keys`
Then vale 1 y el modo de journal es WAL
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| carpeta con `0001-a.sql` (`CREATE TABLE a(x)`) y `0002-b.sql` (`CREATE TABLE b(y)`), base vacía | `abrir_base(ruta, carpeta)` | tablas `a` y `b` existen; `user_version` = 2 |
| la misma base abierta de nuevo | `abrir_base(ruta, carpeta)` | sin cambios, `user_version` = 2 |

## In scope

- Módulo de la capa de datos con la función que abre la conexión y aplica las migraciones pendientes (ADR-003).
- Carpeta de migraciones dentro del paquete, con el mecanismo de lectura de archivos `NNNN-nombre.sql`.
- Ruta de la base por `ORQUIDEA_DB`, con valor por defecto para desarrollo.
- Claves foráneas activas y journal WAL en cada conexión.

## Out of scope

- Tablas reales (sesiones en s2.2, ejemplares en s2.4) — cada historia añade su migración.
- Conectar la base a la aplicación web — la primera historia que la usa (s2.2).
- Migraciones hacia atrás — ADR-003 las descarta.

## Done when

- [deduced] Las pruebas de los criterios anteriores pasan y `./scripts/check` está en verde.
- [deduced] Ningún SQL de este módulo se arma con texto externo (ADR-003).

## Notes

Diseño del épico: `design.md`, componente `orquidea.datos.base`; ADR-003. No hay criterio `[stated]` propio más allá del que la fila de la historia declara en el scope del épico (la base y las migraciones), marcado `@stated` en el primer escenario.
