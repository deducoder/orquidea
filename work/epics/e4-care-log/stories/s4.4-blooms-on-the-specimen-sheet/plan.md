# Story s4.4: Blooms on the specimen sheet — Plan

> Size: M
> Pause: none (default)

## Tasks

### T1 · Registrar una floración y verla en la ficha

- **Files:** modify `web/rutas/cuidados.py`, `web/rutas/coleccion.py` (`ficha` recibe `valores` en lugar de `fecha` y carga `floraciones`), `web/templates/ejemplar_ficha.html`, `tests/test_web_cuidados.py`, `tests/test_web_rutas.py`
- **TDD:** RED pruebas web: sin floraciones («Aún no hay floraciones.»); registrar sin fin → 303 y la ficha la muestra «en curso»; con fin → la muestra terminada; tres en desorden salen de la más reciente a la más antigua; fecha inválida/inexistente/futura y fin anterior al inicio → 422 con mensaje, sin guardar, con los campos devueltos escapados (`"><script>` en `inicio` y en `fin`); el tope → 422; ejemplar inexistente → 404; el formulario de riegos que falla conserva su fecha y el de floraciones no se altera; el mapa de rutas incluye la nueva → GREEN ruta, `valores` en `ficha`, contexto y sección de la plantilla → REFACTOR
- **Satisfies:** `@stated` de registrar (sin fin y con fin) y de fechas inválidas; `@deduced` de ficha vacía, orden y tope; escenarios añadidos del escape, el orden y los valores por defecto
- **Mold:** `web/rutas/cuidados.py::registrar_riego` y la sección «Riegos» de `ejemplar_ficha.html` (s4.2)
- **Verify:** lo guardado es lo que la ficha muestra y una fecha rechazada no toca la base — forced mutations: llamar a `agregar` con el `inicio` y el `fin` crudos sin `validar_floracion` (la fecha futura y el fin anterior se guardan o dan `IntegrityError`); mostrar el historial en orden ascendente; imprimir `inicio` o `fin` con `|safe` (equivalent form: la prueba del `"><script>` falla); omitir el `except CuidadoInvalido` (500, no 422); quitar la sección «Floraciones» de la plantilla (las pruebas no encuentran el sujeto y fallan, no callan); then `uv run pytest tests/test_web_cuidados.py tests/test_web_rutas.py tests/test_web_coleccion.py tests/test_web_fotos.py -q` y `./scripts/check`
- **Commit:** feat(cuidados): registrar una floración y verla en la ficha del ejemplar

### T2 · Fijar el fin y quitar una floración

- **Files:** modify `web/rutas/cuidados.py`, `web/templates/ejemplar_ficha.html`, `tests/test_web_cuidados.py`, `tests/test_web_rutas.py`
- **TDD:** RED pruebas: terminar una en curso la deja terminada (303) y su «Terminar» desaparece; terminar con fin anterior → 422 y sigue en curso; ya terminada → 422; fin inválido o futuro → 422; floración ajena o inexistente → 404 en `fin` y en `quitar`; quitar borra solo esa y no toca las de otro ejemplar; la ficha ofrece «Terminar» solo en las que están en curso y «Quitar» en todas → GREEN rutas y formularios → REFACTOR
- **Satisfies:** `@stated` de fijar el fin y de quitar; `@deduced` de 404 y de «Terminar» solo en curso; escenario añadido de terminada sin «Terminar»
- **Mold:** `web/rutas/cuidados.py::quitar_riego` (s4.2) y `datos/floraciones.terminar` (s4.3)
- **Verify:** una floración ajena no cambia por un id de ejemplar propio y una terminada no vuelve a cambiar — forced mutations: `terminar` con el `floracion` en los dos argumentos de id o sin comprobar el retorno (la ajena cambia o responde 303); `quitar` sin comprobar el retorno; dibujar «Terminar» en todas (la prueba de «solo en curso» falla); no validar el fin con `validar_fecha` (un fin con formato inválido llega a la base y da `IntegrityError` en vez de 422); then `uv run pytest tests/test_web_cuidados.py tests/test_web_rutas.py -q` y `./scripts/check`
- **Commit:** feat(cuidados): terminar y quitar una floración desde la ficha

### T3 · Sesión, CSRF y recorrido del historial de floración

- **Files:** modify `tests/test_web_cuidados.py`, `tests/test_recorrido_coleccion.py`
- **TDD:** RED/caracterización: sin sesión las tres rutas redirigen al acceso y no cambian nada; sin token (o con uno equivocado) 403 y nada cambia; recorrido por la interfaz: agregar un ejemplar, registrar una floración en curso, terminarla, ver el historial con las dos fechas, quitarla → GREEN (deben pasar con T1 y T2; si alguna falla, corregir la ruta antes de seguir) → REFACTOR
- **Satisfies:** `@deduced` de sesión y CSRF; el `@stated` de registrar, terminar y quitar de punta a punta
- **Mold:** `tests/test_web_cuidados.py` (pruebas de sesión y CSRF de riegos) y `tests/test_recorrido_coleccion.py` (recorrido de riegos)
- **Verify:** ninguna escritura de floraciones sucede sin sesión ni token — forced mutations: quitar `Depends(exigir_sesion)` de `FastAPI(...)` (las pruebas de sesión fallan); desactivar la comparación del token en `exigir_sesion`; quitar `{% include "_csrf.html" %}` del formulario de registrar (el recorrido falla); then `uv run pytest tests/test_web_cuidados.py tests/test_recorrido_coleccion.py tests/test_web_proteccion.py -q` y `./scripts/check`
- **Commit:** test(cuidados): sesión, CSRF y recorrido de las floraciones de punta a punta

### T4 · Manual integration test

- Con `uvicorn` real (`ORQUIDEA_DB`/`ORQUIDEA_FOTOS` en una carpeta temporal, `ORQUIDEA_COOKIE_SEGURA=0`, contraseña por `ORQUIDEA_PASSWORD_HASH`): entrar, agregar un ejemplar, registrar una floración en curso y otra terminada, terminar la primera, probar un fin anterior, una fecha futura y el escape, quitar una y comprobar la ficha; después llenar un ejemplar con 500 riegos y 500 floraciones en curso por SQL y anotar el tamaño real de la ficha (sin comprimir y gzip). Apagar el servidor por PID (memoria del proyecto).
- **Verify:** con la aplicación corriendo, la ficha muestra el historial, rechaza lo inválido con el mensaje y responde con `Cache-Control: no-store` y la CSP; la cifra de la ficha llena queda anotada en la retrospectiva (s4.6 decide el presupuesto).

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 — T1 es el esqueleto y toca la firma compartida de `ficha`; T2 el IDOR y la transición; T3 cierra seguridad y el recorrido.
- **Dependencies:** secuencial.
- **Risks:** cambiar `fecha` por `valores` en `ficha` puede romper `registrar_riego` y sus pruebas → se cambia en T1 con la suite de riegos como red; `test_web_rutas.py` falla al añadir rutas → se actualiza en T1 y T2; la ficha con 500 y 500 puede pesar mucho → se anota en T4 y lo decide s4.6; el valor devuelto en los campos es entrada del usuario → escape de Jinja y prueba con `"><script>`.
