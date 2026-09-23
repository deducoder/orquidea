# Story s5.6: Scale, spacing, components and DESIGN.md — Scope

## User story

Como coleccionista que usa Orquídea en el teléfono, en campo, con el pulgar,
quiero que los tamaños de letra, los espacios y cada componente de la interfaz (botón, campo, tarjeta, enlace, aviso) salgan de una escala y una unidad declaradas, con cada control a un tamaño que se toque sin fallar,
para que la interfaz se lea y se use en campo, y s5.7 la vista desde un único `DESIGN.md` generado, no desde valores sueltos.

## Acceptance criteria

```gherkin
@stated
Given ADR-011 (piso de 16 px) y ADR-013 (roles de color) en `accepted`
When se abre el registro de la escala, el espaciado y los componentes
Then un ADR nuevo queda commiteado en `proposed` con los criterios de los tres eslabones y las reglas candidatas con sus parámetros, antes de producir ningún valor

@stated
Given los criterios propuestos
When el humano no los ha aprobado
Then no se produce ninguna escala, unidad ni componente

@deduced
Given una regla candidata de escala cuyo escalón para un rol de lectura cae bajo el piso de 16 px
When corre su comprobación
Then se ve en rojo nombrando el escalón y el piso, antes de elegir

@stated
Given una unidad candidata que deja un control declarado bajo el mínimo de WCAG 2.2 SC 2.5.8
When corre `tokens.py targets`
Then se ve en rojo nombrando el control y la dimensión, antes de elegir

@stated
Given los componentes producidos
When se genera `DESIGN.md` con `design-md.py` y corren `tokens.py pairs`, `targets` y `provenance` sobre él
Then los tres salen con 0 y cuentan una población distinta de cero

@deduced
Given `DESIGN.md` generado
When se vuelve a generar desde las mismas tablas
Then el archivo sale idéntico

@deduced
Given un componente
When se lee su composición
Then cada propiedad es una referencia a un rol, un escalón o un paso, nunca un literal

@stated
Given la regla elegida en cada eslabón
When se escribe la mitad juzgada
Then lleva el nombre del humano y la fecha, o `unsigned`
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `governance/identity/ui/DESIGN.md` generado | `python3 $G/tokens.py targets governance/identity/ui/DESIGN.md` | `targets: N target(s) judged, 0 below 24 px`, exit 0 |
| una unidad candidata que deja el botón a 20 px de alto | ídem sobre la tabla de la candidata | exit 1, nombrando el botón y la dimensión |
| las tablas de s5.5 y s5.6 | `design-md.py --spec-version V …` dos veces | los dos archivos, idénticos |

## In scope

- Eslabón *type scale*: la regla, sus parámetros y el escalón de cada rol del espécimen, sin bajar de 16 px.
- Eslabón *spacing*: una unidad, sus pasos y la composición de cada control declarado (botón, campo, enlace de navegación).
- Eslabón *components*: los componentes que usan las plantillas actuales, cada uno como composición de referencias.
- `governance/identity/ui/type-scale.md`, `spacing.md`, `components.md` y `DESIGN.md` generado.
- ADR en `proposed` → `accepted`; `survival-review` sobre lo producido.

## Out of scope

- La hoja de estilos, las plantillas y quitar los `style` en línea — s5.7.
- Cambiar los roles de color o la paleta: un par que falle con su valor vuelve a ADR-013 con un ADR nuevo.
- Componentes que las plantillas no usan hoy — rabbit hole del brief (biblioteca de componentes).
- Tema oscuro u otra variante — rabbit hole del brief.

## Done when

- [stated] El ADR de la pieza en `proposed` antes de cualquier escala, unidad o componente en el repositorio; los rojos de los criterios medibles escritos en él antes de producir.
- [stated] `DESIGN.md` generado con `design-md.py` y verificado con `pairs`, `targets` y `provenance`, los tres en 0 con población distinta de cero.
- [deduced] Regenerar `DESIGN.md` produce el mismo archivo, y una prueba del gate lo comprueba.
- [stated] Cada control declarado mide al menos lo que fija WCAG 2.2 SC 2.5.8, leído de la fuente el día que se mide, en cada dimensión que declara.
- [deduced] Ningún escalón asignado a un rol de lectura queda bajo 16 px, y ningún par de escalones colapsa en uno al redondear.
- [stated] La mitad juzgada firmada o `unsigned`; el ADR en `accepted`; `./scripts/check` en verde.

## Notes

- Deriva de ADR-011 (piso de 16 px para todo texto; la jerarquía la marcan peso, color y espacio más que tamaño), ADR-013 (trece roles de color), ADR-010 (acciones grandes, navegación al pulgar) y ADR-009 (`target-size` aplica a `ui`).
- Técnica `ui` de gemba-design 0.21.0, eslabones *type scale*, *spacing* y *components*, y `scripts/design-md.py`. Las piezas van en `governance/identity/ui/` (convención `deliverables`).
- Pendiente de ADR-013: si hace falta un gris muy claro para separadores tenues, es un rol nuevo con su propia medición, y el humano lo dejó a que esta historia lo pida.
- Al abrir el ADR se declara "respaldo: ninguno" (memoria del proyecto).
