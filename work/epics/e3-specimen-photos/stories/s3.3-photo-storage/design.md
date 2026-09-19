# Story s3.3: Photo storage — Design

> Complexity: moderate

## 1 · What & why

**Problem:** `procesar_foto` (s3.2) devuelve bytes, pero nada los guarda ni los liga a un ejemplar, y quitar un ejemplar dejaría sus archivos sueltos.
**Value:** una foto sobrevive al reinicio dentro del volumen y desaparece con su ejemplar; las rutas de s3.4 solo tendrán que llamar a dos funciones.

## 2 · Approach

Columna `ejemplares.foto` con un nombre aleatorio (ADR-006) y un módulo de archivos que guarda los dos JPEG, los borra y forma rutas solo desde un nombre validado. Las operaciones que tocan base y disco a la vez (`poner_foto`, `quitar_foto`, `quitar_con_foto`) viven en ese módulo, en el orden escribir → actualizar → borrar, bajo un cerrojo de proceso (ADR-001: un solo proceso).

**Components affected:**

- `orquidea/datos/migraciones/0003-foto-del-ejemplar.sql`: create — `ALTER TABLE ejemplares ADD COLUMN foto TEXT`.
- `orquidea/coleccion/modelo.py`: modify — `Ejemplar.foto: str | None = None`.
- `orquidea/datos/ejemplares.py`: modify — `foto` en `obtener` y `listar`, `fijar_foto`.
- `orquidea/datos/almacen_fotos.py`: create — `directorio_de_fotos`, `preparar_directorio`, `ruta_de_foto`, `poner_foto`, `quitar_foto`, `quitar_con_foto`, `NombreDeFotoInvalido`.
- `orquidea/web/app.py`, `orquidea/web/rutas/coleccion.py`: modify — `app.state.directorio_fotos`, preparación en el ciclo de vida, y `quitar_ejemplar` usa `quitar_con_foto`.
- `tests/conftest.py`: modify — el cliente apunta `directorio_fotos` a un directorio temporal.

**Legacy sweep:** `datos.ejemplares.quitar` sigue existiendo (lo usa `quitar_con_foto` y sus pruebas); la ruta web deja de llamarlo directamente. Ningún otro código queda huérfano. Orphaned tests: `test_datos_ejemplares.py`, `test_web_coleccion.py` y `test_recorrido_coleccion.py` usan `Ejemplar` y las consultas; la columna nueva tiene valor por defecto `None`, así que las igualdades siguen valiendo; se corren todas.

## 3 · Interface / examples

```python
from orquidea.datos.almacen_fotos import poner_foto, quitar_con_foto, ruta_de_foto

directorio = directorio_de_fotos(ruta_de_la_base())  # data/fotos  (o $ORQUIDEA_FOTOS)
poner_foto(conexion, directorio, 1, procesar_foto(datos))  # True; ejemplar 1 -> foto "Xq3vT…"
ruta_de_foto(directorio, "Xq3vT…", miniatura=True)  # data/fotos/Xq3vT…-mini.jpg
ruta_de_foto(directorio, "../x", miniatura=False)  # NombreDeFotoInvalido
poner_foto(conexion, directorio, 999, foto)  # False; no queda ningún archivo
quitar_con_foto(conexion, directorio, 1)  # True; fila y archivos borrados
```

```python
NOMBRE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
```

Semántica: `poner_foto` devuelve `False` (y no deja archivos) si el ejemplar no existe; `quitar_foto` devuelve `False` si el ejemplar no existe; un ejemplar sin foto no es error. Un archivo que no se puede borrar se registra (`orquidea.fotos`) y no impide la operación.

## 4 · Acceptance criteria

**Must:**

- Los dos archivos existen tras `poner_foto`, con nombre aleatorio (`secrets.token_urlsafe(16)`), y la fila apunta a ese nombre.
- Reemplazar borra los archivos anteriores; quitar la foto o el ejemplar borra los vigentes.
- Un ejemplar inexistente no deja archivos; un nombre con `..`, `/` o vacío no forma ruta.
- Escritura atómica: cada archivo se escribe a un temporal y se renombra; si falla la segunda escritura, la primera se borra.
- Dos subidas simultáneas para el mismo ejemplar dejan una foto vigente y solo sus dos archivos (cerrojo).
- La migración `0003` conserva los ejemplares existentes.

**Should:** `preparar_directorio` crea el directorio y falla al arrancar con un error que nombra la ruta si no es escribible.

**Must NOT:** servir el directorio como estático; usar el id del ejemplar o el nombre del archivo subido en una ruta; editar la migración `0002`.

### ASVS L2 recorrido al diseñar

- V12.3 (ruta de archivo con datos del usuario): cubierto — nombre aleatorio validado por expresión regular.
- V12.4 (archivos subidos fuera de la raíz servida y sin ejecución): cubierto — el directorio no se monta en `/static`; se sirve por ruta protegida (s3.4).
- V12.1 (tamaño, cuota): tamaño por archivo en s3.2; cuota total no aplicable a un solo usuario.
- V4.2 (control de acceso a objetos): las rutas de s3.4 dependen de la sesión global; aquí no hay ruta.
- V8 (datos de disco sin cifrar): fuera de alcance, sin datos sensibles.
- Concurrencia (memoria del proyecto): cerrojo de proceso y prueba con hilos.

### Deduced criteria

- Reemplazar borra lo anterior: confirmed
- Quitar el ejemplar borra fila y archivos: confirmed
- Quitar solo la foto deja el ejemplar sin foto: confirmed
- Ejemplar inexistente no deja archivos: confirmed
- Nombre con `..` o `/` se rechaza: confirmed
- Dos subidas simultáneas dejan una sola foto: confirmed — con el cerrojo; sin él, la carrera deja un archivo huérfano (la prueba lo detecta)
- La migración 0003 conserva los ejemplares: confirmed

### Scenarios (delta over the scope)

```gherkin
Given un directorio de fotos que no se puede escribir
When arranca la aplicación
Then falla con un error que nombra la ruta

Given que la escritura de la miniatura falla después de escribir la imagen
When se guarda la foto
Then no queda ningún archivo y la fila no cambia
```
