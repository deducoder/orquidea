# Story s5.4: Typography — Design

> Complexity: moderate

## 1 · What & why

**Problem:** la dirección (ADR-010) pide una sans ligera, cifras tabulares e itálica verdadera, y el encargo (ADR-009) le da a toda la identidad 50 KB; nada decide todavía si eso es la fuente del sistema o una fuente web, ni cuál es el tamaño más pequeño que se sostiene en el teléfono.
**Value:** un sistema tipográfico con roles, piso de legibilidad probado y licencia registrada, que s5.6 convierte en escala y s5.7 enlaza sin volver a decidir nada.

## 2 · Approach

Seguir la técnica `typography`: criterios de la pieza → **parada para aprobación** → ADR-011 en `proposed` con las opciones → medir cada opción y ver en rojo la que viola un criterio medible → leer el piso de legibilidad de su fuente y probarlo renderizando → elegir con el humano → `specimen.md` (y los archivos de la fuente si es web) → ADR-011 `accepted`.

**Components affected:**

- `records/decisions/adr-011-sistema-tipografico.md`: create.
- `governance/identity/specimen.md`: create.
- `src/orquidea/web/static/identidad/` (fuentes `woff2` y su `OFL.txt`): create, **solo si** gana una fuente web.

**Legacy sweep:** nada — net-new.

### Lo que el recorrido encontró

- **No hay ninguna fuente enlazada hoy**: el navegador usa su serif por defecto (Times en escritorio, Noto Serif en Android). Cualquier opción cambia lo que se ve.
- **La CSP** (`default-src 'self'`) obliga a servir una fuente web desde `/static`; Google Fonts por CDN queda fuera.
- **El texto que más exige:** nombres científicos en `<i>` (100 binomios), nombres comunes en otras lenguas (*Tzauhxilotl*), citas largas con URL, fechas `AAAA-MM-DD` en listas de riegos y floraciones (hasta 500 por ficha), y `<small>` para fechas y fuentes.
- **Instrumentos disponibles:** `scripts/medir-primera-carga.py --identidad DIR` para el peso (s5.1); `uv run --with fonttools` para leer glifos y rasgos (`ital`, `tnum`) de un archivo sin agregar una dependencia; Pillow ya está en el proyecto para renderizar a un tamaño dado.
- **Hallazgo heredado de s5.2:** qué familias e itálicas trae cada sistema se verifica con una fuente citada, no se supone.

### Propuesta que necesita aprobación (paso `fitness`)

| # | Criterio | Estrato | From |
|---|-----------|---------|------|
| T1 | Las fuentes de la identidad pesan ≤ 40 KB en gzip, lo que deja ≥ 10 KB de los 50 para el CSS | `mechanical` | commission 1 |
| T2 | Los nombres científicos se ven en itálica verdadera (no oblicua sintética) y todos los glifos del español de México (á é í ó ú ü ñ ¿ ¡ « » — y sus mayúsculas) existen en el estilo que los usa | `mechanical` en una fuente web (se lee el archivo) · `read:` en una del sistema | esta pieza (el criterio 4 que ADR-009 dejó a `typography`) |
| T3 | Las fechas se alinean en columna: la familia trae cifras tabulares | `mechanical` en una fuente web · `read:` en una del sistema | concept (Cuaderno de campo: "cifras tabulares para las fechas") |
| T4 | La licencia permite servirla desde el propio servidor y recortarla a un subconjunto, sin costo | `read:` | esta pieza |

**Opciones en juego** (se miden después de la aprobación, no antes):

- **(A) Pila de fuentes del sistema** (`system-ui`, San Francisco, Roboto, Segoe UI…): 0 KB; lo que se ve depende del teléfono.
- **(B) Atkinson Hyperlegible**: diseñada para lectores con baja visión; OFL.
- **(C) IBM Plex Sans**: con cifras tabulares y aire de documento técnico; OFL.
- **(D) Source Sans 3**: sans humanista de texto muy probada; OFL.

## 3 · Interface / examples

```sh
# peso real de una opción web (subconjunto latino, woff2)
uv run python scripts/medir-primera-carga.py --identidad $S/opcion-b
# glifos y rasgos de un archivo
uv run --with fonttools python -c "from fontTools.ttLib import TTFont; f=TTFont('$S/opcion-b/regular.woff2'); print('tnum' in {r.FeatureTag for r in f['GSUB'].table.FeatureList.FeatureRecord}, all(ord(c) in f.getBestCmap() for c in 'áéíóúüñ¿¡«»—ÁÉÍÓÚÜÑ'))"
```

Rojo esperado en el contraejemplo de T1: una opción cuyos cuatro estilos (regular, itálica, negrita, negrita itálica) pasen de 40 KB.

## 4 · Acceptance criteria

- **Must:**
  - ADR-011 en `proposed` con T1–T4 y las cuatro opciones antes de descargar ningún archivo al repositorio.
  - El peso de cada opción web medido con `--identidad` sobre sus archivos reales; los glifos y `tnum` leídos del archivo; lo del sistema, con la fuente citada y su fecha.
  - El piso de legibilidad leído de la literatura en el momento de producir, con su fuente y fecha, y probado renderizando a ese tamaño.
  - La licencia de cada familia elegida en el espécimen.
- **Should:**
  - Si gana una fuente web, sus archivos entran ya recortados y con su `OFL.txt` al lado.
- **Must NOT:**
  - Copiar una cifra de legibilidad de la técnica o de la memoria sin leer su fuente.
  - Enlazar la fuente o escribir CSS (s5.7).
  - Fijar la escala de la interfaz (s5.6).

### Deduced criteria

- Una opción web que viola el tope se mide con `--identidad` y se ve en rojo antes de elegir: confirmed — el instrumento existe (s5.1) y T1 lo usa con un tope de 40 KB para las fuentes; el tope de 50 KB del instrumento sigue siendo el del encargo, y los 40 se comparan sobre su salida.
- Si hay fuente web, `--identidad` sobre `static/identidad` sale con 0: confirmed.
