# Story s3.4: Specimen sheet with photo — Retrospective

Estimated: M · Actual: M

## Summary

Esqueleto funcional de la épica: la métrica líder del brief queda demostrada por HTTP. Nuevas rutas en el router de la colección: `GET /coleccion/{id}` (ficha del ejemplar con foto y formulario multipart con CSRF), `POST /coleccion/{id}/foto` (valida con `procesar_foto`, guarda con `poner_foto`, traduce los errores a 422/404/500 controlados) y `GET /coleccion/{id}/foto` y `.../foto/miniatura` (`FileResponse` de un archivo cuyo nombre sale de la base, tipo fijo `image/jpeg`, protegido por la sesión). Nuevo `web/limite.py` (`LimiteDeCuerpo`): 413 al pasar de 11 MiB, con y sin `Content-Length`. "Mi colección" gana el enlace "Ficha". 329 pruebas en verde.

## Finalize (reportado por story-implement)

- Gate: `./scripts/check` en verde (ruff, formato, mypy estricto, 329 pruebas) tras cada tarea y al final; cada commit se hizo con `./scripts/check && git commit`.
- Orphaned-test check: se corrieron todas las pruebas que importan `orquidea.web.app`, `rutas.coleccion` o `tests.fabricas`. `test_web_rutas.py` se actualizó con las cuatro rutas nuevas (y su prueba de orden dejó de ser vacía: `/coleccion/nuevo` frente a `/coleccion/{id}`); `test_web_proteccion.py` recorre las rutas nuevas sin cambios (sin sesión, todas redirigen); `test_web_coleccion.py` sigue en verde con el enlace nuevo. Ninguna huérfana sin resolver.
- Acceptance: todos los escenarios del scope y del diseño confirmados por prueba: métrica líder por HTTP (JPEG 4000x3000 con GPS, XMP y comentario → archivos de 1600 y 320 px sin `Exif`, XMP ni GPS en los bytes); ficha con y sin foto y con especie; reemplazo que borra los archivos anteriores; sin sesión redirige; sin CSRF 403; archivo inválido, GIF que dice ser JPEG, sin archivo y mayor a 10 MB 422; mayor al cuerpo permitido 413; ejemplar inexistente 404 (también con archivo inválido); archivo ausente o nombre inválido en la base 404; disco lleno 500 controlado; carrera de `poner_foto` 404. Ningún criterio deducido se retractó.
- Mutaciones forzadas (cada una puso rojo, tras cerrar tres huecos que primero sobrevivieron): guardar los bytes originales, dejar escapar `FotoInvalida` u `OSError`, quitar el 404 por ejemplar inexistente y por carrera, no comprobar el archivo vacío, ficha antes de `nuevo`, ruta con el id, quitar el 404 por archivo ausente o nombre inválido, miniatura por imagen; en el límite: quitar la comprobación de `Content-Length`, quitar el conteo, contar solo el último trozo, no montar el middleware, no sustituir la respuesta.
- Prueba manual (T4) con `uvicorn` real, hash real y directorio temporal: subida de un JPEG con GPS 303; la ficha muestra `<img src="/coleccion/1/foto">`; imagen 200 `image/jpeg` (1600x1200, 11 535 bytes) y miniatura 320x240 (735 bytes), ambas sin `Exif`, XMP ni el texto del comentario; imagen sin sesión 303 al acceso; subir sin CSRF 403; `.txt` 422; 12 MiB multipart con `Content-Length` 413 y multipart chunked 413; 6 subidas simultáneas al mismo ejemplar: seis 303 y exactamente un par de archivos vigente, el que la base nombra; sin errores en el registro del servidor. Un formulario urlencoded chunked de 12 MiB responde 400, no 413: lo rechaza el analizador de formularios del framework al pasar 1 MiB de un campo, antes de que actúe el límite; queda rechazado igual y sin procesar.

## Reviews

**Quality review — PASS WITH RECOMMENDATIONS.** Se leyeron `limite.py`, `rutas/coleccion.py`, la plantilla, `fabricas.py` y las cuatro pruebas nuevas. Corregidos en el acto: el `type: ignore[arg-type]` de la prueba del middleware (ahora funciones honestas), y el tope de lectura `read(TAMANO_MAXIMO + 1)`, redundante con el límite del cuerpo, que una mutación no distinguía; se quitó junto con su comentario. Recomendación: `LimiteDeCuerpo` traga cualquier `Exception` de la aplicación cuando ya se excedió el límite (para no dejar un 500 donde corresponde 413); si un error real ocurriera después de pasarse, quedaría oculto tras el 413; se acepta porque la respuesta correcta a un cuerpo excedido es 413 en todos los casos. Observación: `rutas/coleccion.py` llega a 237 líneas con la ficha, la subida y las imágenes; s3.5 añade poco (miniatura y quitar foto) y no justifica otra división todavía.

**Security review — PASS.** Bandit 1.9.4 sobre los 7 `.py` cambiados (el alcance devuelto coincide con la lista esperada): 0 hallazgos en `src`; 85 × B101 (baja) en `tests/`, el ruido ya registrado en el parking lot. ASVS L2 recorrido al diseñar y verificado: V12.1.1 (tamaño en dos capas: 413 y `procesar_foto`), V12.2.1 (tipo por decodificación; un GIF que dice ser JPEG se rechaza), V12.3 (el nombre subido no se usa; la ruta sale del nombre guardado; nombres `..`, `a/b` y vacío en la base dan 404 sin leer fuera), V12.4 (el directorio no es estático), V12.5 (`image/jpeg` fijo, `nosniff`, sin `Content-Disposition`), V4.2 (la sesión se exige antes de leer nada; probado sin sesión en las tres rutas), CSRF (403 sin token en la ruta real), V7 (el fallo de escritura se registra sin datos del usuario ni se filtra al cliente: "disco lleno" no aparece en la respuesta). `must-security-001` y `must-perf-002` sostenidos de extremo a extremo. Limitación: análisis estático; la prueba manual cubrió la concurrencia y el cuerpo chunked bajo `uvicorn` real.

## What went well

- Poner el límite de cuerpo primero (T1) y probarlo también contra `uvicorn` real destapó lo que la prueba unitaria no veía: FastAPI convierte cualquier excepción al leer el cuerpo en 400/422, y por eso el middleware corta por señal (desconexión y sustitución de la respuesta) y no por excepción.
- Las mutaciones cerraron tres huecos reales de la ruta de subida antes de commitear.

## What to improve

- Mi primera versión del límite lanzaba una excepción desde `receive`; las pruebas ASGI directas la aprobaron y la prueba web con `TestClient` la reprobó (422 en vez de 413). La prueba web chunked, además, no enviaba `Content-Type`, así que la aplicación ni leía el cuerpo: una prueba que pasa o falla por una razón ajena a lo que dice probar. Cada prueba de límites debe comprobar que el cuerpo se leyó.
- El script de la prueba manual se colgó por un `wait` sin argumentos (esperaba también a `uvicorn`), un `pkill -f` mató mi propio shell y tardó tres intentos; scripts de servidor: `wait` con PIDs, sin `pkill -f` de un patrón que esté en la propia orden.

## Learned

1. About the system: FastAPI envuelve en 400/422 cualquier excepción al leer el cuerpo; un límite de tamaño debe actuar como middleware ASGI y cortar por señal (memoria `fastapi-cuerpo-excedido-por-senal`). El analizador urlencoded de Starlette rechaza campos de más de 1 MiB con 400 antes que cualquier límite propio.
2. About the process: una prueba negativa debe demostrar que el camino que niega se ejercitó (el cuerpo se leyó, la ruta existe); si no, pasa por la razón equivocada.
3. Capability gained: `tests/fabricas.py::imagen_jpeg` (JPEG con GPS, XMP y comentario) y la prueba manual de subidas en paralelo con `curl`.
