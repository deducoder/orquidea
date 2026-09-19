# Parking lot

Named findings that were not opened. Append-only; each entry belongs to whoever
wrote it. Retirement moves an entry to `## Retired` with its reason.

## Open items

- **Binding de seguridad sin definir.** No hay escáner declarado ni forma de
  pasarle el alcance, así que no existe `conventions/security/instance.md`; el
  primer `security-review` se detendrá sin él.
  *Origin:* project-create, 2026-09-19 — el equipo decidió definirlo cuando se
  necesite.
  *Promotion:* antes del primer `security-review`: elegir escáner y forma de
  alcance, o registrar `none` con un ADR aceptado.
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

## Retired
