# Story s5.2: Concept — Design

> Complexity: simple

## 1 · What & why

**Problem:** la paleta (s5.3) y la tipografía (s5.4) se van a juzgar contra los criterios del encargo, pero nada dice todavía qué apuesta comparten. Si cada una toma su propia dirección, pueden cumplir cada una su criterio y aun así verse como dos aplicaciones distintas.
**Value:** una dirección elegida y firmada, con las descartadas respondidas por el criterio que no cumplieron, da a s5.3 y s5.4 una apuesta común de la que derivar, y deja escrito por qué no se eligió otra.

## 2 · Approach

Seguir la técnica `concept` de gemba-design 0.21.0: proponer los criterios de selección derivados de ADR-009 y el número de direcciones, **parar para la aprobación**, abrir ADR-010 en `proposed` con ambos, desarrollar las direcciones como apuestas verbales, elegir contra los criterios, escribir `concept.md` y completar el ADR.

**Components affected:**

- `records/decisions/adr-010-direccion-de-la-identidad.md`: create — `add` en `proposed`, `update` si hace falta, `publish` en `accepted`.
- `governance/identity/concept.md`: create — desde `assets/concept.md` de la técnica.

**Legacy sweep:** nada — net-new; ningún código cambia.

### Lo que el recorrido encontró y la dirección tiene que vestir

- **Diez pantallas, ninguna decorativa:** la lista de especies (100 nombres científicos con búsqueda), la ficha de especie (descripción, cuatro cuidados con su **fuente citada larga**, lista de fuentes), "Mi colección" (miniaturas de 96 px, fechas, último riego), la ficha del ejemplar (foto, riegos y floraciones con fecha, formularios), el acceso y las altas y bajas.
- **El catálogo no tiene fotos:** las únicas imágenes son las del usuario. Lo único saturado que la aplicación muestra son sus plantas.
- **El texto es de consulta:** nombres científicos en itálica (`<i>`), nombres comunes en otras lenguas (p. ej. *Tzauhxilotl*), citas con URL y fecha de consulta, fechas `AAAA-MM-DD`. Se parece más a una libreta de registro y a una obra de referencia que a una tienda.
- **Restricciones que la dirección hereda sin decidirlas:** ≥ 7:1 en todo el texto normal (criterio 2), ≤ 50 KB de CSS y fuentes (criterio 1), una sola paleta y ningún logotipo (brief de e5).

### Propuesta que necesita aprobación (paso `fitness`)

**Criterios de selección** — la dirección que gane debe cumplirlos todos:

| # | Criterio | Estrato | From |
|---|-----------|---------|------|
| S1 | Deja la foto del ejemplar como lo único saturado de la pantalla: su firma vive en fondos, tinta y estructura, no en color de marca | `judgement` | commission 3 |
| S2 | Conserva su carácter con texto a ≥ 7:1 y con fuentes del sistema o una sola familia ligera: no depende de medios tonos, de texturas en imagen ni de una fuente de exhibición | `judgement` | commission 1 y 2 |
| S3 | Se lee como una herramienta de registro y consulta (fuentes citadas, fechas, nombres científicos), no como una tienda ni una red social | `judgement` | esta selección |

**Número de direcciones: 3.** Se declara antes de desarrollar ninguna. Con dos, la elección se parece demasiado a "esta o la otra"; con cuatro o más, cada firma cuesta más de lo que añade para una aplicación de un solo usuario.

## 3 · Interface / examples

La forma de una dirección, antes de desarrollarla (sin valores):

```markdown
| Direction | What it bets on | Where it loses |
|-----------|-----------------|----------------|
| {nombre} | {la apuesta, en una línea} | {S{n}: cómo — o `—` si es la elegida} |
```

Una descartada bien respondida: `falla S1: su fondo verde hoja compite con los amarillos de Oncidium y con los verdes de la propia planta`. Una mal respondida, que la técnica rechaza: `no convenció`, `6/10`.

## 4 · Acceptance criteria

- **Must:**
  - ADR-010 commiteado en `proposed`, con S1–S3, sus estratos y su origen, y el número 3, antes del primer commit que desarrolle una dirección.
  - Tres direcciones desarrolladas, ni una más ni una menos.
  - Cada descartada con el criterio que falló, por su número; ninguna puntuación, ranking ni calificación en ningún archivo.
  - La elección firmada por el humano o escrita `unsigned`.
- **Should:**
  - Cada dirección dice qué implicaría para el color y para el tipo, sin fijar valores, para que s5.3 y s5.4 puedan derivar de ella.
- **Must NOT:**
  - Fijar un color, una familia o un tamaño.
  - Desarrollar una dirección antes de la aprobación de S1–S3 y del número.
  - Firmar la elección por el humano.

### Deduced criteria

- Un criterio de selección sin oráculo se responde "no aplica: no hay oráculo", con su razón: confirmed — S1, S2 y S3 son `judgement`; ninguno tiene comprobación, y el paso `counterexample` se responde así para los tres.
- El mismo ADR pasa a `accepted`, mismo archivo y mismo número: confirmed — paso `record-complete` y etapa 2 de la técnica `adr`; el número siguiente libre es 010.
