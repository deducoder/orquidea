---
name: no-enviar-el-correo-a-servicios-externos
description: Nunca poner el correo del usuario en un User-Agent, cabecera o URL hacia un servicio externo; en descargas usar un User-Agent genérico
metadata:
  type: feedback
---

En s5.7 (2026-09-23), al bajar una foto de Wikimedia Commons con `curl`, puse el correo del usuario en el User-Agent porque la política de Wikimedia pide un contacto. Es un dato personal enviado a un servicio ajeno sin que nadie lo pidiera. Salió en una sola petición y se le avisó al usuario de inmediato.

**Why:** el correo sirve para identificar al usuario, no para darlo como contacto a terceros. Lo que se manda a un servicio externo queda publicado y puede quedar en sus registros.

**How to apply:** en cualquier `curl`, `WebFetch` o petición a un tercero, usar un User-Agent genérico sin datos personales (`orquidea-local-test/0.1`). Si un servicio exige un contacto, preguntar al usuario cuál usar antes de la petición.
