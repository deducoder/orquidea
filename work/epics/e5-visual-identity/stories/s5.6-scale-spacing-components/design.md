# Story s5.6: Scale, spacing, components and DESIGN.md — Design

> Complexity: complex — tres eslabones, un generador externo y dos comprobaciones propias

## 1 · What & why

**Problem:** hay colores decididos (s5.5) y un piso de 16 px (s5.4), pero ningún tamaño de título, ningún espacio y ningún componente. s5.7 no puede escribir la hoja de estilos sin ellos, y el `DESIGN.md` que debe leer todavía no existe.
**Value:** cada tamaño, espacio y componente sale de una regla con parámetros declarados. Los controles se tocan con el pulgar sin fallar, y s5.7 lee un único `DESIGN.md` generado, verificado con `pairs`, `targets` y `provenance`.

## 2 · Approach

Técnica `ui`, eslabones *type scale*, *spacing* y *components*, en un solo registro, con el mismo orden que s5.5: criterios → **parada para aprobación** → ADR-014 en `proposed` con reglas candidatas, parámetros y "respaldo: ninguno" → rojos vistos sobre candidatas → producir con scripts → generar `DESIGN.md` → juicio firmado → ADR-014 `accepted`.

**Components affected:**

- `scripts/derivar-medidas.py`: create. Imprime la tabla `Step | Size | Line height | Roles` y la `Step | Value | Where it is used` a partir de la regla y sus parámetros, como `derivar-primitivas.py`. Solo biblioteca estándar.
- `scripts/comprobar-medidas.py`: create. Dos comprobaciones que el addon no trae:
  - `piso`: ningún rol de lectura bajo el piso del espécimen y ningún par de escalones colapsado al redondear.
  - `objetivos --minimo N`: cada `Target | Width | Height` a ≥ N px. `tokens.py targets` fija 24 y no se puede cambiar.

  Las dos cuentan su población y salen con 0/1/2.
- `tests/test_derivar_medidas.py`, `tests/test_comprobar_medidas.py`: create, incluida la prueba que regenera las tablas de `type-scale.md` y `spacing.md`.
- `records/decisions/adr-014-escala-espaciado-componentes.md`: create.
- `governance/identity/ui/type-scale.md`, `spacing.md`, `components.md`, `DESIGN.md`: create.
- `governance/identity/ui/semantics.md`: modify solo si se aprueba la pregunta de abajo (identificadores ASCII).

**Legacy sweep:** nada queda huérfano; todo es nuevo. `semantics.md` cambia solo de nombres, si se aprueba.

### Lo que el recorrido encontró

- **El formato:** `DESIGN.md` es el spec de google-labs-code/design.md, versión **`alpha`**, leído el 2026-09-22. El spec no limita los caracteres de un nombre de token.
- **Un bloqueo con los nombres de s5.5.** `design-md.py` (gemba-design 0.21.0) solo acepta referencias ASCII (`^\{([a-z][A-Za-z0-9.-]*)\}$`). Cuatro roles de `semantics.md` llevan acento: `línea`, `acción-fondo`, `acción-texto` y `acción-presionada`. Un componente con `{colors.acción-fondo}` sale con `refused` (exit 1), y el botón no se puede componer. Es la **pregunta 1** de abajo.
- **Lo que el generador lee y lo que no:**
  - Lee `Role | Value` como colores (la tabla de roles de `semantics.md`), `Step | Size` como escala, `Step | Value` como espaciado y `Component | {vocabulario}` como composiciones.
  - **No se le pasa `primitives.md`**, porque su tabla `Step | Value | Ramp` la leería como espaciado y rechazaría `#FFFFFF`. Tampoco `palette.md` ni `specimen.md`.
  - Los pares que deriva son solo `text` (el `textColor` sobre el `backgroundColor` de cada componente). Los pares de componente (bordes, foco) ya los midió s5.5.
- **El vocabulario del formato no tiene color de borde.** Las propiedades son `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height` y `width`, y el spec acepta `borderColor` solo "con advertencia". Por eso `campo-borde`, `línea`, `foco` y el borde de error viven en `colors` de `DESIGN.md` como tokens, pero ningún componente los compone. Va como `--gap`, y s5.7 los usa por token.
- **`rounded`:** el generador lo declara "no derivado" (Known Gaps). Ningún componente lo lleva.
- **Lo que usan las plantillas** (contado con `grep`):
  - 8 `h1`, 5 `h2`, texto con `<small>` y `<i>`.
  - 13 botones: Entrar, Salir, Buscar, Registrar riego y Registrar floración, Terminar, Quitar, Subir foto, Sí, quitar.
  - 10 `input` y 1 `textarea`.
  - La cabecera de navegación con dos enlaces y el botón Salir.
  - Listas de ejemplares como tarjetas y avisos `role="alert"`.
- **Los roles del espécimen:** `text`, `emphasis` (700, para `h1` y `h2`), `binomial` y `date`, todos con piso de 16 px. ADR-011 advierte que la jerarquía la marcan peso, color y espacio más que tamaño.
- **El gris claro que dejó pendiente s5.5:** ninguna plantilla tiene separadores tenues; las tarjetas se separan con `línea` o con espacio. **No se pide rol nuevo.**
- **La regeneración de `DESIGN.md` no puede ir al gate.** `design-md.py` vive en la caché del plugin, fuera del repositorio. Una prueba que lo invoque dependería de la máquina, y una que se salte sin él sería un verde falso. Se verifica en la integración manual (ver los criterios deducidos).

### Pregunta 1 — identificadores de token en ASCII

| Opción | Qué implica |
|---|---|
| **(a) Recomendada:** los identificadores de token van en ASCII (`linea`, `accion-fondo`, `accion-texto`, `accion-presionada`). `semantics.md` se re-deriva con esos nombres, y ADR-014 registra la decisión y su razón. | ADR-013 no se edita (no cambia de opinión: mismos roles, mismos valores). La prosa sigue en español con acentos; solo los identificadores cambian. De paso, s5.7 escribe `--accion-fondo` en CSS sin escapar nada. |
| (b) Mantener los acentos y aparcar el límite del generador | Ningún componente con acción ni con línea puede entrar en `DESIGN.md`, y s5.6 no se cumple (el botón es su componente principal). |
| (c) Copiar el generador al proyecto y cambiarle la expresión regular | Una segunda copia de un instrumento del addon, que es justo lo que el addon prohíbe. |

El límite del generador, más estrecho que el spec, va al parking lot como hallazgo del addon, igual que el de la columna `Variant`.

### Propuesta que necesita aprobación (paso `fitness`)

| # | Criterio | Eslabón | Estrato | From |
|---|----------|---------|---------|------|
| M1 | Ningún escalón asignado a un rol de lectura (`text`, `binomial`, `date`) queda bajo 16 px, y ningún par de escalones colapsa en uno al redondear | escala | `mechanical` (`comprobar-medidas.py piso`) | specimen (ADR-011) |
| M2 | Cada control declarado (botón, campo, enlace de navegación) mide al menos **44 × 44 px CSS**. Fuente: WCAG 2.2 SC 2.5.5 Target Size (Enhanced), AAA, leída el día que se mide | espaciado | `mechanical` (`comprobar-medidas.py objetivos --minimo 44`) | concept (ADR-010: "acciones grandes", "navegación al pulgar") |
| M3 | Todo valor es reproducible y referenciado: el script regenera las tablas de escala y espaciado idénticas, y en `DESIGN.md` `provenance` sale con 0 fuera de escala | los tres | `mechanical` | este eslabón |
| M4 | La escala se lee como una sola jerarquía con peso y espacio, y los componentes como una familia del Cuaderno de campo | escala, componentes | `judgement`: elección forzada sobre una lámina con la ficha de un ejemplar y el formulario de alta, a 360 px | concept (ADR-010) |

Aplicados del catálogo, no propuestos:
- `target-size`: WCAG 2.2 SC 2.5.8, 24 × 24, con `tokens.py targets` sobre `DESIGN.md`. M2 lo cubre por arriba, pero se corre igual.
- `contrast`: los pares `text` de los componentes, con `tokens.py pairs` y `contraste-de-lectura.py` a 7:1.
- `component-contrast`: medido en s5.5; aquí se cita.
- `provenance`.
- `minimum-size`: el piso de 16 px, que M1 comprueba.

`platform-specs`, `single-ink` y `prior-art` no aplican.

**Componentes propuestos** (los que las plantillas usan hoy):

| Componente | Compone |
|---|---|
| `pagina` | fondo, texto, escala de cuerpo |
| `tarjeta` | superficie, texto, relleno |
| `titulo`, `subtitulo` | texto sobre fondo, escalón de `h1` y de `h2` |
| `boton` | accion-fondo, accion-texto, escala de cuerpo, relleno, alto, ancho mínimo |
| `boton-presionado` | accion-presionada, accion-texto, mismas medidas (variante con nombre relacionado, como pide el spec) |
| `campo` | campo-fondo, texto, escala de cuerpo, relleno, alto, ancho |
| `enlace-navegacion` | enlace sobre fondo, alto, ancho |
| `aviso` | error sobre fondo, escala de cuerpo |
| `fecha` | texto-secundario sobre superficie, escala de cuerpo |

Los enlaces dentro de un párrafo quedan en la excepción *inline* de SC 2.5.8 y 2.5.5, dicha, no supuesta.

**Reglas candidatas** (sus parámetros se fijan en ADR-014 antes de correrlas):

- **Escala:**
  - (A) razón 1.25 desde 16, tres escalones.
  - (B) razón 1.5 desde 16, tres escalones.
  - (C) razón 1.2 desde 16 con `date` y `small` un escalón abajo, la costumbre de hacer más pequeñas las fechas. Se espera que rompa M1.
- **Espaciado:** la unidad como función de la altura de línea del cuerpo.
  - (A) unidad = altura de línea / 3, controles de 6 unidades.
  - (B) unidad = altura de línea / 2, controles de 4 unidades.
  - (C) unidad = altura de línea / 6, controles de 5 unidades ("compacto"). Se espera que rompa M2 y `target-size`.

## 3 · Interface / examples

```sh
uv run python scripts/derivar-medidas.py escala --base 16 --razon 1.25 --escalones 3 --roles "text=0,binomial=0,date=0,emphasis-h2=1,emphasis-h1=2"
# | Step | Size | Line height | Roles |
# |---|---|---|---|
# | 0 | 16px | 24px | text, binomial, date |
# …   exit 0; exit 2 con un parámetro ilegible, nombrándolo

uv run python scripts/comprobar-medidas.py piso governance/identity/ui/type-scale.md --piso 16
# 3 escalón(es) y 3 rol(es) de lectura medidos, 0 bajo el piso, 0 colapsados   → exit 0
# con (C): date → escalón -1 = 13px  necesita 16px  NO                          → exit 1

uv run python scripts/comprobar-medidas.py objetivos governance/identity/ui/DESIGN.md --minimo 44
# boton 48×48  campo …  3 objetivo(s) medidos, 0 bajo 44 px                    → exit 0
# con (C): boton 20 de alto  necesita 44  NO                                   → exit 1
# sin tabla Target: 0 objetivo(s) — nada que juzgar                            → exit 2

D=~/.claude/plugins/cache/gemba/gemba-design/0.21.0/skills/techniques/ui/scripts
python3 $D/design-md.py --spec-version alpha --name Orquídea --decision "ADR-013" --decision "ADR-014" \
  --gap "…bordes y foco: tokens de colors sin componente…" \
  governance/identity/ui/semantics.md governance/identity/ui/type-scale.md \
  governance/identity/ui/spacing.md governance/identity/ui/components.md > governance/identity/ui/DESIGN.md
# design-md: N token(s), 10 component(s), P pair(s), 3 target(s), 0 literal(s) in the prose, 1 `Component` table(s) ignored
```

```markdown
| Component | backgroundColor | textColor | typography | padding | height | width |
|---|---|---|---|---|---|---|
| boton | {colors.accion-fondo} | {colors.accion-texto} | {typography.step-0} | {spacing.step-2} | {spacing.step-6} | {spacing.step-6} |
```

## 4 · Acceptance criteria

- **Must:**
  - ADR-014 en `proposed` con M1–M4 aprobados, las reglas con sus parámetros y "respaldo: ninguno", antes de la primera escala.
  - Rojos vistos antes de producir:
    - M1 sobre la escala (C).
    - M2 y `target-size` sobre el espaciado (C).
    - `provenance` sobre un componente con literal.
    - La regeneración de las tablas sobre una edición a mano.
  - `DESIGN.md` generado con `--spec-version alpha`. `tokens.py pairs`, `targets` y `provenance`, más `comprobar-medidas.py objetivos --minimo 44`, salen en 0 con población distinta de cero.
- **Should:**
  - `survival-review` sobre las cuatro piezas.
- **Must NOT:**
  - Editar `DESIGN.md` a mano.
  - Un literal en una celda de componente.
  - Cambiar un valor de color.
  - Una segunda copia de `design-md.py` o de `tokens.py`.

### Deduced criteria

- Un escalón de lectura bajo el piso se ve en rojo: **confirmed**. La técnica lo pide como contraejemplo del eslabón, y `comprobar-medidas.py piso` es el instrumento.
- Regenerar `DESIGN.md` da el mismo archivo: **confirmed como comprobación de la integración manual, retracted como prueba del gate** (la parte "una prueba del gate lo comprueba" del *Done when* deducido). El generador vive fuera del repositorio, y una prueba que dependa de él o que se salte sin él no es honesta. Sí van al gate las tablas de escala y espaciado, que genera un script del proyecto.
- Ningún escalón de lectura bajo 16 px ni colapso: **confirmed**, es M1.
- Cada propiedad de un componente es una referencia: **confirmed**. `design-md.py` rechaza con exit 1 una celda que no es referencia.

### Stated criteria

Ninguno contradicho. La pregunta 1 no toca un criterio: toca los nombres que s5.5 produjo.
