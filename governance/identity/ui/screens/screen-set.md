---
type: screen-set
commission: "Las pantallas de la interfaz web de Orquídea, derivadas de su inventario"
derived-from: "governance/identity/ui/screens/inventory.md, read-at c9a8ea1"
decision: ADR-017
date: 2026-09-24
---

# Orquídea — Screen set

## The criterion this answers

No se repite aquí: vive en `ADR-017`, abierto antes de que existiera cualquier pantalla de abajo. Esta sección nombra el registro y nada más.

## The rule

La regla A de ADR-017, la del catálogo de dimensiones (`screen-set`):

- cada objeto que no vive dentro de otro tiene su lista y su detalle;
- un objeto con `Within` no tiene pantalla propia y es una sección del detalle del objeto que nombra;
- una tarea tiene una pantalla de paso por cada acción suya que pide un formulario propio o una confirmación, es decir, cuando no basta un control dentro de la lista o del detalle de su objeto;
- toda pantalla existente que nada de lo anterior deriva se conserva (`existing`).

## The parameters

| Parameter | Value | Stratum | Alternatives it beat, and why each lost |
|-----------|-------|---------|------------------------------------------|
| objetos con lista y detalle | O1 Especie y O3 Ejemplar, los que no viven dentro de otro | `judgement` | todos los objetos con lista y detalle (sin `Within`): el dueño confirmó que Cuidado, Riego, Floración y Foto viven dentro de su padre, como hoy |
| objetos que viven dentro de otro | O2 en O1; O4, O5 y O6 en O3 | `judgement` | Riego y Floración con lista propia: el dueño la descartó en la confirmación del inventario |
| tareas con pantalla de paso | las acciones que piden formulario propio o confirmación: A3 (T3), A4 y A5 (T4) | `judgement` | ninguna pantalla de paso, con los formularios dentro de la lista y de la ficha: 6 pantallas, y tres de hoy (P5, P7, P8) se fundirían; el dueño eligió conservarlas |

## The screens

| Id | Screen | Derived from | By | Exists in code |
|----|--------|--------------|----|----------------|
| S1 | Especies, con la búsqueda | O1 | list | P2 |
| S2 | Ficha de especie, con sus cuidados | O1, O2 | detail | P3 |
| S3 | Mi colección | O3 | list | P4 |
| S4 | Ficha del ejemplar, con foto, riegos y floraciones | O3, O4, O5, O6 | detail | P6 |
| S5 | Nuevo ejemplar sin especie | T3 | step | P5 |
| S6 | Editar ejemplar | T4 | step | P7 |
| S7 | Confirmar la baja de un ejemplar | T4 | step | P8 |
| S8 | Inicio | P1 | existing | P1 |
| S9 | Acceso | P9 | existing | P9 |

**Screens measured:** 9, each derived from an entry the inventory has: `inventory-sources: OK (34 entries: 34 read, all found at c9a8ea1; 0 declared, with who and when; 9 screens, each derived from an entry)`, exit 0.

## How it answers the survival criteria

| Criterion | How this answers it |
|-----------|---------------------|
| `platform-specs` | not applicable, because no se entrega marca ni ícono de plataforma |
| `minimum-size` | not applicable, because un conjunto de pantallas no tiene texto dibujado |
| `single-ink` | not applicable, because no hay marca |
| `contrast` | not applicable, because no hay texto sobre un fondo |
| `prior-art` | not applicable, because no se registra ni se entrega marca |
| `component-contrast` | not applicable, because no hay componentes dibujados |
| `target-size` | not applicable, because no hay controles |
| `provenance` | not applicable, because no hay valores de escala; el papel lo cumple que cada pantalla nombre sus entradas (F2) |
| `focus-visible` | not applicable, because no hay controles |

## How it answers the fitness criteria

| Criterion, as approved | From | Stratum | How this answers it |
|------------------------|------|----------|----------|
| F2 — cada pantalla nombra entradas del inventario, y todas existen en él | this link | `mechanical` | sí: 9 pantallas, exit 0; la guarda de ADR-017 (más de cero pantallas contadas) se cumple |
| F4 — el conjunto cubre todas las tareas declaradas | this link | `judgement` | sí: T1 y T2 en S1 y S2 (agregar es un control de S2), T3 en S5, T4 en S6 y S7, T5 a T7 como secciones de S4; firmado abajo |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| si la regla fue la correcta: las pantallas que deriva y la aplicación no muestra (ninguna) y las que la aplicación muestra y la regla no deriva (ninguna; Inicio y Acceso se conservan como `existing`) | sí, la regla A con pantallas de paso | Daniel Efraín Domínguez Urbina, 2026-09-24 |
| si el conjunto cubre todas las tareas declaradas (F4) | sí | Daniel Efraín Domínguez Urbina, 2026-09-24 |

Observación, sin decisión pendiente: "Mi colección" (S3) la deriva la lista del objeto Ejemplar, no una tarea. Ninguna de las siete tareas es "revisar cómo va mi colección", aunque la visión la pone como resultado ("Colección al día"). El dueño decidió no agregarla (2026-09-24). La regla C la perdía justo por eso.

## What was tried and rejected

- **A sin pantallas de paso:** 6 pantallas. El alta sin especie entra en Mi colección, y la edición y la baja en la ficha del ejemplar. Pantallas: Especies (O1, list, P2); Ficha de especie (O1, O2, detail, P3); Mi colección con el alta sin especie (O3, list, P4); Ficha del ejemplar con edición, baja, foto, riegos y floraciones (O3, O4, O5, O6, detail, P6); Inicio (P1, existing); Acceso (P9, existing). F2: `6 screens`, exit 0. Perdió porque fundiría tres pantallas que hoy existen, y el dueño eligió conservarlas.
- **B, solo las existentes:** las mismas 9 pantallas, cada una derivada de su propia `P` (`existing`). F2: `9 screens`, exit 0. Perdió porque no deriva nada: no dice por qué existe cada pantalla ni si cubre una tarea, así que solo sirve como control.
- **C, solo por tarea:** 13 pantallas, una por acción de cada tarea: buscar (T1, T2, P2), leer cuidados (T1, P3), agregar el ejemplar de la especie (T2), agregar sin especie (T3, P5), editar (T4, P7), quitar (T4, P8), poner o cambiar la foto (T5), quitar la foto (T5), registrar un riego (T6), quitar un riego (T6), registrar una floración (T7), terminarla (T7) y quitarla (T7). F2: `13 screens`, exit 0. Perdió porque no deriva Mi colección, Inicio ni Acceso, y convierte en siete páginas lo que hoy son secciones de la ficha del ejemplar.
