---
type: adr
id: ADR-018
title: "La guía de prioridad de las pantallas de objeto de Orquídea"
status: accepted
date: 2026-09-24
epic: —
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-018: La guía de prioridad de las pantallas de objeto de Orquídea

## Status

Accepted, 2026-09-24.

## Context

**La pregunta:** ¿qué lleva cada una de las cuatro pantallas de objeto de Orquídea y en qué orden? Son S1 Especies, S2 Ficha de especie, S3 Mi colección y S4 Ficha del ejemplar, del conjunto de ADR-017.

Historia s3, standalone, con el tercer eslabón de la técnica `screens` de gemba-design 0.24.0. Entrada: `governance/identity/ui/screens/inventory.md` (`read-at` `c9a8ea1`) y `screen-set.md`. La dimensión es `content-priority` (`taste`, `declared`): ninguna regla produce el orden; el agente lo propone desde las tareas y el dueño lo decide y lo firma. Un rango dice qué lleva la pantalla, nunca dónde va ni de qué tamaño.

Este registro se abre y se commitea antes de escribir el primer rango. Las opciones llevan sus órdenes completos desde ahora, no solo su nombre: en s2, el valor de un parámetro se fijó después de ver las salidas, y eso no se repite.

### Criterios de supervivencia, aplicados

| Criterio | Cómo responde |
|---|---|
| `platform-specs` | no aplica: no se entrega marca ni ícono de plataforma |
| `minimum-size` | no aplica: una guía no tiene texto dibujado |
| `single-ink` | no aplica: no hay marca |
| `contrast` | no aplica: todavía no hay texto sobre un fondo |
| `prior-art` | no aplica: no se registra ni se entrega marca |
| `component-contrast` | no aplica: todavía no hay componentes dibujados |
| `target-size` | no aplica: todavía no hay controles |
| `provenance` | no aplica: no hay valores de escala |
| `focus-visible` | no aplica: todavía no hay controles |

### Criterios de fitness, aprobados

Aprobados por Daniel Efraín Domínguez Urbina el 2026-09-24.

| # | Criterio | De dónde | Estrato | Qué lo decide |
|---|---|---|---|---|
| G1 | Cada rango nombra una pantalla del conjunto y una o más tareas del inventario, los rangos corren desde 1 sin huecos y `signed-by` lleva nombre y fecha o dice `unsigned` | de este eslabón | `mechanical` | `inventory-sources.py` con la guía como tercer archivo (cláusula S5) |
| G2 | Cada tarea del inventario queda servida por al menos un rango de alguna pantalla guiada | de este eslabón | `mechanical` | el comando de abajo |
| G3 | En S3 y S4, la foto del ejemplar va antes que los datos de registro (riegos, floraciones) | criterio 3 de ADR-009 ("la foto del ejemplar es la protagonista"), llevado del color al orden | `judgement` | el dueño lee los rangos de S3 y S4 |
| G4 | El orden sirve a las tareas que nombra; registrar un riego en campo (T6) es el caso que decide | de este eslabón, motivado por "Usable en campo" (`governance/vision.md`) | `judgement` | la firma del dueño después de leer la guía completa |

**El comando de G2.** `inventory-sources.py` no lo revisa. Sale 0 si todas las tareas están servidas, 1 si falta alguna (y la nombra) y 2 si no hay tareas o no hay rangos que juzgar:

```sh
python3 - INVENTORY.md GUIDE.md <<'EOF'
import re, sys
ID = re.compile(r'^[A-Z]+\d+$')
def rows(path, heading):
    out, inside = [], False
    for line in open(path, encoding='utf-8'):
        if line.strip() == heading:
            inside = True
            continue
        if inside and line.startswith('#'):
            break
        if inside and line.startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if ID.match(cells[0]):
                out.append(cells)
    return out
tasks = {r[0] for r in rows(sys.argv[1], '### Tasks')}
ranks = rows(sys.argv[2], '## The guide')
if not tasks or not ranks:
    print(f'serves: no subject — {len(tasks)} tasks, {len(ranks)} ranks — no verdict')
    sys.exit(2)
served = {t.strip() for r in ranks for t in r[3].split(',')}
missing = sorted(tasks - served)
for t in missing:
    print(f'G2 FAIL: {t} is served by no rank')
print(f'serves: {len(tasks)} tasks, {len(ranks)} ranks, {len(tasks) - len(missing)} served')
sys.exit(1 if missing else 0)
EOF
```

### Las opciones

**Común a las tres, S1 y S2**, porque no las toca G3 y las decide G4:

| Pantalla | Rango | Contenido | Sirve |
|---|---|---|---|
| S1 | 1 | la búsqueda por nombre científico o común | T1, T2 |
| S1 | 2 | las especies que coinciden, por nombre científico | T1, T2 |
| S2 | 1 | el nombre científico y los nombres comunes | T1, T2 |
| S2 | 2 | los cuidados (luz, riego, temperatura y sustrato), cada uno con su fuente | T1 |
| S2 | 3 | agregar a mi colección | T2 |
| S2 | 4 | la descripción | T1 |
| S2 | 5 | las fuentes de la especie | T1 |

**S3, Mi colección** (cada tarjeta, y después lo que va fuera de ellas):

| Rango | A — foto primero | B — cuidado primero | C — identidad primero |
|---|---|---|---|
| 1 | la miniatura de la foto (T5) | el nombre y la especie (T4, T6, T7) | el nombre y la especie (T4, T6, T7) |
| 2 | el nombre y la especie (T4, T6, T7) | el último riego (T6) | la miniatura de la foto (T5) |
| 3 | el último riego (T6) | la miniatura de la foto (T5) | editar y quitar (T4) |
| 4 | editar y quitar (T4) | editar y quitar (T4) | el último riego (T6) |
| 5 | agregar una planta que no está en el catálogo (T3) | agregar una planta que no está en el catálogo (T3) | agregar una planta que no está en el catálogo (T3) |

**S4, Ficha del ejemplar:**

| Rango | A — foto primero | B — cuidado primero | C — identidad primero (el orden de la plantilla de hoy) |
|---|---|---|---|
| 1 | la foto (T5) | el nombre y la especie, con su ficha (T1, T6, T7) | el nombre y la especie, con su ficha (T1, T6, T7) |
| 2 | el nombre y la especie, con su ficha (T1, T6, T7) | el último riego y registrar un riego (T6) | las notas (T4) |
| 3 | el último riego y registrar un riego (T6) | las floraciones: registrar, terminar y su historial (T7) | la foto, con cambiarla o quitarla (T5) |
| 4 | el historial de riegos, con quitar (T6) | la foto (T5) | el último riego y registrar un riego (T6) |
| 5 | las floraciones: registrar, terminar y su historial (T7) | el historial de riegos, con quitar (T6) | el historial de riegos, con quitar (T6) |
| 6 | cambiar o quitar la foto (T5) | cambiar o quitar la foto (T5) | las floraciones: registrar, terminar y su historial (T7) |
| 7 | las notas (T4) | las notas (T4) | editar y quitar el ejemplar (T4) |
| 8 | editar y quitar el ejemplar (T4) | editar y quitar el ejemplar (T4) | — |

### La rejilla

| Criterio | Estrato | A | B | C |
|---|---|---|---|---|
| G1 — rangos válidos, sin huecos, firma | `mechanical` | sí — `4 of 9 screens guided, signed by Daniel Efraín Domínguez Urbina, 2026-09-24`, exit 0 | sí — `4 of 9 screens guided, unsigned`, exit 0 | sí — `4 of 9 screens guided, unsigned`, exit 0 |
| G2 — cada tarea servida | `mechanical` | sí — `7 tasks, 20 ranks, 7 served`, exit 0 | sí — `7 tasks, 20 ranks, 7 served`, exit 0 | sí — `7 tasks, 19 ranks, 7 served`, exit 0 |
| G3 — foto antes que los registros en S3 y S4 | `judgement` | sí — Daniel Efraín Domínguez Urbina, 2026-09-24 | a la lectura, no: en S3 el último riego (2) va antes que la miniatura (3), y en S4 la foto (4) va después de riegos y floraciones; no juzgado: el dueño eligió A | a la lectura, sí en las dos (S3: miniatura 2 y riego 4; S4: foto 3 y riego 4); no juzgado: el dueño eligió A |
| G4 — sirve a las tareas; T6 en campo decide | `judgement` | sí — Daniel Efraín Domínguez Urbina, 2026-09-24 | no juzgado: el dueño eligió A | no juzgado: el dueño eligió A |

### El rojo de los criterios medibles

Sondas en el scratchpad de la sesión, contra el inventario y el conjunto reales. El comando de G2 se extrajo con `awk` de este mismo archivo, así que lo que corrió es lo que está escrito arriba.

- **G1, rojo:** una firma sin fecha, un rango que sirve a `T9` y los rangos 1 y 3 de S1.
  ```
  S5 FAIL: `signed-by` is `Daniel` — a guide is signed `{who}, {YYYY-MM-DD}` or `unsigned`
  S5 FAIL: S1 rank 3 serves T9, which the inventory does not have as a task
  S5 FAIL: S1 ranks are 1, 3 — a guide ranks from 1 with no gap
  ```
  exit 1. Control: una guía válida da `OK (… 3 of 9 screens guided, signed by …)`, exit 0. Una guía sin filas da `no row in the guide — an empty guide is not a checked one — no verdict`, exit 2.
- **G2, rojo:** una guía válida para G1 en la que ningún rango sirve a T6.
  ```
  G2 FAIL: T6 is served by no rank
  serves: 7 tasks, 4 ranks, 6 served
  ```
  exit 1. Control: la misma guía con un rango que sirve a T6 da `serves: 7 tasks, 5 ranks, 7 served`, exit 0. Una guía sin filas da `serves: no subject — 7 tasks, 0 ranks — no verdict`, exit 2.

## Decision

**La opción A, foto primero, en S3 y S4, con S1 y S2 comunes.** La eligió y firmó Daniel Efraín Domínguez Urbina el 2026-09-24. Está escrita en `governance/identity/ui/screens/priority-guide.md`: 20 rangos en 4 pantallas.

La entrada del parking lot "la ficha repite fuentes largas por cada cuidado" no se promueve aquí: la guía dice qué lleva S2 y no cómo se cita la fuente. Decisión del dueño, en la misma fecha.

## Consequences

- La ficha del ejemplar de hoy sigue la opción C: nombre, notas, foto, riegos, floraciones. La guía pide foto, nombre, registrar un riego, historial, floraciones, cambiar la foto, notas y editar o quitar. La plantilla cambia en la composición, no aquí.
- En Mi colección, hoy la miniatura ya va primero, pero editar y quitar van antes que las notas, y "Agregado el" no está en la guía porque no sirve a ninguna tarea. La composición decide si se queda.
- La composición de S1 a S4 ya tiene su rango 1 firmado, que es la pregunta "¿qué es lo más importante aquí?" de la `survival-review` de una página.
- S5 a S9 no tienen guía: cuando se compongan, primero necesitan una.

## Alternatives considered

- **B, cuidado primero:** registrar un riego en el rango 2 de S4. A la lectura no cumple G3, porque la foto va después de los registros en S3 y S4.
- **C, identidad primero (el orden de hoy):** a la lectura cumple G3, pero pone las notas antes que la foto y registrar un riego en el rango 4 de S4. El dueño eligió A.

Las dos, rango por rango, están arriba y en *What was tried and rejected* de la guía.
