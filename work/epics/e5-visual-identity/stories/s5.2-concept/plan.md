# Story s5.2: Concept — Plan

> Size: S
> Pause: none (default) — salvo la parada del ciclo para la elección firmada por el humano

Aprobación del humano (2026-09-22, en sesión): S1 y S2 como los propone el diseño; S3 reformulado a petición del humano — herramienta de registro y consulta pensada primero para el teléfono, que toma de las redes la foto a todo el ancho en tarjetas, la navegación al alcance del pulgar y las acciones frecuentes grandes y cerca de su contenido, sin métricas, seguidores, "me gusta" ni scroll infinito; y 3 direcciones. Los patrones de las redes entran como presentación y navegación de lo que ya existe: ningún flujo nuevo (no-go del brief de e5).

## Container acts around the tasks

- **A0 · Abrir ADR-010** (`record-open`): criterios S1–S3 con estrato y origen, el número 3 declarado, la rejilla con las tres direcciones por desarrollar y `## Decision` sin resolver. Commit `docs(s5.2): add ADR-010`.
- **A1 · Desarrollar las direcciones y responder el contraejemplo**: las tres apuestas verbales en la rejilla, cada celda criterio × dirección respondida; S1–S3 respondidos "no aplica: no hay oráculo". Commit `docs(s5.2): update ADR-010`.
- **A2 · Completar ADR-010** (`record-complete`) tras la elección firmada y `concept.md`. Commit `docs(s5.2): publish ADR-010`.

## Tasks

### T1 · Escribir el entregable del concepto

- **Files:** create `governance/identity/concept.md` desde `skills/techniques/concept/assets/concept.md` (gemba-design 0.21.0).
- **TDD:** no aplica — documento sin comportamiento; lo cubre el gate (`ruff format`, `check-published-citations`).
- **Satisfies:** scope, escenarios de las descartadas por criterio y de la mitad juzgada.
- **Mold:** `skills/techniques/concept/assets/concept.md`; `governance/identity/commission.md` (forma del entregable hermano).
- **Verify:** `decision: ADR-010`; "3" declarado con su fecha; S1–S3 con estrato y `From`; tres direcciones, cada descartada con `S{n}`; `grep -nE '[0-9]+ ?/ ?10|puntaje|puntuación|ranking'` no encuentra nada; la elección con nombre y fecha del humano o `unsigned`; then `./scripts/check`.
- **Parada:** la elección es del humano, en elección forzada entre las tres; se le presenta la rejilla y una recomendación, y se espera su respuesta antes de escribir `The one chosen`.
- **Commit:** docs(identity): add the chosen direction

### T2 · Prueba de integración manual del orden

- **Verify:** `git log --reverse --date=iso-strict develop..HEAD` muestra `add ADR-010` antes de `update ADR-010`, este antes de T1, y `publish ADR-010` al final; `status: accepted`.

## Order & risks

- **Execution order:** A0 → A1 → (elección) → T1 → A2 → T2.
- **Risks:** direcciones hechas de paja para que gane una → cada una se desarrolla con su mejor versión y su apuesta dicha en positivo; la que pierde, pierde por un criterio nombrado.
