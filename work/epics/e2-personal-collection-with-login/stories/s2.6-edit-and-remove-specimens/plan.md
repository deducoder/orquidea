# Story s2.6: Edit and remove specimens — Plan

> Size: M
> Pause: none (default)

## Tasks

### T1 · Validar con o sin especie; obtener, actualizar y quitar

- **Files:** modify `src/orquidea/coleccion/modelo.py`, `src/orquidea/datos/ejemplares.py`, `src/orquidea/web/app.py` (solo el nombre de la función usada), `tests/test_coleccion_modelo.py`, `tests/test_datos_ejemplares.py`
- **TDD:** RED pruebas: `validar_ejemplar` conserva el comportamiento de s2.5 con `con_especie=False`; con `con_especie=True` acepta nombre vacío pero sigue limitando a 120 y las notas a 2000; `obtener` devuelve el ejemplar o `None`; `actualizar` cambia solo la fila pedida (dos ejemplares de la misma especie) y devuelve `True`/`False`; `quitar` borra solo esa fila y devuelve `True`/`False`; el SQL es parametrizado (nombre con comillas) → GREEN (renombrar `validar_ejemplar_propio`, actualizar sus llamadas y pruebas) → REFACTOR
- **Satisfies:** scenarios de independencia, validación, identificador inexistente y nombre opcional
- **Mold:** `orquidea.datos.ejemplares.agregar_sin_especie` (T1 de s2.5)
- **Verify:** `UPDATE`/`DELETE` sin `WHERE id = ?` (rojo con dos filas); devolver siempre `True` (rojo con el id inexistente); exigir nombre también con especie (rojo); dejar sin límite el nombre con especie (rojo); concatenar el texto en el SQL (rojo con comillas); luego `./scripts/check` completo
- **Commit:** feat(coleccion): actualizar y quitar ejemplares, nombre opcional con especie

### T2 · Editar un ejemplar

- **Files:** modify `src/orquidea/web/app.py`, `src/orquidea/web/templates/coleccion.html`; rename `src/orquidea/web/templates/nuevo_ejemplar.html` → `ejemplar.html`; modify `tests/test_web_coleccion.py`
- **TDD:** RED pruebas con `client`: `GET /coleccion/{id}/editar` trae nombre y notas actuales, el token y (con especie) el nombre científico como texto; `POST` válido → 303 y solo esa fila cambió; ejemplar propio con nombre vacío → 422 con lo escrito y sin cambio; nombre y notas excesivos → 422; ejemplar del catálogo con nombre vacío → 303 y nombre `""`; id inexistente → 404 (GET y POST); id no numérico → 422; sin token → 403; anónimo → 303 al acceso; la lista trae el enlace "Editar" de cada ejemplar y el nombre propio de uno del catálogo; HTML escapado al volver a mostrar → GREEN → REFACTOR
- **Satisfies:** scenarios de edición, validación, id inexistente, CSRF y los deltas del diseño
- **Mold:** rutas de `/coleccion/nuevo` (T2 de s2.5)
- **Verify:** no filtrar por id (rojo: cambia al vecino); no validar (rojo); responder 200 en el error (rojo); `|safe` en el formulario (rojo); ignorar el 404 (rojo); permitir cambiar `especie_id` por el formulario (rojo con un campo extra que no debe tener efecto); quitar el token del formulario (rojo, aserción acotada al `<form>`); luego `./scripts/check` completo
- **Commit:** feat(web): editar ejemplares de la colección

### T3 · Quitar con confirmación

- **Files:** modify `src/orquidea/web/app.py`, `src/orquidea/web/templates/coleccion.html`, `tests/test_web_coleccion.py`; create `src/orquidea/web/templates/confirmar_baja.html`
- **TDD:** RED pruebas: `GET /coleccion/{id}/quitar` muestra la confirmación con el nombre y **no** borra; `POST` con token → 303, esa fila desaparece y las demás (incluida otra de la misma especie) siguen; id inexistente → 404 en GET y POST; sin token → 403 y la fila sigue; anónimo → 303 al acceso y la fila sigue; la lista trae el enlace "Quitar" de cada ejemplar; el formulario de la confirmación trae el token → GREEN → REFACTOR
- **Satisfies:** scenarios de baja, confirmación, independencia, id inexistente y CSRF
- **Mold:** T2
- **Verify:** quitar en el `GET` (rojo); `DELETE` sin `WHERE` (rojo con vecinos); no exigir token (lo cubre la dependencia global: rojo si se quita de `RUTAS`); devolver 303 con id inexistente (rojo); confirmación sin el nombre (rojo); luego `./scripts/check` completo
- **Commit:** feat(web): quitar ejemplares con confirmación

### T4 · Manual integration test

- Con `uvicorn` real: tres ejemplares (dos de la misma especie y uno propio); editar las notas de uno de los dos iguales, cambiar nombre y notas del propio, abrir la confirmación de baja sin confirmar, confirmar; ver la lista tras cada paso y tras reiniciar.
- **Verify:** solo cambió el ejemplar editado, la confirmación no quitó nada, la baja quitó solo uno, todo persiste tras el reinicio y `./scripts/check` está en verde.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 — dominio y repositorio primero; la edición reutiliza el formulario de s2.5; la baja es lo más simple y lo destructivo, al final.
- **Dependencies:** secuenciales, acíclicas.
- **Risks:** la enumeración de rutas de `test_web_proteccion.py` sustituye `{id}` por un texto no numérico y ahora la ruta pide un entero → la dependencia global corre antes de validar el parámetro y responde 303; si no fuera así el test lo dirá y se ajusta el sustituto; renombrar `nuevo_ejemplar.html` debe cubrir toda referencia (grep).
