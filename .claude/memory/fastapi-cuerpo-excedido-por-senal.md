---
name: fastapi-cuerpo-excedido-por-senal
description: "FastAPI convierte en 400/422 cualquier excepción al leer el cuerpo; un límite de tamaño debe cortar por señal (desconexión) y sustituir la respuesta por 413"
metadata:
  type: project
---

Si un middleware ASGI lanza una excepción desde `receive` al pasarse del límite, FastAPI la captura al parsear el formulario y responde 400 o 422, no 413. La solución en `web/limite.py`: al pasarse, `receive` devuelve `http.disconnect` y el `send` reemplaza la respuesta de la aplicación por el 413.

**Why:** descubierto en s3.4 de orquidea: la prueba con `TestClient` dio 422 con la versión que lanzaba una excepción. Además el analizador urlencoded de Starlette rechaza campos de más de 1 MiB con 400 antes de que actúe el límite propio; solo el multipart con archivo llega al 413.
**How to apply:** probar los límites de cuerpo también con `uvicorn` real (`curl -H "Transfer-Encoding: chunked" -F`), y comprobar en la prueba que el cuerpo sí se leyó (con `Content-Type` de formulario). Ver [[starlette-testclient-httpx2]].
