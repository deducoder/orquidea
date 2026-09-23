# Bug b1: Collection title shows markup — Retrospective

## Summary
- Root cause: `8d5b985` (e2) insertó el enlace a `/coleccion/nuevo` dos veces, una en el cuerpo y otra dentro del bloque `title`, y la única prueba del enlace (`'href="/coleccion/nuevo"' in html`) no distingue dónde está ni cuántas veces aparece.
- Fix approach: el bloque `title` vuelve a una línea de texto (`Mi colección — Orquídea`), y una prueba de regresión afirma el título exacto y exactamente un enlace a `/coleccion/nuevo`.

## Finalize
- `./scripts/check` tras T1: `✓ gates passed` (el hook `pre-commit` lo volvió a correr en el commit `8344433`).
- El bug ya no se reproduce: `GET /coleccion` con sesión → 200 y `<title>Mi colección — Orquídea</title>`.
- La prueba se vio en rojo antes del arreglo y con cuatro mutaciones forzadas (arreglo revertido, otro marcado en el título, `<title>` ausente, enlace del cuerpo ausente); el detalle está en `plan.md`, T1.
- Tiempo de implementación: 59 s (`implementation-time.sh develop b1`); sin tracker, no se registra en ningún lado.
- `quality-review`: PASS. La prueba anterior de "enlaza al formulario" ya no aporta cobertura única; se conserva a propósito porque nombra el comportamiento de RF-04 y cuesta una línea.
- `security-review`: PASS. Bandit sobre `tests/test_web_coleccion.py`: 144 B101 (`assert` de pytest), 3 de ellos en la prueba nueva, sin riesgo; la plantilla se revisó a mano.

## Prevention
- Probar cada página localizando el elemento antes de juzgarlo y contando cuando el requisito es "exactamente uno"; una prueba parametrizada que afirme que ningún `<title>` contiene marcado cerraría la clase: aparcada, con promoción en s5.7 (e5), que toca todas las plantillas.
- Pattern: defecto de plantilla + origen Code → una afirmación de presencia (`x in html`) no ve la ubicación ni la duplicación, y el contenido RCDATA (`<title>`) muestra el error como texto sin que nada falle.

## Learned
1. About the system: de las diez plantillas, solo la de inicio tenía su `<title>` bajo prueba; los títulos son la parte de la página que ninguna prueba de comportamiento mira y que el usuario ve en cada pestaña.
2. About the process: el defecto lo encontró el recorrido de gemba de `epic-design` (e5), no una revisión de e2; leer las plantillas completas antes de vestirlas pagó antes de producir nada. Hacer el bug completo aquí en lugar de delegarlo fue lo barato: la regla R1 solo deja delegar la ejecución de un bug, y aquí la ejecución era una línea.
3. Capability gained: una prueba de regresión cuyas mutaciones incluyen "el sujeto quitado", de modo que la localización del `<title>` no puede pasar en vacío.
