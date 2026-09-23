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
- **En gemba-design 0.21.0, `design-md.py` solo acepta referencias ASCII (`^\{([a-z][A-Za-z0-9.-]*)\}$`), y el spec de DESIGN.md (`alpha`) no lo exige.** Un componente con `{colors.acción-fondo}` sale `refused` (exit 1). En Orquídea se resolvió con identificadores ASCII (ADR-014): `semantics.md` usa `linea` y `accion-*`. El límite del generador, más estrecho que el formato, es del addon: aceptar las letras de un identificador YAML, o decir en la técnica `ui` que los identificadores de rol van en ASCII antes de que un eslabón los fije.
  *Origin:* s5.6 (e5), `story-design`, 2026-09-22 — lectura de `design-md.py` contra los roles de `semantics.md`.
  *Promotion:* al reportarlo en el repositorio de gemba-design, o cuando una versión del addon lo corrija; en Orquídea no hace falta deshacer nada.

- **La interfaz vestida de e5 tiene tres juicios sin firmar y dos ajustes visuales sin decidir.**
  - Sin firma (`unsigned`): el criterio 3 de ADR-009 (la foto es la protagonista: a todo el ancho en la ficha, miniatura de 96 px en la colección) y si el subtítulo de 20 px en negrita se distingue del cuerpo (ADR-015, decisión 5).
  - Sin decidir: los enlaces con `accion` quedan 8 px hacia adentro del texto por el relleno de `enlace-navegacion`, y en Acceso el botón "Entrar" queda pegado al campo porque ese formulario no envuelve sus controles en `<p>`.

  Se preguntó al cerrar T5 de s5.7 y el humano pidió cerrar sin responder. Las capturas a 360 px quedaron en el scratchpad de esa sesión, no en el repositorio.
  *Origin:* s5.7 (e5), `story-implement` T5, 2026-09-23 — recorrido renderizado.
  *Promotion:* cuando el humano recorra la aplicación en el teléfono (el mismo momento que la medición en "Slow 3G" que queda pendiente de e5): firma o rechazo de los dos juicios. Un ajuste que se decida hacer va como arreglo propio contra ADR-015.

## Retired

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
