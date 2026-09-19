# Epic e4: Care log — Plan

## Sequence

| Order | Story | Strategy | Priority | Component | Depends on | Enables |
|:-----:|-------|----------|----------|-----------|------------|---------|
| 1 | s4.1 | risk-first | — | — | — | s4.2, s4.3, s4.5: el patrón de la epic (migración con cascada, fechas de calendario validadas, tope de registros, escritura filtrada por ejemplar y registro) donde caben los riesgos de fechas e IDOR |
| 2 | s4.2 | skeleton | — | — | s4.1 (hard) | s4.4, s4.5: el recorrido de la métrica líder de punta a punta (registrar un riego y ver el último en la ficha) y el router `cuidados` |
| 3 | s4.3 | dependency | — | — | s4.1 (hard) | s4.4: la migración `0005` (la numeración es continua, va después de `0004`) y las reglas del intervalo abierto de la floración |
| 4 | s4.4 | quick-win | — | — | s4.2 (hard), s4.3 (hard) | s4.6: registrar, terminar y quitar floraciones en la ficha; cierra RF-07 |
| 5 | s4.5 | quick-win | — | — | s4.1 (hard) | el último riego en "Mi colección"; una consulta para toda la lista |
| 6 | s4.6 | dependency | — | — | s4.4 (hard) | la medición de `must-perf-001` con el historial lleno; al final porque su parte efectiva es del humano |

`Priority` y `Component` quedan en `—`: el proyecto no tiene tracker ni binding que nombre los valores.

**Rationale:** el riesgo mayor es que una fecha mal validada contamine el orden y "el último riego", que un id ajeno quite el registro de otro ejemplar y que el historial engorde la ficha sin tope; s4.1 los resuelve sin HTTP y fija el patrón que s4.3 repite. s4.2 es el esqueleto funcional: cierra la métrica líder de punta a punta y crea el router que s4.4 reutiliza. s4.3 y s4.5 dependen solo de s4.1; s4.3 va antes de s4.4 porque la ficha necesita los dos historiales y la migración `0005` sigue a la `0004`. s4.5 es una extensión pequeña que va después de las floraciones para que la ficha, que es lo que el brief mide, quede completa primero. s4.6 va al final: mide la ficha con todo dentro y su parte de "Slow 3G" es del humano.

## Milestones

- [ ] **Walking skeleton** — s4.1, s4.2 — se registra un riego en un ejemplar y la ficha muestra el historial y la fecha del último; una fecha futura o inválida se rechaza; sin sesión no se registra; `./scripts/check` en verde
- [ ] **Core MVP** — s4.1 a s4.4 — además, floraciones con inicio, fin opcional y fin fijado después; RF-06 y RF-07 completos
- [ ] **Feature complete** — s4.1 a s4.6 — último riego en la lista y peso de la ficha medido por script con el tope lleno
- [ ] **Epic complete** — done criteria met (el criterio rezagado del brief y `must-perf-001` con "Slow 3G" son del humano: stop previsible P4 en `epic-review`)

No hay checkpoint E2E aparte: la épica es un solo proceso con SQLite; el recorrido completo lo hacen la prueba de extremo a extremo de s4.2 y s4.4 y la manual de `story-implement`.

## Parallel streams

None. s4.3 (`orquidea.datos.floraciones`, `0005`) y s4.5 (`datos.riegos`, `coleccion.html`) tocan áreas casi disjuntas, pero el proyecto no delega sin que el humano lo pida y no hay razón de ritmo para hacerlo; s4.2 y s4.4 comparten la ficha y el router.

## Delegation

| Story | Block | Mold | Mode |
|-------|-------|------|------|
| s4.1 | — | — | — |
| s4.2 | — | — | — |
| s4.3 | — | — | — |
| s4.4 | — | — | — |
| s4.5 | — | — | — |
| s4.6 | — | — | — |

## Progress

| Story | Status | Est. | Actual |
|-------|:------:|:----:|:------:|
| s4.1 | done | S | S |
| s4.2 | done | M | M |
| s4.3 | done | S | S |
| s4.4 | done | M | M |
| s4.5 | todo | S | |
| s4.6 | todo | S | |

## Sequencing risks

- Una fecha mal validada (futura, imposible) contamina el orden y "el último riego" → s4.1 primero, con pruebas de límites de fecha; ASVS L2 (validación de entrada) recorrido en el `design.md` de cada historia.
- Un registro ajeno se quita al pasar su id (IDOR) → toda escritura filtra por ejemplar y registro; prueba con dos ejemplares en s4.1 y s4.2.
- El historial sin tope engorda la ficha → tope de 500 desde s4.1; medir con el tope lleno en s4.6 (y el pico de la consulta desde el diseño de s4.1, según la memoria del proyecto).
- Las mediciones con navegador ("Slow 3G") son del humano → prevista como stop P4 en `epic-review`; s4.6 va al final para no frenar el código.
