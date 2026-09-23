# Epic e5: Visual identity — Plan

## Sequence

| Order | Story | Type | Strategy | Priority | Component | Depends on | Enables |
|:-----:|-------|------|----------|----------|-----------|------------|---------|
| 1 | s5.1 | story | dependency | — | — | — | todas: el criterio del encargo commiteado y las comprobaciones de peso y contraste ≥ 7:1 vistas en rojo; nada puede producirse antes |
| 2 | s5.2 | story | dependency | — | — | s5.1 (hard) | s5.3, s5.4: la dirección común contra la que ambas piezas derivan sus criterios |
| 3 | s5.4 | story | risk-first | — | — | s5.2 (hard) | s5.6: la tipografía decide si hay fuente web y cuánto del presupuesto de 50 KB queda |
| 4 | s5.3 | story | dependency | — | — | s5.2 (hard) | s5.5: la paleta por roles con sus pares de texto a ≥ 7:1 |
| 5 | s5.5 | story | dependency | — | — | s5.3 (hard) | s5.6: primitivas y roles semánticos, con `contrast` y `component-contrast` en los valores reales |
| 6 | s5.6 | story | dependency | — | — | s5.4 (hard), s5.5 (hard) | s5.7: escala, espaciado, componentes y `DESIGN.md` generado y verificado |
| 7 | s5.7 | story | dependency | — | — | s5.6 (hard) | cierre: la interfaz vestida, sin estilos en línea, y la primera carga medida con CSS y fuentes |

`Priority` y `Component` quedan en `—`: el proyecto no tiene tracker ni binding que nombre los valores.

**Rationale:** la épica es casi una cadena, porque cada pieza deriva de una anterior ya `accepted` (convención del encargo). La única libertad de orden está entre s5.3 y s5.4, que solo dependen del concepto; s5.4 va primero porque ahí está el riesgo mayor: una fuente web puede comerse el presupuesto de 50 KB (criterio 1), y saberlo pronto cambia lo que queda para la hoja y la escala. s5.1 no es un esqueleto funcional sino el control de toda la épica: sin su commit, ninguna pieza puede demostrar que su criterio fue anterior. **Fuera de la épica y antes de s5.1** va el bug del título de "Mi colección" (bloque `title` con un `<p><a>`), por el flujo de bug.

## Milestones

- **Criterio comprometido** — s5.1 — el ADR-009 está en `proposed` con fecha de autor anterior a cualquier pieza; las comprobaciones de peso y de contraste ≥ 7:1 existen, tienen pruebas y se vieron en rojo sobre un sujeto que viola cada una; `./scripts/check` en verde.
- **Identidad decidida** — s5.1 a s5.4 — concepto, paleta y tipografía con su ADR `accepted`, su mitad juzgada firmada por el humano (o `unsigned` y contada) y `survival-review` corrido sobre la paleta y el espécimen.
- **Feature complete** — s5.1 a s5.7 — `DESIGN.md` generado y verificado con `pairs`, `targets` y `provenance`; todas las plantillas con la hoja derivada y sin atributos `style`; recursos de la identidad ≤ 50 KB gzip medidos por script.
- **Epic complete** — done criteria met (la medición con "Slow 3G" y el criterio 3, la foto como protagonista, son del humano: stops previsibles en `epic-review`).

No hay checkpoint E2E aparte: la épica es un solo proceso y ningún contrato cruza servicios. La costura que importa (tokens de `DESIGN.md` → hoja de estilos → plantillas) la verifica en s5.7 una prueba que compara los valores de la hoja con los tokens, y el recorrido manual en el teléfono.

## Waves

None. s5.3 (`palette.md`, su ADR) y s5.4 (`specimen.md`, su ADR, fuentes en `/static`) tocan áreas disjuntas, pero cada una se detiene dos veces por la aprobación y la firma del humano: son decisiones, no deltas especificados, y ninguna ganaría con un despacho.

## Delegation

| Story | Block | Mold | Mode |
|-------|-------|------|------|
| s5.1 | — | — | chain |
| s5.2 | — | — | chain |
| s5.4 | — | — | chain |
| s5.3 | — | — | chain |
| s5.5 | — | — | chain |
| s5.6 | — | — | chain |
| s5.7 | — | — | chain |

## Progress

| Story | Status | Est. | Actual |
|-------|:------:|:----:|:------:|
| s5.1 | done | S | S |
| s5.2 | done | S | S |
| s5.4 | done | M | S |
| s5.3 | done | S | S |
| s5.5 | done | S | S |
| s5.6 | done | M | M |
| s5.7 | todo | M | |

## Sequencing risks

- La fuente web se come el presupuesto → s5.4 antes que s5.3, con la pila de sistema como opción real en la rejilla de su ADR y el peso medido antes de elegir.
- Las firmas del humano frenan la cadena, porque cada pieza espera a que la anterior esté `accepted` → pedirlas en elección forzada y pocas; una mitad juzgada sin firma se escribe `unsigned` y no bloquea el `accepted` del ADR, pero se cuenta como sin responder.
- Un ADR commiteado después de su pieza invalida el control sin que nada falle → comprobar en cada `story-review` el orden de las fechas de autor con `git log`, no la etiqueta del ADR.
- La medición con "Slow 3G" es del humano (así pasó en e1 a e4) → stop previsto en `epic-review`; el peso en bytes lo mide el script desde s5.1.
