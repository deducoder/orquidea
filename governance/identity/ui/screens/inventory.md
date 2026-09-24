---
type: inventory
commission: "Las pantallas de la interfaz web de Orquídea, derivadas de su inventario"
read-at: "c9a8ea1"
decision: ADR-017
date: 2026-09-24
confirmed-by: "Daniel Efraín Domínguez Urbina, 2026-09-24"
---

# Orquídea — Inventory

## The criterion this answers

No se repite aquí: vive en `ADR-017`, abierto antes de leer cualquier entrada de abajo. Esta sección nombra el registro y nada más.

## The entries

Las citas se leyeron en `c9a8ea1`, relativas a la raíz del repositorio. Las acciones son las operaciones de escritura (`POST`) más una lectura con parámetro, `buscar`, porque sin ella la primera tarea no tendría acción. Las pantallas existentes son los `GET` que dibujan una plantilla. Tres `GET` sirven otra cosa y no se cuentan: `/salud` (`src/orquidea/web/app.py:81`) y la imagen de la foto y su miniatura (`src/orquidea/web/rutas/coleccion.py:223`, `:228`).

### Objects

`Within` lo propuso el agente, leído de dónde se muestra hoy cada objeto: los cuidados en la ficha de especie; los riegos, las floraciones y la foto en la ficha del ejemplar. El dueño lo confirmó tal cual el 2026-09-24.

| Id | Object | Within | Source |
|----|--------|--------|--------|
| O1 | Especie | — | src/orquidea/catalogo/modelo.py:24 |
| O2 | Cuidado | O1 | src/orquidea/catalogo/modelo.py:8 |
| O3 | Ejemplar | — | src/orquidea/coleccion/modelo.py:10 |
| O4 | Riego | O3 | src/orquidea/coleccion/modelo.py:59 |
| O5 | Floración | O3 | src/orquidea/coleccion/modelo.py:65 |
| O6 | Foto | O3 | src/orquidea/coleccion/modelo.py:16 |

### Actions

| Id | Action | Object | Source |
|----|--------|--------|--------|
| A1 | buscar especies | O1 | src/orquidea/web/rutas/catalogo.py:15 |
| A2 | agregar a la colección un ejemplar de una especie | O3 | src/orquidea/web/rutas/coleccion.py:44 |
| A3 | agregar un ejemplar sin especie de catálogo | O3 | src/orquidea/web/rutas/coleccion.py:131 |
| A4 | editar un ejemplar | O3 | src/orquidea/web/rutas/coleccion.py:246 |
| A5 | quitar un ejemplar | O3 | src/orquidea/web/rutas/coleccion.py:272 |
| A6 | subir la foto | O6 | src/orquidea/web/rutas/coleccion.py:183 |
| A7 | quitar la foto | O6 | src/orquidea/web/rutas/coleccion.py:233 |
| A8 | registrar un riego | O4 | src/orquidea/web/rutas/cuidados.py:17 |
| A9 | quitar un riego | O4 | src/orquidea/web/rutas/cuidados.py:29 |
| A10 | registrar una floración | O5 | src/orquidea/web/rutas/cuidados.py:36 |
| A11 | terminar una floración | O5 | src/orquidea/web/rutas/cuidados.py:52 |
| A12 | quitar una floración | O5 | src/orquidea/web/rutas/cuidados.py:70 |

### Existing screens

| Id | Screen | Source |
|----|--------|--------|
| P1 | Inicio | src/orquidea/web/rutas/catalogo.py:10 |
| P2 | Especies (lista y búsqueda) | src/orquidea/web/rutas/catalogo.py:15 |
| P3 | Ficha de especie | src/orquidea/web/rutas/catalogo.py:21 |
| P4 | Mi colección | src/orquidea/web/rutas/coleccion.py:37 |
| P5 | Nuevo ejemplar sin especie | src/orquidea/web/rutas/coleccion.py:126 |
| P6 | Ficha del ejemplar | src/orquidea/web/rutas/coleccion.py:178 |
| P7 | Editar ejemplar | src/orquidea/web/rutas/coleccion.py:240 |
| P8 | Confirmar la baja de un ejemplar | src/orquidea/web/rutas/coleccion.py:265 |
| P9 | Acceso | src/orquidea/web/rutas/acceso.py:37 |

### Tasks

Las propuso el agente a partir del PRD, con la cita de cada requisito, y el dueño las confirmó tal cual el 2026-09-24, salvo T8, que salió con la Sesión (abajo).

| Id | Task | Actions | Source |
|----|------|---------|--------|
| T1 | encontrar una especie y leer sus cuidados | A1 | governance/PRD.md:14 |
| T2 | agregar a mi colección un ejemplar del catálogo | A1, A2 | governance/PRD.md:25 |
| T3 | agregar una planta que no está en el catálogo | A3 | governance/PRD.md:25 |
| T4 | corregir o quitar un ejemplar | A4, A5 | governance/PRD.md:25 |
| T5 | poner, cambiar o quitar la foto de un ejemplar | A6, A7 | governance/PRD.md:31 |
| T6 | registrar un riego, o corregir uno mal anotado | A8, A9 | governance/PRD.md:36 |
| T7 | registrar una floración y, después, su fin | A10, A11, A12 | governance/PRD.md:41 |

## Removed at confirmation

| Id | Entry | Why |
|----|-------|-----|
| O7 | Sesión — `src/orquidea/datos/sesiones.py:11` | infraestructura del acceso, no es un objeto que el usuario consulte; la pantalla Acceso (P9) se conserva como existente |
| A13 | iniciar sesión — `src/orquidea/web/rutas/acceso.py:42` | actúa sobre O7, que se quitó; la hace la pantalla P9 |
| A14 | cerrar sesión — `src/orquidea/web/rutas/acceso.py:73` | actúa sobre O7, que se quitó; es un botón de la plantilla base, no una pantalla |
| T8 | entrar y salir — `governance/PRD.md:46` | sus dos acciones salieron con O7 |

**Entries measured:** 34 read, all found at `c9a8ea1`; 0 declared. 4 removed at confirmation.

## How it answers the survival criteria

| Criterion | How this answers it |
|-----------|---------------------|
| `platform-specs` | not applicable, because no se entrega marca ni ícono de plataforma |
| `minimum-size` | not applicable, because un inventario no tiene texto dibujado |
| `single-ink` | not applicable, because no hay marca |
| `contrast` | not applicable, because no hay texto sobre un fondo |
| `prior-art` | not applicable, because no se registra ni se entrega marca |
| `component-contrast` | not applicable, because no hay componentes dibujados |
| `target-size` | not applicable, because no hay controles |
| `provenance` | not applicable, because no hay valores de escala; el papel lo cumple la cita de cada entrada (F1) |
| `focus-visible` | not applicable, because no hay controles |

## How it answers the fitness criteria

| Criterion, as approved | From | Stratum | How this answers it |
|------------------------|------|----------|----------|
| F1 — cada entrada cita un `archivo:línea` que existe en `read-at`, o dice `declared — quién, fecha` | this link | `mechanical` | `inventory-sources: OK (34 entries: 34 read, all found at c9a8ea1; 0 declared, with who and when)`, exit 0 |
| F3 — el inventario confirmado es el producto, y cada entrada quitada dice por qué | this link | `judgement` | confirmado por el dueño; las cuatro quitadas dicen por qué (abajo, lo juzgado) |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| si este inventario es el producto del que trata el encargo: los `Within`, la Sesión quitada y las siete tareas | sí — confirmado en tres respuestas: `Within` como se propuso, Sesión quitada, tareas tal cual | Daniel Efraín Domínguez Urbina, 2026-09-24 |

## What was not measured

Que la lectura haya sido completa, y que cada línea citada diga lo que su entrada afirma: ningún chequeo resuelve ninguna de las dos, y lo cubre la confirmación.
