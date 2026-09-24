# Story s4: Choose screen patterns — Retrospective

Estimated: una parte de la sesión, sin cifra declarada · Actual: de `266cff5` a `1ec65d5`, unos quince minutos en las fechas de autor, más una pausa de decisión.

## Summary

Patrón de las 9 pantallas, con la opción B: S1 y S2 `list-detail`, S3 Mi colección `feed`, y S4 y S5 a S9 `none` con su razón. La fuente se leyó el mismo día y ADR-019 quedó `accepted`.

## Finalize

- **Gate:** `./scripts/check` salió 0 antes de cada commit de la rama.
- **Pruebas huérfanas:** no aplica; ningún `.py` en el diff.
- **Criterios de aceptación (scope):**
  - ADR en `proposed` con su rojo antes del primer patrón: cumplido (`29fb5ba` antes de `5d3574e`).
  - `inventory-sources.py` sale 0 con `9 of 9`: cumplido.
  - P3 y P4 firmados: cumplido, 2026-09-24.
  - Rojo antes de producir (deducido y confirmado): cumplido.
  - ADR `accepted`: cumplido.
  - Ningún criterio retractado.
- **Survival-review:** `precedence` sale PASS. Los nueve "no aplica" están **firmados por Daniel Efraín Domínguez Urbina el 2026-09-24**.
- **quality-review:**
  - La afirmación de ADR-019 sobre la plantilla de hoy (`<ul class="tarjetas">`, con la miniatura primero) se comprobó contra `coleccion.html:6` y `:9-10`.
  - La paráfrasis de la regla en `screen-pattern.md` remite a la cita textual del ADR, no la sustituye.
- **security-review:** sin sujeto, porque no hay `.py` cambiados.

## What went well

- **Medir las opciones como sondas antes de producir** permitió llenar las celdas medidas en el mismo `update` del rojo. `precedence` sale PASS sin depender de en qué commit se llenaron.
- **La fuente se leyó el mismo día y quedó dicho de dónde.** m3.material.io no entregó texto, así que se usó Android Developers, una de las tres fuentes que el catálogo da por equivalentes, con su fecha de actualización. No se citó de memoria.

## What to improve

- **P1 y P2 tampoco discriminan entre opciones**, igual que G1 y G2 en s3: las tres pasan. En este eslabón es esperable, porque la tabla es cerrada y cualquier valor bien formado pasa. Aun así, la elección se decidió entera por juicio. Si se quiere que algo medible opine, la composición es donde puede hacerlo (contraste, pesos, procedencia).
- **B deja S4 `none` por una razón que se deriva del feed**, no del contenido de la ficha: "la fuente no le da panel de detalle a un feed". Es honesto, pero implica que la forma de la ficha la decidirá la composición y no un layout. Conviene recordarlo al componer S4.

## Learned

1. **Sobre el sistema:** la colección es un feed y las especies una lista con ficha. La forma de hoy de Mi colección (tarjetas, miniatura primero) ya se parece a la elegida. La ficha del ejemplar no, porque su orden de hoy es la opción C de ADR-018.
2. **Sobre el proceso:** con opciones completas en el ADR, medirlas todas como sondas en el commit del rojo cierra la rejilla medible antes de producir. Es el patrón que funcionó en s4 y el que se recomienda para los siguientes eslabones.
3. **Capacidad ganada:** S1 a S4 tienen guía y patrón. La composición, el último eslabón, puede empezar por cualquiera de ellas.
