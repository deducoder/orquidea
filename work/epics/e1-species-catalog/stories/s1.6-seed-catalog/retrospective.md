# Story s1.6: Seed catalog — Retrospective

Estimated: S · Actual: investigación amplia más 2 tareas de código, una sesión (sin tracker, sin tiempo registrado)

## Summary

100 fichas JSON de orquídeas nativas de Chiapas en `src/orquidea/datos/catalogo/`, con cuidados y fuentes, respaldadas por `work/research/chiapas-orchid-seed/report.md`. La aplicación las sirve tal cual (100 enlaces en `/especies`, ficha de cada una). 5 pruebas nuevas.

## Acceptance

- `[stated]` el catálogo real carga 100 especies válidas: `test_el_catalogo_real_tiene_al_menos_cien_especies`; el directorio real tiene 100 archivos, 100 ids distintas.
- `[stated]` cada especie y cada cuidado citan una fuente real consultada: la investigación leyó las páginas de la AOS y la API de iNaturalist; la prueba fija que toda fuente trae URL y "consultada el". Ninguna cita se inventó ni se copió literal (paráfrasis).
- `[stated]` nativas de Chiapas, entre las más conocidas y populares: cumplido con una **proxy** (ver abajo), que es lo que el humano debe revisar.
- `[deduced]` cuidado de género declarado como tal: confirmado y fijado por `test_los_cuidados_de_genero_lo_dicen`. `must-perf-001`: pendiente de la medición con "Slow 3G" de `epic-review`; medida de peso hoy: lista 1,884 B, ficha 1,035 B, htmx 16,356 B con gzip (≪ 200 KB).
- Finalize: `./scripts/check` verde (ruff, format, mypy strict, 51 pruebas); tests huérfanos: ninguno; sin tracker, sin registro de tiempo. Integración manual con uvicorn real: `/`, `/especies`, ficha, `?q=ORQUIDEA` (16 resultados) y htmx, todos 200.

## Reviews

- **quality-review — PASS WITH RECOMMENDATIONS.** Dos pruebas (fuentes con URL, género declarado) pasarían en vacío con un directorio vacío; la primera prueba (≥ 100) evita que eso ocurra sin avisar. Las mutaciones (sin URL, sin fecha, género no declarado, un archivo sin `fuentes`) ponen las pruebas en rojo. La ficha repite una cita larga cuatro veces: estacionado en el parking lot.
- **security-review — PASS.** Bandit 1.9.4 sobre los 2 `.py` cambiados: solo B101 en `tests/` (estacionado). Sin código nuevo de aplicación. Los datos son JSON estático que Jinja escapa.

## Para revisión del humano (lo más importante de esta historia)

1. **Los cuidados son del género, no de la especie.** Ninguna fuente consultada da cuidados medidos para cada una de las 100 especies. Cada dato lo dice en su fuente y en la descripción. Un coleccionista que necesite precisión por especie verá el límite escrito.
2. **"Más conocidas y populares" = más observadas en iNaturalist en Chiapas.** No mide el comercio de plantas ni el cultivo; incluye especies diminutas poco cultivadas (p. ej. *Pleurothallis*, *Platystele*) y deja fuera las de géneros sin fuente (p. ej. *Cyrtopodium*, *Vanilla planifolia* sí entró). Si se prefiere otra regla, la lista se regenera cambiando el criterio.
3. **Nativa** se apoya en el filtro de iNaturalist; Kew POWO estaba bloqueado por un desafío anti-bots y no se eludió.
4. Sin revisión de un experto botánico.

## What went well

Los resúmenes de `WebFetch` perdían detalle, así que se bajó el HTML crudo con `curl` y se leyó el texto de cada tarjeta antes de parafrasear: cada dato de cuidado sale de un texto que se leyó. Se detectó y dejó por escrito la advertencia de la propia AOS ("puede no ser representativa").

## What to improve

Un `cat <<EOF` sin comillas interpretó los backticks del informe como comandos y mutiló el texto en silencio; se detectó al releer el archivo y se rehízo con un heredoc entre comillas. Al escribir Markdown con backticks desde la shell, usar siempre `<<'EOF'`.

## Learned

1. About the system: la AOS publica una "Care and Culture Card" por género en `https://www.aos.org/explore/{género}` con luz, temperatura, riego y sustrato; es la fuente uniforme que encaja con el esquema.
2. About the process: una historia de datos con criterio `[stated]` numérico ("100") pide comprobar primero si hay fuentes para cumplirlo; aquí sí las hubo, pero el camino de salida era un stop P4.
3. Capability gained: 100 especies reales y su mecanismo de regeneración; s1.5 puede mostrar una especie real en línea y `epic-review` puede medir `must-perf-001` sobre datos reales.
