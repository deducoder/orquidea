# Story s5.4: Typography — Scope

## User story

Como coleccionista que lee su colección en el teléfono, en campo,
quiero un sistema tipográfico elegido contra un criterio escrito antes de mirar ninguna familia, con su piso de legibilidad probado y su licencia registrada,
para que los nombres científicos, las fechas y las fuentes citadas se lean bien bajo el sol sin gastar el presupuesto de peso de la identidad.

## Acceptance criteria

```gherkin
@stated
Given ADR-009 (encargo) y ADR-010 (Cuaderno de campo) en `accepted`
When se abre el registro de la tipografía
Then un ADR nuevo queda commiteado en `proposed` con los criterios de la pieza (cada uno con su estrato y su origen) y las opciones en juego, antes de elegir ninguna familia

@stated
Given los criterios de la pieza propuestos
When el humano no los ha aprobado
Then no se especifica ninguna familia

@deduced
Given el criterio 1 del encargo (identidad ≤ 50 KB)
When una opción usa una fuente web
Then su peso se mide con `scripts/medir-primera-carga.py --identidad` sobre los archivos reales, y una opción que lo viola se ve en rojo antes de elegir

@stated
Given el piso de legibilidad (`minimum-size`)
When se declara
Then la cifra se lee de su fuente en el momento de producir, se registra con la fuente y la fecha, y se prueba renderizando a ese tamaño

@stated
Given la familia elegida
When se escribe el espécimen
Then registra la licencia de cada familia, y cada criterio del catálogo tiene su fila (aplicado o "no aplica, porque…")

@stated
Given ADR-010 (celda del herbario × S2)
When se eligen familias
Then se verifica qué familias trae cada sistema (Android, iOS, Windows, macOS), en particular si traen itálica verdadera, y el resultado se registra como `ran:` o `read:` con su fuente
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| Una familia web con regular, itálica y negrita en woff2 | `medir-primera-carga.py --identidad` sobre sus archivos | peso real en KB contra el tope de 50 KB; 1 si lo pasa |
| La pila de fuentes del sistema | medir | 0 archivos: nada que medir en fuentes (el CSS se mide en s5.7) |
| `Arpophyllum giganteum` en itálica | renderizar en la opción elegida | itálica verdadera, no oblicua sintética |

## In scope

- Criterios de la pieza (2 a 4), derivados de ADR-009 y ADR-010 o propios, aprobados antes de especificar nada.
- ADR abierto en `proposed` y completado a `accepted`.
- Las opciones medidas: peso real de cada fuente web candidata; qué trae cada sistema.
- El piso de legibilidad leído de su fuente y probado renderizando.
- `governance/identity/specimen.md` con roles, escala provisional, piso, licencia, catálogo y criterios.
- Si la elegida es una fuente web: sus archivos en `src/orquidea/web/static/identidad/` con su licencia.

## Out of scope

- La escala tipográfica como regla de la interfaz y el espaciado — s5.6 (el espécimen declara los roles y el piso; la regla de la escala es del eslabón `type scale`).
- Enlazar las fuentes o escribir CSS — s5.7.
- Colores — s5.3.

## Done when

- [stated] `git log` muestra el ADR de tipografía en `proposed` antes de cualquier archivo de fuente o del espécimen.
- [stated] El espécimen registra la licencia, el piso de legibilidad con su fuente y fecha, y una fila por cada criterio del catálogo.
- [deduced] Si hay fuente web, `medir-primera-carga.py --identidad src/orquidea/web/static/identidad` sale con 0 y su peso queda registrado.
- [stated] La mitad juzgada lleva nombre y fecha del humano o `unsigned`; el ADR queda en `accepted`; `./scripts/check` en verde.

## Notes

- Deriva de ADR-009, ADR-010 y `governance/identity/{commission,concept}.md`.
- Técnica `typography` de gemba-design 0.21.0 (su paso propio: el piso de legibilidad se lee de su fuente).
- Hallazgo heredado de s5.2: verificar las serif y las itálicas del sistema, no darlas por supuestas.
