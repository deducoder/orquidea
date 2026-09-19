---
name: pkill-f-mata-su-propio-comando
description: En pruebas manuales con uvicorn, pkill -f con el patrón del servidor mata también el shell que lo ejecuta (código 144); apagar por puerto o por PID
metadata:
  type: feedback
---

No apagar el servidor de una prueba manual con `pkill -f "uvicorn orquidea..."` dentro del mismo comando: el patrón coincide con la línea de comando del propio shell, que muere con código 144 y corta el resto del script.

**Why:** en s4.2 (e4) el `pkill` mató el comando a mitad de la verificación y el `pgrep` posterior devolvió un PID que era el suyo, lo que parecía un servidor vivo.
**How to apply:** guardar el PID al arrancar (`uvicorn ... & echo $! > pid`) y `kill $(cat pid)`, y comprobar que apagó con `curl` al puerto (código 000), no con `pgrep -f`. Ver [[tope-atomico-en-un-insert-select]] para el patrón de pruebas de historia.
