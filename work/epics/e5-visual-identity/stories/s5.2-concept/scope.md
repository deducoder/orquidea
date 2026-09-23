# Story s5.2: Concept — Scope

## User story

Como coleccionista que decide cómo se ve Orquídea,
quiero elegir una sola dirección para toda la identidad entre un número de direcciones fijado de antemano, contra criterios escritos antes de desarrollarlas,
para que la paleta y la tipografía partan de la misma apuesta y, dentro de seis meses, siga escrito por qué cayó cada una de las otras.

## Acceptance criteria

```gherkin
@stated
Given ADR-009 en `accepted` (criterios 1, 2 y 3 del encargo)
When se abre el registro del concepto
Then un ADR nuevo queda commiteado en `proposed` con los criterios de selección (cada uno con su estrato y su origen: un criterio del encargo por su número, o propio de esta selección) y el número de direcciones declarado, antes de desarrollar cualquier dirección

@stated
Given los criterios de selección propuestos
When el humano no los ha aprobado
Then no se desarrolla ninguna dirección

@stated
Given las direcciones desarrolladas
When se elige una
Then cada dirección descartada se responde con el criterio que no cumplió, por su número, nunca con una opinión ni una calificación

@stated
Given la elección hecha
When se escribe la mitad juzgada
Then lleva el nombre del humano y la fecha, o dice `unsigned` y cuenta como sin responder

@deduced
Given un criterio de selección sin oráculo
When se llega al paso del contraejemplo
Then se responde "no aplica: no hay oráculo", con su razón

@deduced
Given `concept.md` escrito
When se completa el registro
Then el mismo ADR pasa a `accepted`, mismo archivo y mismo número
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| Tres direcciones declaradas (p. ej. "cuaderno de campo", "lámina de herbario", "vivero") | elegir contra S1–S3 | una elegida; cada una de las otras dos con "falla S{n}: {cómo}" |
| Una dirección que depende de un fondo saturado | juzgarla contra el criterio derivado del 3 del encargo | descartada: "falla S{n}: compite con el magenta de las flores" |

## In scope

- Criterios de selección (2 a 4) propuestos y aprobados por el humano antes de desarrollar nada.
- El número de direcciones, declarado y commiteado antes de desarrollar la primera.
- Un ADR abierto en `proposed` y completado a `accepted`.
- Las direcciones desarrolladas como apuestas verbales (qué persiguen, qué referencias, qué implican para color y tipo), sin valores.
- `governance/identity/concept.md` desde la plantilla de la técnica, con la elección firmada o `unsigned`.

## Out of scope

- Cualquier valor: color, familia tipográfica, tamaño o token — s5.3 a s5.6.
- Un tablero de imágenes (moodboard) con referencias ajenas: es un entregable de otro tamaño y no lo pide ningún criterio.
- Puntuaciones, rankings o calificaciones de las direcciones — la técnica las prohíbe.

## Done when

- [stated] `git log` muestra el ADR del concepto en `proposed`, con los criterios de selección y el número de direcciones, antes de que exista cualquier dirección.
- [stated] `concept.md` responde cada dirección descartada con el criterio que falló, por su número, y no contiene ninguna puntuación.
- [stated] La elección lleva el nombre del humano y la fecha, o está escrita `unsigned`.
- [deduced] El ADR está en `accepted`, mismo archivo y mismo número; `./scripts/check` en verde.

## Notes

- Deriva de ADR-009 y de `governance/identity/commission.md`.
- Técnica `concept` de gemba-design 0.21.0; convención `cycle` (pasos `fitness`, `record-open`, `counterexample`, `measured-judged`).
- Es un SHOULD de la épica: el diseño de e5 registró que no pasa la prueba de desperdicio, y se mantiene porque el humano aprobó el perímetro con él dentro.
