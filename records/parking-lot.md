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

## Retired

### 2026-09-19 · direct fix (resuelto al preparar la orquestación de 0.1.0, antes de que existiera la historia de e1 que iba a llevarlo) · Binding de seguridad sin definir
**Why:** la entrada se unió a la versión 0.1.0 y se resolvió de inmediato: el humano eligió Bandit y `conventions/security/instance.md` quedó escrito y verificado en vivo.
**Swept:** `work/epics/e1-species-catalog/brief.md` (Appetite) la cita como parte de e1; el apetito sigue siendo válido con una historia menos, y el brief no se reescribe (lo escribió epic-start). Nada más la cita.

### 2026-09-19 · s2.2 · La fixture de `app.state.catalogo` está repetida en las pruebas web
**Why:** la promoción se cumplió: s2.2 fue la primera historia de e2 con pruebas web y movió la fixture a `tests/conftest.py` (`client`, que además usa una base temporal); las dos copias se borraron.
**Swept:** `work/epics/e1-species-catalog/retrospective.md` la cita como recomendación de `quality-review`; es un registro histórico y no se reescribe. El scope, el diseño y la retrospectiva de s2.2 la citan como resuelta. Nada más la cita.
