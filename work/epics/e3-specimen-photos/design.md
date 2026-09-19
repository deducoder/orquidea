# Epic e3: Specimen photos — Design

## Gemba findings

- `src/orquidea/web/app.py` (376 líneas): una sola aplicación con acceso, catálogo, colección, `exigir_sesion` (dependencia global con CSRF), cabeceras de seguridad y ciclo de vida; todas las rutas se registran con `@app.get/post`. **Extender tras dividir**: s3.1 separa en `APIRouter` por área y saca sesión y cabeceras a su módulo; la dependencia global `exigir_sesion` se queda en `FastAPI(dependencies=...)`, así los routers nuevos nacen protegidos.
- `exigir_sesion` ya lee `csrf` con `Form()` y `x_csrf_token` de cabecera: una subida `multipart/form-data` con un campo `csrf` funciona sin tocarla. `python-multipart` ya es dependencia (e2).
- `src/orquidea/coleccion/modelo.py`: `Ejemplar` (id, especie_id, nombre, notas, creado) y `resolver`; el dominio no conoce HTTP ni SQL. **Extender** con `foto: str | None`.
- `src/orquidea/datos/ejemplares.py`: SQL parametrizado, cuatro columnas repetidas en `obtener` y `listar`; añadir `foto` ahí y `fijar_foto`. Migraciones `0001` y `0002` existentes; la nueva es `0003` (ADR-003: nunca se edita una aplicada).
- `src/orquidea/datos/base.py`: `ruta_de_la_base()` por `ORQUIDEA_DB`; el directorio de fotos sigue el mismo patrón (`ORQUIDEA_FOTOS`, por defecto junto a la base). En la imagen, `/data` ya es un volumen (`Dockerfile`, e2), así que las fotos lo heredan.
- No existe ficha de ejemplar: `coleccion.html` solo enlaza a la especie, a editar y a quitar. RF-05 pide ver la foto "en su ficha", así que s3.4 crea `/coleccion/{id}`. **Cuidado con el orden de rutas**: `/coleccion/nuevo` debe registrarse antes que `/coleccion/{id}`.
- No hay Pillow ni ninguna biblioteca de imágenes; la biblioteca estándar no decodifica imágenes. **Decisión de diseño:** Pillow como única dependencia nueva (ADR-005).
- El middleware de cabeceras pone `Cache-Control: no-store` a todo salvo `/static`, y la CSP es `default-src 'self'`: las imágenes servidas por rutas propias caben en `'self'`; no se necesita `img-src` nuevo. Las miniaturas no se cachean; se acepta y se mide (fuera de alcance, ver scope).
- Las rutas síncronas corren en un pool de hilos (memoria del proyecto: probar hilos y proceso real en historias de seguridad): el procesamiento de imagen y el reemplazo de archivos deben ser seguros con subidas simultáneas; s3.3 y s3.4 lo cubren con una prueba bajo uvicorn real.
- Pruebas: `tests/conftest.py` ya trae `client` autenticado con base temporal; `tests/test_web_coleccion.py` y `test_recorrido_coleccion.py` cubren el comportamiento de rutas que s3.1 no debe cambiar. Un test que importe módulos movidos y no se actualice es huérfano.
- Parking lot: la entrada de `app.py` (~390 líneas, unida a 0.2.0) promueve en s3.1, que la retira al cerrar. Las demás entradas abiertas no tocan esta épica.

## Target components

| Component | Change | Purpose |
|-----------|--------|---------|
| `orquidea.web.app` | modify | Solo construye la aplicación: middleware, manejador de errores, ciclo de vida y monta los routers (`s3.1`) |
| `orquidea.web.sesion` (`exigir_sesion`, `SesionRequerida`, cookie, `Base`) | create | Dependencia de sesión y CSRF, sacada de `app.py` (`s3.1`) |
| `orquidea.web.rutas.acceso`, `catalogo`, `coleccion` | create | Un `APIRouter` por área, con las rutas de hoy (`s3.1`); `coleccion` gana la ficha, la subida y el servicio de fotos (`s3.4`, `s3.5`) |
| `orquidea.datos.fotos` (procesamiento puro sobre bytes) | create | Bytes subidos → imagen ≤ 1600 px y miniatura, JPEG sin metadatos, con límites (`s3.2`) |
| `orquidea.datos.almacen_fotos` (archivos en disco) | create | Directorio `ORQUIDEA_FOTOS`, guardar, reemplazar y borrar los dos archivos de una foto (`s3.3`) |
| `orquidea/datos/migraciones/0003-foto-del-ejemplar.sql` | create | Columna `ejemplares.foto` (`s3.3`) |
| `orquidea.datos.ejemplares` | modify | `foto` en `obtener`/`listar`, `fijar_foto` (`s3.3`) |
| `orquidea.coleccion.modelo` | modify | `Ejemplar.foto`; reglas de límites de subida como constantes del dominio (`s3.3`, `s3.4`) |
| `orquidea/web/templates/` (`ejemplar_ficha`, `coleccion`, `_csrf`) | create/modify | Ficha con foto y formulario de subida (`s3.4`); miniatura y enlace a la ficha en la lista, y quitar foto (`s3.5`) |
| `tests/` (`test_datos_fotos`, `test_datos_almacen_fotos`, `test_web_fotos`, actualizaciones de `test_web_coleccion`, `test_recorrido_coleccion`) | create/modify | Pruebas de cada capa y el recorrido de extremo a extremo (`s3.1`, `s3.2`, `s3.3`, `s3.4`, `s3.5`) |
| `scripts/` (medición de la primera carga), `Dockerfile`, `README.md` | create/modify | `ORQUIDEA_FOTOS`, respaldo conjunto, límite del cuerpo, medición de peso (`s3.6`) |
| `pyproject.toml` | modify | `pillow` (`s3.2`) |

## Key contracts

- Una foto por ejemplar; `ejemplares.foto` es nulo o el nombre base aleatorio de la foto vigente (ADR-006).
- Ningún archivo en disco lleva metadatos: la salida es un JPEG reconstruido desde píxeles, con la orientación ya aplicada (ADR-005).
- Ancho de la imagen ≤ 1600 px (sin ampliar las menores); miniatura con lado mayor ≤ 320 px; ambas JPEG.
- Entradas admitidas: JPEG, PNG y WebP decodificados por Pillow; el tipo no se toma del nombre ni del `Content-Type`. Se rechaza lo demás, lo que excede el tamaño del archivo o el tope de píxeles, y lo que no decodifica; el rechazo no escribe nada.
- La ruta de un archivo se forma solo con el nombre guardado, validado contra `^[A-Za-z0-9_-]+$`; nunca con el id ni con datos de la petición.
- Toda ruta de fotos exige sesión; toda subida y todo borrado exigen el token CSRF; las imágenes se sirven con las cabeceras de seguridad del resto.
- Orden de las operaciones de archivo: escribir lo nuevo, actualizar la fila, borrar lo anterior; el peor caso es un archivo huérfano, nunca una fila que apunta a nada.
- Quitar un ejemplar borra sus archivos; un ejemplar sin foto o con el archivo ausente se muestra sin romperse.
- `/coleccion/nuevo` se registra antes que `/coleccion/{id}`.
- Los mensajes de la interfaz van en español.

## Decisions (ADRs)

- ADR-005: Procesamiento de fotos con Pillow: se reconstruye la imagen desde sus píxeles — única dependencia nueva; descarta borrar campos del original y herramientas externas; `records/decisions/adr-005-procesamiento-de-fotos-con-pillow.md`.
- ADR-006: Las fotos viven en archivos del disco junto a la base, con un nombre aleatorio guardado en el ejemplar — heredan el volumen `/data`; descarta el BLOB en SQLite y la ruta por id; `records/decisions/adr-006-fotos-en-disco-junto-a-la-base.md`.

## Legacy sweep

Nada se elimina. `orquidea/web/app.py` deja de contener rutas, sesión y cabeceras (s3.1): los tests que importen `exigir_sesion`, `SesionRequerida`, `RUTAS_PUBLICAS` u otros nombres desde `orquidea.web.app` se revisan en s3.1 y no se dejan sin resolver. La entrada del parking lot sobre `app.py` se retira al cerrar s3.1 (`park`). El README dice hoy que la colección vive en un archivo SQLite: s3.6 lo amplía a base más directorio de fotos.
