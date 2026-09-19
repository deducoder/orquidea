---
name: prueba-de-migracion-sin-version-fija
description: Las pruebas de una migración no deben fijar el user_version final a un número; una migración posterior las rompe como huérfanas
metadata:
  type: feedback
---

Una prueba de migración que parte de una base en la versión N afirma la versión final como `len(list(MIGRACIONES.glob("*.sql")))`, no como el literal N+1.

**Why:** en s4.3 (e4) la migración `0005` rompió la prueba de s4.1, que afirmaba `user_version == 4`; era un test huérfano de una historia anterior. La primera corrección (`>= 4`) era más floja de lo necesario; la exacta es contar los archivos.
**How to apply:** al escribir la prueba de una migración nueva, partir de las migraciones anteriores con un glob y comparar la versión final con el número de archivos. Ver [[tope-atomico-en-un-insert-select]] para el patrón de las pruebas de `datos`.
