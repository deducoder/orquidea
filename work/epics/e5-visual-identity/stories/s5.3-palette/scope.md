# Story s5.3: Palette — Scope

## User story

Como coleccionista que lee su colección en el teléfono bajo el sol,
quiero una paleta por roles, producida contra un criterio escrito antes del primer color, con cada par de texto medido a 7:1,
para que la tinta se lea en campo y la foto de mis plantas sea lo único con color vivo en la pantalla.

## Acceptance criteria

```gherkin
@stated
Given ADR-009, ADR-010 y ADR-011 en `accepted`
When se abre el registro de la paleta
Then un ADR nuevo queda commiteado en `proposed` con los criterios de la pieza (estrato y origen de cada uno) y las paletas candidatas, antes de fijar ningún color

@stated
Given los criterios propuestos
When el humano no los ha aprobado
Then no se fija ningún color

@stated
Given los pares de texto de cada candidata
When corre `scripts/contraste-de-lectura.py`
Then una candidata con un par bajo 7:1 se ve en rojo antes de elegir, y la elegida sale con 0 contando su población

@deduced
Given la paleta elegida
When se escribe `palette.md`
Then trae una tabla `Role | Value` y una `Foreground | Ground | Kind` legibles por `contraste-de-lectura.py` y por `tokens.py pairs`, y declara su variante (o que no declara ninguna, y que por eso la relación no se compara)

@stated
Given la elección hecha
When se escribe la mitad juzgada
Then lleva el nombre del humano y la fecha, o `unsigned`
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `palette.md` de la elegida | `uv run python scripts/contraste-de-lectura.py governance/identity/palette.md` | `N par(es) de texto juzgado(s), 0 bajo el umbral`, exit 0 |
| una candidata con tinta suave a 5:1 | ídem sobre su tabla | exit 1, nombrando el par |

## In scope

- Criterios de la pieza aprobados antes de fijar colores; ADR en `proposed` → `accepted`.
- Dos o tres paletas candidatas por roles, medidas; la elegida por el humano.
- `governance/identity/palette.md` con roles, valores, pares medidos, catálogo, criterios y rechazadas.

## Out of scope

- Rampas, primitivas y roles semánticos por función (fondo de botón, borde de campo, foco) — s5.5.
- CSS — s5.7.
- Tema oscuro u otra variante — rabbit hole del brief.

## Done when

- [stated] El ADR de la paleta en `proposed` antes de cualquier color en el repositorio; los rojos de los criterios medibles escritos en él antes de `palette.md`.
- [stated] `contraste-de-lectura.py governance/identity/palette.md` sale con 0 y su población no es cero.
- [stated] La mitad juzgada firmada o `unsigned`; el ADR en `accepted`; `./scripts/check` en verde.

## Notes

- Deriva de ADR-009 (criterios 2 y 3), ADR-010 (neutros de papel, una tinta, un solo acento oscuro) y ADR-011 (todo texto a 16 px: ningún texto es "grande").
- Técnica `color` de gemba-design 0.21.0.
