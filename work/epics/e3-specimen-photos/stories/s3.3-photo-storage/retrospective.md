# Story s3.3: Photo storage — Retrospective

Estimated: M · Actual: M

## Summary

Las fotos ya tienen dónde vivir. Migración `0003` (columna `ejemplares.foto`, nombre aleatorio), `Ejemplar.foto` y `fijar_foto`; `orquidea.datos.almacen_fotos` con `ruta_de_foto` (único lugar donde se forma una ruta, solo desde un nombre validado), `poner_foto`, `quitar_foto` y `quitar_con_foto` (escribir → actualizar → borrar, bajo un cerrojo de proceso), `directorio_de_fotos` (`ORQUIDEA_FOTOS`, por defecto `fotos/` junto a la base) y `preparar_directorio` (se llama al arrancar y falla nombrando la ruta). La ruta web de quitar ejemplar borra sus archivos. 293 pruebas en verde.

## Finalize (reportado por story-implement)

- Gate: `./scripts/check` en verde (ruff, formato, mypy estricto, 293 pruebas) en cada tarea y al final.
- Orphaned-test check: se corrieron todas las pruebas que importan `Ejemplar`, `datos.ejemplares` o `web.app` (`test_datos_ejemplares`, `test_web_coleccion`, `test_recorrido_coleccion`, `test_web_proteccion`, `test_despliegue`, …). `Ejemplar.foto` tiene valor por defecto `None`, así que las igualdades siguen valiendo. `test_despliegue.py` exigió documentar `ORQUIDEA_FOTOS` en el README (deriva variable-README): añadida la fila en `feat(coleccion)`; la guía completa del volumen sigue siendo de s3.6. `tests/conftest.py` se actualizó para apuntar `directorio_fotos` a un directorio temporal y restaurarlo. Ninguna huérfana sin resolver.
- Acceptance: todos los escenarios del scope y del diseño confirmados por prueba (guardar; reemplazar; quitar foto; quitar ejemplar; ejemplar inexistente sin archivos; nombres inválidos; fallo de la segunda escritura; dos subidas simultáneas; migración con datos; directorio por defecto y por `ORQUIDEA_FOTOS`; arranque con directorio no escribible). Ningún criterio deducido se retractó.
- Mutaciones forzadas (cada una puso rojo): no borrar la foto anterior, no borrar al quitar el ejemplar, quitar el cerrojo (prueba de 8 hilos con la ventana ensanchada), no validar el nombre, no limpiar la primera escritura si falla la segunda, no comprobar la existencia del ejemplar (tras simplificar), `fijar_foto` sin `WHERE`, `listar` sin la columna, borrar la migración, volver a llamar `quitar` en la ruta, no preparar el directorio al arrancar.
- Prueba manual (T4): `uvicorn` real con directorio temporal: el directorio se creó solo al arrancar; con un ejemplar dado de alta por HTTP y su foto puesta por el módulo hubo 2 archivos; siguieron 2 tras reiniciar el proceso; quitar el ejemplar por HTTP (303) los dejó en 0.

## Reviews

**Quality review — PASS WITH RECOMMENDATIONS.** Se leyeron `almacen_fotos.py`, `ejemplares.py`, `modelo.py`, la migración, la ruta y las pruebas. Corregido en el acto: el `poner_foto` inicial duplicaba la comprobación de existencia (un `return False` temprano y el `if not cambiada`), y una mutación sobrevivía; se dejó solo la de `fijar_foto`. Los `# type: ignore[union-attr]` de las pruebas se sustituyeron por el helper `_nombre`. Recomendación para s3.4: `poner_foto` deja escapar `OSError` (disco lleno) y una `FotoInvalida` viene de `procesar_foto`, no de aquí; la ruta de subida debe traducir ambas a un mensaje en español y a un código, no dejar un 500. Observación: el cerrojo es de proceso, válido con un solo proceso (ADR-001); con varios procesos habría que revisarlo (mismo supuesto que `LimiteDeIntentos`).

**Security review — PASS.** Bandit 1.9.4 sobre los 9 `.py` cambiados (el alcance devuelto coincide con la lista): 0 hallazgos en `src`; 209 × B101 (baja) en `tests/`, el ruido ya registrado en el parking lot. Guardarraíles y ASVS: V12.3 sostenido (la ruta solo se forma desde un nombre de `[A-Za-z0-9_-]{1,64}` por `fullmatch`, sin id ni nombre subido; 9 casos inválidos probados, incluido `x\n`); V12.4 sostenido (el directorio no se monta como estático); V4.2 diferido a s3.4 (aquí no hay ruta de lectura); `should-security-002` sin regresión. Limitación: análisis estático, sin cobertura de autorización por objeto (s3.4).

## What went well

- La prueba de concurrencia con la ventana ensanchada (`time.sleep` en `fijar_foto`) detecta la falta del cerrojo de forma determinista; sin ensancharla la carrera casi nunca aparece.
- Recorrer ASVS al diseñar dejó claro qué cubre esta historia (V12.3, V12.4) y qué queda para la ruta (V4.2).

## What to improve

- Cometí `feat(datos)` con el gate en rojo por segunda vez: encadené `&&` sin comprobar el código de salida y `mypy` (atributos no exportados en pruebas) y una prueba mía frágil pasaron inadvertidas; lo enmendé antes de seguir. Regla para el resto de la épica: `./scripts/check && git commit`, siempre encadenado.
- Escribí una prueba que fallaba al azar por construcción (comprobaba que el dígito del id no apareciera en un nombre aleatorio); la corrí solo una vez. Toda prueba con aleatoriedad se corre varias veces antes de commitear.
- La deriva variable-README (`test_despliegue.py`) no estaba en el plan de esta historia; el diseño de la épica no la vio porque el gate la escanea, no el código. Lo anoto para s3.6.

## Learned

1. About the system: `mypy --strict` no deja acceder en pruebas a atributos que un módulo importó (`almacen_fotos.os`, `almacen_fotos.fijar_foto`): se parchea el módulo dueño (`os`) o por nombre con cadena.
2. About the process: una prueba con aleatoriedad se corre en bucle antes de commitear (memoria `prueba-con-azar-se-corre-en-bucle`); y el gate se encadena al commit.
3. Capability gained: patrón de prueba de concurrencia con ventana ensanchada para operaciones base+disco.
