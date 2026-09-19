# Story s1.2: Catalog schema and loader — Retrospective

Estimated: M · Actual: 3 tareas más una corrección de revisión, una sesión (sin tracker, sin tiempo registrado)

## Summary

Modelos pydantic de la especie (`orquidea.catalogo.modelo`) con fuente obligatoria y `extra="forbid"`, y `cargar_catalogo` (`orquidea.datos.catalogo`), que valida todos los JSON de un directorio, reúne los errores como `archivo: campo: motivo` y falla sin devolver nada si hay alguno. ADR-002 registra la elección de pydantic. 14 pruebas nuevas; directorio de datos `src/orquidea/datos/catalogo/` vacío (los datos son s1.6).

## Acceptance

- `[stated]` catálogo válido se carga; falta de fuente y campo ausente o de tipo incorrecto nombran archivo y campo: confirmados por `test_catalogo_valido_se_carga_ordenado_por_id`, `test_sin_fuentes_nombra_archivo_y_campo`, `test_campo_anidado_nombra_la_ruta_completa`.
- `[deduced]` todo o nada, JSON roto, ids duplicadas, `./scripts/check` en verde: confirmados por el diseño y por sus pruebas. Ninguno retractado. Escenarios del diseño (directorio vacío, directorio inexistente): cubiertos.
- Finalize: `./scripts/check` verde (ruff, format, mypy strict, 25 pruebas); tests huérfanos: ninguno (los archivos de prueba previos, `test_web_inicio.py`, no importan lo que esta historia cambió); sin tracker, sin registro de tiempo. Integración manual: un directorio con un JSON válido y otro sin `fuentes` falló con `malo.json: fuentes: Field required`; solo con el válido cargó `['epidendrum-radicans']`; el directorio real cargó `[]`.

## Reviews

- **quality-review — PASS WITH RECOMMENDATIONS, ya aplicada.** Hallazgo: `nombres_comunes: list[str]` aceptaba cadenas vacías, sin la restricción que sí tienen los demás textos, y una cadena vacía coincidiría con todo en la búsqueda de s1.4. Corregido con prueba primero en `fix(catalogo): rechaza nombres comunes en blanco`. Sin tipos deshonestos ni excepciones tragadas; las pruebas fallaron bajo mutación.
- **security-review — PASS WITH FINDINGS.** Bandit 1.9.4 sobre los 6 `.py` cambiados (igual que la lista esperada): 14 × B101, todos en `tests/`, ya estacionados en el parking lot desde s1.1; ninguno en código de aplicación. Guardrails: `must-data-001` se cumple en el esquema; `must-security-001` (EXIF) y `should-security-002` (ASVS L2) no aplican (sin fotos ni sesión). El cargador solo lee archivos del repositorio; no ejecuta nada ni sigue rutas externas.

## What went well

El diseño exigió escribir el error esperado literal (`x.json: fuentes: Field required`) antes de codificar, y las pruebas lo afirman con igualdad exacta, no con `in`. Las mutaciones de la carga encontraron el caso de la raíz no-objeto (campo vacío en el mensaje), que se cubrió con prueba.

## What to improve

- Las mutaciones dieron resultados falsos ("sobrevivió") porque el bytecode obsoleto se reutilizaba (mismo tamaño y mismo segundo de mtime). Hay que correr las mutaciones con `PYTHONDONTWRITEBYTECODE=1` y borrando `__pycache__`; sin eso, un mutante "vivo" no es evidencia.
- `ruff format` formatea también los bloques de código de los `.md`: el `design.md` de la historia rompió el gate hasta formatearlo. Los bloques de código de los diseños deben escribirse ya formateados.
- Junté dos fases en un solo commit al principio y lo separé antes de seguir: `design` y `plan` son commits distintos.
- El plan asignaba el directorio inexistente a T3, pero T2 ya lo cubrió porque lo pedía la propia carga; T3 quedó solo con duplicadas.

## Learned

1. About the system: pydantic devuelve rutas de campo como tuplas (`loc`), incluidos índices de lista; unidas con `.` dan `fuentes.1`. Una raíz que no es objeto da `loc == ()`, que se muestra como `(raíz)`.
2. About the process: mutar sin invalidar el bytecode puede dar falsos "supervivientes"; el criterio de verificación es un rojo real, no la ausencia de uno.
3. Capability gained: contrato del catálogo (RF-01, `must-data-001`) que s1.3, s1.4 y s1.6 consumen; e2 ligará ejemplares a `Especie.id`.
