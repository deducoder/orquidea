# Epic e4: Care log — Design

## Gemba findings

- `src/orquidea/datos/ejemplares.py`: SQL parametrizado por función, sin ORM (ADR-003); `quitar` hace `DELETE FROM ejemplares`. **Seguir el patrón**: un módulo por tabla (`riegos.py`, `floraciones.py`), funciones que reciben la conexión.
- `src/orquidea/datos/base.py`: migraciones `NNNN-nombre.sql` continuas (hoy `0001` a `0003`); `conectar` ya activa `PRAGMA foreign_keys = ON`, así que una clave foránea con `ON DELETE CASCADE` borra el historial al quitar el ejemplar sin código propio. **Reutilizar**; las nuevas son `0004` y `0005`, nunca se edita una aplicada.
- `orquidea.datos.almacen_fotos.quitar_con_foto` llama a `quitar` bajo un cerrojo y borra los archivos; los cuidados no tienen archivos, así que no necesitan pasar por ahí: la cascada de SQLite basta.
- `src/orquidea/coleccion/modelo.py`: `Ejemplar` y las reglas de validación (`validar_ejemplar`, `EjemplarInvalido`, constantes de límites); el dominio no conoce HTTP ni SQL. **Extender** con `Riego`, `Floracion` y sus validaciones en el mismo espíritu (una excepción del dominio con mensaje en español).
- `src/orquidea/web/rutas/coleccion.py` (~200 líneas): ya contiene la ficha `/coleccion/{id}` (`_ficha`, `ejemplar_ficha.html`), las rutas de foto y la baja. **No crecer ahí**: las rutas de cuidados van a un `APIRouter` nuevo (`cuidados.py`); solo `_ficha` cambia para cargar los historiales.
- `src/orquidea/web/app.py` monta los routers y `exigir_sesion` es dependencia global (con CSRF por `Form()` o cabecera): un router nuevo nace protegido. Memoria del proyecto: enumerar rutas con `rutas_registradas`, no con `app.routes`, porque `include_router` anida.
- `src/orquidea/web/plantillas.py`: el filtro `fecha` recibe segundos Unix (`creado`). Las fechas de cuidados son texto ISO; se muestran tal cual (`AAAA-MM-DD`, igual que "Agregado el") sin un filtro nuevo.
- `ejemplar_ficha.html` ya tiene la sección Foto; se añaden las secciones Riegos y Floraciones. Formularios con `_csrf.html`, redirección 303 a la ficha después de cada POST (mismo patrón que las fotos): sin htmx.
- `scripts/medir-primera-carga.py` mide "Mi colección" con miniaturas y sale con 1 si pasa del presupuesto; **extender** con la medición de la ficha en lugar de un segundo script (s4.6).
- No existe nada de cuidados: ningún riego, floración ni "último riego" en el código; no hay duplicado que evitar. PRD RF-06 y RF-07 y `governance/architecture/system-design.md` (dominio "seguimiento") lo esperan.
- Parking lot: la entrada de fertilización y notas queda aparcada por el brief; las demás no tocan la épica (la de miniaturas sin caché roza la ficha, pero e4 no añade imágenes).

## Target components

| Component | Change | Purpose |
|-----------|--------|---------|
| `orquidea/datos/migraciones/0004-riegos.sql` | create | Tabla `riegos` con `ejemplar_id` en cascada e índice por `(ejemplar_id, fecha)` (`s4.1`) |
| `orquidea/datos/migraciones/0005-floraciones.sql` | create | Tabla `floraciones` con cascada, `CHECK (fin IS NULL OR fin >= inicio)` e índice (`s4.3`) |
| `orquidea.coleccion.modelo` | modify | `Riego`, `Floracion`, validación de fechas y tope de registros (`s4.1`, `s4.3`) |
| `orquidea.datos.riegos` | create | Agregar, listar, último, último por ejemplar (lista) y quitar riegos (`s4.1`, `s4.5`) |
| `orquidea.datos.floraciones` | create | Agregar, terminar, listar y quitar floraciones (`s4.3`) |
| `orquidea.web.rutas.cuidados` | create | Rutas POST de riegos y floraciones bajo `/coleccion/{id}/…` (`s4.2`, `s4.4`) |
| `orquidea.web.rutas.coleccion` | modify | `_ficha` carga los historiales; la lista carga el último riego (`s4.2`, `s4.4`, `s4.5`) |
| `orquidea.web.app` | modify | Monta el router `cuidados` (`s4.2`) |
| `orquidea/web/templates/ejemplar_ficha.html`, `coleccion.html` | modify | Secciones de riegos y floraciones; último riego en la lista (`s4.2`, `s4.4`, `s4.5`) |
| `tests/` (`test_datos_riegos`, `test_datos_floraciones`, `test_web_cuidados`, `test_recorrido_coleccion`, `test_medicion`) | create/modify | Pruebas de cada capa y el recorrido de extremo a extremo (`s4.1`, `s4.2`, `s4.3`, `s4.4`, `s4.5`, `s4.6`) |
| `scripts/medir-primera-carga.py`, `README.md` | modify | Medir la ficha con el historial lleno; documentar el historial (`s4.6`) |

## Key contracts

- Una fecha de cuidado es texto `AAAA-MM-DD` válido y no posterior al día actual del servidor (UTC); se valida en el dominio con `datetime.date.fromisoformat` y con nada más (ADR-008).
- Una floración con `fin` nulo está en curso; con `fin`, `fin >= inicio` (dominio y `CHECK`). `terminar` solo pone el fin de una floración en curso.
- Orden del historial: cronológico; riegos por fecha y floraciones por inicio, y a igual fecha, por `id`. La ficha los muestra del más reciente al más antiguo, y "último riego" es el mayor `fecha`.
- Tope de 500 registros por ejemplar y tipo; el 501.º se rechaza con un mensaje claro. El tope acota el HTML de la ficha y se mide en s4.6 con el tope lleno.
- Toda escritura filtra por `ejemplar_id` **y** `id` del registro: un id de otro ejemplar no encuentra nada (404), nunca borra o cambia el registro ajeno.
- El id del ejemplar de la ruta debe existir (404 si no); el formulario solo aporta fechas, nunca ids.
- Toda ruta nueva es POST con redirección 303 a `/coleccion/{id}`, exige sesión y el token CSRF (dependencia global); un fallo de validación vuelve a la ficha con 422 y el mensaje, sin cambiar la base.
- Quitar el ejemplar borra sus riegos y floraciones por cascada (`PRAGMA foreign_keys = ON` en toda conexión).
- Los mensajes de la interfaz van en español; el texto se muestra con el escape automático de las plantillas.
- `/coleccion/nuevo` se registra antes que `/coleccion/{id}` (ya cumplido); las rutas de cuidados cuelgan de `/coleccion/{id}/riegos` y `/coleccion/{id}/floraciones`.

## Decisions (ADRs)

- ADR-008: Riegos y floraciones en dos tablas, con fechas de calendario en texto ISO — descarta la tabla genérica de eventos (rabbit hole del brief) y los enteros Unix (el día cambiaría con la zona); `records/decisions/adr-008-cuidados-en-dos-tablas-con-fechas-de-calendario.md`.

## Legacy sweep

Nada se elimina: e4 es net-new. `README.md` dice hoy que la colección vive en una base SQLite y un directorio de fotos; s4.6 añade que también guarda el historial de cuidados. Los tests de `test_recorrido_coleccion.py` y `test_web_coleccion.py` que asumen la ficha de e3 se revisan en s4.2 y s4.4 y no se dejan sin resolver.
