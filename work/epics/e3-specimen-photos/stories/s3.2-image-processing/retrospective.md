# Story s3.2: Image processing — Retrospective

Estimated: M · Actual: M

## Summary

`orquidea.datos.fotos.procesar_foto(bytes)` devuelve una imagen de ancho ≤ 1600 px y una miniatura de lado mayor ≤ 320 px, ambas JPEG reconstruidos desde los píxeles (sin EXIF, GPS, XMP, comentario ni ICC), con la orientación ya aplicada; rechaza con `FotoInvalida` lo que no es JPEG, PNG o WebP, lo que excede 10 MB o 64 MP y lo que no decodifica. Dependencia nueva: `pillow` 12.3.0 (ADR-005). 13 pruebas nuevas; suite completa en verde.

## Finalize (reportado por story-implement)

- Gate: `./scripts/check` en verde (ruff, formato, mypy estricto, 269 pruebas) tras cada tarea y al final.
- Orphaned-test check: el story no cambió ningún módulo existente (solo añadió `datos/fotos.py` y la dependencia), así que ninguna prueba previa importa algo que cambiara; nada que resolver.
- Acceptance: todos los escenarios del scope confirmados por prueba (GPS con 1600x1200 y miniatura 320x240; 800x600 sin ampliar; orientación 6; PNG con alfa; XMP, comentario e ICC; bytes basura, GIF, truncado, 10 MB, 64 MP). Los escenarios del diseño (WebP, JPEG truncado, texto de PNG) también. Ningún criterio deducido se retractó.
- Mutaciones forzadas (cada una puso rojo): quitar la reconstrucción desde píxeles (2 pruebas), quitar `exif_transpose`, quitar el tope de ancho, guardar con `exif=`, quitar el límite de bytes, el de píxeles, admitir GIF, no envolver `OSError`, no tratar la bomba de descompresión.
- Prueba manual (T3): un JPEG de 4000x3000 con GPS, XMP y comentario salió en 1600x1200 (11 537 bytes) y 320x240 (737 bytes), sin los marcadores en ninguno.

## Reviews

**Quality review — PASS.** Se leyeron `fotos.py` y `test_datos_fotos.py`. Un hallazgo corregido en el acto: la prueba del PNG con alfa usaba `# type: ignore[union-attr]` (tipo deshonesto); ahora comprueba `isinstance(pixel, tuple)` (`test(fotos): comprobar el píxel sin ignorar el tipo`). Observación: `Image.MAX_IMAGE_PIXELS` se fija al importar el módulo, es estado global de Pillow; se acepta porque la aplicación es un solo proceso y el tope es el mismo en todo el proyecto.

**Security review — PASS WITH FINDINGS.** Bandit 1.9.4 sobre `src/orquidea/datos/fotos.py` y `tests/test_datos_fotos.py` (el alcance devuelto coincide con la lista esperada): sin hallazgos en `src`; 21 × B101 (severidad baja) en `tests/`, el ruido que ya está en el parking lot ("Bandit reporta B101 en `tests/`"), sin entrada nueva. Guardarraíles: `must-security-001` sostenido (prueba de bytes de salida) y `must-perf-002` sostenido (ancho y miniatura); `should-security-002` — ASVS V12.1.1 y V12.2.1 cubiertos aquí, V12.4 y V12.5 diferidos a s3.3 y s3.4 como el diseño declaró. Limitación: análisis estático, sin cobertura de la subida por HTTP (s3.4).

## What went well

- Escribir la prueba buscando los bytes en la salida, y no `getexif()`, encontró un defecto real antes de que existiera una ruta: el comentario JPEG sobrevivía.
- El recorrido ASVS al diseñar dejó claros los límites que esta historia sí cubre y los que dejó a s3.3/s3.4.

## What to improve

- Cometí T1 con el gate en rojo (un import sin usar en la prueba) porque leí solo el final de la salida; lo enmendé antes de seguir. Para el resto de la épica el gate se confirma por código de salida, no por su cola.
- El diseño listaba el rechazo de un JPEG truncado como escenario, pero no dijo que el fallo aparece al decodificar y no al abrir; `procesar_foto` lo cubre con un segundo `try` alrededor de la reconstrucción.

## Learned

1. About the system: Pillow copia el comentario JPEG de `Image.info` al guardar; `copy`, `resize` y `thumbnail` conservan `info`. Solo una imagen nueva hecha con los bytes de los píxeles queda limpia (memoria `pillow-guarda-comentario-jpeg`).
2. About the process: `ruff format` reformatea también los bloques de código de los `.md` del work log; formatear antes de commitear el diseño.
3. Capability gained: probar la ausencia de metadatos por bytes y forzar mutaciones que cambian el contenido, no solo la forma.
