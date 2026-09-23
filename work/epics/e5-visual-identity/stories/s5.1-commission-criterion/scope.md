# Story s5.1: Commission criterion — Scope

## User story

Como coleccionista que usa Orquídea en el teléfono y decide cómo se ve,
quiero que el criterio contra el que se juzgará toda la identidad visual quede escrito, con sus comprobaciones medibles vistas fallar, antes de que exista cualquier color, tipo o token,
para que cada pieza de e5 se juzgue contra algo que ya estaba ahí y no contra una justificación armada después.

## Acceptance criteria

```gherkin
@stated
Given el encargo aprobado el 2026-09-22 (perímetro: concept, color, typography y ui; logo fuera)
When se abre el registro del encargo
Then ADR-009 queda commiteado en `proposed` con el catálogo de supervivencia resuelto una vez y los tres criterios de adecuación con su estrato, antes de cualquier pieza

@stated
Given el criterio 1 (recursos de la identidad ≤ 50 KB gzip, `mechanical`)
When su comprobación corre sobre un sujeto que lo viola
Then sale en rojo nombrando el peso y el tope, y ese rojo queda escrito en ADR-009 antes de producir

@stated
Given el criterio 2 (texto de lectura corrida ≥ 7:1 contra su fondo, `mechanical`)
When su comprobación corre sobre un par que lo viola
Then sale en rojo nombrando el par y su razón, y ese rojo queda escrito en ADR-009 antes de producir

@stated
Given el criterio 3 (la foto del ejemplar es la protagonista, `judgement`)
When se llega al paso del contraejemplo
Then se responde "no aplica: no hay oráculo", con su razón, sin inventar una comprobación

@deduced
Given una comprobación sin nada que medir (ningún recurso de identidad, ningún par)
When corre
Then sale en rojo por población vacía, distinguible del rojo del criterio, y nunca en verde

@deduced
Given el entregable `commission.md` escrito y la mitad juzgada firmada por el humano o escrita `unsigned`
When se completa el registro
Then el mismo ADR-009 pasa a `accepted`, mismo archivo y mismo número
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| Un recurso de identidad de 60 KB que no comprime (p. ej., una fuente) | correr la comprobación del criterio 1 | rojo: el peso medido > 51 200 bytes, con la población contada (1 recurso) |
| El par `#767676` sobre `#ffffff` (4.54:1, pasa AA) | correr la comprobación del criterio 2 | rojo: 4.54:1 < 7:1, con el par nombrado |
| Ningún recurso de identidad en `/static` | correr la comprobación del criterio 1 | rojo por población vacía, no un verde |

## In scope

- ADR-009 abierto en `proposed` y commiteado antes de todo lo demás, en la forma de rejilla de la convención del ciclo.
- Las dos comprobaciones medibles, escritas con TDD en el proyecto (la de peso, extendiendo `scripts/medir-primera-carga.py`; la de contraste ≥ 7:1, propia del proyecto porque el instrumento del addon fija 4.5:1), cada una contando su población.
- El rojo de cada una sobre un sujeto que viola su criterio, escrito en ADR-009 y commiteado antes de `commission.md`.
- `governance/identity/commission.md` desde la plantilla de la técnica, con lo medido y lo juzgado separados.
- ADR-009 completado a `accepted`.

## Out of scope

- Cualquier color, tipo, token o CSS — s5.2 a s5.7.
- Conectar la comprobación de peso al gate (`./scripts/check`) sobre los recursos reales — s5.7, cuando existan; hoy no hay población.
- Correr la comprobación de contraste sobre la paleta — s5.3 y s5.5.
- El concepto y sus propios criterios — s5.2.

## Done when

- [stated] `git log` muestra el commit de ADR-009 en `proposed` con fecha de autor anterior a la de `commission.md` y a la de cualquier pieza.
- [stated] ADR-009 registra el rojo de los criterios 1 y 2 sobre sujetos que los violan, y el criterio 3 como "no aplica: no hay oráculo".
- [deduced] Las dos comprobaciones tienen pruebas en `./scripts/check`, incluida la de población vacía; `./scripts/check` en verde.
- [deduced] `commission.md` existe en `governance/identity/` con `decision: ADR-009`, y ADR-009 está en `accepted`.
- [stated] La mitad juzgada lleva el nombre del humano y la fecha, o está escrita `unsigned` y contada como sin responder.

## Notes

- Criterios aprobados por el humano el 2026-09-22, en esta sesión: perímetro (logo fuera), catálogo resuelto y las tres adecuaciones tal como se propusieron.
- Diseño de la épica: `../../design.md` (hallazgos sobre `medir-primera-carga.py`, la CSP y el umbral fijo de `contrast.py`).
- Convenciones que gobiernan: `cycle`, `survival-criteria`, `commission` y `deliverables` de gemba-design 0.21.0; técnica `commission`.
