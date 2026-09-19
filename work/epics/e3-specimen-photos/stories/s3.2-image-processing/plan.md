# Story s3.2: Image processing — Plan

> Size: M
> Pause: none (default)

## Tasks

### T1 · Reducir y reconstruir la imagen sin metadatos

- **Files:** create `src/orquidea/datos/fotos.py`, `tests/test_datos_fotos.py`; modify `pyproject.toml`, `uv.lock` (`uv add pillow`)
- **TDD:** RED prueba con un JPEG 4000x3000 con GPS que espera 1600x1200, miniatura 320x240 y EXIF vacío en ambas → GREEN `procesar_foto` con `ImageOps.exif_transpose`, `thumbnail`/`resize` y `save(format="JPEG")` sin argumentos de metadatos → REFACTOR una sola función `_jpeg(imagen, ancho_o_lado, calidad)`
- **Satisfies:** escenario `@stated` GPS; imagen 800x600 no se amplía; orientación 6; PNG con alfa
- **Mold:** ADR-005; `src/orquidea/datos/base.py` (módulo de datos con excepción propia)
- **Verify:** la salida de una imagen con GPS/XMP/comentario/ICC no contiene esos bytes y mide ≤ 1600 px — forced mutations, each of which must turn it red: guardar pasando `exif=` o `icc_profile=` del original; devolver el archivo original sin reconstruir (equivalent form); quitar `exif_transpose` (la prueba de orientación 6 debe fallar); quitar el tope de ancho; then `uv run pytest tests/test_datos_fotos.py -q` y `./scripts/check` completo (archivo nuevo escaneado por el gate)
- **Commit:** feat(fotos): reducir la foto y quitarle los metadatos

### T2 · Rechazar entradas no confiables

- **Files:** modify `src/orquidea/datos/fotos.py`, `tests/test_datos_fotos.py`
- **TDD:** RED pruebas de bytes basura, GIF, JPEG truncado, más de `TAMANO_MAXIMO`, más de `PIXELES_MAXIMOS` (PNG con cabecera enorme y datos mínimos) → GREEN `FotoInvalida` con mensajes en español, tamaño comprobado antes de abrir y píxeles antes de `load()` → REFACTOR
- **Satisfies:** escenarios de bytes inválidos, formato no admitido, tamaño y píxeles; WebP y JPEG truncado del diseño
- **Mold:** `EjemplarInvalido` en `src/orquidea/coleccion/modelo.py` (excepción de dominio con mensaje en español)
- **Verify:** ningún rechazo deja escapar una excepción de Pillow y el de píxeles ocurre sin decodificar los píxeles — forced mutations: quitar la comprobación de `TAMANO_MAXIMO`; quitar la de `PIXELES_MAXIMOS` (la prueba con 20000x20000 debe volverse lenta o fallar por otra excepción); aceptar GIF añadiéndolo a `FORMATOS` (equivalent form); no envolver `OSError` (el JPEG truncado debe fallar); then `uv run pytest tests/test_datos_fotos.py -q` y `./scripts/check`
- **Commit:** feat(fotos): rechazar archivos que no son fotos admisibles

### T3 · Manual integration test

- Con una foto JPEG real con GPS (generada con Pillow y `exiftool`-independiente: se inyecta un GPS y se lee de vuelta) ejecutar `uv run python -c` que procese, escriba a un directorio temporal y verifique con una lectura independiente de los bytes (buscar los marcadores `Exif`, `http://ns.adobe.com/xap` y las coordenadas) que no hay rastro.
- **Verify:** los marcadores no aparecen en ninguno de los dos archivos y `./scripts/check` está en verde.

## Order & risks

- **Execution order:** T1 → T2 → T3 — T1 contiene el riesgo de seguridad (metadatos); T2 cierra la superficie de entrada.
- **Dependencies:** secuencial.
- **Risks:** Pillow no se instala o su versión cambia la API de `Exif`/`comment` → ver el error y ajustar la prueba; si falla la instalación es P3/P5. Una prueba que mira solo `getexif()` no ve XMP ni comentarios → las pruebas buscan los bytes en la salida.
