---
name: tope-atomico-en-un-insert-select
description: Un tope de registros por ejemplar se comprueba dentro del mismo INSERT ... SELECT, no contando aparte; probarlo con hilos y una conexión por hilo
metadata:
  type: feedback
---

Un límite por ejemplar (p. ej. 500 riegos) se impone con `INSERT ... SELECT ... WHERE EXISTS (ejemplar) AND (SELECT COUNT(*) ...) < tope`, y la causa del rechazo se distingue después con otra consulta.

**Why:** cada petición abre su propia conexión y las rutas síncronas corren en hilos; contar y luego insertar deja pasar altas simultáneas. En s4.1 la mutación "contar y luego insertar" puso roja la prueba 15 de 15 veces (barrera + una conexión por hilo), así que la prueba sí ve la carrera.
**How to apply:** la prueba usa `threading.Barrier` y `conectar(ruta)` por hilo (no una conexión compartida). Ver [[concurrency-and-real-process-in-security-stories]] y [[prueba-con-azar-se-corre-en-bucle]].
