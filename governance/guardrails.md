# Guardrails: Orquídea

Quality bars the work must respect. `Level` is `must` or `should`. `ID` =
`{level}-{category}-{NNN}`. Each guardrail says how it's verified and, where it
applies, which requirement it derives from.

| ID | Level | Guardrail | Verification | Derived from |
|----|-------|-----------|--------------|--------------|
| must-test-001 | must | Todo comportamiento nace de una prueba que falla primero (TDD); ningún requisito sin pruebas. | `./scripts/check` corre las pruebas; se revisa en cada story-review | — |
| must-quality-001 | must | El linter (ruff) no reporta errores. | `./scripts/check` | — |
| must-quality-002 | must | El formateador (ruff format) no reporta cambios pendientes. | `./scripts/check` | — |
| must-quality-003 | must | Tipado estricto (mypy `strict`) sin errores. | `./scripts/check` | — |
| must-data-001 | must | Cada especie del catálogo cita al menos una fuente (literatura o herbario). | El esquema JSON la exige; un archivo sin fuente se rechaza al cargar | RF-01, RF-03 |
| must-perf-001 | must | La primera carga es usable en ≤ 5 s con el perfil de red "Slow 3G" y transfiere ≤ 200 KB (gzip), sin contar fotos. | Medición manual con las herramientas del navegador en cada epic-review | — |
| must-perf-002 | must | Las fotos se reducen al subirlas (ancho máximo 1600 px) y en las listas se sirven en miniatura. | Prueba automatizada del procesamiento de imágenes | RF-05 |
| must-security-001 | must | Toda foto se guarda sin metadatos EXIF, incluida la ubicación GPS. Motivo: una foto de una orquídea nativa con coordenadas puede revelar dónde crecen poblaciones silvestres (riesgo de saqueo) y la ubicación del domicilio del usuario. Propuesto desde el dominio, no desde la tabla de marcos de referencia. | Prueba automatizada: una imagen con EXIF/GPS sale sin ellos | RF-05 |
| should-security-002 | should | Línea base OWASP ASVS nivel 2. Disparador: la aplicación tiene inicio de sesión ("login básico", RF-08); fuente: OWASP ASVS. | security-review en cada historia, contra los requisitos L2 aplicables | — |
