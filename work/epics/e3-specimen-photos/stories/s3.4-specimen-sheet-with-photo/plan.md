# Story s3.4: Specimen sheet with photo — Plan

> Size: M
> Pause: none (default)

## Tasks

### T1 · Limitar el tamaño del cuerpo de la petición

- **Files:** create `web/limite.py`, `tests/test_web_limite.py`; modify `web/app.py`
- **TDD:** RED pruebas ASGI directas (con `Content-Length` grande, chunked sin cabecera, dentro del límite) y una web (`POST` gigante a `/acceso` → 413) → GREEN `LimiteDeCuerpo` y `add_middleware` → REFACTOR
- **Satisfies:** escenarios del cuerpo excedido (con y sin `Content-Length`)
- **Mold:** ADR-006 y `web/app.py` (middleware existente); ninguno de terceros: `Starlette` no trae límite de cuerpo
- **Verify:** el cuerpo excedido nunca llega a la aplicación y uno dentro del límite pasa intacto — forced mutations: quitar la comprobación de `Content-Length`; quitar el conteo de bytes (el caso chunked debe fallar); contar solo el último mensaje en vez del acumulado (equivalent form); no montar el middleware en `app.py`; then `uv run pytest tests/test_web_limite.py -q` y `./scripts/check` completo
- **Commit:** feat(web): limitar el tamaño del cuerpo de la petición

### T2 · Ficha del ejemplar y entrega de la imagen

- **Files:** modify `web/rutas/coleccion.py`, `templates/coleccion.html`, `tests/test_web_rutas.py`; create `templates/ejemplar_ficha.html`, `tests/test_web_fotos.py`
- **TDD:** RED pruebas de la ficha (con y sin foto, 404, sin sesión), de las dos imágenes (contenido, tipo, `nosniff`, 404 sin foto, 404 con archivo ausente, 404 con nombre inválido en la base) y del orden con `/coleccion/nuevo` → GREEN rutas y plantilla → REFACTOR
- **Satisfies:** ficha con y sin foto; entrega protegida; 404
- **Mold:** `confirmar_baja` en `rutas/coleccion.py` (ruta con `_ejemplar_o_404` y `resolver`) y `confirmar_baja.html`
- **Verify:** la imagen entregada es exactamente el archivo guardado y solo con sesión — forced mutations: registrar `/coleccion/{id}` antes de `/coleccion/nuevo` (la prueba de orden y la de alta fallan); formar la ruta con el `id` en vez del nombre guardado; quitar el 404 por archivo ausente (500); entregar sin sesión (dependencia global fuera); then `uv run pytest tests/test_web_fotos.py tests/test_web_rutas.py tests/test_web_proteccion.py -q` y `./scripts/check` completo
- **Commit:** feat(coleccion): ficha del ejemplar que muestra su foto

### T3 · Subir la foto

- **Files:** modify `web/rutas/coleccion.py`, `templates/ejemplar_ficha.html`, `tests/test_web_fotos.py`, `tests/test_web_rutas.py`
- **TDD:** RED prueba de extremo a extremo (JPEG con GPS 4000x3000 → 303, archivo de 1600 px sin metadatos, ficha con la imagen), reemplazo, sin CSRF, no imagen, GIF, sin archivo, 413, disco lleno y sin sesión → GREEN `POST /coleccion/{id}/foto` → REFACTOR
- **Satisfies:** los dos `@stated` y los demás escenarios de subida
- **Mold:** `agregar_ejemplar_propio` (validar, error 422 con el formulario, redirigir 303) y ADR-005/006
- **Verify:** tras cada rechazo el directorio y la fila quedan como estaban, y tras una subida buena el archivo no lleva metadatos — forced mutations: guardar los bytes originales en vez de `procesar_foto` (la prueba de GPS falla); dejar escapar `FotoInvalida` (500); guardar antes de procesar; no exigir CSRF en la ruta (la dependencia global lo hace, por eso la prueba de CSRF ejercita la ruta real, no la dependencia); then `uv run pytest tests/test_web_fotos.py -q` y `./scripts/check` completo
- **Commit:** feat(coleccion): subir la foto de un ejemplar desde su ficha

### T4 · Manual integration test

- Con `uvicorn` real, hash real y directorio temporal: iniciar sesión con `curl`, subir una foto JPEG con GPS, verla en la ficha, pedir imagen y miniatura, subir tres fotos en paralelo al mismo ejemplar, subir un archivo de 12 MiB (413) y uno chunked sin `Content-Length`, y comprobar el directorio y los bytes con una lectura independiente.
- **Verify:** un solo par de archivos vigente tras las subidas en paralelo, sin `Exif` ni GPS en ellos, 413 en ambos casos y ningún archivo tras los rechazos.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 — el límite del cuerpo es la defensa de recursos y debe existir antes de aceptar un solo archivo; T2 antes que T3 para que la subida tenga dónde verse.
- **Dependencies:** secuencial.
- **Risks:** el middleware ASGI mal escrito rompe otras rutas (la suite completa lo cubre); el cuerpo multipart se lee en la dependencia global antes del handler (`csrf` es `Form`), por eso el límite va en un middleware y no en la ruta; una excepción del middleware de límite dentro de `BaseHTTPMiddleware` de las cabeceras podría escapar como 500 → la prueba web de 413 lo detecta.
