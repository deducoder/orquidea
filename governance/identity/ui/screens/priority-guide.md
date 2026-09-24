---
type: priority-guide
commission: "Las pantallas de la interfaz web de Orquídea, derivadas de su inventario"
derived-from: "governance/identity/ui/screens/screen-set.md y governance/identity/ui/screens/inventory.md (read-at c9a8ea1)"
decision: ADR-018
date: 2026-09-24
signed-by: "Daniel Efraín Domínguez Urbina, 2026-09-24"
---

# Orquídea — Priority guide

## The criterion this answers

No se repite aquí: vive en `ADR-018`, abierto antes de escribir cualquier rango de abajo. Esta sección nombra el registro y nada más.

## The rule

Ninguna regla que un tercero pudiera aplicar produce este orden. El agente lo propuso a partir de las tareas del inventario, en tres opciones completas commiteadas en ADR-018 antes del primer rango. El dueño eligió la opción A y la firmó.

Lo que pone un contenido por encima de otro en este encargo:

- en S3 y S4, la foto del ejemplar va primero (G3, del criterio 3 de ADR-009);
- después, lo que identifica al ejemplar;
- después, registrar un riego (T6, el caso de campo que decide G4), antes que el resto de los registros;
- lo que corrige o quita va al final.

En S1 y S2, comunes a las tres opciones, el orden sigue a T1 y T2: encontrar la especie, leer sus cuidados y agregarla.

## The guide

| Screen | Rank | Content | Serves |
|--------|------|---------|--------|
| S1 | 1 | la búsqueda por nombre científico o común | T1, T2 |
| S1 | 2 | las especies que coinciden, por nombre científico | T1, T2 |
| S2 | 1 | el nombre científico y los nombres comunes | T1, T2 |
| S2 | 2 | los cuidados (luz, riego, temperatura y sustrato), cada uno con su fuente | T1 |
| S2 | 3 | agregar a mi colección | T2 |
| S2 | 4 | la descripción | T1 |
| S2 | 5 | las fuentes de la especie | T1 |
| S3 | 1 | la miniatura de la foto | T5 |
| S3 | 2 | el nombre y la especie | T4, T6, T7 |
| S3 | 3 | el último riego | T6 |
| S3 | 4 | editar y quitar | T4 |
| S3 | 5 | agregar una planta que no está en el catálogo | T3 |
| S4 | 1 | la foto | T5 |
| S4 | 2 | el nombre y la especie, con su ficha | T1, T6, T7 |
| S4 | 3 | el último riego y registrar un riego | T6 |
| S4 | 4 | el historial de riegos, con quitar | T6 |
| S4 | 5 | las floraciones: registrar, terminar y su historial | T7 |
| S4 | 6 | cambiar o quitar la foto | T5 |
| S4 | 7 | las notas | T4 |
| S4 | 8 | editar y quitar el ejemplar | T4 |

**Screens guided:** 4 de 9 (S1 a S4). S5 a S9 quedan sin guía por alcance de s3.

## The signature

El orden de arriba es `taste`: nada lo mide, y vale porque lo firmó quien lo encarga, Daniel Efraín Domínguez Urbina, el 2026-09-24 (`signed-by`).

## How it answers the survival criteria

| Criterion | How this answers it |
|-----------|---------------------|
| `platform-specs` | not applicable, because no se entrega marca ni ícono de plataforma |
| `minimum-size` | not applicable, because una guía no tiene texto dibujado |
| `single-ink` | not applicable, because no hay marca |
| `contrast` | not applicable, because no hay texto sobre un fondo |
| `prior-art` | not applicable, because no se registra ni se entrega marca |
| `component-contrast` | not applicable, because no hay componentes dibujados |
| `target-size` | not applicable, because no hay controles |
| `provenance` | not applicable, because no hay valores de escala |
| `focus-visible` | not applicable, because no hay controles |

## How it answers the fitness criteria

| Criterion, as approved | From | Stratum | How this answers it |
|------------------------|------|----------|----------|
| G1 — rangos que nombran pantallas y tareas existentes, sin huecos, con firma fechada | this link | `mechanical` | ver ADR-018, la rejilla: `inventory-sources.py` con la guía |
| G2 — cada tarea servida por al menos un rango | this link | `mechanical` | ver ADR-018, la rejilla: el comando de G2 |
| G3 — en S3 y S4, la foto antes que los registros | commission 3 (ADR-009) | `judgement` | sí: la miniatura es el rango 1 de S3, y la foto el rango 1 de S4 |
| G4 — el orden sirve a las tareas; T6 en campo decide | this link | `judgement` | sí: registrar un riego es el rango 3 de S4, después de la foto y del nombre, y antes que cualquier otro registro |

## What was judged, and by whom

Arriba está todo lo medido: que cada rango nombra una pantalla y una tarea que existen, sin huecos. Lo que sigue lo **decidió** una persona, y se puede discutir.

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| la opción de S3 y S4 | A, foto primero | Daniel Efraín Domínguez Urbina, 2026-09-24 |
| G3: la foto antes que los registros en S3 y S4 | sí | Daniel Efraín Domínguez Urbina, 2026-09-24 |
| G4: el orden sirve a las tareas que nombra, con T6 en campo como caso que decide | sí | Daniel Efraín Domínguez Urbina, 2026-09-24 |
| si la entrada del parking lot "la ficha repite fuentes largas" se promueve aquí | no: la guía dice qué lleva S2, no cómo se cita la fuente; se decide al componer S2 | Daniel Efraín Domínguez Urbina, 2026-09-24 |

## What was tried and rejected

Copiadas de ADR-018 sin cambios. S1 y S2 son comunes a las tres opciones.

**B — cuidado primero.** A la lectura no cumple G3: la foto va después de los registros.

| Screen | Rank | Content | Serves |
|---|---|---|---|
| S3 | 1 | el nombre y la especie | T4, T6, T7 |
| S3 | 2 | el último riego | T6 |
| S3 | 3 | la miniatura de la foto | T5 |
| S3 | 4 | editar y quitar | T4 |
| S3 | 5 | agregar una planta que no está en el catálogo | T3 |
| S4 | 1 | el nombre y la especie, con su ficha | T1, T6, T7 |
| S4 | 2 | el último riego y registrar un riego | T6 |
| S4 | 3 | las floraciones: registrar, terminar y su historial | T7 |
| S4 | 4 | la foto | T5 |
| S4 | 5 | el historial de riegos, con quitar | T6 |
| S4 | 6 | cambiar o quitar la foto | T5 |
| S4 | 7 | las notas | T4 |
| S4 | 8 | editar y quitar el ejemplar | T4 |

**C — identidad primero (el orden de hoy en S4).** A la lectura cumple G3. En S4 pone las notas antes que la foto y registrar un riego en el rango 4. El dueño eligió A sobre ella.

| Screen | Rank | Content | Serves |
|---|---|---|---|
| S3 | 1 | el nombre y la especie | T4, T6, T7 |
| S3 | 2 | la miniatura de la foto | T5 |
| S3 | 3 | editar y quitar | T4 |
| S3 | 4 | el último riego | T6 |
| S3 | 5 | agregar una planta que no está en el catálogo | T3 |
| S4 | 1 | el nombre y la especie, con su ficha | T1, T6, T7 |
| S4 | 2 | las notas | T4 |
| S4 | 3 | la foto, con cambiarla o quitarla | T5 |
| S4 | 4 | el último riego y registrar un riego | T6 |
| S4 | 5 | el historial de riegos, con quitar | T6 |
| S4 | 6 | las floraciones: registrar, terminar y su historial | T7 |
| S4 | 7 | editar y quitar el ejemplar | T4 |
