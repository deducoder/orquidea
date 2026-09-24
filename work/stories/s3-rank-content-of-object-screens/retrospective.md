# Story s3: Rank content of object screens — Retrospective

Estimated: una parte de la sesión, sin cifra declarada · Actual: de `a47c2dc` a `988b176`, unos veinte minutos en las fechas de autor, más dos pausas de decisión.

## Summary

Guía de prioridad de S1 a S4: 20 rangos, con la opción A (foto primero) en S3 y S4, firmada por el dueño. ADR-018 abierto con los órdenes completos de las tres opciones y su rojo, y después `accepted`. La promoción de la entrada de fuentes largas quedó decidida como "no aquí".

## Finalize

- **Gate:** `./scripts/check` salió 0 antes de cada commit de la rama.
- **Pruebas huérfanas:** no aplica; ningún `.py` en el diff.
- **Criterios de aceptación (scope):**
  - ADR en `proposed` con su rojo antes del primer rango: cumplido (`9a6a68e` antes de `045980d`).
  - `inventory-sources.py` sale 0 con 4 pantallas guiadas: cumplido.
  - El comando de G2 da `7 tasks, 20 ranks, 7 served`: cumplido.
  - La guía está firmada, y G3 y G4 están juzgados: cumplido, 2026-09-24.
  - Rojo antes de producir (deducido y confirmado): cumplido.
  - ADR `accepted`: cumplido.
  - Ningún criterio retractado.
- **Survival-review:** `precedence` sale PASS. Los nueve "no aplica" están **firmados por Daniel Efraín Domínguez Urbina el 2026-09-24**.
- **quality-review:**
  - El comando de G2 que corrió se extrajo con `awk` del propio ADR, así que el instrumento es el texto escrito y no una copia.
  - Las opciones B y C se midieron armadas desde las tablas de la guía, y las dos dan G1 y G2 verdes. G1 y G2 no las distinguen: la elección se decidió solo por juicio, y así quedó dicho en la rejilla.
- **security-review:** sin sujeto, porque no hay `.py` cambiados.

## What went well

- **La lección de s2 se aplicó y se notó.** Las tres opciones entraron al ADR con sus órdenes completos antes del primer rango, así que la opción elegida existía, tal cual, en `fda183f`.
- **Revisar las promociones del parking lot al diseñar encontró una.** La de "fuentes largas" se tocaba con el rango 2 de S2, y el dueño la decidió de forma explícita en vez de que se quedara sin mirar.
- **El PASS de `precedence` aclaró el FAIL de s2.** El gate ignora los commits `accept`: con las celdas medidas llenadas en el `accept`, el veredicto es PASS. El FAIL de s2 vino de un `update` hecho después de la pieza. La entrada aparcada sigue siendo válida (el gate no distingue celdas de criterios), pero ahora se sabe cuándo aparece.

## What to improve

- **G1 y G2 no discriminan entre opciones.** Las tres pasan las dos. Un criterio medible que ninguna opción puede reprobar no ayuda a elegir; solo filtra guías mal formadas. Si se quiere que lo medible opine, hace falta algo como "T6 servida en los tres primeros rangos de S4", escrito antes. Queda como nota para la próxima guía, no como cambio aquí.
- **La guía de S5 a S9 queda pendiente.** La composición de esas pantallas no puede empezar sin ella, así que conviene hacerla antes de componerlas.

## Learned

1. **Sobre el sistema:** la ficha del ejemplar de hoy sigue el orden C (nombre, notas, foto, riegos). La guía pide foto, nombre y registrar un riego. En Mi colección, "Agregado el" no sirve a ninguna tarea.
2. **Sobre el proceso:** `precedence.py` fecha el registro por su último `add` o `update`, y los commits `accept` no cuentan. Las celdas medidas se llenan en el `accept`. Guardado en la memoria del gate.
3. **Capacidad ganada:** S1 a S4 tienen su rango 1 firmado, que es la primera pregunta del juicio de una página en la composición.
