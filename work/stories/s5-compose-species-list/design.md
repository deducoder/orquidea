# Story s5: Compose species list — Design

Registro: ADR-020, en `proposed` desde `fecd977`, con su rojo en `f85d373`.

## 1 · What & why

**Problema:** ninguna pantalla de la cadena `screens` tiene página generada. Con el `DESIGN.md` de s1, `page.py` no puede generar ninguna, porque los pasos tipográficos no declaran su peso.

**Valor:** la escala declara el peso que ya decidió el espécimen, y S1 Especies sale como la primera página generada, medida a 7:1 y elegida entre dos candidatos contra el concepto.

## 2 · Approach

- **Pesos:** columna `Font weight` en `governance/identity/ui/type-scale.md` (`0` 400, `1` 700, `2` 700, citando `specimen.md:26-27`), y `DESIGN.md` regenerado con el comando de ADR-016 más un `--decision` de ADR-020 y sin el `--gap` del peso.
- **Composición:** `governance/identity/ui/screens/composition-s1.md` con el candidato elegido, y su página generada.

### Recorrido

- `type-scale.md`: tabla `Step | Size | Line height | Roles`. La plantilla de 0.24.0 pide `Font weight` antes de `Roles that take it`.
- `specimen.md:26-27`: `text` 400 y `emphasis` 700 (`h1`, `h2`). `subtitulo` es `h2`, así que `step-1` va a 700. `binomial` y `date` son 400 en `step-0`.
- `identidad.css` ya pinta 700 en títulos (líneas 90, 97, 120 y 178): no cambia.
- `especies.html` y el catálogo: el contenido de los candidatos, con cita.
- **Parking lot:** revisé las promociones al diseñar. La entrada de fuentes largas es de S2, no de S1, y no se cumple.
- **Legacy sweep:** se quita el `--gap` del peso de ADR-016, porque el formato ya lo compone. Nada más queda huérfano.

### Nombre del entregable

La convención de entregables fija el directorio (`ui/screens/`) y la técnica fija la plantilla. Con una composición por pantalla, el archivo lleva la pantalla en el nombre: `composition-s1.md`, y la página, `composition-s1.html`.

## 3 · Interface / examples

```sh
PG=~/.claude/plugins/cache/gemba/gemba-design/0.24.0/skills/techniques/screens/scripts/page.py; D=governance/identity/ui/screens
python3 $PG --design governance/identity/ui/DESIGN.md --guide $D/priority-guide.md --pattern $D/screen-pattern.md $D/composition-s1.md > $D/composition-s1.html
# esperado: page: S1 (list-detail), … all ≥ 4.5:1 …, exit 0
```

## 4 · Acceptance criteria

### Deduced criteria

- Rojo antes de producir: confirmado (`f85d373`).
- ADR `accepted`, mismo archivo: confirmado.
- `./scripts/check` verde: confirmado. Las pruebas de tokens leen `DESIGN.md`, así que se corre después de regenerarlo.

### Scenarios (delta over the scope)

- **MUST:** `DESIGN.md`, regenerado dos veces, sale idéntico.
- **MUST NOT:** tocar `especies.html` ni `identidad.css`.
