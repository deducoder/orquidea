# Story s5.5: Interface color roles — Retrospective

Estimated: S · Actual: S — 4 tareas y 3 actos de contenedor, 737 s de implementación (`implementation-time.sh`, del padre de la primera tarea a la última), 9 commits en la rama.

## Summary

- `scripts/derivar-primitivas.py` (solo biblioteca estándar) deriva de `palette.md` tres rampas de doce escalones con una de las tres reglas de ADR-013. Lo cubren 38 pruebas, incluida una que regenera `primitives.md` y lo compara con el archivo.
- `governance/identity/ui/primitives.md` usa la regla (A) anclas en OKLCH: cada rol de la paleta queda en su valor exacto, con desvío 0.000.
- `governance/identity/ui/semantics.md` tiene trece roles por función, cada uno una referencia a un escalón. R1: 10 pares de texto, 0 bajo 7:1 (el más bajo 8.38:1). `component-contrast`: 12 pares, 0 bajo 3:1 (el más bajo 3.34:1). `provenance`: 13 tokens, 0 fuera de escala. Invariancia: no comparada, porque no hay variante.
- ADR-013 siguió el orden `proposed` → `update` con los rojos → `accepted`. El orden por fecha de autor quedó comprobado: el registro se abrió antes del script y de cualquier valor.

**Finalize (reportado por `story-implement`):**
- Gate: `./scripts/check` en verde, 550 pruebas, y 551 tras el arreglo de la revisión.
- Pruebas huérfanas: ninguna. El único código tocado es nuevo y solo lo importa `tests/test_derivar_primitivas.py`.
- Aceptación: los ocho escenarios del scope se cumplen. Los dos `@deduced` los confirmó el diseño; ninguno se retiró.
- El plan existió; no hubo que saltarlo.

**`survival-review`:** mecánico en verde (10 pares con `contrast.py`, `pairs` 22/0, `provenance` 13/0). `targets` no tiene sujeto en esta pieza (va en s5.6). Invariancia sin sujeto. Los cinco "no aplica" (`platform-specs`, `minimum-size`, `single-ink`, `prior-art`, `target-size`) los firmó Daniel Efraín Domínguez Urbina el 2026-09-22. Respuestas a las preguntas: `acción-presionada` en `azul-900` sí se lee como Cuaderno de campo; el gris muy claro para separadores se deja a que lo pida s5.6.

**`quality-review`:** PASS WITH RECOMMENDATIONS, ambas aplicadas en `260ff51`:
- `derivar()` con una regla desconocida caía en silencio a HSL (`scripts/derivar-primitivas.py`, rama `else`). Ahora lanza `ValueError`, y lo prueba `test_una_regla_desconocida_no_cae_en_otra`.
- `test_dos_roles_no_comparten_escalon` aceptaba `{2, 4}`. Ahora afirma `4`, porque el empate va al escalón más oscuro.
- Observación que se deja fuera, dicha en voz alta: en `_rampa_anclas`, si un escalón intermedio cayera fuera de la luminosidad de sus dos anclas, `t` saldría de [0, 1] y el croma se extrapolaría. Con la paleta actual no pasa, y la prueba de luminosidad lo vería. No se aparca porque solo pasaría si cambia la paleta, y entonces la regla se vuelve a correr y a medir.

**`security-review`:** Bandit (`conventions/security/instance.md`) sobre los dos `.py` cambiados dio 42 hallazgos, todos B101 (`assert`) en `tests/test_derivar_primitivas.py`, y 0 en el script. PASS: es el `assert` de pytest, que ruff ya ignora en `tests/**`. Guardrails: `must-security-001` (EXIF) y `should-security-002` (ASVS L2) no aplican, porque no se tocó código de la aplicación ni entradas del usuario.

## What went well

- **El contraejemplo salió de las candidatas, no de una muestra fabricada.** El margen fino medido al abrir ADR-013 (`renglón` sobre `papel` 3.34:1) predijo dónde rompería una regla que se aleja de la paleta, y (B) lo rompió: 2.76:1. Solo el rojo de `provenance` necesitó una muestra construida.
- **Las mutaciones antes del commit** (seis sobre el script y tres sobre `primitives.md`) se pusieron en rojo, incluida la forma equivalente (potencia 2.2 en lugar de la linealización sRGB). Corrieron sin bytecode, por la memoria del proyecto.
- **No hizo falta un instrumento nuevo de contraste:** `contraste-de-lectura.py` (7:1) y `tokens.py pairs` y `provenance` cubrieron todo. El recorrido del diseño lo vio antes de planear.

## What to improve

- **La ruta de las piezas se copió de la historia anterior.** El scope y el diseño decían `governance/identity/`, y la convención `deliverables` pide `governance/identity/ui/`. Se corrigió al producir; va a memoria.
- **El diseño propuso un respaldo que habría escondido el rojo** ("`campo-borde`, o el escalón más cercano que llegue a 3:1"). ADR-013 lo quitó al abrirse ("Respaldo: ninguno"), después de que el humano aprobara el diseño "tal como está". Se avisó en la parada de R3, pero el cambio habría tenido que salir en la parada de aprobación de los criterios. Va a memoria.
- **Una tabla generada desde la salida de un instrumento salió mal:** leí la columna equivocada de `tokens.py pairs` y los 22 pares quedaron como "componente". Lo vi al releer el archivo antes del commit, no con una comprobación. El conteo por tipo (10 y 12) lo confirmó después de corregir.
- **La plantilla y el instrumento del addon no coinciden en la columna `Variant`:** `invariance.py` trata `—` como ilegible. Se quitó la columna en `semantics.md` y quedó aparcado como hallazgo del addon.

## Learned

1. **About the system:** la paleta tiene un solo punto frágil, el borde (`renglón`, 3.34:1 sobre `papel`). Cualquier regla que aproxime en lugar de anclar lo rompe, así que las piezas de s5.6 que usen bordes o separadores tenues necesitan su propio rol y su propia medición, no un escalón vecino. El salto `neutro-50` → `neutro-100` (`#F7F3EA` → `#D4CFC4`) quedó dicho en ADR-013.
2. **About the process:** en una técnica cuyo entregable es una regla, lo que el ADR fija antes de correr (parámetros, y qué pasa cuando un valor no llega a su umbral) decide si el paso `counterexample` puede verse en rojo. Por eso "Respaldo" es un parámetro declarado.
3. **Capability gained:** `scripts/derivar-primitivas.py` con OKLab probado contra valores de referencia, y una prueba de regeneración que pone el gate en rojo si `primitives.md` se edita a mano o si cambia la regla registrada sin regenerar.
