# Story s3.6: Deployment and measurement — Retrospective

Estimated: S · Actual: S

## Summary

Cierra el trabajo de código de la épica. (1) Miniatura de 192 px y calidad 75 en lugar de 320 px y 80 (ADR-007 sustituye a ADR-005, que queda `superseded by ADR-007`): con un proxy de foto con detalle pasa de ~15,5 KB a ~5,2 KB. (2) `scripts/medir-primera-carga.py` mide la primera carga de "Mi colección" (HTML y JavaScript en gzip, miniaturas tal cual) con fotos de ejemplo o con las reales que se le den; `tests/test_medicion.py` la exige ≤ 200 KB en el gate: 25 ejemplares con foto dan 146,5 KB (HTML 1,2, JavaScript 16,0, miniaturas 129,3). (3) README con la sección "Fotos" y el respaldo de `/data` completo, y pruebas de deriva que atan a sus constantes las cifras de la guía (foto máxima, ancho, lado de la miniatura, cuerpo máximo, sesión, inactividad, intentos, bloqueo) y las fotos dentro del volumen. Se retiró del parking lot la entrada de las cifras a mano. 346 pruebas en verde.

## Finalize (reportado por story-implement)

- Gate: `./scripts/check` en verde (ruff, formato, mypy estricto, 346 pruebas) tras cada tarea; cada commit con `./scripts/check && git commit`.
- Orphaned-test check: `test_datos_fotos.py` fijaba el tamaño de la miniatura con literales `(320, 240)` y `(LADO_MINIATURA, 240)`; se actualizaron a `(192, 144)` en el mismo commit que la constante. `test_web_fotos.py` comprueba `<= 320` para la miniatura y sigue valiendo; `test_despliegue.py` (deriva variable-README) sigue verde. Ninguna huérfana sin resolver.
- Acceptance: los seis escenarios del scope y los dos del diseño confirmados. Miniatura ≤ 192 px sin metadatos y más ligera que la de 320 px (medición del proxy, en ADR-007 y en el script); las fotos dentro de `/data` por prueba con el `Dockerfile`; la guía dice volumen con base y fotos, respaldo conjunto, 10 MB, 1600 px, 192 px, 11 MiB, proxy, sin ubicación y cómo medir; cada cifra falla si cambia su constante; el script imprime el desglose y sale con 1 si pasa del presupuesto (probado con `--presupuesto 1`). Ningún criterio deducido se retractó.
- Mutaciones forzadas (cada una puso rojo): `LADO_MINIATURA = 320`; el script sin contar las miniaturas, contando la imagen completa, sin JavaScript, con veredicto siempre OK, sin restaurar el estado de la aplicación; en la guía, `TAMANO_MAXIMO` a 20 MiB, `ANTIGUEDAD_MAXIMA` a 8 h, `ORQUIDEA_FOTOS=/tmp/fotos` en el `Dockerfile`, la base fuera del volumen. Una primera versión de la prueba del script dejaba pasar "sin miniaturas"; se añadió una cota inferior al peso.
- Prueba manual (T4) con `uvicorn` real y una carpeta temporal como volumen, sin `ORQUIDEA_FOTOS`: subir una foto con GPS (303) dejó en el volumen `orquidea.sqlite3` y `fotos/` con los dos archivos; tras reiniciar el proceso sobre el mismo volumen la imagen se sirvió (200, 11 535 bytes); el script dio el desglose anterior y código de salida 0.

## Reviews

**Quality review — PASS WITH RECOMMENDATIONS.** Se leyeron el script, `fotos.py`, la guía y las tres pruebas. Corregidos en el acto: una variable sin uso (`limite`) y líneas largas en el script, y una mutación que sobrevivía (sin cota inferior sobre las miniaturas). Recomendaciones: (1) el proxy de foto (ruido fractal) es una estimación del peso, no una foto de orquídea: por eso el script acepta las reales y la guía lo dice; la cifra verdadera es del humano. (2) `_numero_en_palabras` solo conoce el 5: si `MAXIMO` o `BLOQUEO` cambian, la prueba falla con un mensaje que pide añadir la palabra a la prueba y revisar la guía; es el comportamiento deseado (falla en voz alta) pero obliga a tocar la prueba. (3) `scripts/*.py` no está en el alcance de `mypy` (`files = ["src", "tests"]`); ruff sí lo lee.

**Security review — PASS.** Bandit 1.9.4 sobre los 5 `.py` cambiados (el alcance devuelto coincide con la lista esperada): 0 hallazgos fuera de `tests/`; 63 × B101 (baja) en `tests/`, ruido ya registrado. El script no acepta entrada de red: lee las rutas de fotos que da quien lo corre y usa un directorio temporal. La guía no incluye secretos; se comprobó con la prueba existente de que no trae un hash real. V12.4: la guía aclara que el directorio de fotos va en un volumen y fuera de `/static`. Limitación: análisis estático.

## What went well

- La medición cambió una decisión con datos: la miniatura de 320 px de ADR-005 no salió de ninguna medida y el proxy mostró que triplicaba el peso sin verse mejor a 96 px; el ADR nuevo deja la razón escrita en lugar de una constante cambiada en silencio.
- Convertir el presupuesto en una prueba del gate lo vuelve una propiedad vigilada, no una medición manual de cada `epic-review`.

## What to improve

- Volví a caer en bytecode viejo tras mutar (mismo tamaño de archivo y mismo segundo de mtime): el gate falló con una constante ya restaurada. La memoria del proyecto ya lo decía y no limpié `__pycache__` en esa tanda de mutaciones; toda tanda de mutaciones limpia el bytecode al restaurar.
- La primera medición con ruido fino (per-pixel) dio 2-4 KB por miniatura y habría dado un falso "todo bien": el ruido a escala de pixel se promedia al reducir. Un proxy de peso de una miniatura necesita detalle a la escala de la miniatura (ruido fractal).

## Learned

1. About the system: el peso de una miniatura de foto real es del orden de 15 KB a 320 px y calidad 80 (proxy), 3x más que a 192 px y calidad 75; con la lista mostrándolas a 96 px, 192 px ya es 2x.
2. About the process: las constantes que la guía repite se atan con una prueba que importa la constante y la busca en el README; el fallo aparece en el gate, no en el `epic-review`.
3. Capability gained: `scripts/medir-primera-carga.py` (medición reutilizable con fotos reales) y `foto_con_detalle`, un proxy de foto con detalle a varias escalas.
