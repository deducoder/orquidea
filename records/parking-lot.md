# Parking lot

Named findings that were not opened. Append-only; each entry belongs to whoever
wrote it. Retirement moves an entry to `## Retired` with its reason.

## Open items

- **Push al teléfono sin verificar.** `conventions/notifications/instance.md`
  declara push por Remote Control, pero la prueba del 2026-09-19 no llegó al
  teléfono porque Remote Control estaba inactivo.
  *Origin:* project-create, 2026-09-19 — prueba en vivo del binding.
  *Promotion:* la primera sesión con Remote Control activo, o antes del primer
  `delegate`/`orchestrate`: repetir la prueba y actualizar `## Last verified`.
- **Fertilización y notas por fecha en el seguimiento.** El seguimiento de
  ejemplares cubre riegos y floraciones (RF-06, RF-07); fertilización y notas
  libres fechadas quedaron fuera.
  *Origin:* project-create, 2026-09-19 — acotado del seguimiento básico.
  *Promotion:* cuando se planee la siguiente versión después de la primera
  entrega.
- **Bandit reporta B101 en `tests/`.** El binding de seguridad escanea todos los `.py` cambiados, pruebas incluidas, y Bandit marca cada `assert` (B101, severidad baja); ruff ya lo ignora en `tests/` (`per-file-ignores`). Cada `security-review` de historia arrastra ese ruido.
  *Origin:* s1.1 (e1), `security-review` 2026-09-19 — 7 hallazgos B101, todos en `tests/test_web_inicio.py`.
  *Promotion:* cuando el ruido oculte un hallazgo real, o al actualizar `conventions/security/instance.md` (por ejemplo excluyendo `tests/` o saltando B101).
- **La ficha repite fuentes largas por cada cuidado.** Con el catálogo semilla, cada uno de los cuatro cuidados imprime la cita completa de su fuente (URL, fecha y aclaración de que es del género), lo que hace larga y repetitiva la ficha.
  *Origin:* s1.6 (e1), prueba manual con el catálogo real, 2026-09-19.
  *Promotion:* cuando se revise el diseño de la ficha, o si un usuario la encuentra difícil de leer; una salida sería numerar las fuentes de la especie y referirlas por número.
- **`orquidea.datos.catalogo` (módulo) y `datos/catalogo/` (directorio de datos) comparten nombre.** No chocan al importar (el módulo tiene prioridad), pero se prestan a confusión.
  *Origin:* e1, `epic-close` (architecture-review a escala de épica), 2026-09-19.
  *Promotion:* si alguien tropieza con ello, o al añadir otro módulo de datos; renombrar el directorio de datos, con un ADR nuevo que sustituya el punto 2 de ADR-002.
- **`docker build` y `docker run` sin verificar (dos épicas seguidas).** El cliente de Docker existe en esta máquina pero el daemon no responde, así que ni el `Dockerfile` de e1 ni el volumen de e2 se han construido. El wheel sí se verificó en un entorno limpio.
  *Origin:* s2.7 (e2), `story-review`, 2026-09-19 — prueba manual del empaquetado.
  *Promotion:* la primera sesión con Docker Desktop en marcha, o el primer despliegue del humano: construir la imagen, arrancarla con `-v` y `ORQUIDEA_PASSWORD_HASH`, y comprobar `/salud`, el acceso y que la colección sobrevive a recrear el contenedor.
- **Varias subidas simultáneas del tamaño máximo pueden agotar la memoria de un VPS pequeño.** Con el arreglo de `procesar_foto` (reducir antes de copiar) una foto de 48 MP pica en ~280 MB (JPEG, PNG RGB) y ~430 MB (PNG RGBA); una de 64 MP (el tope), ~360 y ~570 MB. Un solo usuario rara vez sube en paralelo, pero tres PNG RGBA grandes a la vez pasarían de 1,5 GB.
  *Origin:* e3, `epic-review` (medición del pico de memoria con un proceso aparte), 2026-09-19.
  *Promotion:* al desplegar en un VPS de 1 GB o menos, o si el proceso muere por OOM: bajar `PIXELES_MAXIMOS` o serializar `procesar_foto` con un semáforo (una foto a la vez).
- **Las miniaturas no se cachean y se piden en cada visita a "Mi colección".** El middleware pone `Cache-Control: no-store` a todo salvo `/static`; con 25 fotos son ~130 KB en cada visita, y la URL por id no cambia aunque cambie la foto.
  *Origin:* e3, `epic-review`, 2026-09-19 — resultado de `scripts/medir-primera-carga.py`.
  *Promotion:* si la lista se siente lenta con la colección real: servir las imágenes con `Cache-Control: private, max-age` y una URL que incluya el nombre aleatorio de la foto (cambia al reemplazarla).
- **La aplicación no comprime sus respuestas: el presupuesto de peso depende del proxy.** La ficha con 500 riegos y 500 floraciones en curso pesa 500 476 bytes sin comprimir y 14 459 en gzip (medido con `uvicorn` real); `must-perf-001` se cuenta en gzip "como lo serviría un proxy" (decisión de e3), pero la aplicación no lleva `GZipMiddleware` y no se ha verificado que el proxy de Dokploy comprima.
  *Origin:* e4, `story-implement` de s4.4 (medición de la ficha llena), 2026-09-19; documentado en el README por s4.6.
  *Promotion:* al verificar el despliegue real (mismo momento que la entrada de `docker build`): si el proxy no comprime, añadir `GZipMiddleware` (o la compresión del proxy) con un ADR; o si la lista o la ficha se sienten lentas con datos reales.
- **Quitar `'unsafe-inline'` de `style-src` en la CSP.** Hoy la CSP lo permite porque cuatro plantillas llevan atributos `style`; s5.7 (e5) los mueve a `identidad.css`, y desde entonces ya nada lo necesita. Quitarlo toca `CONTENT_SECURITY_POLICY` en `web/app.py` y la prueba `test_la_csp_no_permite_scripts_en_linea`, que hoy afirma su presencia; htmx inyecta estilos en línea para sus indicadores salvo que se configure `htmx.config.includeIndicatorStyles = false`, y eso hay que comprobarlo antes.
  *Origin:* e5, `epic-design`, 2026-09-22 — recorrido de las plantillas y de la CSP.
  *Promotion:* al cerrar s5.7, si ninguna plantilla conserva un atributo `style`: una historia o arreglo con su prueba de CSP y la comprobación de htmx.
- **En gemba-design 0.21.0, la plantilla `semantics.md` de la técnica `ui` pide una columna `Variant`, pero `invariance.py` no acepta `—` en ella.** Con una identidad sin variante (Orquídea, ADR-012), la columna llena de `—` hace que `invariance.py` salga con 2 por `unreadable variant value '—'`, no por `no subject`. Solo sale "sin sujeto" cuando la tabla no trae columna `Variant`, y eso contradice la plantilla. En `governance/identity/ui/semantics.md` se quitó la columna y se explicó por qué. `palette.md` conserva su columna con `—`, que ningún eslabón pasa por `invariance.py`. El arreglo es del addon: tratar una columna de variante vacía o con `—` como "sin sujeto", o que la plantilla diga que se omite. No es de Orquídea.
  *Origin:* s5.5 (e5), `story-implement` T3 y `survival-review`, 2026-09-22 — salida de `invariance.py governance/identity/ui/semantics.md texto fondo`.
  *Promotion:* al reportarlo en el repositorio de gemba-design, o cuando una versión del addon lo corrija: entonces se vuelve a poner la columna en `semantics.md` si la plantilla lo sigue pidiendo.
- **El tiempo de la primera carga con "Slow 3G" (`must-perf-001`, ≤ 5 s) no se ha medido nunca: e1, e2, e3 y e5 lo difirieron.** El peso sí se mide por script en cada épica. En e5: "Mi colección" con 25 fotos, 148.1 KB de 200, e identidad 1.6 KB de 50. El 2026-09-23 el servidor quedó listo para medir, con 25 ejemplares con foto, y el humano pidió cerrar sin medir.
  *Origin:* e5, `epic-review`, 2026-09-23 — stop previsto desde el diseño de e5, diferido por el humano como en e1–e3.
  *Promotion:* el primer despliegue real en Dokploy (el mismo momento que la entrada de `docker build`): medir en el teléfono o con DevTools en "Slow 3G" contra el servidor desplegado. Si pasa de 5 s, es un bug contra `must-perf-001`.
- **Tres scripts de `scripts/` tienen cada uno su lector de tablas markdown:** `contraste-de-lectura.py` (`tablas`/`filas`), `derivar-primitivas.py` (`_roles_de`) y `comprobar-medidas.py` (`_filas`), además de los de las pruebas. Cada uno encuentra la tabla por la primera celda de la cabecera, con diferencias pequeñas (quitar comillas invertidas, filas separadoras). Son scripts sueltos cargados por ruta, y compartir el lector exige un módulo común y manejo de `sys.path`, un costo que hoy no se paga con tres usos.
  *Origin:* e5, `epic-close` (architecture-review a escala de épica), 2026-09-23.
  *Promotion:* un cuarto script que lea tablas, o un defecto que aparezca en un lector y no en los otros.
- **`precedence.py` (gemba-design 0.23.0) no puede juzgar un eslabón que se vuelve a correr contra un registro nuevo.** Compara la última edición `add`/`update` de cada registro citado con el **primer** commit de la pieza, el que la creó. En s1, `semantics.md` y `components.md` citan ADR-016, pero nacieron en e5: el veredicto es `FAIL — not before the piece: ADR-016` aunque el registro precede a toda tarea de s1. La técnica `ui` pide volver a correr el eslabón en el mismo archivo ("a change upstream is re-run downstream"), así que el caso es el esperado, no uno raro. El arreglo es del addon: comparar contra el primer commit que tocó la pieza después del `add` del registro, o juzgar por registro en lugar de por archivo.
  *Origin:* s1, `story-implement` (antes de completar ADR-016), 2026-09-23 — `precedence.py check governance/identity/ui/components.md`.
  *Promotion:* al reportarlo en el repositorio de gemba-design, o cuando una versión del addon lo corrija. Mientras tanto, la revisión lo lee a mano y lo dice.
- **La técnica `adr` (gemba 0.23.0) solo sabe sustituir un registro entero.** ADR-016 reemplaza decisiones sueltas de ADR-013, ADR-014 y ADR-015 (identificadores ASCII, el hueco de bordes, `height`/`width` como mínimo, esquinas sin token). Marcar los tres como `superseded by ADR-016` diría que caen enteros, y no es así. Se dejaron `accepted`, y ADR-016 nombra cada decisión que reemplaza. Quien lea ADR-014 no ve que su decisión 6 ya no rige.
  *Origin:* s1, `story-design`, 2026-09-23 — decidido por el humano con la recomendación del diseño.
  *Promotion:* al reportarlo al método, o si una lectura de ADR-013 a ADR-015 aplica una decisión reemplazada.

## Retired

### 2026-09-23 · s1 · El gate no ataba la cadena de la identidad entre `semantics.md`, `primitives.md` y `DESIGN.md`
**Why:** se cumplió la promoción ("la siguiente historia que toque `governance/identity/ui/`"). `test_la_cadena_de_colores_esta_atada` (`tests/test_identidad_ui.py`) comprueba que cada rol de `semantics.md` valga lo que su escalón en `primitives.md`, en la tabla `Role` y en la `Token`, y que los colores de `DESIGN.md` sean esos mismos 13 roles. Se vio en rojo con la mutación de la entrada (`acción-fondo` a `#1F3A60` en `semantics.md`). Reusa el lector `_filas` de `comprobar-medidas.py`: no suma un lector de tablas.
**Swept:** la citan el `plan.md` de s1 (T9), que la resuelve, y la retrospectiva de e5, registro histórico que no se reescribe. Nada más la cita.

### 2026-09-23 · s1 · La interfaz vestida de e5 tenía dos juicios sin firmar y dos ajustes sin decidir
**Why:** s1 la tomó en su alcance. Los dos juicios los firmó Daniel Efraín Domínguez Urbina el 2026-09-23, sobre capturas a 360 px con fotos reales: el criterio 3 de ADR-009, sí, y la decisión 5 de ADR-015, sí. Los dos ajustes se decidieron en ADR-016: los enlaces `accion` sin sangría y el campo de Acceso en su propio párrafo. La entrada pedía que un ajuste fuera un arreglo propio contra ADR-015; el humano lo juntó en s1.
**Swept:** la citan como pendiente la retrospectiva de e5, el `scope.md` de s5.7 y el handoff `work/sessions/2026-09-23-e5-closed.md`: son registros históricos y no se reescriben. El `scope.md`, el `plan.md`, `components.md` y ADR-016 de s1 la resuelven. Nada más la cita.

### 2026-09-23 · s1 · `design-md.py` de gemba-design 0.21.0 solo aceptaba referencias ASCII
**Why:** se cumplió la promoción ("cuando una versión del addon lo corrija"). El generador de 0.23.0 acepta letras de cualquier escritura, y s1 renombró los tokens a `línea` y `acción-*` (ADR-016, que reemplaza la decisión 6 de ADR-014).
**Swept:**
- Registros históricos que no se reescriben: el `design.md` de s5.6, la retrospectiva de e5 y `work/epics/e5-visual-identity/docs.md:95`. Este último es la documentación de e5 y describe el límite como vigente; es de `epic-close`, y cambiarlo aquí rompería la regla de un solo escritor.
- La memoria `design-md-py-que-lee` decía "solo acepta referencias ASCII": se corrige en esta misma historia.
- El `scope.md` y el `plan.md` de s1 la resuelven.

### 2026-09-23 · s5.7 (e5) · Ninguna prueba afirmaba el `<title>` de las páginas salvo el de inicio
**Why:** se cumplió la promoción ("s5.7, que toca todas las plantillas"). `tests/test_web_titulos.py` recorre las nueve páginas GET que devuelven HTML y afirma que su `<title>` es texto. Cuenta su cobertura contra `rutas_registradas`, así que una página nueva sin título probado la pone en rojo. Se vio en rojo con el bloque `title` de `especies.html` en la forma de b1.
**Swept:** citan la entrada el `scope.md` y el `design.md` de s5.7, que la resuelven. También la citan la retrospectiva de b1 (`work/bugs/b1-collection-title-shows-markup/retrospective.md:16`, "aparcada, con promoción en s5.7") y el handoff `work/sessions/2026-09-22-e5-identity-decided.md`: los dos son registros históricos y no se reescriben. Nada más la cita.

### 2026-09-19 · s3.6 (e3) · Las cifras de la guía de despliegue estaban escritas a mano
**Why:** la promoción se cumplió ("cuando la guía crezca"): s3.6 amplió la guía con las fotos y añadió en `tests/test_despliegue.py` una prueba que importa las constantes (foto máxima, ancho, lado de la miniatura, cuerpo máximo, duración y inactividad de la sesión, intentos y bloqueo) y falla si la guía ya no dice la misma cifra; con una constante cambiada a propósito, la prueba se pone en rojo.
**Swept:** `work/epics/e2-personal-collection-with-login/stories/s2.7-deployment-persistence-config/retrospective.md` la cita como recomendación ("también en el parking lot"); es un registro histórico y no se reescribe. El scope y el diseño de s3.6 la citan como resuelta por esa historia. Nada más la cita.

### 2026-09-19 · s3.1 (e3) · `orquidea/web/app.py` reunía todas las rutas, la sesión, las cabeceras y el ciclo de vida
**Why:** la promoción se cumplió: s3.1 fue la primera historia de 0.2 que tocó las rutas y dividió `app.py` en `web/sesion.py`, `web/plantillas.py` y un `APIRouter` por área en `web/rutas/`; `app.py` quedó en 74 líneas.
**Swept:** `work/epics/e3-specimen-photos/brief.md` (Appetite) la cita como parte de la épica y sigue siendo válida; el brief no se reescribe (lo escribió `epic-start`). El scope y el diseño de la épica y de s3.1 la citan como resuelta por s3.1. `work/epics/e2-personal-collection-with-login/retrospective.md` y `docs.md` describen la estructura de e2, cuando `app.py` reunía todo; son registros históricos y no se reescriben; la documentación de desarrollador al día es de `epic-close`. Nada más la cita.

### 2026-09-19 · direct fix (resuelto al preparar la orquestación de 0.1.0, antes de que existiera la historia de e1 que iba a llevarlo) · Binding de seguridad sin definir
**Why:** la entrada se unió a la versión 0.1.0 y se resolvió de inmediato: el humano eligió Bandit y `conventions/security/instance.md` quedó escrito y verificado en vivo.
**Swept:** `work/epics/e1-species-catalog/brief.md` (Appetite) la cita como parte de e1; el apetito sigue siendo válido con una historia menos, y el brief no se reescribe (lo escribió epic-start). Nada más la cita.

### 2026-09-19 · s2.2 · La fixture de `app.state.catalogo` está repetida en las pruebas web
**Why:** la promoción se cumplió: s2.2 fue la primera historia de e2 con pruebas web y movió la fixture a `tests/conftest.py` (`client`, que además usa una base temporal); las dos copias se borraron.
**Swept:** `work/epics/e1-species-catalog/retrospective.md` la cita como recomendación de `quality-review`; es un registro histórico y no se reescribe. El scope, el diseño y la retrospectiva de s2.2 la citan como resuelta. Nada más la cita.
