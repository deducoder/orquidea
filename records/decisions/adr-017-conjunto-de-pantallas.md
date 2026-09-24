---
type: adr
id: ADR-017
title: "El conjunto de pantallas de Orquídea, derivado de su inventario"
status: proposed
date: 2026-09-24
epic: —
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-017: El conjunto de pantallas de Orquídea, derivado de su inventario

## Status

Proposed.

## Context

**La pregunta:** ¿con qué regla se derivan las pantallas de la interfaz web de Orquídea a partir de su inventario (objetos, acciones, pantallas existentes y tareas), leído del código y confirmado por el dueño?

Historia s2, standalone, con la técnica `screens` de gemba-design 0.24.0. Esta vuelta corre dos eslabones de la cadena: **inventario** y **conjunto de pantallas**. La guía de prioridad, el patrón y la composición quedan fuera; cada uno abrirá su propio criterio cuando exista el conjunto.

Este registro se abre y se commitea **antes de leer la primera entrada del inventario**. El diseño de la historia recorre el código después, y ese recorrido es la lectura del inventario. Por eso el registro va antes que el diseño y no como primera tarea del plan, como en s1.

La dimensión que decide este registro es `screen-set` del catálogo de interfaz (`conventional`, `derived`). Su regla de referencia es la A de abajo.

### Criterios de supervivencia, aplicados

Ninguno tiene sujeto en un inventario ni en un conjunto de pantallas: todavía no se dibuja nada.

| Criterio | Cómo responde |
|---|---|
| `platform-specs` | no aplica: no se entrega marca ni ícono de plataforma |
| `minimum-size` | no aplica: un inventario y un conjunto no tienen texto dibujado |
| `single-ink` | no aplica: no hay marca |
| `contrast` | no aplica: todavía no hay texto sobre un fondo |
| `prior-art` | no aplica: no se registra ni se entrega marca |
| `component-contrast` | no aplica: todavía no hay componentes dibujados |
| `target-size` | no aplica: todavía no hay controles |
| `provenance` | no aplica: estos eslabones no producen valores de escala; lo que cumple ese papel aquí es la cita de cada entrada (criterio 1) |
| `focus-visible` | no aplica: todavía no hay controles |

### Criterios de fitness, aprobados

Aprobados por Daniel Efraín Domínguez Urbina el 2026-09-24. Ninguno viene de ADR-009: los criterios 1 y 2 de ese encargo se miden en la composición y el 3 en la guía de prioridad. Los cuatro son propios de estos eslabones.

| # | Criterio | Eslabón | Estrato | Qué lo decide |
|---|---|---|---|---|
| F1 | Cada entrada del inventario cita un `archivo:línea` que existe en su `read-at`, o dice `declared — quién, fecha` | inventario | `mechanical` | `inventory-sources.py` (cláusulas S1, S2, S4) |
| F2 | Cada pantalla del conjunto nombra entradas del inventario, y todas existen en él | conjunto | `mechanical` | `inventory-sources.py` con el conjunto (cláusula S3) |
| F3 | El inventario confirmado es el producto del que trata el encargo, y cada entrada quitada dice por qué | inventario | `judgement` | la firma del dueño después de leer las cuatro tablas |
| F4 | El conjunto cubre todas las tareas declaradas: ninguna se queda sin las pantallas de sus pasos | conjunto | `judgement` | leer lado a lado las tareas y las pantallas, más las que la regla deriva y la aplicación no muestra, y al revés |

### Las reglas en juego

| Regla | Operación | Parámetros |
|---|---|---|
| **A** — catálogo (ORCA) | por cada objeto que no vive dentro de otro, su lista y su detalle; el que tiene `Within`, como sección del detalle de su padre; por cada tarea, sus pasos; cada pantalla existente que nada deriva, conservada (`existing`) | qué objetos llevan lista y detalle; qué objetos viven dentro de otro; qué tareas llevan pantallas de pasos |
| **B** — solo las existentes | una pantalla por cada pantalla existente del inventario, y nada más; es el control: lo que la aplicación ya muestra | ninguno |
| **C** — solo por tarea | una pantalla por cada paso de cada tarea declarada; sin listas ni detalles por objeto | qué tareas se declaran y en cuántos pasos |

### La rejilla

Lo que una regla produce no puede medirse hasta que corre: esas celdas quedan `pending: measured when run`, como hueco declarado, y se llenan corriendo la regla, nunca cambiando un criterio o un parámetro.

| Criterio | Estrato | A | B | C |
|---|---|---|---|---|
| F1 — cita o declaración en cada entrada | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| F2 — cada pantalla nombra entradas existentes | `mechanical` | pending: measured when run | pending: measured when run | pending: measured when run |
| F3 — el inventario es el producto | `judgement` | común a las tres: el inventario es el mismo | común | común |
| F4 — cubre todas las tareas | `judgement` | pending: measured when run | pending: measured when run | pending: measured when run |

### El rojo de los criterios medibles

Se escribe aquí antes de producir: F1 y F2, con `inventory-sources.py` sobre un sujeto que los viola.

Sondas en el scratchpad de la sesión, con `read-at: "50e5a26"` (el commit de este registro) y `--repo` en este repositorio. Ninguna lee una entrada real: las citas son a propósito inexistentes y el resto se declara como `sonda`.

- **F1, rojo:** un objeto que cita `src/orquidea/web/app.py:99999` y otro sin fuente.
  ```
  S1 FAIL: O1 cites src/orquidea/web/app.py:99999 — the file has 83 lines at 50e5a26
  S2 FAIL: O2 has no source, and is not `declared — {who}, {YYYY-MM-DD}`
  ```
  exit 1. Control: el mismo inventario con el objeto declarado da `OK (4 entries: 0 read, all found at 50e5a26; 4 declared, with who and when)`, exit 0; un inventario sin filas da `no entry to check — an empty inventory is not a verified one — no verdict`, exit 2.
- **F2, rojo:** una pantalla que deriva de `O9` y otra que dice existir como `P7`; ninguna de las dos está en el inventario.
  ```
  S3 FAIL: S1 derives from O9, which the inventory does not have
  S3 FAIL: S2 exists in code as P7, which the inventory does not have
  ```
  exit 1. Control: una pantalla que deriva de `O1` y existe como `P1` da `… 1 screens, each derived from an entry`, exit 0.
- **Guarda de F2, por un hueco del instrumento:** un conjunto sin filas, o con la tabla bajo otro encabezado que `## The screens`, sale `OK (… 0 screens, each derived from an entry)` con exit 0, no con 2. Visto en las sondas: la primera versión de la de F2 usaba `###` y salió verde. Por eso F2 se da por cumplido solo si la salida cuenta **más de cero pantallas**. Si el conteo es cero, no hay veredicto.

## Decision

Sin resolver.

## Consequences

Sin resolver.

## Alternatives considered

Sin resolver: las reglas B y C de arriba son las candidatas.
