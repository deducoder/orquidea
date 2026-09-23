# Story s5.3: Palette — Plan

> Size: S
> Pause: none (default) — salvo la parada del ciclo para la elección firmada por el humano

Aprobación del humano (2026-09-22, en sesión): P1–P3, los siete roles (`papel`, `hoja`, `tinta`, `tinta suave`, `renglón`, `acento`, `alerta`) y bajar al scratchpad fotos con licencia libre para juzgar P2.

## Container acts around the tasks

- **A0 · Abrir ADR-012**: P1–P3, roles, tres candidatas descritas sin valores, `## Decision` sin resolver. `docs(s5.3): add ADR-012`.
- **A1 · Candidatas con valores, medidas, y contraejemplo**: cada candidata en tablas `Role | Value` y `Foreground | Ground | Kind` en el scratchpad, medida con `contraste-de-lectura.py` (salida literal); el rojo de P1 visto sobre un sujeto que lo viola; P2 y P3 "no aplica: no hay oráculo". `docs(s5.3): update ADR-012`.
- **A2 · Completar ADR-012** tras la elección y `palette.md`. `docs(s5.3): publish ADR-012`.

## Tasks

### T1 · Lámina de juicio para P2 y P3

- Bajar al scratchpad 2–3 fotos de Wikimedia Commons con licencia libre, de especies del catálogo de colores fuertes; componer, con Pillow, una tarjeta de ejemplar por candidata (papel, hoja, foto a todo el ancho, binomio, fecha, enlace) en Roboto a 16 px y 3×; mostrarlas al humano con su licencia y autor.
- **Verify:** las imágenes existen y se ven; cada foto tiene su licencia y autor anotados; nada de esto entra al repositorio.
- Sin commit.

### T2 · Escribir la paleta

- **Files:** create `governance/identity/palette.md` desde `skills/techniques/color/assets/palette.md` (gemba-design 0.21.0).
- **TDD:** no aplica — documento; la comprobación de P1 corre sobre él.
- **Mold:** la plantilla; `governance/identity/specimen.md`.
- **Verify:** `uv run python scripts/contraste-de-lectura.py governance/identity/palette.md` sale con 0 y cuenta ≥ 10 pares; variante declarada como ninguna con su consecuencia; una fila por criterio del catálogo; mitad juzgada firmada o `unsigned`; then `./scripts/check`.
- **Parada:** la elección y la firma son del humano.
- **Commit:** docs(identity): add the palette

### T3 · Prueba de integración manual del orden

- **Verify:** `add` → `update` → T2 → `publish`, por fecha de autor; `status: accepted`.

## Order & risks

- **Execution order:** A0 → A1 → T1 → (elección) → T2 → A2 → T3.
- **Risks:** una foto sin licencia clara → solo Wikimedia Commons con licencia en la página del archivo, anotada; escribir una salida sin correrla → cada cifra del ADR se copia de la salida vista (memoria del proyecto).
