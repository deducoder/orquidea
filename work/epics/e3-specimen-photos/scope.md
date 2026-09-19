# Epic e3: Specimen photos — Scope

## Objective

El coleccionista sube una foto de cada uno de sus ejemplares y la ve en la ficha del ejemplar y, en miniatura, en "Mi colección", sin que la imagen guardada revele nunca dónde se tomó.

**Value:** cada planta de la colección se reconoce a simple vista y la foto vive junto a su ejemplar; se cumple RF-05 y se cierran `must-perf-002` y `must-security-001`, que la versión 0.2 debe demostrar con pruebas.

## Stories

| ID | Story | Size | Description |
|----|-------|:----:|-------------|
| s3.1 | Dividir `web/app.py` en routers | S | Separar acceso, catálogo y colección en `APIRouter`, y sacar `exigir_sesion` y las cabeceras a su propio módulo, sin cambiar comportamiento (parking lot, unido a 0.2.0). |
| s3.2 | Procesamiento de imágenes | M | Función pura que recibe los bytes subidos y devuelve una imagen de ancho ≤ 1600 px y una miniatura, ambas JPEG sin metadatos, con límites de entrada (ADR-005; `must-perf-002`, `must-security-001`). |
| s3.3 | Almacenamiento de fotos | M | Migración `0003`, directorio `ORQUIDEA_FOTOS`, guardar, reemplazar y borrar los archivos de un ejemplar, y borrarlos al quitar el ejemplar (ADR-006). |
| s3.4 | Ficha del ejemplar con foto | M | Página `/coleccion/{id}` con la foto a tamaño completo, formulario de subida y ruta protegida que sirve la imagen y la miniatura (RF-05). |
| s3.5 | Miniaturas en "Mi colección" y quitar foto | S | La lista muestra la miniatura de cada ejemplar con enlace a su ficha, y la ficha permite quitar la foto (RF-05, `must-perf-002`). |
| s3.6 | Despliegue con fotos y medición | S | Guía y `Dockerfile` con el directorio de fotos dentro del volumen, límite de tamaño del cuerpo, y script que mide el peso de la primera carga de "Mi colección" con miniaturas (`must-perf-001`). |

Dependencias: s3.2 sin dependencias; s3.3 de s3.2; s3.4 de s3.1 y s3.3; s3.5 de s3.4; s3.6 de s3.4. Sin ciclos. El brief pide dividir `app.py` antes de añadir rutas: s3.1 va antes de s3.4, la primera que las añade.

## In scope

- **MUST:** una foto por ejemplar, subida, reemplazada y quitada por el usuario (RF-05); toda foto guardada sin metadatos EXIF y con ancho ≤ 1600 px (`must-security-001`, `must-perf-002`); miniatura en las listas; la orientación de la foto se conserva aunque se descarte el EXIF; las fotos solo se entregan con sesión; quitar un ejemplar borra sus archivos; las fotos sobreviven a un redespliegue dentro del volumen; `app.py` dividido en routers antes de añadir rutas.
- **SHOULD:** rechazo claro (mensaje en español) de archivos que no son imagen, demasiado grandes o de formato no admitido; script de medición de la primera carga.

## Out of scope

- Varias fotos por ejemplar o galerías — no-go del brief (RF-05) — **never** en esta versión.
- Edición de imagen (recortar, rotar) en la app — no-go del brief — **never** en esta versión.
- Almacenamiento en servicios externos — no-go del brief (system-context) — **never**.
- Varios tamaños y formatos modernos (WebP, AVIF) — rabbit hole del brief — **not now**.
- Reconocer la orquídea en la foto — rabbit hole del brief — **not now**.
- Descargar la foto original — RF-05 no lo pide y ADR-005 descarta el original — **not now**.
- Foto en la ficha de la especie del catálogo — RF-05 habla de ejemplares; las especies del catálogo no llevan foto — **not now**.
- Caché del navegador para las fotos (hoy `Cache-Control: no-store` en todo salvo `/static`) — no lo pide ningún criterio; se mide en s3.6 y, si pesa, va al parking lot — **not now**.

## Done when

- [stated] Subir una foto con GPS en el EXIF y comprobar que la imagen guardada no tiene metadatos y mide ≤ 1600 px de ancho (métrica líder del brief), demostrado por una prueba automatizada de extremo a extremo y por el recorrido manual de `story-implement`.
- [stated] La lista de "Mi colección" con miniaturas transfiere ≤ 200 KB en la primera carga, sin contar las fotos a tamaño completo (métrica rezagada del brief, `must-perf-001`). El peso en bytes se mide por script en s3.6; la medición con "Slow 3G" en el navegador solo la puede hacer el humano con la aplicación desplegada: **stop previsible** (P4 en `epic-review`).
- [deduced] Ninguna imagen llega al disco con metadatos EXIF (incluido GPS, XMP o comentarios) ni con ancho mayor a 1600 px, y la miniatura tampoco lleva metadatos (`must-security-001`, `must-perf-002`).
- [deduced] Un ejemplar tiene a lo sumo una foto; subir otra reemplaza la anterior y borra sus archivos; quitar la foto o el ejemplar borra los archivos (RF-05, ADR-006).
- [deduced] Sin sesión, ninguna ruta de fotos entrega la imagen; toda subida exige el token CSRF; ninguna ruta de archivo se forma con datos de la petición (`should-security-002`, ADR-006).
- [deduced] Un archivo que no es JPEG, PNG o WebP, que excede el tamaño o los píxeles permitidos, o que no se puede decodificar se rechaza con un mensaje claro y no deja archivos ni cambios en la base (ADR-005).
- [deduced] Tras la división en routers, todas las rutas existentes se comportan igual y la suite de e1 y e2 sigue en verde sin cambiar sus aserciones.
- [stated] All stories complete · docs updated · retrospective done

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| Una subida maliciosa o defectuosa (bomba de descompresión, archivo enorme, formato disfrazado) agota memoria o CPU del único proceso | M | H | Límites de bytes y de píxeles en s3.2 y s3.4, tipo decidido por lo que Pillow decodifica; `security-review` en s3.2 a s3.5 contra ASVS L2 (subida de archivos) recorrido desde el diseño de cada historia |
| Se pierde el giro de la foto al descartar el EXIF, o un contenedor de metadatos sobrevive (XMP, comentarios) | M | H | ADR-005: aplicar la orientación y reconstruir el JPEG desde píxeles; pruebas con GPS, XMP y orientación en s3.2 |
| El proxy del despliegue (Dokploy) o uvicorn cortan las subidas antes que el límite propio, o el directorio de fotos no es escribible por el usuario `app` | M | M | s3.6 documenta el límite y el propietario del volumen; la aplicación falla con error explícito al arrancar si no puede escribir; configurar el VPS es del humano, previsto como stop P5 si hay que actuar allá |
| La medición de `must-perf-001` con "Slow 3G" y el criterio rezagado dependen del humano y de un navegador con herramientas de desarrollo (e1 y e2 los descubrieron tarde) | H | M | Previstos desde aquí como stop P4 en `epic-review`; el peso en bytes se mide por script en s3.6 |
| Dividir `app.py` rompe rutas o el orden de `/coleccion/nuevo` frente a `/coleccion/{id}` | M | M | s3.1 se apoya en la suite existente sin editar aserciones; `/coleccion/nuevo` se registra antes que `/coleccion/{id}` con prueba explícita |
