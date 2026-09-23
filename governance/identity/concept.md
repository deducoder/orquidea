---
type: concept
commission: "La identidad visual de la interfaz web de Orquídea: paleta, tipografía y la interfaz derivada de ellas"
decision: ADR-010
date: 2026-09-22
---

# Orquídea — La dirección, y contra qué se eligió

## The criterion this answers

No se repite aquí: vive en `ADR-010`, abierto y commiteado antes de desarrollar ninguna dirección. Esta sección nombra el registro y nada más.

## How many directions, declared before any existed

**3**, declarado el 2026-09-22, antes de desarrollar la primera.

## The criteria this selection was made against

| # | Criterion | Stratum | From |
|---|-----------|---------|------|
| S1 | Deja la foto del ejemplar como lo único saturado de la pantalla: su firma vive en fondos, tinta y estructura, no en color de marca | `judgement` | commission 3 |
| S2 | Conserva su carácter con texto a ≥ 7:1 y con fuentes del sistema o una sola familia ligera: no depende de medios tonos, de texturas en imagen ni de una fuente de exhibición | `judgement` | commission 1 y 2 |
| S3 | Es una herramienta de registro y consulta pensada primero para el teléfono: toma de las redes la foto a todo el ancho en tarjetas, la navegación al alcance del pulgar y las acciones frecuentes grandes y cerca de su contenido; no toma métricas, seguidores, "me gusta" ni scroll infinito | `judgement` | esta selección (humano, 2026-09-22) |

## The directions considered

| Direction | What it bets on | Where it loses |
|-----------|-----------------|----------------|
| Cuaderno de campo | La libreta del naturalista: hoja clara, tinta casi negra, renglones y fechas de bitácora; cada ejemplar es una hoja con su foto a todo el ancho | — |
| Lámina de herbario | La hoja de herbario de museo: papel crema, etiqueta de colecta recuadrada, serif clásica para los binomios | S2, y S3 en parte |
| Vivero | La app de jardinería amable: verde hoja de marca, esquinas redondeadas, botones píldora | S1 |

## The one chosen

**Cuaderno de campo**, contra los criterios S1, S2 y S3 de esta selección.

**Why the others lost**, one line each, each naming the criterion:

- **Lámina de herbario** — falla S2: su carácter depende de una serif clásica con itálica y versalitas reales, que es una fuente web que compite por los 50 KB, y del tono sepia de papel viejo, que empuja el texto hacia medios tonos; y cumple S3 solo en parte: la etiqueta recuadrada es una forma de escritorio que en el teléfono se vuelve una columna densa.
- **Vivero** — falla S1: su verde de marca saturado compite en la misma tarjeta con los verdes de la planta y con los amarillos y magentas de las flores.

## What was measured, and what was judged

- **Measured:** nada. S1, S2 y S3 son juicio y no tienen oráculo (ADR-010, contraejemplos).
- **Judged:** las respuestas de cada dirección a cada criterio, propuestas por el agente en la rejilla de ADR-010; y la selección misma, en elección forzada entre las tres, por **Daniel Efraín Domínguez Urbina**, el 2026-09-22.

## What this direction does not decide

La paleta, las familias, los tamaños y los espacios: los producen s5.3 a s5.6 contra sus propios criterios, derivados de este y de ADR-009, no por regla a partir de esta dirección. Lo que queda fijado para ellos es la apuesta:

- **Color:** neutros cálidos de papel, una tinta casi negra y un solo acento de tinta oscuro reservado para acciones y enlaces; la foto es el único color vivo.
- **Tipo:** una sans (del sistema o una sola familia ligera) para la interfaz, cifras tabulares para las fechas, itálica verdadera para los nombres científicos; la estructura (renglones, márgenes, etiquetas pequeñas) hace el trabajo que en otras direcciones haría el color.
- **Teléfono:** cada ejemplar como una hoja con su foto a todo el ancho, navegación principal al alcance del pulgar, acciones frecuentes grandes y al pie de su contenido. Ningún flujo nuevo.
