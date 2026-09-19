---
type: adr
id: ADR-008
title: "Riegos y floraciones en dos tablas, con fechas de calendario en texto ISO"
status: accepted
date: 2026-09-19
epic: e4
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-008: Riegos y floraciones en dos tablas, con fechas de calendario en texto ISO

## Status

Accepted.

## Context

RF-06 y RF-07 piden un historial por ejemplar: riegos (una fecha) y floraciones (fecha de inicio y, opcional, de fin). Hasta hoy la base guarda instantes como enteros (`ejemplares.creado`, segundos Unix) y ADR-003 fija `sqlite3` con migraciones propias, sin ORM.

Fuerzas:

- **Lo que registra el coleccionista es un día, no un instante.** "Regué el sábado" no tiene hora ni zona; un entero en UTC movería el día según la zona del servidor.
- **El brief acota**: basta con riegos y floraciones; un modelo genérico de eventos que anticipe la fertilización es un rabbit hole, y la fertilización está aparcada por decisión del humano.
- **Las dos cosas tienen forma distinta**: el riego es una fecha; la floración es un intervalo abierto (sin fin mientras dura).
- **La baja de un ejemplar debe llevarse su historial** (`PRAGMA foreign_keys = ON` ya está en `conectar`).

Opciones:

- **(A) Una tabla `cuidados` con `tipo`, `inicio`, `fin`.** Un solo lugar, pero el riego arrastra una columna `fin` que nunca usa y el `CHECK` de cada tipo se vuelve condicional; es el modelo genérico que el brief descarta.
- **(B) Dos tablas, `riegos(fecha)` y `floraciones(inicio, fin)`, con `ejemplar_id` como clave foránea `ON DELETE CASCADE`.**
- **(C) Fechas como enteros (segundos Unix) por coherencia con `creado`.** Coherente, pero el día depende de la zona con que se convierta.

## Decision

Opción (B), con las fechas guardadas como texto `AAAA-MM-DD` (fecha de calendario, sin hora ni zona), que ordena igual alfabética y cronológicamente y que `datetime.date.fromisoformat` valida. Cada tabla lleva `id INTEGER PRIMARY KEY`, `ejemplar_id` con `ON DELETE CASCADE` e índice por `(ejemplar_id, fecha)`; `floraciones` lleva un `CHECK (fin IS NULL OR fin >= inicio)`. Las migraciones son `0004` (riegos) y `0005` (floraciones): cada una entra con la historia que la usa.

## Consequences

**Positive:**
- El día que el usuario elige es el que se guarda y se muestra, en cualquier zona.
- La baja del ejemplar borra su historial sin código propio.
- Cada tabla dice exactamente lo que guarda; añadir la fertilización después es una tabla más, sin tocar estas.

**Negative / costs:**
- Dos tablas y dos módulos de acceso con un parecido de forma; se acepta antes que un genérico que nadie pidió.
- Las fechas se validan en el dominio (formato y "no futura"): SQLite no impone que el texto sea una fecha, solo el `CHECK` del orden en `floraciones`.
- "Hoy" para rechazar fechas futuras es el del servidor (UTC): al oeste de UTC deja pasar el día siguiente durante unas horas; se acepta, es lo lenient.

## Alternatives considered

- **(A) Tabla única `cuidados`:** es el modelo genérico de eventos que el brief marca como rabbit hole.
- **(C) Segundos Unix:** el día registrado cambiaría con la zona de conversión.
