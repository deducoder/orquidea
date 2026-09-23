# Story s5.1: Commission criterion — Retrospective

Estimated: S · Actual: S (5 tareas del plan más un arreglo de la revisión; 438 s de implementación según `implementation-time.sh develop s5.1`, medido antes del arreglo)

## Summary

El criterio de toda la identidad visual quedó escrito antes de cualquier pieza: ADR-009 se abrió en `proposed` (`50f3ed2`) antes de todo código, las comprobaciones del peso ≤ 50 KB (`adf0e45`) y del contraste ≥ 7:1 en todo texto normal (`e51c828`) se vieron en rojo sobre sujetos que las violan y esos rojos se escribieron en el ADR (`8c6f6da`) antes de `governance/identity/commission.md` (`cdda7e3`), firmado por el humano; ADR-009 pasó a `accepted` en el mismo archivo (`14b9938`). La revisión encontró y arregló un verde falso (`09d50d9`).

### Finalize (lo que `story-implement` reportó)

- Gate: `./scripts/check` → `✓ gates passed`, 512 pruebas, antes del arreglo de la revisión; tras `09d50d9`, verde de nuevo (el hook `pre-commit` lo corrió).
- Orden: `git log --reverse --date=iso-strict develop..HEAD` muestra `add ADR-009` (21:32:24) antes de T1 (21:35:11), `update ADR-009` (21:38:34) antes de `commission.md` (21:39:42) y `publish ADR-009` (21:40:14) al final.
- Modo por defecto de `medir-primera-carga.py`: misma salida que `develop` con `--n 3` (comparada sin las cifras en KB).
- Pruebas huérfanas: `tests/test_despliegue.py` menciona el script y la historia no la tocó; solo afirma que el README lo nombra, sigue siendo cierta y pasa (16 pruebas). Documentar `--identidad` en el README queda para s5.7, cuando haya recursos que medir.
- Aceptación: los seis escenarios del scope se cumplen (cuatro `@stated`, dos `@deduced` confirmados por el diseño); ninguno se retractó. La pregunta del diseño (alcance del criterio 2) la respondió el humano: todo el texto de tamaño normal.
- `quality-review`: un hallazgo crítico — `.gitkeep` contaba como recurso y daba OK con población 1 — corregido en `09d50d9`; observación descartada en voz alta: `scripts/` fuera de mypy (preexistente). `security-review`: PASS; Bandit, 65 B101 en las pruebas, ninguno en los scripts.

## What went well

- Abrir el ADR antes que el código hizo que el orden se verificara con `git log` y no con la palabra de nadie: cuatro actos del registro con cuatro mensajes (`add`, `update`, `publish`) y fechas de autor en orden.
- Los controles al lado de cada rojo (vacío → 2, par que cumple → 0) dejan ver en el ADR que el rojo es del criterio y no de un archivo que falta.
- Reusar el formato de tablas de `tokens.py pairs` hace que `contraste-de-lectura.py` pueda correr sobre `palette.md` y `semantics.md` sin conversión.

## What to improve

- **El plan predijo el resultado de una mutación sin correrla.** Decía que `>` en lugar de `>=` rompería `#595959` "a 7.00:1"; da 7.0047 y la mutación sobrevivió. Se resolvió sacando `llega_al_umbral` y probándolo con 7.0 exacto. En adelante el plan escribe la mutación y la propiedad, no su resultado.
- **Las mutaciones del plan no incluían "un sujeto falso presente".** Todas quitaban el sujeto o rompían el cálculo; ninguna ponía algo que no es sujeto donde se busca. Lo encontró la revisión, no el TDD.
- **`ruff format` rechazó tres commits** (design, T1, T2) por líneas largas o bloques de código en `.md`, aunque la memoria del proyecto ya lo advertía: formatear antes de cada commit, no después del rechazo.

## Learned

1. About the system: la medición de primera carga ya contaba todo `/static` que la página enlaza como "JavaScript"; cuando s5.7 enlace la hoja, el total de `must-perf-001` la incluirá sin cambios, pero las fuentes (enlazadas desde el CSS, no desde la página) no — por eso la identidad se mide por directorio.
2. About the process: la técnica `commission` cabe en una historia S cuando los criterios se aprobaron antes de abrirla; el costo real estuvo en las comprobaciones, no en los documentos.
3. Capability gained: dos instrumentos del proyecto con el contrato 0/1/2 de `conventions/mechanical`, listos para s5.3 a s5.7; y dos memorias: [[mutacion-de-frontera-se-prueba-en-el-predicado]] y [[poblacion-no-cuenta-lo-que-no-es-sujeto]].
