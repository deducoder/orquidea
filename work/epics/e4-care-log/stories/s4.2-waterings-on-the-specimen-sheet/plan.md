# Story s4.2: Waterings on the specimen sheet — Plan

> Size: M
> Pause: none (default)

## Tasks

### T1 · La ficha y el 404 del ejemplar, públicos y con la conexión

- **Files:** modify `web/rutas/coleccion.py`
- **TDD:** refactor sin comportamiento nuevo: RED no aplica (la suite existente es la red); se cambia `_ficha` → `ficha(request, conexion, estado, ejemplar, error="", fecha="")` y `_ejemplar_o_404` → `ejemplar_o_404`, con sus llamadores; la ficha aún no carga riegos → REFACTOR
- **Satisfies:** base de todos los escenarios de la ficha; el criterio «las pruebas de e1 a e3 siguen en verde sin cambiar sus aserciones»
- **Mold:** `web/rutas/coleccion.py` (`_ficha`, `subir_foto`)
- **Verify:** la suite web de e1 a e3 pasa sin editar una aserción — forced mutations: dejar un llamador de `_ficha` con la firma vieja (`subir_foto` falla con `TypeError`: `tests/test_web_fotos.py` en rojo); then `uv run pytest tests/test_web_coleccion.py tests/test_web_fotos.py tests/test_recorrido_coleccion.py -q` y `./scripts/check`
- **Commit:** refactor(coleccion): la ficha recibe la conexión y se comparte con otros routers

### T2 · Registrar un riego y verlo en la ficha

- **Files:** create `web/rutas/cuidados.py`, `tests/test_web_cuidados.py`; modify `web/rutas/coleccion.py` (la ficha carga `riegos`, `ultimo`, `hoy`), `web/app.py` (monta el router), `web/templates/ejemplar_ficha.html`, `tests/test_web_rutas.py`
- **TDD:** RED pruebas web: sin riegos («Aún no hay riegos.», sin «Último riego»); registrar guarda, redirige 303 y la ficha muestra el riego y el último; tres riegos en desorden salen del más reciente al más antiguo; fecha inválida/inexistente/futura → 422 con mensaje y sin guardar, conservando lo escrito y escapado (`"><script>`); el tope → 422; ejemplar inexistente → 404; el mapa de rutas incluye la nueva → GREEN router, contexto de la ficha y sección de la plantilla → REFACTOR
- **Satisfies:** los tres primeros `@stated` y el de la fecha inválida; `@deduced` de ficha vacía, tope y 404; los escenarios añadidos del escape, el orden y la foto intacta
- **Mold:** `web/rutas/coleccion.py` (`subir_foto`: 422 con `ficha` y redirección 303) y `web/templates/ejemplar_ficha.html` (sección Foto)
- **Verify:** lo guardado es lo que la ficha muestra y una fecha rechazada no toca la base — forced mutations: no llamar a `validar_fecha` antes de `agregar` (la fecha futura se guarda); `agregar` con la cadena cruda sin `strip` no aplica; mostrar el historial en orden ascendente (la prueba de orden falla); imprimir el valor del campo con `|safe` (equivalent form: la prueba del `"><script>` falla); omitir el `except CuidadoInvalido` del tope (500, no 422); quitar la sección «Riegos» de la plantilla (la prueba de «Último riego» no encuentra el sujeto y falla, no calla); then `uv run pytest tests/test_web_cuidados.py tests/test_web_rutas.py tests/test_web_coleccion.py -q` y `./scripts/check` completo (archivo nuevo escaneado por el gate)
- **Commit:** feat(cuidados): registrar un riego y verlo en la ficha del ejemplar

### T3 · Quitar un riego

- **Files:** modify `web/rutas/cuidados.py`, `web/templates/ejemplar_ficha.html`, `tests/test_web_cuidados.py`, `tests/test_web_rutas.py`
- **TDD:** RED pruebas: quitar borra ese riego y el último se recalcula; el riego de otro ejemplar → 404 y sigue; riego inexistente → 404; ejemplar inexistente → 404; el otro ejemplar no cambia → GREEN ruta y botón por riego → REFACTOR
- **Satisfies:** `@stated` de quitar; `@deduced` de 404 y de independencia entre ejemplares
- **Mold:** `web/rutas/coleccion.py` (`quitar_la_foto`: POST, 404, redirección 303) y `datos/riegos.quitar` (s4.1)
- **Verify:** un riego ajeno no se borra por un id de ejemplar propio — forced mutations: la ruta llama a `quitar` con el `riego` en los dos argumentos o sin comprobar el retorno (el riego ajeno se borra o responde 303: la prueba falla); no redirigir tras quitar; then `uv run pytest tests/test_web_cuidados.py tests/test_web_rutas.py -q` y `./scripts/check`
- **Commit:** feat(cuidados): quitar un riego de la ficha

### T4 · Sesión, CSRF y recorrido de la métrica líder

- **Files:** modify `tests/test_web_cuidados.py`, `tests/test_recorrido_coleccion.py`
- **TDD:** RED/caracterización: sin sesión las dos rutas redirigen al acceso y no cambian nada; sin token CSRF, 403 y nada cambia; recorrido de extremo a extremo (agregar un ejemplar, registrar un riego, ver «Último riego», quitar el ejemplar y verificar que su historial desapareció) → GREEN (deben pasar con lo de T2 y T3; si alguna falla, corregir la ruta antes de seguir) → REFACTOR
- **Satisfies:** `@deduced` de sesión y CSRF; el `@stated` líder de punta a punta; la cascada por HTTP
- **Mold:** `tests/test_web_proteccion.py` (rutas sin sesión) y `tests/test_web_fotos.py` (prueba de CSRF)
- **Verify:** ninguna escritura de riegos sucede sin sesión ni token — forced mutations: registrar la ruta fuera del router incluido con la dependencia global (equivalent form: `dependencies=[]` no aplica al global; se comprueba quitando `Depends(exigir_sesion)` de `FastAPI(...)`, la prueba de sesión falla); enviar el token en un campo con otro nombre (403 no ocurre: la de CSRF falla); then `uv run pytest tests/test_web_cuidados.py tests/test_recorrido_coleccion.py tests/test_web_proteccion.py -q` y `./scripts/check`
- **Commit:** test(cuidados): sesión, CSRF y recorrido de los riegos de punta a punta

### T5 · Manual integration test

- Con `uvicorn` real (`ORQUIDEA_DB`/`ORQUIDEA_FOTOS` en una carpeta temporal, `ORQUIDEA_COOKIE_SEGURA=0`, contraseña por `ORQUIDEA_PASSWORD_HASH`): entrar, agregar un ejemplar, abrir su ficha, registrar un riego de hoy y otro de hace una semana, ver el historial y el último, probar una fecha futura y el escape, quitar un riego y comprobar que el último se recalcula; mirar la salida del proceso y las cabeceras de la ficha.
- **Verify:** con la aplicación corriendo, la ficha muestra el último riego tras registrar, rechaza la fecha futura con el mensaje y responde con `Cache-Control: no-store` y la CSP.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 → T5 — T1 habilita el reuso de la ficha sin cambiar comportamiento; T2 es el esqueleto y el mayor riesgo (validación, escape, orden); T3 el IDOR; T4 cierra seguridad y la métrica líder.
- **Dependencies:** secuencial.
- **Risks:** `test_web_rutas.py` falla en cuanto se añade una ruta → se actualiza en la misma tarea (T2 y T3); `test_web_proteccion.py` sustituye `{id}` pero no `{riego}` y pide la ruta literal → basta con que la dependencia global responda 303 antes de validar el parámetro (ya ocurre con `{id}`), se comprueba en T2; cambiar la firma de `ficha` rompe `subir_foto` → T1 aparte, con la suite de fotos como red; el valor devuelto en el campo es entrada del usuario → escape de Jinja y prueba con `"><script>`.
