# Epic e1: Species catalog — Plan

## Sequence

| Order | Story | Strategy | Priority | Component | Depends on | Enables |
|:-----:|-------|----------|----------|-----------|------------|---------|
| 1 | e1.1 | skeleton | — | — | — | e1.3, e1.5: aplicación mínima que corre y pasa los gates |
| 2 | e1.2 | risk-first | — | — | — | e1.3, e1.6: esquema y carga validada, el contrato central de la épica |
| 3 | e1.3 | dependency | — | — | e1.1 (hard), e1.2 (hard) | e1.4, e1.5: ficha visible de una especie |
| 4 | e1.5 | risk-first | — | — | e1.1 (hard), e1.3 (hard) | primera prueba real de la métrica líder en el VPS |
| 5 | e1.4 | quick-win | — | — | e1.3 (hard) | búsqueda sobre el catálogo ya desplegado |
| 6 | e1.6 | risk-first | — | — | e1.2 (hard) | medición de must-perf-001 sobre datos reales |

`Priority` y `Component` quedan en `—`: el proyecto no tiene tracker ni binding que nombre los valores.

**Rationale:** e1.1 abre como esqueleto: prueba el stack y los gates de extremo a extremo con lo mínimo. e1.2 va enseguida porque el esquema con fuente obligatoria es el contrato del que dependen ficha, búsqueda y semilla. e1.3 cierra el primer camino completo (JSON validado a ficha). El despliegue (e1.5) se adelanta antes de la búsqueda: el brief pide desplegar temprano, y sus incógnitas (datos del VPS, forma de despliegue) son las de mayor riesgo, así que conviene encontrarlas con la mitad del trabajo pendiente y no al final; no puede ir antes de e1.3 porque su criterio es ver una especie en su ficha en línea. e1.4 es la victoria rápida sobre lo ya desplegado. e1.6 va al final porque depende de que el humano aporte especies y fuentes reales, y nada más la espera.

## Milestones

- [ ] **Walking skeleton** — e1.1 — la aplicación arranca, sirve una página y `./scripts/check` está en verde
- [ ] **Core MVP** — e1.1, e1.2, e1.3 — un JSON válido se ve como ficha de especie; uno inválido se rechaza con archivo y campo
- [ ] **E2E integration checkpoint** — e1.5 — la aplicación corre en el VPS real y la ficha de una especie de ejemplo se ve en línea
- [ ] **Feature complete** — e1.1 a e1.6 — todas las historias hechas, búsqueda funcionando, catálogo semilla con fuentes
- [ ] **Epic complete** — done criteria met (incluida la medición de must-perf-001 sobre el catálogo semilla)

## Parallel streams

None. Las historias se recorren en secuencia; e1.2 y e1.1 no tienen dependencia mutua pero se ejecutan sin paralelismo.

## Delegation

| Story | Block | Mold | Mode |
|-------|-------|------|------|
| e1.1 | — | — | — |
| e1.2 | — | — | — |
| e1.3 | — | — | — |
| e1.5 | — | — | — |
| e1.4 | — | — | — |
| e1.6 | — | — | — |

## Progress

| Story | Status | Est. | Actual |
|-------|:------:|:----:|:------:|
| e1.1 | todo | S | — |
| e1.2 | todo | M | — |
| e1.3 | todo | M | — |
| e1.5 | todo | M | — |
| e1.4 | todo | S | — |
| e1.6 | todo | S | — |

## Sequencing risks

- Los datos del VPS y los datos botánicos con fuentes no están escritos en ningún artefacto → e1.5 y e1.6 se detienen (P5) en su diseño en lugar de inventarlos; la ubicación de e1.5 a mitad de la secuencia adelanta ese aviso.
- Mover e1.5 antes de e1.4 rompe el orden por tamaño a propósito → se acepta: se secuencia por riesgo, no por tamaño.
