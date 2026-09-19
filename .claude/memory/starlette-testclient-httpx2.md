---
name: starlette-testclient-httpx2
description: "Starlette 1.6 TestClient wants httpx2, not httpx; and local story ids are s{N}.{M}"
metadata: 
  node_type: memory
  type: project
  originSessionId: b2fd6d7f-35bd-4d47-93ab-28daff59da3f
  modified: 2026-09-19T14:16:21.112Z
---

Con starlette 1.6 (FastAPI reciente), `TestClient` con `httpx` emite `StarletteDeprecationWarning`; la dependencia de desarrollo correcta es `httpx2` (`uv add --dev httpx2`).

**Why:** descubierto en s1.1 de orquidea; la advertencia desaparece al cambiar de paquete.
**How to apply:** al agregar pruebas web en este proyecto, usar `httpx2`. Los ids locales sin tracker son `s{N}.{M}` (p. ej. `s1.1`), nunca `e1.1`.
