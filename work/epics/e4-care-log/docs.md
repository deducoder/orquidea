# Epic e4: Care log — Docs

## Worked example

Registrar un riego en la ficha de un ejemplar y ver el último, con valores reales (prueba manual de s4.2 con `uvicorn` y `curl`, y las pruebas de `tests/test_web_cuidados.py`).

Entrada: el ejemplar 1 ya existe; el 12 de septiembre de 2026 (UTC) el usuario elige la fecha del riego y envía `POST /coleccion/1/riegos` con `fecha=2026-09-12` y `csrf=<token de la sesión>` (el formulario lo trae en el campo oculto de `_csrf.html`).

1. `exigir_sesion` (`web/sesion.py`, dependencia global): valida la cookie `__Host-sesion` y el `csrf`; sin ellos, 303 al acceso o 403. La ruta nueva no la repite.
2. `registrar_riego` (`web/rutas/cuidados.py`): `ejemplar_o_404` (importado de `web/rutas/coleccion.py`) carga el ejemplar 1; un id inexistente ya sería un 404.
3. `validar_fecha(" 2026-09-12 ", hoy())` (`coleccion/modelo.py`) recorta, exige el formato `[0-9]{4}-[0-9]{2}-[0-9]{2}` con dígitos ASCII, `date.fromisoformat` comprueba que exista y compara con `hoy()` (el día del servidor en UTC, definido en `web/rutas/coleccion.py`): devuelve `"2026-09-12"`. Con `2026-09-25` lanzaría `CuidadoInvalido("La fecha no puede ser posterior a hoy.")`.
4. `datos.riegos.agregar(conexion, 1, "2026-09-12")` ejecuta **una** sentencia, `INSERT INTO riegos … SELECT ?, ? WHERE EXISTS (ejemplar) AND (SELECT COUNT(*) …) < 500`: el ejemplar existe y tiene menos de `CUIDADOS_MAXIMO` riegos, así que inserta y devuelve `Riego(id=1, ejemplar_id=1, fecha="2026-09-12")`. El `CHECK` de la tabla `riegos` (`GLOB '[0-9]…-[0-9]…-[0-9]…'`) es la segunda barrera.
5. Respuesta `303` a `/coleccion/1`. `ficha_del_ejemplar` llama a `ficha()` (`web/rutas/coleccion.py`), que carga `listar_riegos` (ascendente por fecha e id) y arma el contexto: `riegos` invertido (más reciente primero) y `ultimo = riegos[-1]`. La plantilla `ejemplar_ficha.html` pinta «Último riego: <strong>2026-09-12</strong>» y la lista.
6. "Mi colección" (`mi_coleccion`) pide `datos.riegos.ultimos(conexion)` **una vez**: `SELECT ejemplar_id, MAX(fecha) FROM riegos GROUP BY ejemplar_id` → `{1: "2026-09-12"}`, y cada fila muestra «Último riego: 2026-09-12» o «Sin riegos».

```mermaid
sequenceDiagram
    participant N as Navegador
    participant S as exigir_sesion
    participant R as registrar_riego
    participant D as modelo.validar_fecha
    participant A as datos.riegos.agregar
    N->>S: POST /coleccion/1/riegos (fecha, csrf)
    S->>R: sesión y CSRF válidos
    R->>D: validar_fecha(fecha, hoy())
    D-->>R: "2026-09-12" (o CuidadoInvalido → 422 con la ficha)
    R->>A: agregar(conexion, 1, "2026-09-12")
    A-->>R: Riego(id=1, …) (None → ejemplar inexistente; CuidadoInvalido → tope)
    R-->>N: 303 /coleccion/1
    N->>R: GET /coleccion/1 → ficha(): historial y último riego
```

Una floración sigue el mismo camino con `validar_floracion` y una máquina de estados de dos estados: `POST /coleccion/1/floraciones` con `inicio=2026-03-01` y `fin=` vacío guarda `Floracion(id=1, ejemplar_id=1, inicio="2026-03-01", fin=None)` (en curso); `POST /coleccion/1/floraciones/1/fin` con `fin=2026-03-20` ejecuta `UPDATE … SET fin = ? WHERE id = ? AND ejemplar_id = ? AND fin IS NULL AND inicio <= ?` y la deja terminada; repetirlo da 422 «Esa floración ya terminó.».

## Extension guide

**Añadir otro tipo de cuidado (p. ej. la fertilización aparcada en el parking lot).** Sigue el patrón de riegos y floraciones (ADR-008: una tabla por tipo, sin genérico):

1. Migración nueva `src/orquidea/datos/migraciones/0006-fertilizaciones.sql` con `ejemplar_id … ON DELETE CASCADE`, un `CHECK` de la forma de la fecha (`GLOB`) e índice `(ejemplar_id, fecha)`. Las migraciones aplicadas no se editan (ADR-003).
2. Dominio en `coleccion/modelo.py`: un modelo `pydantic` y su validación con `validar_fecha`; el tope reutiliza `CUIDADOS_MAXIMO`.
3. `datos/fertilizaciones.py` con `agregar` (un solo `INSERT … SELECT … WHERE EXISTS … AND COUNT < ?`, `None` si el ejemplar no existe, `CuidadoInvalido` en el tope con el nombre del cuidado), `listar`, `quitar(ejemplar_id, id)` filtrando por los dos.
4. Rutas `POST` en `web/rutas/cuidados.py` (validar antes de escribir, 303 a la ficha, 422 con `ficha(..., valores={…})`, 404 por filtro) y una sección en `web/templates/ejemplar_ficha.html`; añade los campos que un formulario devuelve a `valores` de `ficha()`.
5. Pruebas: `tests/test_datos_fertilizaciones.py` (copia de `test_datos_riegos.py`: orden, ajeno, cascada, tope, `CHECK`, migración sobre la versión anterior, altas simultáneas), `tests/test_web_cuidados.py` (con `_desfasar_los_ids()` en las pruebas de camino feliz y de IDOR), las rutas en `RUTAS` de `tests/test_web_rutas.py` y la ficha llena en `scripts/medir-primera-carga.py::medir_ficha`.

**Cambiar el tope o la política de fechas.** `CUIDADOS_MAXIMO` (500) vive en `coleccion/modelo.py`; el README y su prueba de deriva (`test_cada_cifra_de_la_guia_es_la_de_su_constante`) lo repiten. «Hoy» es `hoy()` en `web/rutas/coleccion.py` (UTC): cambiar a la zona del usuario es una decisión con un ADR nuevo que sustituya el punto de ADR-008, no un cambio de la constante.

**Añadir un dato por ejemplar a "Mi colección".** Una función en `datos/` que devuelva un diccionario por `ejemplar_id` en **una** consulta (como `ultimos`), cargada una vez en `mi_coleccion` y probada con `set_trace_callback` (una sola sentencia).

Errores comunes: contar el tope en una consulta aparte antes de insertar (las peticiones tienen conexiones propias: dos altas simultáneas lo rebasan); confiar en el `CHECK` en vez de llamar a `validar_fecha` antes de escribir (el usuario vería un 500 por `IntegrityError` en lugar de un 422); filtrar `quitar` solo por el id del registro (un id ajeno lo borraría); escribir pruebas de IDOR con ids que coinciden (un cruce de argumentos pasaría); olvidar la ruta nueva en `tests/test_web_rutas.py`.

## Data flow

```
formulario de la ficha ──POST──▶ exigir_sesion ──▶ cuidados.py: registrar_riego / registrar_floracion / terminar_floracion / quitar_riego / quitar_la_floracion
   fecha (str) ──▶ validar_fecha / validar_floracion (coleccion/modelo.py) ──▶ str "AAAA-MM-DD" (y None si no hay fin)
   ──▶ datos/riegos.py: agregar · quitar         ──▶ tabla riegos       (0004-riegos.sql)
   ──▶ datos/floraciones.py: agregar · terminar · quitar ──▶ tabla floraciones (0005-floraciones.sql)
lectura de la ficha:   GET /coleccion/{id} ──▶ ficha() ──▶ listar_riegos + listar_floraciones ──▶ ejemplar_ficha.html
lectura de la lista:   GET /coleccion       ──▶ mi_coleccion ──▶ datos.riegos.ultimos ──▶ coleccion.html
baja del ejemplar:     POST /coleccion/{id}/quitar ──▶ DELETE ejemplares ──▶ ON DELETE CASCADE ──▶ riegos y floraciones
medición:              scripts/medir-primera-carga.py ──▶ coleccion_temporal() ──▶ medir · medir_ficha ──▶ gzip ≤ 200 KB
```

Tipos en cada frontera: `str` (formulario) → `str` validada / `tuple[str, str | None]` (`validar_floracion`) → `Riego{id, ejemplar_id, fecha}` y `Floracion{id, ejemplar_id, inicio, fin: str | None}` (modelos `pydantic` de `coleccion/modelo.py`) → contexto de la plantilla (`riegos` invertido, `ultimo`, `floraciones` invertido, `hoy`, `fecha`, `inicio`, `fin`). Errores de dominio: `CuidadoInvalido` (→ 422 con la ficha); ejemplar o registro inexistente o ajeno → 404 (`ejemplar_o_404`, `quitar`/`terminar` devuelven `False`). `ficha(request, conexion, estado, ejemplar, error, valores)` devuelve lo que el usuario escribió en `valores`, escapado por Jinja.

## Invariants & contracts

- **Una fecha de cuidado es `AAAA-MM-DD` válida, con dígitos ASCII y no posterior a hoy (UTC).** Lo imponen `validar_fecha` y el `CHECK … GLOB` de `riegos` y `floraciones`. Síntoma de violación: un 500 por `sqlite3.IntegrityError` al registrar. Comprobación: `tests/test_coleccion_modelo.py` (formatos `20260919`, `2026-W38-3` y otros alfabetos) y las pruebas de `CHECK` de `test_datos_riegos.py` y `test_datos_floraciones.py`.
- **Ningún ejemplar pasa de 500 riegos ni de 500 floraciones**, ni con altas simultáneas: el tope y la existencia del ejemplar van dentro del mismo `INSERT`. Síntoma: 501 filas. Comprobación: `test_altas_simultaneas_no_rebasan_el_tope` (8 hilos, una conexión por hilo, `Barrier`; falló 15 de 15 al contar aparte).
- **Una floración terminada no cambia**, y `fin >= inicio` siempre: `terminar` es un `UPDATE` condicionado (`fin IS NULL AND inicio <= ?`) y la tabla lo respalda con `CHECK (fin IS NULL OR fin >= inicio)`. Síntoma: un fin que cambia o anterior al inicio. Comprobación: `test_terminar_una_ya_terminada…`, `test_terminar_simultaneo…`.
- **Toda escritura filtra por `ejemplar_id` y por el id del registro.** Síntoma: el registro de otro ejemplar se borra o cierra. Comprobación: pruebas de dos ejemplares con ids desfasados (`_desfasar_los_ids`) en `test_web_cuidados.py` y de datos.
- **Quitar un ejemplar borra su historial** (`PRAGMA foreign_keys = ON` en `datos/base.py::conectar` más `ON DELETE CASCADE`). Síntoma: filas huérfanas en `riegos`/`floraciones`. Comprobación: `test_quitar_el_ejemplar_borra_sus_riegos…` y el recorrido de `test_recorrido_coleccion.py`.
- **La lista pide los últimos riegos en una sola sentencia**, sin importar cuántos ejemplares haya. Síntoma: una consulta por fila. Comprobación: `test_ultimos_es_una_sola_sentencia…` y `test_la_lista_pide_los_ultimos_riegos_una_sola_vez`.
- **Los historiales van del más reciente al más antiguo** en la ficha (los datos, ascendentes por fecha o inicio y luego id). Comprobación: `test_la_ficha_lista_los_riegos…` y `…las_floraciones…`.
- **Cada migración es un archivo nuevo y las pruebas no fijan la versión final.** Síntoma: una migración nueva rompe la prueba de la anterior. Comprobación: `len(list(MIGRACIONES.glob("*.sql")))` en las pruebas de migración.
- **Presupuesto de peso:** la ficha con 50+50 y con el tope 500+500, en gzip y sin fotos, ≤ 200 KB (`test_medicion.py`); la aplicación no comprime, lo hace el proxy.

## Failure-mode catalog

- **«Al registrar un riego me sale un error 500».** Causa: una fecha llegó a `agregar` sin pasar por `validar_fecha` y el `CHECK` lanzó `IntegrityError`. Diagnóstico: el registro del servidor nombra `CHECK constraint failed: riegos`; buscar la ruta que llama a `agregar` sin `validar_fecha`. Arreglo: validar antes de escribir (patrón de `registrar_riego`).
- **«El navegador me deja elegir hoy pero el servidor dice que es posterior a hoy» (o al revés: deja pasar mañana).** Causa: «hoy» es el del servidor en UTC (ADR-008); al este de UTC, por la mañana, el día local ya es el siguiente; al oeste, por la noche, se acepta un día de más. Diagnóstico: comparar `datetime.now(UTC).date()` con la fecha local y el `max` del campo (`hoy`). Arreglo: es una decisión de diseño, documentada en el README; cambiarla exige un ADR que sustituya el punto de ADR-008.
- **«Puedo tener más de 500 riegos».** Causa: el tope se contó en una consulta y el alta en otra. Diagnóstico: `test_altas_simultaneas_no_rebasan_el_tope` en bucle de 15 corridas; leer `agregar` y confirmar que es un solo `INSERT … SELECT`. Arreglo: dejar la comprobación dentro del `INSERT`.
- **«La floración aparece dos veces cerrada» / «no puedo cerrar una floración».** Causa: `terminar` devolvió `CuidadoInvalido` («Esa floración ya terminó.» tiene prioridad sobre «El fin no puede ser anterior al inicio.» si ya tenía fin). Diagnóstico: `SELECT inicio, fin FROM floraciones WHERE id = ?`. Arreglo: si el fin estaba mal, quitar la floración y registrarla de nuevo (no se reabre).
- **«Un formulario rechazado me borró lo que escribí en otro»** o **«el campo trae la fecha del otro formulario».** Causa: `valores` de `ficha()` mezclado entre formularios (`fecha` del riego, `inicio` y `fin` de la floración). Diagnóstico: `test_una_floracion_rechazada_conserva_sus_campos…` y su inverso. Arreglo: cada formulario lee solo su propia clave.
- **«Registré el riego de un ejemplar que acababa de quitar y me lleva a un 404».** Causa: `agregar` devuelve `None` si el ejemplar desapareció entre `ejemplar_o_404` y el alta (ventana de milisegundos); la ruta redirige a una ficha inexistente. Diagnóstico: `agregar(...) is None`. Arreglo: aceptado (retrospectiva de s4.2); si molesta, convertir `None` en 404.
- **«Una prueba de IDOR pasa pero la ruta cruza los ids».** Causa: el id del ejemplar y el del registro coincidían (1 y 1). Diagnóstico: aplicar la mutación de argumentos cruzados y ver que ninguna prueba falla. Arreglo: `_desfasar_los_ids()` (memoria del proyecto).
- **«La prueba de migración de una historia anterior falla al añadir una migración».** Causa: afirmaba `user_version == N`. Diagnóstico: el mensaje `assert (5,) == (4,)`. Arreglo: comparar con el número de archivos de `MIGRACIONES` (retrospectiva de s4.3).
- **«La ficha con muchos registros tarda o pesa medio megabyte».** Causa: la aplicación no comprime; con 500+500 la ficha pesa 488,7 KB sin comprimir (13,8 KB en gzip). Diagnóstico: `uv run python scripts/medir-primera-carga.py` y `curl -H 'Accept-Encoding: gzip' -I` contra el despliegue para ver si el proxy comprime. Arreglo: activar la compresión del proxy o añadir `GZipMiddleware` con un ADR (entrada del parking lot).
- **«Una ruta nueva de cuidados falla `test_web_rutas`».** Causa: el mapa de rutas declarado es exacto. Diagnóstico: la diferencia entre `RUTAS` y `rutas_registradas(app.routes)`. Arreglo: declarar la ruta nueva; `test_web_proteccion.py` la cubre sola.
