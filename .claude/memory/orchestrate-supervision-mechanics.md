---
name: orchestrate-supervision-mechanics
description: Cómo supervisar orchestrate en este harness — nombre de la sesión bg, avisos de inactividad y push al teléfono
metadata:
  type: project
---

Al lanzar `claude --bg "/gemba-code:orchestrate run eN"`, la sesión aparece primero con el prompt como nombre (con `/`, no direccionable) y ~15 s después se renombra; `SUPERVISOR eN` se envía al nombre de `claude agents --json`, no al inicial.

**Why:** los envíos al nombre con `/` fallaron; el aviso `notify_when_idle` re-suscrito sobre una sesión ya inactiva se dispara al instante y duplica avisos.
**How to apply:** esperar al renombre antes de presentarse; para esperar el cierre usar un bucle en segundo plano sobre `docs.md`/roadmap/push, no re-suscripciones. El push al teléfono no sale mientras la terminal supervisora está activa, así que el binding de notificaciones no se puede verificar desde una sesión atendida.
