# Story s5.5: Interface color roles — Plan

> Size: S
> Pause: none (default) — salvo la parada del ciclo para la elección firmada por el humano (R3)

Aprobación del humano (2026-09-22, en sesión): R1–R3, los trece roles por función de `design.md` y las tres reglas candidatas (A) anclas en OKLCH, (B) uniforme en OKLCH, (C) uniforme en HSL, tal como están.

## Container acts around the tasks

- **A0 · Abrir ADR-013** (`records/decisions/adr-013-roles-de-color.md`, molde `adr-012-paleta.md`): pregunta, R1–R3 con estrato y origen, los criterios del catálogo aplicados, las tres reglas con **todos sus parámetros fijados** (espacio, pasos y su luminosidad, asignación de cada rol) y la rejilla con cada celda medible en `pending: measured when run`; `## Decision` sin resolver. Antes de que exista el script o cualquier valor. `docs(s5.5): add ADR-013`.
- **A1 · Correr las candidatas y ver los rojos** (tras T1): cada regla con el script hacia el scratchpad, con sus roles semánticos resueltos; `contraste-de-lectura.py`, `tokens.py pairs` y `tokens.py provenance` sobre cada una, salida literal copiada; los cuatro rojos de la tabla de `design.md` vistos sobre la candidata que los viola; R3 "no aplica: no hay oráculo". Rellenar la rejilla sin tocar criterios ni parámetros. `docs(s5.5): update ADR-013`.
- **A2 · Completar ADR-013** a `accepted` tras T3, mismo archivo y número, con `published: no` como ADR-012. `docs(s5.5): publish ADR-013`.

## Tasks

### T1 · Script que deriva las primitivas

- **Files:** create `scripts/derivar-primitivas.py`, `tests/test_derivar_primitivas.py`.
- **TDD:** RED pruebas de la conversión sRGB ↔ OKLab (blanco → L = 1; `#1F3A5F` contra valores de referencia publicados; ida y vuelta de los siete valores de la paleta al mismo hex), de cada regla (anclas: el escalón ancla es el valor exacto de la paleta; uniforme: luminosidades en pasos iguales; HSL: pasos iguales de L de HSL), de la salida `Step | Value | Ramp` y de los códigos de salida → GREEN el mínimo, solo biblioteca estándar → REFACTOR.
- **Satisfies:** R2 (reproducible); scope `@deduced` "cada rol lleva su valor de identidad, primitiva y desvío".
- **Mold:** `scripts/contraste-de-lectura.py` y `tests/test_contraste_de_lectura.py` (lectura de tablas `Role | Value`, carga por `importlib`, salidas 0/1/2); los parámetros, de ADR-013.
- **Verify:** la propiedad es que cada valor emitido se reproduce de la regla y que las anclas salen idénticas a la paleta — mutaciones que deben ponerla en rojo: quitar la linealización sRGB (y su forma equivalente, sustituirla por potencia 2.2); interpolar en sRGB en lugar de OKLab (el punto medio entre dos anclas cambia); redondear el hex por truncamiento en vez de al más cercano; con un rol de la paleta ausente, salir con 2 nombrándolo, nunca con una rampa más corta. Then `uv run pytest tests/test_derivar_primitivas.py` y `./scripts/check` completo (archivo nuevo que el gate escanea).
- **Commit:** feat(identity): derive colour primitives from the palette

### T2 · Lámina de juicio para R3

- Tras A1: una página HTML en el scratchpad por candidata que pase R1 y R2, con el formulario de alta real (campo, campo con error, botón, botón presionado, anillo de foco, enlace, texto secundario) sobre `papel` y sobre `hoja`, y la rampa azul completa; mostrarla al humano en el navegador.
- **Verify:** las láminas se ven y cada una nombra su regla; nada entra al repositorio.
- **Parada:** la elección y la firma de R3 son del humano.
- Sin commit.

### T3 · Primitivas y roles semánticos

- **Files:** create `governance/identity/primitives.md` y `governance/identity/semantics.md` desde las plantillas de la técnica `ui` (gemba-design 0.21.0); modify `tests/test_derivar_primitivas.py` con la prueba de regeneración.
- **TDD:** RED la prueba de regeneración (corre el script con los parámetros registrados en `primitives.md` y compara con su tabla) falla porque el archivo no existe → GREEN escribir `primitives.md` con la salida del script → REFACTOR. `semantics.md` es documento; lo verifican los instrumentos.
- **Satisfies:** los `@stated` de 7:1, componente, invariancia no comparada y firma; R1, R2; los dos `@deduced` confirmados en el diseño.
- **Mold:** las plantillas; `governance/identity/palette.md`.
- **Verify:** la propiedad es que `primitives.md` es exactamente lo que la regla produce — mutaciones: cambiar un hex a mano en `primitives.md` (rojo); cambiar un parámetro registrado sin regenerar (rojo); borrar la tabla (rojo por población cero, nunca verde). Luego, sobre lo producido: `uv run python scripts/contraste-de-lectura.py governance/identity/semantics.md` en 0 con población ≥ 9; `tokens.py pairs governance/identity/semantics.md` en 0; `tokens.py provenance` sobre las dos tablas concatenadas en 0 con 13 tokens; `invariance.py` reporta sin sujeto y `semantics.md` lo escribe como no comparado; una fila por criterio del catálogo en cada archivo; mitad juzgada firmada o `unsigned`. Then `./scripts/check` completo.
- **Commit:** docs(identity): add the colour primitives and semantic roles

### T4 · Prueba de integración manual

- `survival-review` sobre `primitives.md` y `semantics.md` — su `## When` ("after any technique of this addon has produced something") se cumple tras T3.
- Correr de cero, desde el árbol limpio, el script con los parámetros de `primitives.md` y los tres instrumentos, y comparar con lo commiteado.
- Orden por fecha de autor: `add ADR-013` → `update ADR-013` → T3 → `publish ADR-013`; `status: accepted`.
- **Verify:** misma tabla, los tres instrumentos en 0 con su población, orden de commits correcto.

## Order & risks

- **Execution order:** A0 → T1 → A1 → T2 → (elección) → T3 → A2 → T4. T1 es la parte arriesgada (la conversión de color es donde un error pasa desapercibido), por eso va primera tras abrir el registro.
- **Dependencies:** secuenciales; A0 antes de T1 porque los parámetros de las reglas se fijan antes de que exista la herramienta que las corre.
- **Risks:**
  - Una conversión OKLab mal hecha que "se ve bien" → valores de referencia publicados en las pruebas, y la ida y vuelta de la paleta al mismo hex.
  - Una regla que no cabe en la gama sRGB (croma alto a luminosidad extrema) → recorte de croma declarado como parámetro en ADR-013, no improvisado.
  - `campo-borde` al límite (3.34:1 sobre `papel`) → es el contraejemplo esperado; si ninguna regla lo sostiene, se fija `renglón` a su valor exacto y se dice.
  - Escribir una cifra sin correr su comando → cada cifra del ADR y de los entregables se copia de la salida vista.
