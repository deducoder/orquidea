---
name: asvs-checklist-at-design
description: En historias con seguridad, recorrer la lista ASVS L2 aplicable durante el diseño, no en la security-review
metadata:
  type: feedback
---

En una historia que toca autenticación, sesión o cookies, recorrer los requisitos ASVS L2 aplicables (`should-security-002`) al escribir el `design.md`, y ponerlos como criterios.

**Why:** en s2.2 de orquidea la `security-review` encontró dos huecos que ya estaban en la guardia (prefijo `__Host-` de la cookie, registro de eventos de autenticación) y costaron un commit no planeado.
**How to apply:** antes del plan, listar los capítulos ASVS que la historia toca (V2 contraseñas, V3 sesión, V4 control de acceso, V7 registro) y marcar cada uno como cubierto, diferido a una historia con nombre, o no aplicable. Ver [[starlette-testclient-httpx2]] para las pruebas web.
