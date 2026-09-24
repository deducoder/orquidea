# Story s2: Derive screens from inventory — Design

Registro: ADR-017, en `proposed` desde `50e5a26`, con su rojo en `e3c1be3`, antes de este recorrido.

## 1 · What & why

**Problema:** las pantallas de Orquídea salieron historia por historia (e1 a e4), cada una de la ruta que su requisito necesitaba. Nadie ha comprobado que el conjunto cubra lo que el usuario hace, ni que cada objeto del dominio tenga dónde verse.

**Valor:** un inventario con cita y un conjunto de pantallas derivado por una regla declarada. Las pantallas que la regla deriva y la aplicación no muestra, y las que la aplicación muestra sin que nada las derive, quedan a la vista como insumo de historias futuras. Además, es la entrada de los tres eslabones siguientes: guía, patrón y composición.

## 2 · Approach

Dos entregables en `governance/identity/ui/screens/` (la ruta la fija la convención de entregables de gemba-design): `inventory.md` y `screen-set.md`, con las plantillas de la técnica. Ningún código de la aplicación cambia.

### Lo que se leyó (recorrido)

- **Modelos:** `catalogo/modelo.py` (`Especie`, `Cuidados`, `Cuidado`) y `coleccion/modelo.py` (`Ejemplar`, `Riego`, `Floracion`, y `foto` como campo del ejemplar). `datos/sesiones.py` (`Sesion`) es infraestructura del acceso.
- **Rutas:** 25 decoradores en `web/app.py` y `web/rutas/*.py`. Nueve `GET` dibujan una plantilla: son las pantallas existentes. Tres `GET` sirven otra cosa: `/salud` y las dos de la imagen de la foto. El resto son `POST`, o sea acciones.
- **Plantillas:** la ficha del ejemplar (`ejemplar_ficha.html`) ya lleva foto, riegos y floraciones como secciones (`<section>` con `<h2>`). Los riegos y las floraciones no tienen pantalla propia, y los cuidados viven en la ficha de especie.
- **Tareas:** el código no las nombra. El PRD las describe como requisitos (RF-02 a RF-08, `governance/PRD.md`). Se proponen citando esas líneas, y el dueño las confirma, cambia o declara.

### Decisiones que toma el dueño, no el agente

- Qué objetos viven dentro de otro (`Within`). Candidatos: `Cuidado` en `Especie`; `Riego`, `Floracion` y la foto en `Ejemplar`.
- Qué se quita en la confirmación, con razón. Candidato: `Sesion`, que no es un objeto de la interfaz.
- Las tareas y sus acciones.

### Componentes afectados

- Crear: `governance/identity/ui/screens/inventory.md` y `screen-set.md`.
- Modificar: ADR-017 (rejilla, decisión y `accepted`).
- Legacy sweep: nada queda huérfano; es nuevo.

### Gobierno

- `must-test-001` (TDD): esta historia no escribe código. Su "prueba que falla primero" es el rojo de F1 y F2 con `inventory-sources.py`, visto y escrito en ADR-017 antes de producir.
- Convención de entregables de gemba-design: la raíz es `governance/identity/`, y las pantallas van en `ui/screens/`.

## 3 · Interface / examples

### Usage

```sh
S=~/.claude/plugins/cache/gemba/gemba-design/0.24.0/skills/techniques/screens/scripts
python3 $S/inventory-sources.py --repo . governance/identity/ui/screens/inventory.md
python3 $S/inventory-sources.py --repo . governance/identity/ui/screens/inventory.md governance/identity/ui/screens/screen-set.md
```

### Expected output (success + error)

```
# verde
inventory-sources: OK (N entries: R read, all found at {read-at}; D declared, with who and when; K screens, each derived from an entry)   # exit 0, con K > 0 (guarda de F2)
# rojo del criterio (visto en ADR-017)
S1 FAIL: O1 cites src/orquidea/web/app.py:99999 — the file has 83 lines at 50e5a26                                                         # exit 1
# sin veredicto
inventory-sources: no entry to check — an empty inventory is not a verified one — no verdict                                              # exit 2
```

### Key data structures

Una fila del inventario, tal como la lee el instrumento:

```
| O3 | Ejemplar | — | src/orquidea/coleccion/modelo.py:10 |
| A11 | registrar riego | O4 | src/orquidea/web/rutas/cuidados.py:17 |
| T5 | registrar un riego | A5, A6, A11 | governance/PRD.md:36 |
```

## 4 · Acceptance criteria

### Deduced criteria

- **Rojo de F1 y F2 escrito en ADR-017 antes de producir:** confirmado. Ya está en `e3c1be3`.
- **ADR-017 `accepted`, mismo archivo y mismo número:** confirmado.
- **`./scripts/check` verde:** confirmado. Los entregables son `.md`, y ruff formatea `.md` (memoria del proyecto), así que se corre antes de cada commit.

### Scenarios (delta over the scope)

```gherkin
@deduced
Given el conjunto de pantallas escrito
When corre inventory-sources.py
Then la salida cuenta más de cero pantallas; con cero no hay veredicto aunque salga exit 0 (guarda de F2)
```

- **MUST:** `read-at` es un commit que existe y contiene cada archivo citado.
- **MUST:** cada tarea cita una línea del PRD o dice `declared — Daniel Efraín Domínguez Urbina, {fecha}`.
- **MUST:** las reglas B y C también corren sobre el mismo inventario confirmado, y sus pantallas van a *What was tried and rejected* o a la rejilla, para que la elección no sea una primera idea.
- **MUST NOT:** completar el inventario por el dueño. Lo que el código no dice, se pregunta.
- **MUST NOT:** tocar rutas o plantillas.
