# Epic e2: Personal collection with login — Retrospective

## Summary

Un único usuario inicia sesión con su contraseña y lleva su colección de orquídeas: agrega ejemplares ligados a una especie del catálogo (con los cuidados a un clic) o con nombre y notas propios, los edita y los quita. Toda la aplicación exige sesión por defecto (cookie `__Host-` `HttpOnly`/`SameSite=Lax`/`Secure`, sesión en el servidor con caducidad, CSRF en todo `POST`, cabeceras de seguridad, límite de intentos). La colección vive en SQLite con migraciones numeradas y la imagen la guarda en un volumen. Siete historias, dos ADR (ADR-003 persistencia con `sqlite3`, ADR-004 autenticación) y una guía de despliegue con todas las variables de entorno.

## Metrics

- Stories: 7 (s2.1 a s2.7) · Estimated: S, M, S, M, S, S, S · Actual: S, M, S, M, S, M, S (solo s2.6 creció, de S a M, por generalizar el formulario y la validación).
- 249 pruebas (52 heredadas de e1), `./scripts/check` en verde, una dependencia nueva (`python-multipart`), 6 entradas nuevas en el parking lot y 1 retirada.
- Surgió a mitad de la épica y no estaba planeado: dos defectos entre historias, hallados en `epic-review` y corregidos con prueba (`fix(web)`), y la corrección en `s2.2` de dos huecos ASVS (prefijo `__Host-`, registro de accesos) que el diseño no había listado.
- Sin despachos: ninguna historia llevó `dispatch.md`, por lo que no hubo miembro que plantar ("none dispatched").

## Scope verification

Cada elemento de "In scope" y "Done when" de `scope.md`, releído contra el código:

- **MUST — contraseña única y sesión (RF-08)** → **Fulfilled**: `src/orquidea/autenticacion.py`, `src/orquidea/datos/sesiones.py`, rutas `/acceso` y `/salir` en `src/orquidea/web/app.py`; `test_autenticacion.py`, `test_datos_sesiones.py`, `test_web_acceso.py`.
- **MUST — toda ruta protegida salvo acceso, `/salud` y `/static`** → **Fulfilled**: `exigir_sesion` global y `RUTAS_PUBLICAS` en `app.py`; `test_web_proteccion.py` enumera `app.routes` y comprueba que una ruta nueva nace protegida.
- **MUST — ejemplares con o sin especie de catálogo, agregados, editados, quitados y listados (RF-04)** → **Fulfilled**: `src/orquidea/coleccion/modelo.py`, `src/orquidea/datos/ejemplares.py`, rutas de `/coleccion` en `app.py`; `test_web_coleccion.py`, `test_datos_ejemplares.py`, `test_coleccion_modelo.py`.
- **MUST — la colección persiste entre reinicios y redespliegues** → **Fulfilled con reserva**: persiste entre reinicios (probado con `uvicorn` real y con el wheel en un entorno limpio, migración nueva aplicada sola); el volumen de la imagen (`Dockerfile`, `VOLUME /data`) tiene pruebas de configuración pero la imagen **no se construyó** (sin daemon de Docker), diferido por el humano.
- **MUST — CSRF en todo `POST`; línea base de seguridad razonable (`should-security-002`)** → **Fulfilled**: `exigir_sesion`, cabeceras en `cabeceras_de_seguridad`; Bandit sin hallazgos en `src/`; ASVS recorrido por historia.
- **SHOULD — límite de intentos; cabeceras; fixture unificada** → **Fulfilled**: `LimiteDeIntentos`, middleware, `tests/conftest.py` (entrada del parking lot retirada).
- **[stated] tras iniciar sesión, agregar un ejemplar del catálogo y verlo en "mi colección"** → **Fulfilled**: `tests/test_recorrido_coleccion.py` (contraseña real, ficha del catálogo real, token del propio formulario, colección, reabrir la base) y prueba manual con `uvicorn`.
- **[stated] el usuario registra toda su colección real, incluidas plantas fuera del catálogo, sin otra herramienta** → **Not fulfilled** por lo que el código puede demostrar; diferido por el humano ("a — diferir todo y dejar que e2 cierre": `decisions.md`, entrada Answered de `epic-review`). Lo que el código sí cubre: agregar del catálogo y fuera del catálogo, editar, quitar y persistir. Lo que falta: el despliegue en el VPS y las plantas reales.
- **[deduced] sin sesión toda ruta salvo las públicas redirige o responde 401/403** → **Fulfilled** (`test_web_proteccion.py`).
- **[deduced] varios ejemplares de una especie independientes; sin especie con nombre y notas; se edita y quita** → **Fulfilled** (`test_web_coleccion.py`, mutaciones sobre `WHERE id = ?`).
- **[deduced] la colección persiste entre reinicios y sobrevive a un redespliegue con el volumen** → **Fulfilled con la misma reserva** (Docker no verificado).
- **[deduced] contraseña no en claro, sesión invalidada al cerrar, CSRF, cookies `HttpOnly`/`SameSite`** → **Fulfilled** (`test_autenticacion.py`, `test_web_acceso.py`, `test_web_proteccion.py`).
- **[deduced] toda consulta parametrizada** → **Fulfilled**: única interpolación en `datos/base.py` (un entero derivado de un nombre de migración validado); `ruff` (S608) lo vigila.
- **[stated] all stories complete · docs updated · retrospective done** → historias y retrospectiva hechas; `docs.md` lo escribe `epic-close`.
- **Guardia `must-perf-001` (verificación manual en `epic-review`)** → **Parcial, diferida por el humano**: peso medido (primera carga `/acceso` 351 B + htmx 16,352 B con gzip, muy por debajo de 200 KB; `/especies` con 100 especies 2,055 B con gzip); tiempo con "Slow 3G" y CSP frente a htmx no verificados (necesitan un navegador).

No hay compromisos de eliminación en el alcance.

## What went well

- Decidir ADR-003 y ADR-004 en el diseño de la épica (no dentro de una historia) dejó a las siete historias apoyándose en contratos ya escritos; ninguna reabrió la persistencia ni la autenticación.
- Aislar primero el código criptográfico y de sesión (s2.2), luego cerrar la puerta a todo (s2.3) y solo entonces guardar datos del usuario (s2.4 en adelante) hizo que ningún dato de la colección existiera sin protección.
- Convertir la regla de arquitectura "toda ruta exige sesión" en una prueba que enumera `app.routes` (s2.3) protegió automáticamente cinco rutas nuevas de s2.4 a s2.6 sin tocarla.
- Las mutaciones sistemáticas (cada propiedad de cada plan) encontraron pruebas que no mordían en cada historia; la lista de escapes por contexto (atributo, texto, `<textarea>`) y el aislar el `<form>` concreto se volvieron reflejos.

## What to improve

- Los dos defectos de `epic-review` (registro con `uvicorn`, verificaciones scrypt en paralelo) vivían en s2.2 y las pruebas unitarias de esa historia los dejaron pasar: las pruebas usaban `caplog` y un solo hilo. Probar comportamiento de **ejecución** (proceso real, concurrencia) en las historias de seguridad, no solo la lógica.
- ASVS se recorrió en la revisión de s2.2 y en el diseño desde s2.3; hacerlo en el diseño desde la primera historia de seguridad habría ahorrado un commit no planeado (ya en memoria).
- Un criterio `[stated]` dependiente del humano se previó desde el diseño (lección de e1) y aun así costó un stop; es el costo esperado y se avisó, pero se podría haber pedido la respuesta al terminar el diseño para no esperar al final.
- `docker build` sigue sin verificarse en dos épicas seguidas: dejar de posponerlo como precondición del primer despliegue.

## Learned

1. About the system: en FastAPI las rutas síncronas corren en un pool de hilos y scrypt libera el GIL: cualquier estado compartido (contador de intentos, verificación costosa) necesita un cerrojo; uvicorn solo configura sus propios registros, así que el `INFO` de un registro propio se pierde sin un manejador; una dependencia global de sesión corre antes de validar los parámetros de ruta y deja las rutas nuevas protegidas por defecto.
2. About the process: los defectos entre historias solo aparecen al leer el rango completo con el proceso real en marcha; el `epic-review` pagó su costo (dos correcciones con prueba). Las pruebas de deriva pequeñas (nombres de variables, Dockerfile) son baratas y evitan olvidos entre código, imagen y guía.
3. Capability gained: una colección personal protegida y persistente (RF-04 y RF-08 completos), una base con migraciones que crece sin perder datos, una fixture web con base temporal y sesión, y una guía de despliegue con volumen, variables y generación del hash.
