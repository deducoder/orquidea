# Story s1: Adopt the gemba-design 0.23.0 vocabulary — Design

> Complexity: moderate

## 1 · What & why

**Problem:** gemba-design 0.23.0 trae un catálogo cerrado de dimensiones de interfaz (`conventions/interface-dimensions.md`) que pide responder cada una — declarada, o "no aplica, porque…" — y un generador que ya acepta radio, propiedades fuera del vocabulario e identificadores con acento. La identidad de e5 respondió seis de catorce dimensiones de la técnica `ui`, rodeó el formato en cuatro sitios, y dejó dos juicios sin firmar y dos ajustes sin decidir.

**Value:** cada decisión visual de la hoja queda escrita en un entregable o en `DESIGN.md`, con su número recalculado por un script, y no solo en la prosa de ADR-014 y ADR-015. Lo que se ve en la pantalla y lo que dicen los tokens coinciden, y la interfaz queda sin juicios pendientes.

## 2 · Approach

Un registro nuevo, **ADR-016**, abierto en `proposed` con los criterios de fitness aprobados, vuelve a correr los eslabones *semantic roles* y *components* de la técnica `ui` con el vocabulario de 0.23.0: renombra los roles, declara las dimensiones del catálogo que faltan, regenera `DESIGN.md` y propaga a la hoja. Todo se recalcula por script y se compara con lo que hay; lo que cambie se corrige en su eslabón.

### Qué dice hoy el código, dimensión por dimensión

Las catorce dimensiones del catálogo con destino `ui`, contra lo que la hoja (`identidad.css`) ya hace:

| Dimensión | Hoy en la hoja | En los entregables de e5 | 0.23.0 lo lleva a `DESIGN.md` |
|---|---|---|---|
| `color-ramp`, `color-roles`, `type-scale`, `spacing` | tokens | ADR-013, ADR-014 | sí, sin cambio |
| `control-size` | `min-height`/`min-width: 48px` (`:70`, `:142`, `:155`) | `height`/`width` fijos, usados como mínimo | `minWidth`/`minHeight` se aceptan; `targets` no los mide |
| `composition` | diez componentes | ADR-014 | sí |
| `interaction-states` | `button:active`, `:focus-visible` | `boton-presionado`; foco como `--gap` | como componente sí; foco no |
| `corner-radius` | `border-radius: 0` (`:140`, `:153`) | "not derived" | **sí**: tabla `Level \| Value` y columna `rounded` |
| `stroke` | `1px` en bordes, `2px` en el foco (lista cerrada de ADR-015) | literales admitidos | **no**: `{stroke.*}` sale `refused` |
| `elevation` | la tarjeta es `superficie` + borde `linea` sobre `fondo` (`:181`) | no se trató | **no**: "not derived" |
| `grid` | una columna; `main` con margen `spacing.step-2` (`:51`) | no se trató | no hay grupo |
| `measure` | **sin límite**: el renglón ocupa todo el ancho en escritorio | no se trató | **no** |
| `density` | una sola | no se trató | no hay grupo |
| `iconography` | ningún ícono ni `<svg>` en las plantillas | no-go del brief de e5 | **no**: Known Gap del generador |

**Información nueva que salió del recorrido** (lo que la historia recalcula y corrige si cambia):

1. **La elevación existe y no estaba declarada.** La tarjeta es un plano elevado, apartado por tono (`superficie` sobre `fondo`) y por borde (`linea`). No es "ninguna".
2. **El `error` como borde de campo no tiene aplicación.** ADR-013 lo midió como par de componente, pero ninguna plantilla marca un campo inválido: los errores son un `<p role="alert">`. Destino: el par se sigue midiendo en `semantics.md` y `components.md` dice que ningún componente lo usa. No se inventa un estado nuevo.
3. **Declarar solo `minWidth` vacía la población de `targets`.** El generador escribe la tabla `Target` solo con `height`/`width` literales. Sin ellos, `tokens.py targets` sale sin sujeto (exit 2) y `tests/test_identidad_ui.py:23` se pone en rojo. El mínimo declarado se mide **recalculando**: `comprobar-medidas.py objetivos` lee `minWidth`/`minHeight` del frontmatter de `DESIGN.md`.
4. **Sin medida, en escritorio el renglón no tiene tope.** A 360 px caben unos 40 caracteres; a 1280 px, más de 140.
5. **0.23.0 ya no rechaza una columna mal escrita** (`backgroundColour` se acepta con advertencia, antes salía exit 1). Destino: la regeneración compara la advertencia del generador — `0 unrecognised component properties` salvo las que ADR-016 declare, con su número exacto.

### Componentes afectados

- `governance/identity/ui/semantics.md`: modificar — renombre `linea` → `línea`, `accion-*` → `acción-*`; `decision:` añade ADR-016.
- `governance/identity/ui/components.md`: modificar — tabla `Level | Value`, columnas `rounded`, `borderColor`, `minWidth`, `minHeight`; sección de las dimensiones declaradas sin token (stroke, elevation, grid, measure, density, iconography) con su valor o su "no aplica, porque…"; `decision:` añade ADR-016.
- `governance/identity/ui/DESIGN.md`: regenerar con el generador de 0.23.0, con los `--gap` de lo que el formato no lleva.
- `src/orquidea/web/static/identidad/identidad.css`: modificar — nombres nuevos en `:root` y en cada `var()`; la medida y los ajustes que ADR-016 decida.
- `scripts/comprobar-medidas.py`: modificar — `objetivos` lee también los mínimos declarados del frontmatter (TDD en `tests/test_comprobar_medidas.py` o donde vivan sus pruebas).
- `tests/test_identidad_hoja.py`: modificar — la lista cerrada de ADR-015 cambia solo si ADR-016 añade un literal (la medida); el lector de tokens aprende `rounded` si la hoja lo usa como token.
- `src/orquidea/web/templates/acceso.html`: modificar — los controles envueltos en `<p>`, como en `ejemplar.html:10`.
- `records/decisions/adr-016-*.md`: crear.
- `records/parking-lot.md`: retirar las dos entradas y aparcar el hallazgo de `precedence.py`.

**Fuera, dicho:** la clase HTML `accion` de las plantillas (quince usos) no es un token; es un selector y se queda en ASCII. `primitives.md` no cambia: sus nombres (`neutro-400`, `azul-800`) no llevan acento.

**Legacy sweep:**
- Los nombres ASCII `--colors-linea` y `--colors-accion-*` en `identidad.css:13–18` y en cada `var()`: se reemplazan. `test_la_hoja_usa_solo_tokens_de_la_identidad` los nombra si queda uno.
- Los `height`/`width` usados como mínimo en `components.md`: se decide en ADR-016 (opción A, B o C abajo). Con la B, las celdas se borran.
- El `--gap` de ADR-014 sobre los bordes: lo reemplaza `borderColor`.
- ADR-013, ADR-014 y ADR-015 siguen `accepted`: no se editan. Ver la pregunta 1.

## 3 · Interface / examples

### Usage

```sh
# el renombre, regenerado con 0.23.0 (se registra completo en ADR-016)
python3 $D/design-md.py --spec-version alpha --name Orquídea \
  --decision "ADR-013: roles de color de la interfaz" \
  --decision "ADR-014: escala tipográfica, espaciado y componentes" \
  --decision "ADR-016: identidad en el vocabulario de gemba-design 0.23.0" \
  --gap "…trazo…" --gap "…elevación…" --gap "…medida…" --gap "…retícula y densidad…" \
  governance/identity/ui/semantics.md governance/identity/ui/type-scale.md \
  governance/identity/ui/spacing.md governance/identity/ui/components.md > governance/identity/ui/DESIGN.md

# el mínimo declarado, recalculado
uv run python scripts/comprobar-medidas.py objetivos governance/identity/ui/DESIGN.md --minimo 44
```

### Expected output (success + error)

```
# DESIGN.md, frontmatter
colors:
  línea: "#8C8475"
  acción-fondo: "#1F3A5F"
rounded:
  recto: "0px"
components:
  campo:
    backgroundColor: "{colors.campo-fondo}"
    borderColor: "{colors.campo-borde}"
    rounded: "{rounded.recto}"
    minHeight: "{spacing.step-6}"
    minWidth: "{spacing.step-6}"

# stderr del generador
design-md: 22 token(s), 10 component(s), 8 pair(s), … N unrecognised component properties accepted

# comprobar-medidas.py, verde
4 objetivo(s) medidos, 0 bajo 44 px

# comprobar-medidas.py, rojo — un mínimo a spacing.step-4 (32px)
boton minWidth 32  necesita 44  NO
4 objetivo(s) medidos, 1 bajo 44 px        (exit 1)

# comprobar-medidas.py, sin sujeto — ni tabla Target ni mínimos declarados
0 objetivo(s) medidos — nada que juzgar      (exit 2)

# la hoja con un nombre viejo
--colors-linea no es un token de DESIGN.md
```

### Key data structures

```css
/* identidad.css, :root — el renombre */
--colors-línea: #8C8475;
--colors-acción-fondo: #1F3A5F;
--colors-acción-texto: #FFFFFF;
--colors-acción-presionada: #0C274A;
```

### Los criterios de fitness que se proponen (se aprueban antes de producir)

Se proponen aquí para que los revises; entran a ADR-016 al abrirlo, y nada se produce antes.

| # | Criterio | Dimensión | Estrato | From |
|---|---|---|---|---|
| V1 | Las catorce dimensiones del catálogo con destino `ui` tienen respuesta en un entregable: declarada (con referencia a un token o con su valor y su fuente), o "no aplica, porque…". Un script las cuenta y sale en rojo con una sin respuesta o con población cero | todas | `mechanical` | este eslabón |
| V2 | Cada control declarado llega a 44 × 44 px CSS en su mínimo, medido recalculando desde lo que declara `DESIGN.md` (`minWidth`/`minHeight`, o la tabla `Target`). Fuente: WCAG 2.2 SC 2.5.5, AAA | `control-size` | `mechanical` | ADR-014 M2 |
| V3 | El texto corrido de una ficha se lee sin que el renglón cruce la pantalla de escritorio, y a 360 px no cambia nada | `measure` | `judgement` — elección forzada entre las candidatas, renderizadas a 1280 y a 360 px con la ficha de un ejemplar con notas largas | concept (ADR-010, S3) |
| V4 | Esquinas, trazos y planos se leen como el Cuaderno de campo: papel y tinta, sin sombra de pantalla | `corner-radius`, `stroke`, `elevation` | `judgement` — elección forzada entre las candidatas de elevación, sobre la colección con tres tarjetas a 360 px | concept (ADR-010) |

**Del catálogo, aplicados (no propuestos):** `contrast`, `component-contrast` y `provenance`, recalculados sobre lo regenerado; `target-size` (SC 2.5.8), con `tokens.py targets` si queda tabla `Target`; `minimum-size`, sin cambio (M1). `platform-specs`, `single-ink` y `prior-art`: no aplican, igual que en e5.

### Candidatas que irán a la rejilla de ADR-016

- **Mínimo de control:** (A) `height`/`width` fijos, como hoy; (B) solo `minHeight`/`minWidth`, medidos recalculando; (C) los dos. Recomiendo **(B)**: es lo que la hoja hace (`min-height`), y la (A) declara un ancho fijo de 48 que el botón "Agregar una planta…" no tiene.
- **Medida:** (A) sin tope, como hoy; (B) `max-width: 34em` en `main` (unos 68 caracteres a 16 px); (C) `40em` (unos 80). La cifra en `em` entra como literal en la lista cerrada de ADR-015 y como `--gap` en `DESIGN.md`: el formato no la lleva.
- **Elevación:** (A) tono + borde, como hoy; (B) solo tono; (C) solo borde.
- **Radio:** un solo nivel, `recto: 0px`, citado por `boton`, `boton-presionado`, `campo` y `tarjeta`. No hay candidatas: ADR-015 ya lo decidió; aquí solo pasa a ser un token.
- **Trazo, retícula, densidad, iconografía:** se declaran como están (1 y 2 px; una columna con margen de `spacing.step-2`; una densidad; ningún ícono, por el brief) y van como `--gap`. No hay candidatas: no hay decisión nueva.
- **Ajustes del parking lot:** la sangría de `.accion` (`:72`, `padding: 0 var(--spacing-step-1)`) — (A) quitar el relleno horizontal fuera de la cabecera; el objetivo sigue en 48 por `min-width` · (B) dejarla. El botón de Acceso — envolver los controles en `<p>`, como el resto de los formularios; sin candidata, porque es la forma que ya usa el código.

## 4 · Acceptance criteria

- **Must:**
  - ADR-016 commiteado en `proposed` con V1–V4 aprobados antes del primer valor producido.
  - `DESIGN.md` regenerado con 0.23.0, idéntico en dos corridas. El stderr del generador cuenta las propiedades fuera del vocabulario, y el número coincide con las declaradas en ADR-016.
  - `pairs`, `provenance`, 7:1, piso y objetivos recalculados sobre lo regenerado. Cada cifra que cambie contra la de e5 queda anotada en ADR-016, y si ninguna cambia se dice.
  - El chequeo de V1 cuenta 14 dimensiones y 0 sin respuesta, y se vio en rojo con una quitada.
  - `comprobar-medidas.py objetivos` mide los mínimos declarados, y se vio en rojo con uno de 32 px.
- **Should:**
  - `test_identidad_ui.py` corre también el chequeo de V1, para que una dimensión que se borre ponga el gate en rojo.
- **Must NOT:**
  - Copiar o parchar `design-md.py` o `tokens.py`.
  - Editar ADR-013, ADR-014 o ADR-015 para cambiar lo que deciden.
  - Inventar un token para un valor que el formato no lleva (un "escalón" de `spacing` de 1 px, o `spacing.step-medida`).
  - Firmar un juicio en nombre del humano.

### Deduced criteria

- "la prueba de tokens de la hoja, la de objetivos y la de piso siguen verdes con los nombres nuevos, y ninguna propiedad de `identidad.css` usa un nombre anterior": **confirmed**. `tokens_de_design()` lee los nombres de `DESIGN.md` sin lista fija, `var\((--[\w-]+)\)` casa letras con acento (`\w` Unicode) y CSS admite identificadores no ASCII. La de objetivos solo sigue verde si el script aprende a leer los mínimos (información nueva 3).
- "`./scripts/check` verde con los nombres nuevos": **confirmed**, con la misma condición.
- "`survival-review` corrido sobre las piezas tocadas, con su población contada": **confirmed**.
- "Las dos entradas retiradas del parking lot, y el hallazgo de `precedence.py` aparcado": **confirmed**.

### Scenarios (delta over the scope)

```gherkin
Given un componente con `minWidth: {spacing.step-6}` y sin `width`
When corre `comprobar-medidas.py objetivos DESIGN.md --minimo 44`
Then lo cuenta como objetivo medido y juzga 48 contra 44

Given los entregables de ui sin la respuesta de `measure`
When corre el chequeo de V1
Then sale en rojo nombrando `measure`, con la población contada

Given `DESIGN.md` regenerado
When se compara el stderr del generador
Then el número de propiedades fuera del vocabulario es el que ADR-016 declara
```

## Preguntas abiertas

1. **Sustitución parcial.** La técnica `adr` solo sustituye un registro entero (`status: superseded by ADR-{NNN}`). ADR-016 reemplaza decisiones sueltas: la 6 de ADR-014 (ASCII) y, según la rejilla, la 3 y el `--gap` de bordes de ADR-014 y la 3 de ADR-015 (esquinas sin token). Marcar ADR-014 y ADR-015 como `superseded` diría que caen enteros, y no es así. **Recomiendo:** dejarlos `accepted`, que ADR-016 nombre cada decisión que reemplaza, y aparcar el hueco como hallazgo del método.
2. **La medida cambia la pantalla en escritorio.** Es la única decisión de esta historia que se ve distinto, más allá de la sangría. Si prefieres no tocarla, V3 se retira y `measure` se responde "no aplica, porque la app es primero para el teléfono", con SC 1.4.8 como apoyo.
