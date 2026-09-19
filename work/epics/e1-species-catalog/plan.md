# Epic e1: Species catalog — Plan

## Sequence

| Order | Story | Strategy | Priority | Component | Depends on | Enables |
|:-----:|-------|----------|----------|-----------|------------|---------|
| 1 | s1.1 | skeleton | — | — | — | s1.3, s1.5: aplicación mínima que corre y pasa los gates |
| 2 | s1.2 | risk-first | — | — | — | s1.3, s1.6: esquema y carga validada, el contrato central de la épica |
| 3 | s1.3 | dependency | — | — | s1.1 (hard), s1.2 (hard) | s1.4, s1.5: ficha visible de una especie |
| 4 | s1.5 | risk-first | — | — | s1.1 (hard), s1.3 (hard) | primera prueba real de la métrica líder en el VPS |
| 5 | s1.4 | quick-win | — | — | s1.3 (hard) | búsqueda sobre el catálogo ya desplegado |
| 6 | s1.6 | risk-first | — | — | s1.2 (hard) | medición de must-perf-001 sobre datos reales |

`Priority` y `Component` quedan en `—`: el proyecto no tiene tracker ni binding que nombre los valores.

**Rationale:** s1.1 abre como esqueleto: prueba el stack y los gates de extremo a extremo con lo mínimo. s1.2 va enseguida porque el esquema con fuente obligatoria es el contrato del que dependen ficha, búsqueda y semilla. s1.3 cierra el primer camino completo (JSON validado a ficha). El despliegue (s1.5) se adelanta antes de la búsqueda: el brief pide desplegar temprano, y sus incógnitas (datos del VPS, forma de despliegue) son las de mayor riesgo, así que conviene encontrarlas con la mitad del trabajo pendiente y no al final; no puede ir antes de s1.3 porque su criterio es ver una especie en su ficha en línea. s1.4 es la victoria rápida sobre lo ya desplegado. s1.6 va al final porque depende de que el humano aporte especies y fuentes reales, y nada más la espera.

## Milestones

- [ ] **Walking skeleton** — s1.1 — la aplicación arranca, sirve una página y `./scripts/check` está en verde
- [ ] **Core MVP** — s1.1, s1.2, s1.3 — un JSON válido se ve como ficha de especie; uno inválido se rechaza con archivo y campo
- [ ] **E2E integration checkpoint** — s1.5 — la aplicación corre en el VPS real y la ficha de una especie de ejemplo se ve en línea
- [ ] **Feature complete** — s1.1 a s1.6 — todas las historias hechas, búsqueda funcionando, catálogo semilla con fuentes
- [ ] **Epic complete** — done criteria met (incluida la medición de must-perf-001 sobre el catálogo semilla)

## Parallel streams

None. Las historias se recorren en secuencia; s1.2 y s1.1 no tienen dependencia mutua pero se ejecutan sin paralelismo.

## Delegation

| Story | Block | Mold | Mode |
|-------|-------|------|------|
| s1.1 | — | — | — |
| s1.2 | — | — | — |
| s1.3 | — | — | — |
| s1.5 | — | — | — |
| s1.4 | — | — | — |
| s1.6 | — | — | — |

## Progress

| Story | Status | Est. | Actual |
|-------|:------:|:----:|:------:|
| s1.1 | done | S | S |
| s1.2 | done | M | M |
| s1.3 | done | M | M |
| s1.5 | todo | M | — |
| s1.4 | todo | S | — |
| s1.6 | todo | S | — |

## Sequencing risks

- Los datos del VPS y los datos botánicos con fuentes no están escritos en ningún artefacto → s1.5 y s1.6 se detienen (P5) en su diseño en lugar de inventarlos; la ubicación de s1.5 a mitad de la secuencia adelanta ese aviso.
- Mover s1.5 antes de s1.4 rompe el orden por tamaño a propósito → se acepta: se secuencia por riesgo, no por tamaño.
