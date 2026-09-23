# Story s5.3: Palette — Design

> Complexity: moderate

## 1 · What & why

**Problem:** la dirección (ADR-010) dice papel, tinta y un acento oscuro, y el encargo (ADR-009) exige 7:1 a todo texto normal; no existe todavía ningún valor, y s5.5 no puede derivar primitivas ni roles sin una paleta decidida.
**Value:** una paleta por roles con cada par de texto medido, que s5.5 convierte en rampas y roles por función, y una elección firmada frente a fotos reales de orquídeas.

## 2 · Approach

Técnica `color`: criterios de la pieza → **parada para aprobación** → ADR-012 en `proposed` con las candidatas → cada candidata en el formato de tablas de `contraste-de-lectura.py`, medida, y el rojo de la que viola visto → las candidatas junto a fotos reales de orquídeas para el juicio → elección firmada → `palette.md` → ADR-012 `accepted`.

**Components affected:**

- `records/decisions/adr-012-paleta.md`: create.
- `governance/identity/palette.md`: create.

**Legacy sweep:** nada — net-new.

### Lo que el recorrido encontró

- **Todo texto es "normal":** ADR-011 fija 16 px para todo; el umbral de texto grande (24 px, o 18.7 px en negrita) solo lo alcanzarían títulos que s5.6 ponga más grandes. Así que **cada** par de texto de la paleta, incluida la tinta suave de fechas y fuentes, necesita 7:1.
- **El acento no puede distinguir enlaces solo por color.** Con tinta casi negra y un acento oscuro que llegue a 7:1 sobre el papel, el acento contra la tinta queda muy por debajo de 3:1 (el mínimo de WCAG 1.4.1 para distinguir por color). Consecuencia para s5.6/s5.7, no para la paleta: los enlaces van subrayados.
- **Variante:** la identidad no declara ninguna (sin tema oscuro, rabbit hole del brief). `palette.md` lo dice, y el eslabón de roles de s5.5 reporta la relación como no comparada, no como pasada.
- **Instrumentos:** `scripts/contraste-de-lectura.py` lee `Role | Value` y `Foreground | Ground | Kind` (s5.1); `tokens.py pairs` del addon lee el mismo formato.
- **Fotos para juzgar:** el repositorio no tiene fotos de orquídeas (las de prueba son ruido fractal). Para el juicio se bajan al scratchpad dos o tres fotos con licencia libre (Wikimedia Commons) de especies del catálogo de colores fuertes (magenta, amarillo), nunca al repositorio.

### Propuesta que necesita aprobación (paso `fitness`)

| # | Criterio | Estrato | From |
|---|-----------|---------|------|
| P1 | Cada par de texto de la paleta (tinta, tinta suave, acento como texto, alerta como texto, sobre papel y sobre hoja) llega a ≥ 7:1 | `mechanical` | commission 2 |
| P2 | Junto a fotos reales de orquídeas de colores fuertes, ningún color de la paleta compite con la flor | `judgement` — elección forzada entre las candidatas, con las fotos | commission 3 (y S1 de ADR-010) |
| P3 | Se lee como papel y tinta: fondo neutro cálido, tinta casi negra, un solo acento; nada de marca | `judgement` | concept (ADR-010) |

**Roles propuestos** (los de la paleta; los roles por función los añade s5.5): `papel` (fondo), `hoja` (tarjeta sobre el papel), `tinta` (texto), `tinta suave` (fechas, fuentes, etiquetas), `renglón` (líneas y bordes), `acento` (enlaces y acciones), `alerta` (errores). Sin rol de éxito: la aplicación confirma redirigiendo, no con un mensaje verde.

**Candidatas** (se miden y se fijan después de la aprobación): tres, que varían el tono del papel y del acento dentro de la dirección — p. ej. papel cálido con acento azul tinta, papel blanco con acento sepia, papel gris frío con acento verde bosque.

## 3 · Interface / examples

```sh
uv run python scripts/contraste-de-lectura.py $S/candidata-a.md
uv run python scripts/contraste-de-lectura.py governance/identity/palette.md
```

```markdown
| Role        | Value   |
|-------------|---------|
| papel       | #…      |
| tinta suave | #…      |

| Foreground  | Ground | Kind |
|-------------|--------|------|
| tinta suave | papel  | text |
| renglón     | papel  | component |
```

## 4 · Acceptance criteria

- **Must:**
  - ADR-012 en `proposed` con P1–P3 y las candidatas antes de fijar un valor en el repositorio.
  - Cada candidata medida con `contraste-de-lectura.py`; la elegida sale con 0 y cuenta su población.
  - Siete roles con valor; pares declarados para todo texto sobre `papel` y sobre `hoja`.
  - La variante declarada como ninguna, con la consecuencia dicha.
- **Should:**
  - `renglón` sobre `papel` declarado como `component` para que s5.5 lo mida contra 3:1.
- **Must NOT:**
  - Un color saturado de marca.
  - Guardar las fotos de prueba en el repositorio.

### Deduced criteria

- `palette.md` trae las dos tablas legibles por ambos instrumentos y declara su variante o su ausencia: confirmed — el formato es el de `conventions/mechanical`, y la plantilla de la técnica pide la columna de variante.
