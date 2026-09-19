# Epic e3: Specimen photos — Retrospective

## Summary

El coleccionista sube una foto de cada ejemplar desde su ficha (`/coleccion/{id}`), la ve a tamaño completo allí y en miniatura en "Mi colección", la reemplaza o la quita. Toda foto se reconstruye desde sus píxeles con Pillow (ancho ≤ 1600 px, miniatura de 192 px, JPEG sin EXIF, GPS, XMP, comentario ni ICC, orientación ya aplicada), se guarda en el disco junto a la base con un nombre aleatorio y solo se entrega con la sesión iniciada. `orquidea/web/app.py` se dividió en routers por área. Seis historias, tres ADR (005 Pillow, 006 fotos en disco, 007 miniatura de 192 px que sustituye a 005) y una guía de despliegue con respaldo, límites y un script que mide la primera carga.

## Metrics

- Stories: 6 (s3.1 a s3.6) · Estimated: S, M, M, M, S, S · Actual: S, M, M, M, S, S (ninguna cambió de talla).
- 350 pruebas (unas 250 heredadas de e2), `./scripts/check` en verde; una dependencia nueva (`pillow`); 2 entradas nuevas en el parking lot y 2 retiradas (`app.py` y las cifras de la guía).
- Surgió a mitad de la épica y no estaba planeado: dos commits con el gate en rojo (s3.2 y s3.3) enmendados antes de seguir; el cambio de miniatura de 320 a 192 px (ADR-007) a partir de la medición de s3.6; y en este review un pico de memoria de ~1 GB con fotos de 48 MP, corregido con prueba en `fix(fotos)`.
- Sin despachos: ninguna historia llevó `dispatch.md` ("none dispatched").

## Scope verification

- **MUST — una foto por ejemplar, subida, reemplazada y quitada (RF-05)** → **Fulfilled**: `web/rutas/coleccion.py` (`subir_foto`, `quitar_la_foto`), `datos/almacen_fotos.py` (`poner_foto`, `quitar_foto`); `tests/test_web_fotos.py`, `tests/test_datos_almacen_fotos.py`.
- **MUST — sin EXIF y ancho ≤ 1600 px (`must-security-001`, `must-perf-002`)** → **Fulfilled**: `datos/fotos.py`; prueba por bytes en `test_datos_fotos.py` y por HTTP en `test_web_fotos.py`.
- **MUST — miniatura en las listas** → **Fulfilled**: `templates/coleccion.html`; el diseño decía "≤ 320 px" y quedó en 192 px por ADR-007 (cumple el "≤ 320"; el `design.md` no se reescribe).
- **MUST — orientación conservada** → **Fulfilled** (`test_la_orientacion_exif_se_aplica_a_los_pixeles`).
- **MUST — fotos solo con sesión; quitar un ejemplar borra sus archivos** → **Fulfilled** (`test_web_proteccion.py`, `test_quitar_un_ejemplar_con_foto_borra_sus_archivos`).
- **MUST — las fotos sobreviven a un redespliegue dentro del volumen** → **Fulfilled con reserva**: `test_despliegue.py` fija que caen dentro de `/data` y se comprobó reiniciando `uvicorn` sobre la misma carpeta; la imagen de Docker sigue sin construirse (parking lot).
- **MUST — `app.py` dividido en routers antes de añadir rutas** → **Fulfilled**: s3.1 (`web/rutas/`, `web/sesion.py`); `app.py` en 74 líneas.
- **SHOULD — rechazo claro de archivos inválidos; script de medición** → **Fulfilled** (422/413 con mensajes en español; `scripts/medir-primera-carga.py`).
- **[stated] subir una foto con GPS y comprobar que no tiene metadatos y mide ≤ 1600 px** → **Fulfilled**: `test_subir_una_foto_con_gps_la_guarda_reducida_y_sin_metadatos` y la prueba manual con `uvicorn`.
- **[stated] lista con miniaturas ≤ 200 KB en la primera carga (`must-perf-001`)** → **Fulfilled por script, con reserva aceptada por el humano**: 146,5 KB con 25 ejemplares con fotos de ejemplo; la medición con "Slow 3G", el navegador y fotos reales queda pendiente del humano (`decisions.md`, `Answered` de `epic-review`: "a — se da por cumplido con esa medición y se cierra la épica dejando el "Slow 3G" pendiente").
- **[deduced] sin metadatos en imagen ni miniatura; una foto por ejemplar y borrado de archivos; sin sesión nada se entrega y CSRF; los rechazos no dejan rastro; la suite de e1 y e2 sigue igual tras la división** → **Fulfilled** (`test_datos_fotos.py`, `test_datos_almacen_fotos.py`, `test_web_fotos.py`, `test_web_rutas.py`; las pruebas existentes solo cambiaron el destino de un `monkeypatch`, un import y el helper que enumera rutas, no sus aserciones).
- **[stated] all stories complete · docs updated · retrospective done** → historias y retrospectiva hechas; `docs.md` lo escribe `epic-close`.

No hay compromisos de eliminación en el alcance.

## Reviews a escala de épica

**Quality review — PASS WITH RECOMMENDATIONS.** Rango `889fba9..HEAD`, 27 `.py`. Lo que solo se ve entre historias: `procesar_foto` (s3.2) copiaba los píxeles cuatro veces y ninguna prueba de la historia medía memoria; una foto de 48 MP subía el proceso ~780 MB (~1 GB de pico), y una de 64 MP más. Corregido en `fix(fotos)` (reducir antes de copiar, sin copia si no hay orientación, conversión de modo tras reducir) con prueba en un proceso aparte (picos ~280, 273 y 430 MB a 48 MP; ~360 y 570 MB a 64 MP). Recomendaciones estacionadas: subidas simultáneas de tamaño máximo y caché de las miniaturas. Sin tipos deshonestos ni pruebas sin valor nuevas.
**Security review — PASS.** Bandit 1.9.4 sobre el mismo rango: 0 hallazgos fuera de `tests/`; 489 × B101 en `tests/` (ruido ya registrado). Composición de guardarraíles: sesión y CSRF globales protegen las cuatro rutas de fotos; el límite de cuerpo actúa antes del multipart; las rutas de archivo salen solo de un nombre validado; un nombre o notas con HTML salen escapados en `alt` y en la lista (comprobado con un ejemplar de nombre `"><script>…`). Limitación: análisis estático; la concurrencia y el cuerpo chunked se probaron bajo `uvicorn` real.

## What went well

- Hacer del riesgo mayor (metadatos y entrada no confiable) la primera historia y una función pura dejó a las siguientes apoyándose en contratos ya probados; las mutaciones sistemáticas cerraron huecos reales en cada historia.
- Probar con el proceso real (`uvicorn`, `curl` con hilos y chunked) encontró lo que `TestClient` no veía: FastAPI convierte en 400/422 cualquier excepción al leer el cuerpo, el analizador urlencoded corta a 1 MiB, y la memoria.
- Convertir mediciones y cifras en pruebas del gate (mapa de rutas, presupuesto de peso, deriva guía-constantes, pico de memoria) vuelve propiedades vigiladas lo que antes era una verificación manual de cada review.
- Sustituir una decisión con datos (ADR-007) dejó escrita la razón en vez de cambiar una constante en silencio.

## What to improve

- Dos commits salieron con el gate en rojo por encadenar mal el código de salida; a partir de s3.4 todo commit fue `./scripts/check && git commit`. Debe ser el hábito desde el primer commit de la épica.
- Ninguna historia midió recursos: el pico de memoria solo apareció en el review, y la medición del peso de la lista al final (s3.6). Para historias que procesan entrada del usuario, medir memoria y tiempo desde su diseño, con el tamaño máximo permitido.
- Una prueba de aleatoriedad frágil (s3.3) y una de límites que no leía el cuerpo (s3.4) pasaban o fallaban por una razón ajena a lo que decían probar; toda prueba negativa debe demostrar que ejercitó el camino.
- El criterio rezagado se previó como stop desde el diseño (lección de e1 y e2) y aun así costó una espera; la medición real (fotos propias, "Slow 3G") sigue sin hacerse.

## Learned

1. About the system: Pillow copia el comentario JPEG de `Image.info` al guardar y solo una imagen reconstruida desde los bytes de sus píxeles queda limpia; una foto de teléfono cuesta ~150 MB por copia de píxeles; en FastAPI 0.141 `include_router` anida las rutas (`_IncludedRouter`) y toda excepción al leer el cuerpo se vuelve 400/422, así que un límite de tamaño corta por señal en un middleware ASGI.
2. About the process: las decisiones de una épica que dependen de una medición se toman cuando existe el dato (ADR-007 tras medir), y los ADR se sustituyen, no se editan; los defectos entre historias vuelven a aparecer solo al leer el rango completo con el proceso real.
3. Capability gained: fotos de ejemplares por HTTP con garantías probadas (sin metadatos, límites de tamaño, coherencia base-disco bajo concurrencia), routers por área donde añadir las rutas de e4, y `scripts/medir-primera-carga.py` con fotos reales.
