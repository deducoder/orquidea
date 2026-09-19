# Epic e2: Personal collection with login — Plan

## Sequence

| Order | Story | Strategy | Priority | Component | Depends on | Enables |
|:-----:|-------|----------|----------|-----------|------------|---------|
| 1 | s2.1 | skeleton | — | — | — | s2.2, s2.4: base SQLite con migraciones, la pieza de la que cuelgan sesiones y ejemplares |
| 2 | s2.2 | risk-first | — | — | s2.1 (hard) | s2.3, s2.7: contraseña, sesión y cierre; el código de mayor riesgo de seguridad de la épica |
| 3 | s2.3 | risk-first | — | — | s2.2 (hard) | s2.4: todas las rutas protegidas, CSRF y cabeceras antes de que exista un solo dato del usuario |
| 4 | s2.4 | dependency | — | — | s2.1 (hard), s2.3 (hard) | s2.5, s2.6: el recorrido de la métrica líder de punta a punta (iniciar sesión, agregar del catálogo, verlo) |
| 5 | s2.5 | quick-win | — | — | s2.4 (hard) | plantas fuera del catálogo, requisito de la métrica rezagada |
| 6 | s2.6 | quick-win | — | — | s2.4 (hard) | editar y quitar, cierra RF-04 |
| 7 | s2.7 | dependency | — | — | s2.2 (hard) | que la colección sobreviva a un redespliegue; lo último porque su parte efectiva es del humano |

`Priority` y `Component` quedan en `—`: el proyecto no tiene tracker ni binding que nombre los valores.

**Rationale:** el riesgo mayor de la épica es la autenticación hecha a mano (ADR-004): un error abre la colección a un tercero. Por eso s2.1 pone lo mínimo que necesita (la base) y s2.2 y s2.3 van enseguida, con la protección completa antes de que exista un solo dato del usuario. s2.4 es el esqueleto funcional: cierra el recorrido de la métrica líder del brief de punta a punta y valida que el contrato con `Especie.id` de e1 alcanza. s2.5 y s2.6 son extensiones pequeñas de s2.4 sobre la misma tabla y las mismas vistas. s2.7 no bloquea nada del código; va al final porque la configuración del VPS es del humano y queda como el stop previsible que el diseño ya declaró.

## Milestones

- [ ] **Walking skeleton** — s2.1, s2.2, s2.3, s2.4 — un usuario inicia sesión, agrega un ejemplar desde una ficha del catálogo y lo ve en "Mi colección"; sin sesión, ninguna ruta responde; `./scripts/check` en verde
- [ ] **Core MVP** — s2.1 a s2.5 — además, un ejemplar fuera del catálogo con nombre y notas
- [ ] **Feature complete** — s2.1 a s2.7 — editar, quitar y configuración de despliegue con volumen; RF-04 y RF-08 completos
- [ ] **Epic complete** — done criteria met (el criterio rezagado del brief y `must-perf-001` con "Slow 3G" son del humano: stop previsible en `epic-review`)

No hay checkpoint E2E aparte: la épica es un solo proceso con SQLite; el recorrido completo lo hace la prueba manual de s2.4 con el catálogo real.

## Parallel streams

None. Todas las historias tocan `orquidea.web.app` y sus plantillas; ninguna corre en paralelo.

## Delegation

| Story | Block | Mold | Mode |
|-------|-------|------|------|
| s2.1 | — | — | — |
| s2.2 | — | — | — |
| s2.3 | — | — | — |
| s2.4 | — | — | — |
| s2.5 | — | — | — |
| s2.6 | — | — | — |
| s2.7 | — | — | — |

## Progress

| Story | Status | Est. | Actual |
|-------|:------:|:----:|:------:|
| s2.1 | done | S | S |
| s2.2 | done | M | M |
| s2.3 | done | S | S |
| s2.4 | todo | M | — |
| s2.5 | todo | S | — |
| s2.6 | todo | S | — |
| s2.7 | todo | S | — |

## Sequencing risks

- Un error en autenticación, sesión o CSRF abre la colección → s2.2 y s2.3 con pruebas de comportamiento adverso y `security-review` en cada una; nada se guarda del usuario antes de que la protección esté completa.
- La configuración del VPS (volumen, variables, secreto) y las mediciones con navegador son del humano → previstas como stop P5/P4; s2.7 va al final para no frenar el código.
- s2.2 añade `python-multipart`, la única dependencia nueva → se acepta; si la instalación fallara, es P3/P5 en esa historia.
