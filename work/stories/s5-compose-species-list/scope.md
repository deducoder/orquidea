# Story s5: Compose species list — Scope

## User story

Como dueño de Orquídea,
quiero declarar en la escala tipográfica el peso que ya fija el espécimen, y componer la pantalla Especies (S1) entre dos candidatos generados con `page.py` de gemba-design 0.24.0,
para que la primera página de la cadena `screens` salga generada, medida y elegida contra el concepto, y no escrita a mano.

## Acceptance criteria

```gherkin
@stated
Given ningún peso declarado ni ninguna fila de composición escrita
When se abre el ADR de esta historia en `proposed`
Then trae los criterios de supervivencia aplicados, W1 y K1 a K3 aprobados el 2026-09-24 con su estrato, y los candidatos A y B fila por fila, commiteado antes de producir

@stated
Given `type-scale.md` con la columna `Font weight` y `DESIGN.md` regenerado
When se genera la página de un candidato
Then `page.py` no rechaza ningún paso por `fontWeight`

@stated
Given cada candidato
When corren `page.py` y el comando de K1 del ADR
Then `page.py` sale 0 con su censo y cada texto dibujado llega a 7:1 sobre su fondo

@stated
Given los dos candidatos generados y en verde
When el dueño responde "¿qué es lo más importante aquí?" en cada uno, y después elige contra S1, S2 y S3 del concepto
Then la composición elegida lleva las respuestas con nombre y fecha, y la otra queda en *What was tried and rejected*

@deduced
Given un `DESIGN.md` sin `fontWeight`, una composición con un texto por debajo de 7:1 y otra a la que le falta un rango de la guía
When corren `page.py` y el comando de K1
Then salen en rojo por su criterio antes de producir
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `type-scale.md` sin `Font weight` | `page.py` sobre el candidato A | `refused: step-0 (used by pagina) declares no fontWeight …`, exit 1 |
| el candidato A con los pesos declarados | `page.py` | página HTML y `page: S1 (list-detail), … all ≥ 4.5:1 …`, exit 0 |

## In scope

- La columna `Font weight` de `type-scale.md`, con el valor que da `specimen.md`, y `DESIGN.md` regenerado.
- La composición de S1 con dos candidatos, generados y juzgados.
- Aparcar la falta de `img` en `page.py`.
- `survival-review` sobre la página y sobre la escala.

## Out of scope

- Componer S2, S3 y S4. S3 y S4 esperan a que el addon pueda dibujar la foto.
- Cambiar `especies.html`: la composición es el entregable, y llevarla a la plantilla es otra historia.
- Variantes `-focus` en los componentes.

## Done when

- [stated] El ADR estaba commiteado en `proposed`, con su rojo, antes del primer valor producido.
- [stated] `DESIGN.md` declara `fontWeight` en los tres pasos, y regenerado sale idéntico dos veces.
- [stated] Los dos candidatos salen de `page.py` con exit 0, y K1 da 7:1 en cada texto.
- [stated] Las dos preguntas del juicio y la del foco tienen nombre y fecha, o dicen `unsigned`.
- [deduced] El ADR queda `accepted`, en el mismo archivo y con el mismo número.
- [deduced] `./scripts/check` verde.

## Notes

- Standalone: sale por su cuenta con `integrate`.
- Criterios aprobados por el humano el 2026-09-24: W1, K1 y K2 (`mechanical`), K3 (`judgement`). Dos candidatos, A (en la página) y B (en tarjetas).
- El dueño firmó la guía (ADR-018), así que ya conoce la respuesta de la primera pregunta. Se dice en el juicio.
