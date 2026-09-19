# Notifications — Instance binding

> Lo que este proyecto responde a `delegate` y `orchestrate` cuando un bloque
> delegado termina y alguien tiene que enterarse. Son hechos de esta
> instancia, no una regla genérica: por eso este archivo vive en el proyecto y
> no en el plugin.

- **Channel:** notificación push al teléfono a través de Remote Control de
  Claude Code. **Sin verificar**: ver `## Last verified`.
- **How a message reaches it:** la herramienta de notificación push de la
  sesión de Claude Code; con Remote Control activo, además de la notificación
  de terminal llega al teléfono.
- **What is pushed:** un resumen al final de cada bloque delegado (qué terminó,
  qué falló). El avance rutinario no se envía.
- **When it sends nothing:** el trabajo continúa; el resumen queda en la
  terminal de la sesión.

## Last verified

2026-09-19: se envió un mensaje de prueba desde la sesión. La notificación de
terminal llegó; el push al teléfono **no** se envió porque Remote Control
estaba inactivo ("Mobile push not sent (Remote Control inactive)"). El canal
principal queda sin verificar; el comportamiento cuando no se envía (seguir, con
el resumen en terminal) sí quedó observado.
