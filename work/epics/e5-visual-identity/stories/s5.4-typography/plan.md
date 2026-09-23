# Story s5.4: Typography — Plan

> Size: M
> Pause: none (default) — salvo la parada del ciclo para la elección firmada por el humano

Aprobación del humano (2026-09-22, en sesión): T1–T4 y las opciones (A) sistema, (B) Atkinson Hyperlegible, (C) IBM Plex Sans y (D) Source Sans 3, tal como las propone el diseño.

## Container acts around the tasks

- **A0 · Abrir ADR-011** (`record-open`): T1–T4 con estrato y origen, las cuatro opciones, la rejilla por llenar y `## Decision` sin resolver. Commit `docs(s5.4): add ADR-011`.
- **A1 · Medir las opciones y responder el contraejemplo** (`counterexample`), en el scratchpad y nunca en el repositorio: descargar el subconjunto latino `woff2` de regular, itálica, negrita y negrita itálica de (B), (C) y (D) desde `cdn.jsdelivr.net/npm/@fontsource/…`; medir con `--identidad` (T1, rojo si pasa de 40 KB); leer glifos es-MX, `ital` y `tnum` con `fonttools` (T2, T3); leer las licencias (T4); leer qué familias e itálicas trae cada sistema para (A), con fuente y fecha. Leer el piso de legibilidad de la literatura, con fuente y fecha. Todo a la rejilla. Commit `docs(s5.4): update ADR-011`.
- **A2 · Completar ADR-011** tras la elección firmada y el espécimen. Commit `docs(s5.4): publish ADR-011`.

## Tasks

### T1 · Probar el piso de legibilidad renderizando

- Renderizar con Pillow, a la densidad de un teléfono (3×), el texto más exigente (un binomio en itálica, una fecha, una cita) al tamaño del piso leído en A1 y un paso debajo, con la opción que gane o con las finalistas; la imagen queda en el scratchpad y se le muestra al humano.
- **Verify:** la imagen existe y se ve; la prueba en papel no aplica (la aplicación no se imprime) y el espécimen lo dice.
- Sin commit: su producto es la fila del piso en el espécimen.

### T2 · Escribir el espécimen (y los archivos de la fuente, si es web)

- **Files:** create `governance/identity/specimen.md` desde `skills/techniques/typography/assets/specimen.md` (gemba-design 0.21.0); si gana una fuente web, create `src/orquidea/web/static/identidad/fuentes/*.woff2` y `OFL.txt`.
- **TDD:** no aplica — documento y archivos binarios de terceros; el peso lo comprueba `--identidad` y el gate cubre el resto.
- **Mold:** `skills/techniques/typography/assets/specimen.md`; `governance/identity/concept.md`.
- **Verify:** `decision: ADR-011`; roles, piso con fuente y fecha, licencia, una fila por cada criterio del catálogo en su orden, T1–T4 con `ran:`/`read:`/`judged:`; si hay fuente web, `uv run python scripts/medir-primera-carga.py --identidad src/orquidea/web/static/identidad` sale con 0 y los archivos de fuente suman ≤ 40 KB; then `./scripts/check`.
- **Parada:** la elección y la mitad juzgada son del humano; se escribe después de su respuesta, o `unsigned`.
- **Commit:** docs(identity): add the type specimen (y `feat(identidad): add the text typeface` aparte si hay archivos de fuente)

### T3 · Prueba de integración manual del orden

- **Verify:** `add ADR-011` antes de `update ADR-011`, este antes de T2, `publish ADR-011` al final; `status: accepted`.

## Order & risks

- **Execution order:** A0 → A1 → T1 → (elección) → T2 → A2 → T3.
- **Risks:**
  - Afirmar qué trae un sistema sin fuente (pasó en s5.2) → cada fila de (A) cita su documento y fecha, o dice `read: unverified`.
  - El subconjunto de Fontsource no es el que se serviría → se mide exactamente el archivo que entraría al repositorio.
