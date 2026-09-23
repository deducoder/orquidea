# Story s5.1: Commission criterion — Plan

> Size: S
> Pause: none (default) — salvo las dos paradas del ciclo nombradas abajo (antes de producir, y la firma de la mitad juzgada)

## Container acts around the tasks

No son tareas: son los actos del registro que la técnica `adr` nombra por su estado, con su propio mensaje.

- **A0 · Abrir ADR-009** (`record-open`), antes de T1: `records/decisions/adr-009-criterio-del-encargo-de-identidad.md` en `proposed`, con la pregunta, las opciones de criterio consideradas, la rejilla criterio × opción con el estrato de cada uno, el catálogo resuelto, el alcance del criterio 2 decidido por el humano el 2026-09-22 (todo el texto de tamaño normal) y `## Decision` sin resolver. Commit `docs(s5.1): add ADR-009`.
- **A1 · Anotar los rojos** (`counterexample`), después de T3: la salida literal de cada comprobación sobre su sujeto violador, y el criterio 3 como "no aplica: no hay oráculo". Commit `docs(s5.1): update ADR-009`, antes de T4.
- **A2 · Completar ADR-009** (`record-complete`), después de T4 y de la firma: `accepted`, decisión, consecuencias y alternativas. Commit `docs(s5.1): publish ADR-009`. `published: no` — el proyecto no tiene espacio de documentación externo (igual que ADR-008).

## Tasks

### T1 · Medir el peso de los recursos de la identidad contra 50 KB

- **Files:** modify `scripts/medir-primera-carga.py` (`MedicionDeIdentidad`, `TOPE_DE_IDENTIDAD`, `medir_identidad`, opción `--identidad DIR` en `main`); modify `tests/test_medicion.py`.
- **TDD:** RED pruebas de `medir_identidad` (suma el gzip de cada archivo del directorio; frontera 51 200 pasa y 51 201 no, con archivos construidos al tamaño gzip exacto o midiendo y comparando contra el tope inyectado) y de `main(["--identidad", …])` (0 dentro, 1 sobre el tope con "PASA DEL TOPE", 2 con directorio vacío o inexistente y "nada que medir") → GREEN la función y la rama de `main` → REFACTOR reusar `_kb` y el patrón de impresión existente.
- **Satisfies:** scope, escenario del criterio 1 y el de población vacía; design Must 2.
- **Mold:** `scripts/medir-primera-carga.py::main` y `medir` (medición en gzip, `--presupuesto`, salida 0/1); contrato de salida 0/1/2 de `conventions/mechanical` (gemba-design 0.21.0).
- **Verify:** un directorio sobre el tope nunca sale 0 y uno sin archivos nunca sale 0 — forced mutations, each must turn it red: comparar con `<` en lugar de `<=` (la frontera de 51 200 cambia); devolver 0 con población vacía; contar el tamaño sin comprimir en lugar del gzip; el modo por defecto de `main` sin `--identidad` sigue dando exactamente la salida de hoy (prueba existente `test_el_script_sale_con_1_si_pasa_del_presupuesto_y_con_0_si_no` sin cambios); then `uv run pytest tests/test_medicion.py -q` y `./scripts/check`.
- **Commit:** feat(medicion): measure the identity assets against a 50 KB cap

### T2 · Comprobar el contraste del texto contra 7:1

- **Files:** create `scripts/contraste-de-lectura.py`; create `tests/test_contraste_de_lectura.py`.
- **TDD:** RED pruebas de la razón (`#767676`/`#ffffff` = 4.54, `#595959`/`#ffffff` = 7.00, `#5a5a5a`/`#ffffff` = 6.90, simétrica), de la lectura de tablas (encuentra `Foreground | Ground | Kind` y `Role | Value` por la primera celda de su encabezado, en cualquier lugar del markdown), del juicio (solo `Kind = text`; `large` y `component` no se juzgan ni se cuentan) y de `main` (0 todo pasa, 1 algún par bajo 7:1 nombrándolo, 2 sin pares de texto, rol que no resuelve o color ilegible nombrando la entrada) → GREEN el script mínimo → REFACTOR.
- **Satisfies:** scope, escenario del criterio 2 y el de población vacía; design Must 3.
- **Mold:** contrato y formato de tablas de `conventions/mechanical/convention.md` y `instruments/tokens.py pairs` (gemba-design 0.21.0); fórmula de `skills/reviews/survival-review/scripts/contrast.py` con su caso de control `#767676`.
- **Verify:** ningún par de texto bajo 7:1 sale 0, y sin pares nunca sale 0 — forced mutations, each must turn it red: umbral 4.5 en lugar de 7 (`#767676` pasaría); `>` en lugar de `>=` (`#595959` a 7.00 fallaría); juzgar también `large` (una tabla con un `large` a 5:1 cambiaría de 0 a 1); quitar la tabla de pares (debe dar 2, no 0); un rol inexistente en la tabla de pares (debe dar 2 nombrándolo); then `uv run pytest tests/test_contraste_de_lectura.py -q` y `./scripts/check` (archivo nuevo: gate completo).
- **Commit:** feat(identidad): check that text pairs reach 7:1 contrast

### T3 · Contraejemplos: ver cada comprobación en rojo (prueba de integración manual)

- Correr las dos comprobaciones como las correrá una persona, sobre sujetos construidos para violar su criterio, en el scratchpad (no en el repositorio): un directorio con un archivo aleatorio de 60 KB (`fuente.woff2`), un directorio vacío, un markdown con `#767676` sobre `#ffffff` como `text`, uno con `#595959` (el control que pasa) y uno sin tabla.
- **Verify:** criterio 1 → exit 1 con el peso y el tope; vacío → exit 2 "nada que medir"; criterio 2 → exit 1 nombrando el par y 4.54:1; control → exit 0 con la población contada (1); sin tabla → exit 2. Cada salida se copia literalmente a ADR-009 (acto A1). Un rojo que viene de otra cosa (archivo inexistente, script que no corre) no cuenta como el rojo del criterio.
- Sin commit de código: su producto es el acto A1.

### T4 · Escribir el entregable del encargo

- **Files:** create `governance/identity/commission.md` desde `skills/techniques/commission/assets/commission.md` (gemba-design 0.21.0).
- **TDD:** no aplica — documento sin comportamiento; el gate lo cubre (`ruff format` sobre los bloques de código, `check-work-log-layout`, `check-published-citations`).
- **Satisfies:** scope, escenario de `commission.md` y done-when de `decision: ADR-009`.
- **Mold:** `skills/techniques/commission/assets/commission.md`; convención `deliverables` (raíz `governance/identity/`).
- **Verify:** `decision: ADR-009` en el frontmatter; tres criterios con estrato y "se espera que toque"; las ocho entradas del catálogo, cada una aplicada o con su razón; medido y juzgado separados, con la mitad juzgada **firmada por el humano o `unsigned`**; then `./scripts/check` (archivo nuevo: gate completo).
- **Parada:** antes de escribir la mitad juzgada se pregunta al humano si la firma con su nombre y fecha; sin respuesta, se escribe `unsigned`.
- **Commit:** docs(identity): add the commission criteria

### T5 · Prueba de integración manual del orden

- **Verify:** `git log --format='%h %ad %s' --date=iso-strict develop..HEAD` muestra `docs(s5.1): add ADR-009` antes que T1, `docs(s5.1): update ADR-009` antes que T4, y `docs(s5.1): publish ADR-009` al final; `grep -n '^status:' records/decisions/adr-009-*` → `accepted`; `uv run python scripts/medir-primera-carga.py` sin `--identidad` imprime lo mismo que en `develop`.

## Order & risks

- **Execution order:** A0 → T1 → T2 → T3 → A1 → T4 → A2 → T5 — el orden lo fija el ciclo: el registro antes de toda comprobación, los rojos antes del entregable. Entre T1 y T2, la de peso primero porque toca un script existente con pruebas que no deben cambiar.
- **Dependencies:** secuenciales; T1 y T2 no dependen entre sí, pero ambas de A0 y T3 de ambas.
- **Risks:**
  - La copia de la fórmula WCAG diverge del addon → la prueba de control `#767676` = 4.54 es la del propio addon; si el addon cambia su fórmula, la divergencia se ve comparando esa cifra.
  - `ruff format` reformatea bloques de Python en los `.md` y el hook rechaza el commit (pasó en el diseño) → correr `uv run ruff format` sobre cada `.md` antes de hacer commit.
  - Firmar por el humano sin su respuesta → parada explícita en T4; `unsigned` si no hay firma.
