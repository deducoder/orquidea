---
name: concurrency-and-real-process-in-security-stories
description: En historias de login/sesión probar concurrencia y el proceso real (uvicorn), no solo la lógica con caplog y un hilo
metadata:
  type: feedback
---

En historias que tocan autenticación, sesión o límites de intentos, incluir en el plan una prueba con varios hilos y una comprobación con `uvicorn` real (registros, cabeceras, cookies).

**Why:** en e2 de orquidea, `epic-review` halló dos defectos de s2.2 que las pruebas unitarias no vieron: el `INFO` de "acceso correcto" no salía bajo uvicorn (solo hay manejadores para sus propios registros), y `POST /acceso` corre en un pool de hilos: 12 verificaciones scrypt (64 MiB cada una) en paralelo y contador de intentos no atómico.
**How to apply:** rutas síncronas de FastAPI = hilos; todo estado compartido lleva cerrojo y una prueba con `ThreadPoolExecutor`; probar registros con `capsys` tras arrancar el ciclo de vida, no solo con `caplog`. Ver [[asvs-checklist-at-design]] y [[epic-stated-criteria-external]].
