# Story s5.7: Apply the identity to the templates — Scope

## User story

Como coleccionista que usa Orquídea en el teléfono, en campo,
quiero que todas las pantallas se vean con la identidad decidida (papel cálido, azul tinta, controles grandes, la foto como protagonista),
para leer y usar la aplicación bajo el sol y con red lenta, en lugar de las plantillas sin estilo de hoy.

## Acceptance criteria

```gherkin
@stated
Given `governance/identity/ui/DESIGN.md` generado y verificado (s5.6)
When se escribe la hoja de estilos
Then vive en `src/orquidea/web/static/identidad/`, se sirve desde `/static` y `base.html` la enlaza

@stated
Given la hoja de estilos
When una prueba compara cada valor de color, tamaño y espacio con los tokens de `DESIGN.md` y de `specimen.md`
Then todos son tokens, y la prueba se pone en rojo con un valor inventado

@stated
Given todas las plantillas
When se buscan atributos `style`
Then no queda ninguno

@stated
Given las pruebas de comportamiento
When se aplica la identidad
Then ninguna cambia, salvo la que afirmaba el estilo en línea (`tests/test_web_coleccion.py`)

@stated
Given los recursos de la identidad
When corre `medir-primera-carga.py --identidad`
Then pesan ≤ 50 KB en gzip, y la primera carga de "Mi colección" sigue dentro de `must-perf-001`, con el CSS contado

@deduced
Given cada página de la aplicación
When una prueba parametrizada lee su `<title>`
Then es texto sin `<` ni `>` (parking lot, clase de b1)

@deduced
Given la CSP actual (`default-src 'self'`)
When se enlaza la hoja
Then la CSP no cambia, porque la hoja y (si las hubiera) las fuentes se sirven desde `/static`

@stated
Given la interfaz vestida
When el humano la recorre en el teléfono
Then juzga el criterio 3 de ADR-009 (la foto es la protagonista) con nombre y fecha, o queda `unsigned`
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `identidad.css` con `color: #F7F3EA` | la prueba de tokens | pasa: `#F7F3EA` es `colors.fondo` |
| la misma hoja con `padding: 10px` | ídem | rojo, nombrando `10px` y la regla |
| `src/orquidea/web/static/identidad/` | `medir-primera-carga.py --identidad …` | `≤ 50 KB`, exit 0 |

## In scope

- Una hoja de estilos escrita a mano (sin cadena de construcción) que usa solo tokens de `DESIGN.md` y de `specimen.md`, enlazada en `base.html`.
- Quitar los siete atributos `style` de las plantillas y ajustar la única prueba que los afirmaba.
- La prueba que compara la hoja con los tokens.
- La medición de la primera carga con el CSS contado, y el peso de la identidad contra 50 KB.
- La prueba de títulos de todas las páginas (parking lot, promoción en s5.7).
- Las dos preguntas abiertas de s5.6: si el subtítulo de 20 px se distingue del cuerpo en negrita, y las esquinas (`rounded` sin token).
- El recorrido en el teléfono y la firma del criterio 3 de ADR-009.

## Out of scope

- Quitar `'unsafe-inline'` de `style-src` en la CSP: su entrada del parking lot se promueve **al cerrar** s5.7, como historia o arreglo propio con su prueba y la comprobación de htmx.
- Generar la hoja desde `DESIGN.md` — rabbit hole del brief; la hoja se escribe a mano y la prueba la compara.
- Cambiar tokens: un valor que falte o no funcione vuelve a su eslabón (s5.5, s5.6) con un ADR nuevo.
- Cualquier cambio de comportamiento (rutas, formularios, datos) — no-go del brief.
- Tema oscuro, logotipo, favicon — rabbit holes y no-go del brief.

## Done when

- [stated] `base.html` enlaza la hoja servida desde `/static`, y ninguna plantilla conserva un atributo `style`.
- [stated] La prueba de tokens pasa, y se vio en rojo con un valor inventado.
- [stated] Las pruebas de comportamiento siguen en verde sin cambios, salvo la del estilo en línea.
- [stated] `medir-primera-carga.py --identidad` ≤ 50 KB y la primera carga dentro de `must-perf-001`, medidas por script con el CSS contado.
- [deduced] La prueba de títulos recorre todas las páginas y se vio en rojo con un título roto.
- [deduced] La CSP no cambió.
- [stated] El criterio 3 de ADR-009 y el juicio de la interfaz vestida, firmados con nombre y fecha o `unsigned`. La medición con "Slow 3G" en el navegador queda como stop previsto para `epic-review`.
- [stated] `./scripts/check` en verde.

## Notes

- Deriva de `DESIGN.md` y ADR-014 (escala, espaciado, componentes y huecos: bordes, foco, peso y cifras tabulares por token, fuera de `components`), ADR-013 (roles), ADR-011 (pila de sistema, 700 en títulos, `tabular-nums` en fechas, itálica en binomios) y ADR-010 (foto a todo el ancho, navegación al pulgar, acciones grandes, enlaces subrayados).
- Riesgo que ya se sabe: los formularios en línea de la ficha con botones de 48 × 48 pueden no caber en fila a 360 px.
- Memoria: `design-md-py-que-lee` (qué lee y cómo se regenera `DESIGN.md`).
