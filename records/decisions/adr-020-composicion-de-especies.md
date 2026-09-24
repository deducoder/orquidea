---
type: adr
id: ADR-020
title: "El peso de la escala y la composición de la pantalla Especies"
status: accepted
date: 2026-09-24
epic: —
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-020: El peso de la escala y la composición de la pantalla Especies

## Status

Accepted, 2026-09-24.

## Context

**La pregunta:** ¿cómo se compone S1 Especies entre dos candidatos generados? Y antes, ¿qué peso declara cada paso de la escala, para que el generador pueda dibujar una página?

Historia s5, standalone. Tiene dos piezas:

- **Pesos**, del eslabón `ui`. `page.py` de gemba-design 0.24.0 rechaza todo paso tipográfico sin `fontWeight`. Con el `DESIGN.md` de s1 salen cuatro rechazos (sonda de la sesión). El peso ya está decidido en `governance/identity/specimen.md:26-27`: `text` 400 y `emphasis` 700 para `h1` y `h2`. En 0.23.0 el formato no lo componía (`type-scale.md:81`, y el `--gap` de ADR-016). En 0.24.0, `design-md.py` lee una columna `Font weight` en la escala. Aquí no se elige nada: el valor se lee del espécimen, y por eso no hay opciones.
- **Composición de S1**, el quinto eslabón de la técnica `screens`, con la guía de ADR-018 (S1: rango 1 la búsqueda, rango 2 las especies que coinciden) y el patrón de ADR-019 (S1 `list-detail`). Hay dos candidatos declarados antes de producir el primero.

**Lo que trajo producir los pesos**, en `c521f89`:

- `derivar-medidas.py escala` acepta `--pesos` y emite `Font weight`. `comprobar-medidas.py piso` lee `Roles` por su encabezado. Los dos cambios tienen su prueba, que se vio en rojo primero.
- `DESIGN.md`, regenerado con 0.24.0, trae además una tabla `Target` que el generador saca de los mínimos declarados (4 controles de 48 × 48). También quita el Known Gap que decía que un mínimo declarado nunca se medía. `comprobar-medidas.py objetivos` cuenta ahora 8: los mismos 4 controles como tabla y como mínimo, que cuentan juntos, como decidió s1. `test_identidad_ui.py` lo dice.
- `7053e36` hace lo mismo con la familia: `--familia` en `derivar-medidas.py`, con su prueba en rojo primero; la columna `Font family` (`specimen.md:19`); `DESIGN.md` regenerado, idéntico en dos corridas; y `--typography-step-N-font-family` en `:root`. `--familia`, la propiedad de `identidad.css` que pinta el cuerpo, se queda: la prueba del espécimen la lee. Los dos nombres tienen el mismo valor, y la cadena lo comprueba.
- `identidad.css` declara los tres pesos en `:root`, porque la cadena hoja ↔ `DESIGN.md` de s1 lo exige, y `h1`/`h2` los citan con `var()`. Los `700` de `strong`, `dt` y el aviso siguen como literal admitido: son el rol `emphasis` del espécimen, no un paso de la escala. El render no cambia.

S3 y S4 no se componen: `page.py` no dibuja imágenes, y su rango 1 es la foto. Está aparcado (`7602e44`).

### Criterios de supervivencia, aplicados

| Criterio | Pesos | Página de S1 |
|---|---|---|
| `platform-specs` | no aplica: no hay marca | no aplica: no hay marca |
| `minimum-size` | no aplica: el tamaño no cambia; el piso de 16 px lo midió el espécimen (ADR-011) | no aplica, por la misma razón: la página usa los pasos de la escala |
| `single-ink` | no aplica: no hay marca | no aplica: no hay marca |
| `contrast` | no aplica: el peso no cambia los pares | aplica: cada texto sobre el fondo donde cae, lo mide `page.py` (piso 4.5:1) |
| `prior-art` | no aplica | no aplica |
| `component-contrast` | no aplica | aplica: el borde del campo (`campo-borde` sobre su contenedor), ya medido como par de componente en s1; la página no agrega pares nuevos de componente |
| `target-size` | no aplica | aplica: botón, campo y enlaces declaran `minHeight`/`minWidth` de `spacing.step-6` (48 px), como en ADR-016 |
| `provenance` | aplica: cada peso cita `specimen.md` | aplica: el control de literales de `page.py` rechaza todo valor que no venga de un token o de un parámetro declarado |
| `focus-visible` | no aplica | aplica, pero sin mitad con script: ningún componente tiene variante `-focus`, así que el censo deja cada control al foco del navegador. Se juzga tabulando la página |

### Criterios de fitness, aprobados

Aprobados por Daniel Efraín Domínguez Urbina el 2026-09-24.

| # | Criterio | Pieza | De dónde | Estrato | Qué lo decide |
|---|---|---|---|---|---|
| W1 | Cada paso tipográfico declara el peso y la familia que le da `specimen.md` (`step-0` 400; `step-1` y `step-2` 700; la pila de `specimen.md:19` en los tres), `page.py` deja de rechazar por `fontWeight` y la página generada escribe esa `font-family` | pesos y familia | commission 2, vía el espécimen | `mechanical` | `design-md.py`, después `page.py` sobre el candidato A, y `grep` de `font-family` en su página |
| K1 | Cada texto que la página dibuja llega a 7:1 sobre el fondo donde cae | página | commission 2 | `mechanical` | el comando de K1 (abajo), cuya salida lee `scripts/contraste-de-lectura.py` |
| K2 | `page.py` genera la página sin ningún rechazo: pesos por rango, contraste, literales y los rangos de la guía | página | de este eslabón | `mechanical` | `page.py`, exit 0, y su censo |
| K3 | Lo más importante de la página es la búsqueda (rango 1 de la guía), y el candidato elegido gana contra S1, S2 y S3 de `concept.md` (ADR-010) | página | concepto | `judgement` | las dos preguntas del dueño, en orden. Él firmó la guía, así que ya conoce la respuesta de la primera |

**El comando de K1.** Lee la composición y el `DESIGN.md`, y escribe en la salida estándar una tabla `Foreground | Ground | Kind` con un par por texto dibujado. La lee `contraste-de-lectura.py`, que sale 0 si todos llegan a 7:1, 1 si alguno no, y 2 si no hay pares. El fondo sigue la regla "box or text" del encabezado de `page.py`:

- un componente con `padding` es su propio fondo;
- uno sin `padding` cae en el fondo de la fila que lo contiene, o en el de la página;
- la etiqueta de un `input` usa el color y el fondo de su contenedor;
- una fila sin contenido no dibuja texto.

```sh
python3 - DESIGN.md COMPOSITION.md <<'EOF' > PARES.md
import re, sys
def front(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    end = lines.index('---', 1)
    tree, stack = {}, []
    for line in lines[1:end]:
        if not line.strip():
            continue
        depth = (len(line) - len(line.lstrip())) // 2
        key, _, val = line.strip().partition(':')
        stack = stack[:depth] + [key]
        node = tree
        for k in stack[:-1]:
            node = node.setdefault(k, {})
        node[key] = val.strip().strip('"') if val.strip() else {}
    return tree
d = front(sys.argv[1])
def color(ref):
    return d['colors'][re.match(r'^\{colors\.(.+)\}$', ref).group(1)]
text = open(sys.argv[2], encoding='utf-8').read()
page = re.search(r'^page: (.+)$', text, re.M).group(1).strip()
rows, inside = [], False
for line in text.split('\n'):
    if line.strip() == '## The composition':
        inside = True
        continue
    if inside and line.startswith('#'):
        break
    if inside and line.startswith('|'):
        c = [x.strip() for x in line.strip().strip('|').split('|')]
        if re.match(r'^[A-Z]+\d+$', c[0]):
            rows.append(c)
comp = lambda r: d['components'][page if r[3] in ('', '—', '-') else r[3]]
by_id = {r[0]: r for r in rows}
def container(r):
    return comp(by_id[r[6]]) if r[6] not in ('', '—', '-') else d['components'][page]
print('| Foreground | Ground | Kind |\n|---|---|---|')
n = 0
for r in rows:
    if r[4] in ('', '—', '-'):
        continue
    if r[2] == 'input':
        print(f"| {color(container(r)['textColor'])} | {color(container(r)['backgroundColor'])} | text |")
        n += 1
    ground = comp(r)['backgroundColor'] if 'padding' in comp(r) else container(r)['backgroundColor']
    print(f"| {color(comp(r)['textColor'])} | {color(ground)} | text |")
    n += 1
print(f'{n} pares de texto', file=sys.stderr)
EOF
uv run python scripts/contraste-de-lectura.py PARES.md
```

### Los candidatos

Dos, declarados antes de producir el primero. Los dos llevan `screen: S1`, `page: pagina` y `lang: es-MX`, y usan la guía y el patrón de arriba. Los parámetros comunes son `margin` = `{spacing.step-2}` y `border-width` = `1px`, el trazo del borde del campo según ADR-015 y ADR-016. El contenido es real: el título y los controles salen de `especies.html`, y las especies son las tres primeras del catálogo.

**A, en la página**, con `gap` = `{spacing.step-2}`:

| Id | Rank | Element | Component | Content | From | Within |
|----|------|---------|-----------|---------|------|--------|
| C1 | 1 | h1 | titulo | Especies | src/orquidea/web/templates/especies.html:4 | — |
| C2 | 1 | input | campo | Buscar especies | src/orquidea/web/templates/especies.html:7 | — |
| C3 | 1 | button | boton | Buscar | src/orquidea/web/templates/especies.html:10 | — |
| C4 | 2 | a | enlace-navegacion | Arpophyllum giganteum | src/orquidea/datos/catalogo/arpophyllum-giganteum.json:3 | — |
| C5 | 2 | a | enlace-navegacion | Aulosepalum hemichrea | src/orquidea/datos/catalogo/aulosepalum-hemichrea.json:3 | — |
| C6 | 2 | a | enlace-navegacion | Barkeria skinneri | src/orquidea/datos/catalogo/barkeria-skinneri.json:3 | — |

**B, en tarjetas**, con `gap` = `{spacing.step-1}`: la búsqueda en una `tarjeta` y los resultados en otra.

| Id | Rank | Element | Component | Content | From | Within |
|----|------|---------|-----------|---------|------|--------|
| C1 | 1 | h1 | titulo | Especies | src/orquidea/web/templates/especies.html:4 | — |
| C2 | 1 | section | tarjeta | — | — | — |
| C3 | 1 | input | campo | Buscar especies | src/orquidea/web/templates/especies.html:7 | C2 |
| C4 | 1 | button | boton | Buscar | src/orquidea/web/templates/especies.html:10 | C2 |
| C5 | 2 | section | tarjeta | — | — | — |
| C6 | 2 | a | enlace-navegacion | Arpophyllum giganteum | src/orquidea/datos/catalogo/arpophyllum-giganteum.json:3 | C5 |
| C7 | 2 | a | enlace-navegacion | Aulosepalum hemichrea | src/orquidea/datos/catalogo/aulosepalum-hemichrea.json:3 | C5 |
| C8 | 2 | a | enlace-navegacion | Barkeria skinneri | src/orquidea/datos/catalogo/barkeria-skinneri.json:3 | C5 |

### La rejilla

| Criterio | Estrato | A | B |
|---|---|---|---|
| W1 — peso y familia del espécimen; ningún rechazo por `fontWeight`; la página escribe la familia | `mechanical` | sí — peso en `c521f89` (`0` 400, `1` 700, `2` 700, ningún rechazo); familia en `7053e36`: la página escribe `font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif` | sí — el mismo `DESIGN.md`, la misma `font-family` |
| K1 — 7:1 en cada texto | `mechanical` | sí — `7 par(es) de texto juzgado(s), 0 bajo el umbral`, exit 0 | sí — `7 par(es) de texto juzgado(s), 0 bajo el umbral`, exit 0 |
| K2 — `page.py` exit 0 | `mechanical` | sí — `6 rows in 2 ranks, 4 components, 0 representative, 3 parameters, 0 literals outside a token; ranks 25 ≥ 16 px; 7 texts on their ground, all ≥ 4.5:1; 5 focusable, 0 ring …, 5 on the browser's focus, not measured` | sí — `8 rows in 2 ranks, 5 components, …; 7 texts on their ground, all ≥ 4.5:1; 5 focusable, … 5 on the browser's focus, not measured` |
| K3 — lo más importante es la búsqueda; elección contra S1, S2 y S3 del concepto | `judgement` | pregunta 1: la búsqueda; **elegido** contra S1, S2 y S3 — Daniel Efraín Domínguez Urbina, 2026-09-24 | pregunta 1: la búsqueda; perdió la elección forzada — Daniel Efraín Domínguez Urbina, 2026-09-24 |

### El rojo de los criterios medibles

Sondas en el scratchpad de la sesión. Los candidatos se extrajeron de las tablas de arriba y el comando de K1 de este archivo, así que lo que corrió es lo que está escrito. Una primera extracción del candidato A arrastró las filas de B (12 filas) y dio un rechazo de contención que no es el de W1. Se descartó, se corrigió la extracción (6 filas en A, 8 en B) y se repitió.

- **W1, rojo:** el candidato A con el `DESIGN.md` de s1.
  ```
  refused: step-0 (used by pagina) declares no fontWeight — every step the page uses declares its weight
  refused: step-2 (used by titulo) declares no fontWeight — every step the page uses declares its weight
  refused: step-0 (used by campo) declares no fontWeight — …
  refused: step-0 (used by boton) declares no fontWeight — …
  refused: step-0 (used by enlace-navegacion) declares no fontWeight — …
  ```
  exit 1.
- **W1, la familia, rojo** (W1 creció el 2026-09-24, con la aprobación del dueño, cuando las capturas de los candidatos salieron en Times): la página del candidato A generada con el `DESIGN.md` de `c521f89` tiene **0** apariciones de `font-family`. El navegador pone su letra por defecto, una serif, y no la pila de sistema de `specimen.md:19`. Sonda: con una columna `Font family` en una copia de la escala, `design-md.py` sale 0 y la página escribe `font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif`.
- **K2, rojo:** el candidato A sin sus filas de rango 2: `refused: rank 2 of S1 has no row in the composition`, exit 1.
- **K1, rojo:** una copia del `DESIGN.md` con un componente `tenue` (`textColor` `línea`), y el candidato A con una especie pintada con él: `#8C8475 sobre #F7F3EA (texto): 3.34:1 necesita 7:1 NO`, `7 par(es) de texto juzgado(s), 1 bajo el umbral`, exit 1. Control: el candidato A tal cual da `7 par(es) de texto juzgado(s), 0 bajo el umbral`, exit 0 (la etiqueta y el texto del campo cuentan por separado). Una composición sin filas da `0 par(es) de texto juzgado(s) — nada que juzgar`, exit 2.

## Decision

1. **La escala declara `Font family` y `Font weight`** tal como los da `specimen.md` (`c521f89`, `7053e36`), y `DESIGN.md` se genera con el comando de ADR-016 más `--decision "ADR-020: el peso y la familia de cada paso de la escala"` y sin el `--gap` del peso. Sale idéntico en dos corridas.
2. **S1 Especies se compone con el candidato A**, en la página y sin cajas, en `governance/identity/ui/screens/composition-s1.md`. Su página generada es `composition-s1.html`. Lo eligió Daniel Efraín Domínguez Urbina el 2026-09-24:
   - pregunta 1: la búsqueda, en los dos candidatos;
   - elección forzada: A, con una razón por principio, redactadas por el agente y elegidas por el dueño;
   - foco al tabular: se ve y nada lo tapa.

## Consequences

- `page.py` ya puede generar cualquier pantalla con este `DESIGN.md`: el peso y la familia dejan de ser un Known Gap. Las cifras tabulares siguen fuera del formato.
- `derivar-medidas.py` y `comprobar-medidas.py` leen y escriben las columnas opcionales de la escala. El refactor de los lectores de tablas que está aparcado sigue abierto: aquí solo se tocó lo mínimo.
- `identidad.css` cambia de nombres y no de render: los tokens de peso y familia en `:root`, y `h1`/`h2` con `var()`.
- `especies.html` no cambia. La composición elegida es casi la plantilla de hoy (título, campo, botón y lista sobre el fondo), así que llevarla al producto es trabajo pequeño, para otra historia.
- S2 falta componerla. S3 y S4 esperan a que el generador pueda dibujar la foto (parking lot).

## Alternatives considered

- **Candidato B, en tarjetas:** mide igual (K1 7 de 7, `page.py` exit 0) y da la misma respuesta a la pregunta 1. Perdió la elección forzada: en S1, las tarjetas blancas ponen un plano más entre el fondo y la tinta; en S3, a 360 px se ajustan a su contenido y no usan todo el ancho.
- **Juzgar con la letra por defecto del navegador:** rechazado por el dueño cuando las capturas salieron en Times. Por eso W1 creció a peso y familia.
