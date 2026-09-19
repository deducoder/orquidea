# Story s3.5: Thumbnails and remove photo — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · Miniaturas en "Mi colección"

- **Files:** modify `templates/coleccion.html`, `tests/test_web_fotos.py`
- **TDD:** RED prueba: la lista con un ejemplar con foto y otro sin ella muestra una miniatura enlazada solo del primero → GREEN plantilla → REFACTOR
- **Satisfies:** escenarios `@stated` y del ejemplar sin foto
- **Mold:** `coleccion.html` (fila existente) y la ruta de miniatura de s3.4
- **Verify:** hay exactamente una `<img>` de miniatura, con el enlace correcto, y ninguna para el ejemplar sin foto — forced mutations: mostrar la imagen a tamaño completo en la lista (la prueba de la ruta exacta falla); mostrar `<img>` también sin foto (imagen rota); quitar el enlace; then `uv run pytest tests/test_web_fotos.py tests/test_web_coleccion.py -q` y `./scripts/check` completo
- **Commit:** feat(coleccion): mostrar la miniatura de cada ejemplar en la lista

### T2 · Quitar la foto

- **Files:** modify `web/rutas/coleccion.py`, `templates/ejemplar_ficha.html`, `tests/test_web_fotos.py`, `tests/test_web_rutas.py`
- **TDD:** RED pruebas de quitar (archivos, ejemplar intacto, idempotencia, sin CSRF, sin sesión, inexistente, botón solo con foto) → GREEN ruta y botón → REFACTOR
- **Satisfies:** escenarios de quitar la foto
- **Mold:** `quitar_ejemplar` en `rutas/coleccion.py` y `quitar_foto` de `datos/almacen_fotos.py` (s3.3)
- **Verify:** tras quitar, el directorio queda sin los archivos y la fila conserva el ejemplar — forced mutations: llamar a `quitar_con_foto` en lugar de `quitar_foto` (el ejemplar desaparece); no borrar los archivos; devolver 200 sin redirigir; then `uv run pytest tests/test_web_fotos.py tests/test_web_rutas.py tests/test_web_proteccion.py -q` y `./scripts/check` completo
- **Commit:** feat(coleccion): quitar la foto de un ejemplar

### T3 · Manual integration test

- Con `uvicorn` real: subir una foto, ver la miniatura en la lista, quitarla desde la ficha, ver que la lista ya no la muestra y que el directorio queda vacío.
- **Verify:** lista con `<img>` antes, sin `<img>` después, archivos 2 → 0 y el ejemplar sigue.

## Order & risks

- **Execution order:** T1 → T2 → T3 — la miniatura es lo que RF-05 pide; quitar es la corrección.
- **Dependencies:** secuencial.
- **Risks:** el peso de las miniaturas contra `must-perf-001` → se mide en s3.6 con una foto realista.
