# Story s2.4: Add catalog specimens and see them — Plan

> Size: M
> Pause: none (default)

## Tasks

### T1 · Tabla, modelo y repositorio de ejemplares

- **Files:** create `src/orquidea/datos/migraciones/0002-ejemplares.sql`, `src/orquidea/coleccion/__init__.py`, `src/orquidea/coleccion/modelo.py`, `src/orquidea/datos/ejemplares.py`, `tests/test_coleccion_modelo.py`, `tests/test_datos_ejemplares.py`
- **TDD:** RED pruebas: `agregar` devuelve el `Ejemplar` con id y `creado` y lo guarda; dos altas de la misma especie son dos filas distintas; `listar` ordena por id y persiste al reabrir la base; sin especie y sin nombre la base rechaza la fila (`CHECK`); `resolver` empareja cada ejemplar con su `Especie` y da `None` si no está en el catálogo o no tiene especie; el SQL es parametrizado (un `especie_id` con comillas se guarda literal) → GREEN → REFACTOR
- **Satisfies:** scenarios de independencia, persistencia y especie desaparecida
- **Mold:** `src/orquidea/datos/sesiones.py` (repositorio parametrizado) y `src/orquidea/catalogo/modelo.py` (modelo pydantic)
- **Verify:** quitar el `CHECK` (rojo), concatenar el `especie_id` en el SQL (rojo con la comilla), ordenar descendente (rojo), `resolver` que devuelve la primera especie en vez de buscar por id (rojo con dos especies), que cruce las especies entre ejemplares (rojo); luego `./scripts/check` completo
- **Commit:** feat(coleccion): tabla, modelo y repositorio de ejemplares

### T2 · Rutas de la colección, botón en la ficha y lista

- **Files:** modify `src/orquidea/web/app.py`, `src/orquidea/web/templates/base.html`, `src/orquidea/web/templates/especie.html`; create `src/orquidea/web/templates/coleccion.html`, `src/orquidea/web/templates/_csrf.html`, `tests/test_web_coleccion.py`
- **TDD:** RED pruebas con `client`: `POST /coleccion` con especie válida → 303 a `/coleccion` y una fila; especie inexistente → 404 sin fila; sin `especie_id` → 422; sin token → 403; anónimo → 303 a `/acceso`, sin fila; `GET /coleccion` vacía muestra el mensaje; con dos ejemplares de la misma especie muestra dos entradas enlazadas a `/especies/{id}`; con la especie fuera del catálogo muestra el identificador y el aviso; un nombre científico con HTML sale escapado; la ficha trae el formulario de agregar con `csrf` y `especie_id`; la cabecera trae el enlace "Mi colección" → GREEN → REFACTOR
- **Satisfies:** scenarios 1 a 4, 6 a 9 y los deltas
- **Mold:** rutas de s2.2/s2.3 (`Base`, redirección 303) y `especies.html`
- **Verify:** no validar la especie contra el catálogo (rojo); redirigir con 200 en lugar de 303; mostrar el `especie_id` en vez del nombre; olvidar `escape` (rojo: plantilla con `|safe`); quitar el mensaje vacío (rojo); quitar el campo `csrf` del botón (rojo); luego `./scripts/check` completo
- **Commit:** feat(web): mi colección con ejemplares del catálogo

### T3 · Recorrido de la métrica líder de punta a punta

- **Files:** create `tests/test_recorrido_coleccion.py`
- **TDD:** RED prueba sin atajos: contraseña real con `hashear_contrasena`, `POST /acceso`, `GET /especies/{id}` sobre el catálogo real, extraer el token del formulario "Agregar a mi colección" del HTML, `POST /coleccion`, seguir la redirección y comprobar el ejemplar en "Mi colección"; reabrir la base y comprobar que sigue → GREEN (no debería requerir código nuevo; si lo requiere, es un defecto de T2) → REFACTOR
- **Satisfies:** scenario 5 (métrica líder) y el de persistencia
- **Mold:** T2
- **Verify:** quitar el botón de la ficha o el token del formulario (rojo); luego `./scripts/check`
- **Commit:** test(coleccion): recorrido de la métrica líder de punta a punta

### T4 · Manual integration test

- Con `uvicorn` real, hash de la orden y `ORQUIDEA_COOKIE_SEGURA=0`: acceder con `curl`, abrir una ficha del catálogo real, agregar dos ejemplares de la misma especie y uno de otra, ver la colección, reiniciar el proceso y volver a verla.
- **Verify:** tres ejemplares, dos de la misma especie con enlaces a su ficha; persisten tras el reinicio; `./scripts/check` en verde.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 — datos primero, luego la web, luego la prueba que ata todo.
- **Dependencies:** secuenciales, acíclicas.
- **Risks:** `Form()` global en `exigir_sesion` más `Form()` propio de la ruta puede chocar → T2 lo ejercita; el campo del botón (`especie_id`) viaja en el formulario, no en la URL; una tabla con columnas que s2.4 no usa (`nombre`, `notas`) es un adelanto deliberado, no un descuido.
