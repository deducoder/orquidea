# Story s5.5: Interface color roles — Design

> Complexity: moderate

## 1 · What & why

**Problem:** la paleta (ADR-012) trae siete roles de identidad con valores fijos, pero la interfaz necesita roles por función: el fondo de un botón, el borde de un campo, el anillo de foco, el estado presionado. Hoy no existe ninguno, y s5.6 no puede componer componentes sin ellos.
**Value:** cada color de la interfaz sale de la paleta por una regla que corre un script, con su contraste medido en el valor real; cambiar un color mañana es cambiar un parámetro y volver a correr, no parchar a mano.

## 2 · Approach

Técnica `ui`, eslabones *colour primitives* y *semantic roles*, en un solo registro: criterios de los dos eslabones → **parada para aprobación** → ADR-013 en `proposed` con las reglas candidatas y sus parámetros → los rojos de cada criterio medible vistos sobre una candidata que los viola → `primitives.md` producido por un script del proyecto → `semantics.md` con cada rol como referencia a un escalón → juicio firmado → ADR-013 `accepted`.

**Components affected:**

- `scripts/derivar-primitivas.py`: create — lee `palette.md` y los parámetros de la regla, imprime la tabla de primitivas. Solo biblioteca estándar (la conversión sRGB ↔ OKLab son unas 30 líneas).
- `tests/test_derivar_primitivas.py`: create — TDD del script, y una prueba que regenera `primitives.md` con sus parámetros registrados y lo compara con el archivo.
- `records/decisions/adr-013-roles-de-color.md`: create.
- `governance/identity/primitives.md`, `governance/identity/semantics.md`: create.

**Legacy sweep:** nada — net-new. Ninguna plantilla ni hoja usa color todavía (eso es s5.7).

### Lo que el recorrido encontró

- **Los instrumentos ya existen, no se escribe uno nuevo de contraste.** `scripts/contraste-de-lectura.py` juzga los pares `text` a 7:1 (s5.1); `tokens.py pairs` del addon juzga los `component` a 3:1, con la cifra del catálogo (`NEED_COMPONENT`, WCAG 1.4.11). `tokens.py provenance` comprueba que cada `Token | Value | From` sea un escalón de una tabla `Step | Value`: con eso se verifica que ningún rol semántico es un literal.
- **Lo que sí falta es reproducir la regla.** La plantilla exige que cada primitiva se reproduzca "corriendo la regla otra vez", y el valor de la épica es que un cambio se re-derive. Un cálculo hecho en el scratchpad no se puede volver a correr: por eso el script vive en `scripts/`, con TDD.
- **Un desvío de la plantilla, declarado.** La tabla de primitivas se escribe `Step | Value | Ramp` (no `Ramp | Step | Value`) porque `tokens.py provenance` encuentra la escala por la primera celda del encabezado; el nombre del escalón lleva la rampa (`azul-700`). Mismas columnas, otro orden.
- **El margen fino es el del borde.** Medido hoy con `tokens.py pairs` sobre `palette.md`: `renglón` sobre `papel` da **3.34:1** y sobre `hoja` 3.70:1, contra 3:1. Una regla que redondee el renglón a un escalón más claro rompe `component-contrast` en `papel` y no en `hoja`: ese es el contraejemplo natural del eslabón semántico. El texto tiene holgura (el par más bajo, 8.38:1).
- **Lo que la interfaz usa** (plantillas actuales, contadas con `grep`): 19 enlaces, 13 botones, 13 formularios, 10 `input`, 1 `textarea`, 2 avisos `role="alert"`. Ningún estado deshabilitado, ningún mensaje de éxito (la aplicación confirma redirigiendo). La acción destructiva ("Sí, quitar") se distingue por su texto y su página de confirmación.
- **Contextos:** dos fondos, `papel` y `hoja`. **Variante: ninguna** (ADR-012): `invariance.py` no tiene sujeto y `semantics.md` lo reporta como no comparado.
- **ADR-010, consecuencia pendiente:** con un solo acento oscuro, los estados se distinguen por texto, forma o posición, no por color vivo. Aquí se decide su color; que no dependa *solo* del color (WCAG 1.4.1) es de los componentes, s5.6.

### Propuesta que necesita aprobación (paso `fitness`)

| # | Criterio | Eslabón | Estrato | From |
|---|----------|---------|---------|------|
| R1 | Cada par de texto de los roles semánticos, sobre `papel` y sobre `hoja`, llega a ≥ 7:1 | semántico | `mechanical` — `contraste-de-lectura.py` | commission 2 |
| R2 | Todo valor es reproducible: el script con los parámetros registrados regenera `primitives.md` idéntico, y cada rol semántico es un escalón de una rampa (`tokens.py provenance`, 0 fuera de escala) | ambos | `mechanical` | este eslabón |
| R3 | Los roles añadidos (botón, campo, foco, presionado) se leen como parte del Cuaderno de campo, y el azul sigue siendo una sola familia a lo largo de su rampa | ambos | `judgement` — elección forzada entre las reglas candidatas, sobre una lámina con un formulario real (campo, botón, foco, error) en `papel` y en `hoja` | concept (ADR-010) |

Aplicados del catálogo, no propuestos: `contrast` (texto, subsumido por R1), `component-contrast` (borde de campo, fondo de botón y anillo de foco, contra cada fondo adyacente, a la cifra que el catálogo fije el día que se mida), `provenance`. Los demás se responden "no aplica, porque…" en el entregable.

**Roles por función propuestos** (el conjunto es parámetro del encargo):

| Rol | Resuelve a (relación) | Kind medido |
|-----|------------------------|-------------|
| `fondo` | `papel` | — (es fondo) |
| `superficie` | `hoja` | — (es fondo) |
| `texto` | `tinta` | text |
| `texto-secundario` | `tinta suave` | text |
| `línea` | `renglón` | component |
| `enlace` | `acento` | text |
| `acción-fondo` | `acento` | component (contra `papel` y `hoja`) |
| `acción-texto` | `hoja` | text (sobre `acción-fondo`) |
| `acción-presionada` | un escalón más oscuro que `acción-fondo` — rol que la identidad no trae | component; y `acción-texto` encima, text |
| `campo-fondo` | `hoja` | — |
| `campo-borde` | `renglón`, o el escalón más cercano que llegue a 3:1 en ambos fondos | component |
| `foco` | `acento` | component (contra `papel` y `hoja`) |
| `error` | `alerta` | text; y como borde de campo, component |

Sin rol de éxito, de aviso ni de deshabilitado: la interfaz no los usa (YAGNI; si s5.6 los necesita, se añaden por la regla).

**Reglas candidatas** (se fijan sus parámetros en ADR-013 después de la aprobación; sus valores se miden al correrlas):

- **(A) Rampa por anclas en OKLCH:** cada rampa pasa por los valores de la paleta de su tono (la neutra por `papel`, `renglón`, `tinta suave` y `tinta`) e interpola L, C y h entre ellos en posiciones de luminosidad declaradas. Desvío cero en los roles de la paleta.
- **(B) Rampa uniforme en OKLCH:** luminosidad en pasos iguales, croma y tono del rol fuente; cada rol de la paleta toma el escalón más cercano y se reporta su desvío.
- **(C) Rampa uniforme en HSL:** la forma habitual de las bibliotecas de CSS; candidata a romper el contraste por su luminosidad no perceptual.

## 3 · Interface / examples

```sh
# primitivas: imprime la tabla Step | Value | Ramp
uv run python scripts/derivar-primitivas.py governance/identity/palette.md \
    --regla anclas --pasos 50,100,200,300,400,500,600,700,800,900,950
# | Step | Value | Ramp |
# |---|---|---|
# | neutro-50 | #F7F3EA | neutro |   ← ancla: papel
# ...
# exit 0; exit 2 con un rol que no resuelve o un parámetro ilegible, nombrándolo

# texto a 7:1 sobre los roles semánticos
uv run python scripts/contraste-de-lectura.py governance/identity/semantics.md
# 9 par(es) de texto juzgado(s), 0 bajo el umbral   → exit 0

# componentes a 3:1, y cada rol desde un escalón
G=~/.claude/plugins/cache/gemba/gemba-design/0.21.0/conventions/mechanical/instruments
python3 $G/tokens.py pairs governance/identity/semantics.md
cat governance/identity/primitives.md governance/identity/semantics.md > $S/roles.md
python3 $G/tokens.py provenance $S/roles.md
# provenance: 13 token(s) judged, 0 not from the declared scale
```

Rojos esperados antes de elegir (contraejemplos):

| Sujeto | Comprobación | Salida |
|--------|--------------|--------|
| candidata cuyo `campo-borde` cae a un escalón más claro que `renglón` | `tokens.py pairs` | exit 1, `campo-borde/fondo … need 3.0:1 component FAIL` |
| candidata cuyo `texto-secundario` cae a un escalón más claro que `tinta suave` | `contraste-de-lectura.py` | exit 1, nombrando el par |
| `semantics.md` con un rol escrito como literal que no es escalón | `tokens.py provenance` | exit 1, `… names …, which no scale declares FAIL` |
| `primitives.md` editado a mano | `test_derivar_primitivas.py` | la prueba de regeneración falla |

```markdown
| Token | Value | From |
|---|---|---|
| campo-borde | #8C8475 | neutro-400 |
```

## 4 · Acceptance criteria

- **Must:**
  - ADR-013 en `proposed`, con R1–R3 aprobados y las reglas con sus parámetros, commiteado antes del primer valor de `primitives.md`.
  - Los cuatro rojos de la tabla de arriba vistos y escritos en ADR-013 antes de producir.
  - `contraste-de-lectura.py`, `tokens.py pairs` y `tokens.py provenance` en 0 sobre lo producido, cada uno contando una población distinta de cero.
  - La prueba de regeneración de `primitives.md` en el gate.
- **Should:**
  - `survival-review` corrido sobre las dos piezas.
- **Must NOT:**
  - Cambiar un valor de `palette.md`.
  - Un rol semántico que sea un literal sin escalón.
  - Reportar la invariancia como pasada.
  - Dependencias nuevas: la conversión de color es biblioteca estándar.

### Deduced criteria

- Cada rol de la paleta lleva su valor de identidad, el de la primitiva y la diferencia, o se declara fijado: **confirmed** — lo exige la plantilla de `semantics.md` (columnas `Identity value` y `Drift`); con la regla (A) el desvío es cero y se dice, no se omite.
- Un rol semántico es una referencia a un escalón, nunca un literal: **confirmed** — lo exige la técnica, y ahora tiene instrumento (`tokens.py provenance` sobre las dos tablas).

### Stated criteria

Ninguno contradicho por el recorrido.
