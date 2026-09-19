---
type: adr
id: ADR-003
title: "La colección se guarda con sqlite3 de la biblioteca estándar y migraciones numeradas propias"
status: accepted
date: 2026-09-19
epic: e2
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-003: La colección se guarda con sqlite3 de la biblioteca estándar y migraciones numeradas propias

## Status

Accepted

## Context

e2 introduce la primera persistencia de la aplicación: los ejemplares (RF-04) y las sesiones del único usuario (RF-08). ADR-001 fijó SQLite y difirió a la primera historia que lo necesite la pieza de acceso y de migraciones. Otras épicas dependen de esta elección: el seguimiento de riegos y floraciones (RF-06, RF-07) y las fotos (RF-05) añadirán tablas a la misma base.

Fuerzas:

- **Un solo usuario y un solo proceso** (RF-08, ADR-001): no hay concurrencia de escritura que justifique una capa de abstracción.
- **Tipado estricto** (`must-quality-003`): lo que devuelve la capa de datos debe ser tipado sin stubs de terceros.
- **Pocas tablas y pocas consultas** en 0.1.0 (ejemplares y sesiones): un ORM sería más código que las consultas mismas.
- **Los datos son del usuario y viven en el disco del VPS**: el esquema evoluciona en producción, así que las migraciones son indispensables desde la primera tabla.
- **El catálogo no entra en la base**: sigue en JSON (ADR-002). Un ejemplar guarda el `id` de la especie, sin clave foránea a una tabla.

Opciones:

- **(A) `sqlite3` de la biblioteca estándar con SQL escrito a mano; migraciones como scripts SQL numerados, aplicados en orden y registrados en `PRAGMA user_version`.** Sin dependencias nuevas; el SQL es explícito; las filas se convierten a modelos pydantic o dataclasses tipados en el borde.
- **(B) SQLAlchemy (o SQLModel) con Alembic.** ORM y migraciones maduras. Tres dependencias grandes para dos tablas; los tipos de SQLAlchemy exigen su plugin de mypy y más configuración; el peso en la imagen crece sin beneficio para un solo usuario.
- **(C) Un ORM ligero (peewee, sqlmodel sin Alembic).** Menos peso que B, pero aún una dependencia con su propia forma de migrar y de tipar; ninguna ventaja clara sobre el SQL directo con este volumen.

## Decision

**Opción (A):**

1. El acceso a datos usa `sqlite3` de la biblioteca estándar, con consultas parametrizadas siempre (nunca SQL armado con texto del usuario), en un módulo de la capa de datos.
2. Las migraciones son archivos SQL numerados (`0001-….sql`, `0002-….sql`) dentro del paquete; al abrir la base se aplican, en orden y cada una en su transacción, las que sean mayores que `PRAGMA user_version`, y el número se actualiza al terminar cada una. Una migración ya aplicada nunca se edita: un cambio es otra migración.
3. La ruta del archivo de base de datos sale de la variable de entorno `ORQUIDEA_DB`, con un valor por defecto para desarrollo; en producción apunta a un volumen persistente.
4. Las claves foráneas se activan en cada conexión (`PRAGMA foreign_keys = ON`) y el modo de journal es WAL.
5. El `id` de especie de un ejemplar es un texto sin clave foránea: el catálogo vive fuera de la base. Que el `id` exista en el catálogo lo valida el dominio al guardar, no la base.

## Consequences

**Positive:**
- Sin dependencias nuevas; la imagen no crece.
- El SQL se lee tal cual se ejecuta y se prueba con una base en memoria.
- Las tablas de 0.2 (riegos, floraciones, fotos) entran como migraciones nuevas sin rediseñar nada.

**Negative / costs:**
- Convertir filas a objetos tipados es código propio, repetitivo en cada tabla.
- No hay migraciones cuesta abajo (revertir); un error en producción se corrige con una migración hacia adelante.
- El mecanismo de migración es propio y hay que probarlo (orden, idempotencia, fallo a mitad); si el esquema crece mucho, reevaluar (B) con un ADR que lo sustituya.
- Un ejemplar cuyo `id` de especie desaparezca del catálogo queda huérfano; el dominio debe mostrarlo sin romperse.

## Alternatives considered

- **(B) SQLAlchemy/SQLModel + Alembic:** tres dependencias y configuración de tipos para dos tablas; contradice la ligereza que ADR-001 eligió sobre Django.
- **(C) ORM ligero:** una dependencia con su propia forma de migrar y de tipar, sin ventaja frente al SQL directo con este volumen.
