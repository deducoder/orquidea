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

## Retired

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
