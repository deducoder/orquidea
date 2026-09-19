# Epic e2: Personal collection with login — Scope

## Objective

Un coleccionista inicia sesión en su aplicación y lleva ahí el registro de los ejemplares que posee, cada uno ligado a su especie del catálogo (con sus cuidados a un clic) o con nombre propio cuando la planta no está en el catálogo.

**Value:** el catálogo de e1 deja de ser solo consulta y se vuelve la base de un registro personal protegido; se desbloquea la versión 0.2 (fotos, riegos y floraciones), que cuelga de los ejemplares.

## Stories

| ID | Story | Size | Description |
|----|-------|:----:|-------------|
| s2.1 | Persistencia con migraciones | S | Módulo de datos con `sqlite3`, migraciones numeradas por `PRAGMA user_version` y ruta de la base por `ORQUIDEA_DB` (ADR-003). |
| s2.2 | Inicio y cierre de sesión | M | Formulario de acceso con contraseña única (hash scrypt en el entorno), sesión en el servidor, cookie segura, límite de intentos y orden que genera el hash (RF-08, ADR-004); la fixture de `app.state.catalogo` pasa a `tests/conftest.py`. |
| s2.3 | Proteger todas las rutas | S | Toda ruta salvo el acceso, `/salud` y `/static` exige sesión; CSRF en todo `POST`; cabeceras de seguridad (RF-08, `should-security-002`). |
| s2.4 | Agregar ejemplares del catálogo y verlos | M | Botón "Agregar a mi colección" en la ficha y página "Mi colección" que lista los ejemplares con enlace a su ficha; varios ejemplares de la misma especie son independientes (RF-04). |
| s2.5 | Ejemplares fuera del catálogo | S | Agregar un ejemplar sin especie de catálogo, con nombre y notas (RF-04). |
| s2.6 | Editar y quitar ejemplares | S | Editar nombre y notas de un ejemplar y quitarlo, con confirmación (RF-04). |
| s2.7 | Configuración de despliegue con persistencia | S | `Dockerfile` y guía con volumen para la base, variables de entorno y la orden del hash; la colección sobrevive a un redespliegue. |

Dependencias: s2.2 de s2.1; s2.3 de s2.2; s2.4 de s2.1 y s2.3; s2.5 y s2.6 de s2.4; s2.7 de s2.2. Sin ciclos.

## In scope

- **MUST:** contraseña única y sesión (RF-08); toda ruta protegida salvo acceso, `/salud` y `/static`; ejemplares ligados a una especie del catálogo o con nombre propio, agregados, editados, quitados y listados (RF-04); la colección persiste entre reinicios y redespliegues; CSRF en todo `POST`; línea base de seguridad razonable para un login (`should-security-002`).
- **SHOULD:** límite de intentos de acceso; cabeceras de seguridad; parte de la fixture web unificada (parking lot).

## Out of scope

- Registro de usuarios y varias cuentas — no-go del brief (RF-08) — **never** en esta versión.
- Recuperación de contraseña por correo — no-go del brief (system-context) — **never** mientras no haya sistemas externos.
- Fotos, riegos y floraciones (RF-05 a RF-07) — no-go del brief, pertenecen a la versión 0.2.
- Buscar, filtrar u ordenar dentro de "Mi colección" — no lo pide ningún RF; una colección personal es corta — **not now**: si el volumen lo pide, épica futura.
- Importar o exportar la colección (por ejemplo desde una hoja de cálculo) — no lo pide ningún RF — **not now**.
- Cambiar la contraseña desde la interfaz — se cambia la variable de entorno (ADR-004) — **not now**.
- Despliegue efectivo al VPS — depende del humano y sigue pendiente desde e1 — **not now**, ver Risks.

## Done when

- [stated] Tras iniciar sesión, agregar un ejemplar del catálogo y verlo en "mi colección" (métrica líder del brief), demostrado por una prueba de extremo a extremo y por el recorrido manual de `story-implement`.
- [stated] El usuario registra toda su colección real, incluidas plantas fuera del catálogo, sin otra herramienta (métrica rezagada del brief). Solo el humano puede confirmarla, con la aplicación desplegada y sus plantas reales: **stop previsible** (P4 en `epic-review`).
- [deduced] Sin sesión, toda ruta —salvo el formulario de acceso, `/salud` y `/static`— redirige al acceso o responde 401/403 (RF-08, contrato del system-design).
- [deduced] Se pueden tener varios ejemplares de la misma especie, cada uno independiente; un ejemplar sin especie de catálogo lleva nombre y notas; se puede editar y quitar (RF-04).
- [deduced] La colección persiste entre reinicios del proceso y sobrevive a un redespliegue cuando la base está en el volumen configurado.
- [deduced] La contraseña no se guarda en claro, la sesión se invalida al cerrar, todo `POST` exige token CSRF y las cookies son `HttpOnly` y `SameSite` (`should-security-002`, ADR-004).
- [deduced] Toda consulta a la base es parametrizada (ADR-003).
- [stated] All stories complete · docs updated · retrospective done

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| El criterio rezagado del brief y la medición de `must-perf-001` con "Slow 3G" dependen del humano, de la aplicación desplegada y de un navegador con herramientas de desarrollo; e1 los descubrió tarde | H | M | Previstos desde aquí como stop P4 en `epic-review`; el peso en bytes se mide por script en cada historia web y la parte del humano se pide al cierre de la épica |
| Un error en el código propio de autenticación, sesión o CSRF abre la colección a un tercero | M | H | Historias s2.2 y s2.3 con pruebas de comportamiento adverso (sesión inválida, CSRF ausente, fuerza bruta); `security-review` en cada historia contra ASVS L2 |
| La base o el secreto no llegan al VPS: sin volumen la colección se pierde al redesplegar; sin `ORQUIDEA_PASSWORD_HASH` nadie entra | M | H | s2.7 documenta volumen y variables y la aplicación falla cerrada; configurar el VPS es del humano, previsto como stop P5 si hay que actuar allá |
| Proteger todas las rutas rompe las pruebas web de e1, que no tienen sesión | H | L | s2.2 mueve la fixture a `conftest.py` con un cliente autenticado; s2.3 actualiza las pruebas existentes en el mismo cambio |
