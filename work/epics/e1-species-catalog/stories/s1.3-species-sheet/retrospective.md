# Story s1.3: Species sheet — Retrospective

Estimated: M · Actual: 3 tareas de código, una sesión (sin tracker, sin tiempo registrado)

## Summary

`app.py` carga el catálogo una vez al importarse (un JSON inválido detiene el arranque) y sirve `GET /especies` (lista con mensaje de vacío) y `GET /especies/{id}` (ficha con nombre, nombres comunes, descripción, los cuatro cuidados cada uno con su fuente y las fuentes de la especie; 404 si no existe). La página de inicio enlaza a la lista. 6 pruebas nuevas.

## Acceptance

- `[stated]` lista con enlace por especie, ficha con datos generales y los cuatro cuidados, fuente junto a cada cuidado: confirmados por `test_lista_muestra_nombre_y_enlace_de_cada_especie` y `test_ficha_muestra_datos_generales_y_cada_cuidado_con_su_fuente` (una fuente distinta por cuidado en la fixture, para que una fuente repetida falle).
- `[deduced]` 404, datos escapados, catálogo vacío sin error: confirmados por el diseño y sus pruebas. Escenario añadido por el diseño (catálogo inválido detiene el arranque): `test_catalogo_invalido_detiene_el_arranque`. Ninguno retractado.
- Finalize: `./scripts/check` verde (ruff, format, mypy strict, 31 pruebas); tests huérfanos: `tests/test_web_inicio.py` importa `orquidea.web.app`, que esta historia cambió sin tocar ese archivo; se leyó y sigue cubriendo GET / y htmx, y pasa. Sin tracker, sin registro de tiempo. Integración manual con uvicorn real y un catálogo temporal de una especie (no versionado): lista, ficha con las cuatro fuentes y 404 correctos; el catálogo real (vacío) da 200 con el mensaje.

## Reviews

- **quality-review — PASS.** `app.py`, las tres plantillas y las pruebas leídas. Observación: `request.app.state.catalogo` es `Any` para mypy (el estado de Starlette no está tipado), así que el tipo `list[Especie]` no lo verifica el gate en las rutas; aceptable con dos rutas, a revisar si crecen los consumidores. La prueba del 404 pasó en vacío antes de existir la ruta (FastAPI ya devuelve 404); solo la mutación "sin 404" demostró su valor.
- **security-review — PASS WITH FINDINGS.** Bandit 1.9.4 sobre `app.py` y `tests/test_web_especies.py` (la lista esperada): 14 × B101, todos en `tests/`, ya estacionados; ninguno en `app.py`. Guardrails: `must-security-001` (EXIF) no aplica; `should-security-002` (ASVS L2) no aplica todavía, sin sesión, pero el escape de datos (V5) queda cubierto por prueba. El `id` de la URL solo se compara con los ids cargados, no toca disco ni SQL.

## What went well

Las mutaciones se corrieron con bytecode desactivado desde el principio (lección de s1.2) y los tres mutantes de la ficha murieron a la primera. La prueba de arranque inválido carga una copia del módulo con `importlib` en vez de recargar `orquidea.web.app`, así que no contamina a las demás.

## What to improve

`ruff format` volvió a fallar en un archivo de prueba nuevo porque solo formateé `src`; el flujo es `uv run ruff format` completo antes del gate, no por carpeta.

## Learned

1. About the system: `app.state` es `Any` para mypy; el catálogo como estado de la aplicación funciona pero pierde el tipo en las rutas.
2. About the process: una prueba de "404" sobre una ruta que aún no existe pasa en vacío; el rojo real lo da la mutación.
3. Capability gained: primer camino completo JSON validado a ficha; s1.4 añade la búsqueda sobre `request.app.state.catalogo`, y s1.5 desplegará esto.
