# Story s5.5: Interface color roles — Scope

## User story

Como coleccionista que usa Orquídea en el teléfono, en campo,
quiero que cada color de la interfaz (fondo de botón, borde de campo, foco, error) salga de la paleta por una regla declarada, con su contraste medido en los valores reales,
para que la interfaz se siga leyendo bajo el sol y un cambio futuro de color se haga en la regla y se vuelva a derivar, no a mano.

## Acceptance criteria

```gherkin
@stated
Given ADR-012 (paleta) en `accepted`
When se abre el registro de los roles de color
Then un ADR nuevo queda commiteado en `proposed` con los criterios de los dos eslabones (primitivas y roles semánticos) y las reglas candidatas con sus parámetros, antes de producir ningún valor

@stated
Given los criterios propuestos
When el humano no los ha aprobado
Then no se produce ninguna rampa ni ningún rol

@stated
Given una regla candidata que deja un par de texto bajo 7:1 o un par de componente bajo el umbral de `component-contrast`
When corre la comprobación de contraste
Then se ve en rojo nombrando el par, antes de elegir la regla

@stated
Given las primitivas y los roles semánticos producidos
When corre la comprobación de contraste sobre sus pares
Then sale con 0 pares bajo el umbral y cuenta una población distinta de cero

@stated
Given la paleta declara que no tiene variante
When se comprueba la relación de invariancia
Then el entregable dice que la relación no se comparó, nunca que pasó

@deduced
Given un rol de la paleta aproximado por un escalón de rampa
When se escriben los roles semánticos
Then cada rol de la paleta lleva junto a sí el valor de la paleta, el de la primitiva a la que resolvió y la diferencia; o se declara fijado a su valor exacto

@deduced
Given un rol semántico
When se lee su valor
Then es una referencia a un escalón de rampa, nunca un literal

@stated
Given la regla elegida
When se escribe la mitad juzgada
Then lleva el nombre del humano y la fecha, o `unsigned`
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `semantics.md` con los roles elegidos | `uv run python scripts/contraste-de-lectura.py governance/identity/semantics.md` | `N par(es) de texto juzgado(s), 0 bajo el umbral`, exit 0 |
| una regla candidata cuyo rol `texto secundario` cae a 5:1 sobre `hoja` | ídem sobre la tabla de la candidata | exit 1, nombrando el par |
| `palette.md` sin variante declarada | `invariance.py` sobre la tabla | sin sujeto; el entregable lo reporta como no comparado |

## In scope

- Criterios de los dos eslabones aprobados antes de producir valores; ADR en `proposed` → `accepted`.
- Eslabón de primitivas: rampas por una regla con espacio de color, curva y pasos declarados, y el escalón que toma cada rol de la paleta.
- Eslabón de roles semánticos: roles por función (los de la paleta y los que no trae, como foco o fondo de botón) como referencias a escalones, con contraste de texto y de componente medido.
- `governance/identity/primitives.md` y `governance/identity/semantics.md`, según las plantillas de la técnica `ui`.
- `survival-review` sobre lo producido.

## Out of scope

- Escala tipográfica, espaciado, componentes y `DESIGN.md` — s5.6.
- CSS y plantillas — s5.7.
- Tema oscuro u otra variante — rabbit hole del brief; por eso la invariancia no se compara.
- Cambiar la paleta: un rol que falle en su valor exacto fijado es rojo de la identidad y vuelve a ADR-012 con un ADR nuevo, no se parcha aquí.

## Done when

- [stated] El ADR de los roles de color en `proposed` antes de cualquier rampa en el repositorio; los rojos de los criterios medibles escritos en él antes de `primitives.md`.
- [stated] La comprobación de contraste sobre los pares de `semantics.md` sale con 0 y su población no es cero, con texto a ≥ 7:1 y componentes al umbral de `component-contrast`.
- [stated] La relación de invariancia reportada como no comparada.
- [deduced] Cada valor de `primitives.md` se reproduce corriendo la regla otra vez; cada parámetro nombra las alternativas que venció.
- [stated] La mitad juzgada firmada o `unsigned`; el ADR en `accepted`; `./scripts/check` en verde.

## Notes

- Deriva de ADR-012 (paleta, sin variante), ADR-011 (todo texto a 16 px: ningún texto es "grande") y ADR-009 (criterio 2, texto ≥ 7:1).
- Técnica `ui` de gemba-design 0.21.0, eslabones *colour primitives* y *semantic roles*; instrumentos `contrast.py` e `invariance.py` de `survival-review`, invocados por su ruta.
- `scripts/contraste-de-lectura.py` del proyecto (s5.1) aplica el 7:1; el umbral de `component-contrast` se lee del catálogo el día que se mide.
