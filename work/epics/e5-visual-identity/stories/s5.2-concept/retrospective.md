# Story s5.2: Concept — Retrospective

Estimated: S · Actual: S (210 s de implementación según `implementation-time.sh develop s5.2`; el tiempo real lo ocuparon las dos paradas de aprobación)

## Summary

La identidad tiene dirección: **Cuaderno de campo**, elegida por el humano en elección forzada entre tres direcciones declaradas antes de desarrollar ninguna, contra S1 (la foto es lo único saturado, del criterio 3 del encargo), S2 (carácter con ≥ 7:1 y fuentes ligeras, de los criterios 1 y 2) y S3 (registro y consulta primero para el teléfono, con patrones de las redes, pedido por el humano). ADR-010 se abrió en `proposed` (`264f112`), las direcciones se desarrollaron en él (`2fc1124`), `concept.md` se escribió con la elección firmada (`7a11cd3`) y el ADR pasó a `accepted` (`1203dcb`).

### Finalize (lo que `story-implement` reportó)

- Gate: `./scripts/check` → `✓ gates passed`.
- Orden: `git log --reverse --date=iso-strict develop..HEAD` — `add ADR-010` (21:56:32) → `update ADR-010` (21:57:10) → `concept.md` (22:00:40) → `publish ADR-010` (22:01:11).
- Pruebas huérfanas: ninguna posible — el diff no toca código (0 archivos `.py`).
- Aceptación: los seis escenarios del scope se cumplen; los dos `@deduced` los confirmó el diseño; `grep` de puntuaciones sobre `concept.md` no encuentra nada.
- Aprobaciones del humano, en sesión el 2026-09-22: S1, S2, el S3 reformulado y el número 3 (su "sigue" se tomó como aprobación, dicho en voz alta y reversible mientras el ADR estaba en `proposed`); la elección de (A) se registró como firmada por su "vamos con a".
- `quality-review`: PASS WITH RECOMMENDATIONS — una afirmación no verificada en la celda (B) × S2 (abajo). `security-review`: PASS; sin `.py`, Bandit no se invoca por la regla del binding.

## What went well

- La reformulación de S3 por el humano llegó **antes** de abrir el ADR, así que entró como criterio y no como justificación posterior; y dejó explícito el límite del brief (patrones de presentación, ningún flujo nuevo).
- Ninguna dirección descartada cayó por gusto: cada una nombra su criterio (C por S1, B por S2 y en parte S3), y la recomendación coincidió con la única que cumplía los tres.

## What to improve

- **Una afirmación de hecho viajó dentro de un juicio.** La celda (B) × S2 dice que las serif del sistema en Android no dan itálica real; Noto Serif sí la trae. El veredicto se sostiene por la textura y el tono sepia, pero la frase no se comprobó y el ADR ya es `accepted`. Queda aquí como hallazgo; s5.4 verifica qué trae cada sistema al elegir familias.
- **Tomar "sigue" como aprobación fue una lectura**, no una respuesta a la pregunta hecha. Se dijo en voz alta y era reversible; en una parada de aprobación conviene que la pregunta admita un sí corto para no tener que interpretar.

## Learned

1. About the system: el catálogo no tiene fotos; lo único saturado que la aplicación muestra son las plantas del usuario, lo que hace que S1 sea barato para cualquier dirección de neutros.
2. About the process: en una historia de juicio el tiempo real está en las paradas del humano, no en escribir; `implementation-time.sh` mide 210 s y no dice nada del costo de la historia.
3. Capability gained: la memoria [[afirmaciones-de-plataforma-se-verifican-antes-de-aceptar]].
