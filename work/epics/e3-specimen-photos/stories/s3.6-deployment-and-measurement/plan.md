# Story s3.6: Deployment and measurement — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · Miniatura de 192 px (ADR-007)

- **Files:** modify `datos/fotos.py`, `tests/test_datos_fotos.py`; create `records/decisions/adr-007-miniatura-de-192-px-para-la-lista.md`; modify `records/decisions/adr-005-procesamiento-de-fotos-con-pillow.md` (solo su estado)
- **TDD:** RED prueba de que la miniatura de una foto con detalle mide ≤ 192 px de lado mayor y pesa menos de la mitad que con 320 px (cifra del ADR) → GREEN `LADO_MINIATURA = 192`, calidad 75 → REFACTOR
- **Satisfies:** escenario de la miniatura más ligera
- **Mold:** ADR-007 y `datos/fotos.py` (constantes existentes)
- **Verify:** la miniatura respeta el nuevo lado y sigue sin metadatos — forced mutations: dejar `LADO_MINIATURA = 320` (la prueba de peso y de lado fallan); subir la calidad a 95 (la de peso falla); then `uv run pytest tests/test_datos_fotos.py tests/test_web_fotos.py -q` y `./scripts/check` completo
- **Commit:** feat(fotos): miniatura de 192 px para la lista

### T2 · Script de medición y prueba de presupuesto

- **Files:** create `scripts/medir-primera-carga.py`, `tests/test_medicion.py`
- **TDD:** RED prueba: la colección de 25 ejemplares con foto con detalle mide ≤ 200 KB, cuenta 25 miniaturas, incluye el HTML y `htmx` en gzip, y el script sale con 1 si se le da un presupuesto menor → GREEN `medir` y `main` → REFACTOR
- **Satisfies:** el `@stated` y el escenario del script
- **Mold:** `tests/conftest.py` (estado temporal de la aplicación y sesión) y `tests/fabricas.py`
- **Verify:** el total sale de bytes realmente pedidos a la aplicación — forced mutations: no contar las miniaturas (el total cae y la prueba de conteo falla); contar la imagen a tamaño completo en lugar de la miniatura (el presupuesto se pasa); no pedir el JavaScript estático; then `uv run pytest tests/test_medicion.py -q` y `./scripts/check` completo
- **Commit:** feat(scripts): medir el peso de la primera carga de la colección

### T3 · Guía de despliegue y pruebas de deriva

- **Files:** modify `README.md`, `Dockerfile` (comentario), `tests/test_despliegue.py`; modify `records/parking-lot.md` (retirar con `park`)
- **TDD:** RED pruebas: fotos dentro del volumen; cada cifra de la guía contra su constante (foto máxima, ancho, cuerpo, sesión, inactividad, intentos, bloqueo); la guía menciona respaldo, proxy, ubicación → GREEN README → REFACTOR
- **Satisfies:** los escenarios de despliegue y deriva
- **Mold:** `tests/test_despliegue.py` (`test_el_readme_documenta_cada_variable_que_lee_el_codigo`)
- **Verify:** cambiar una constante sin la guía pone rojo — forced mutations: cambiar `TAMANO_MAXIMO` a 20 MiB; cambiar `ANTIGUEDAD_MAXIMA` a 8 h; apuntar `ORQUIDEA_FOTOS` a `/tmp/fotos` en el `Dockerfile` (la prueba del volumen falla); then `uv run pytest tests/test_despliegue.py -q` y `./scripts/check` completo
- **Commit:** docs(despliegue): guía de fotos, respaldo y límites, con pruebas de deriva

### T4 · Manual integration test

- Con `uvicorn` real y un directorio temporal como "volumen": subir una foto, reiniciar el proceso, comprobar que sigue; correr el script con fotos con detalle generadas y con el presupuesto por defecto.
- **Verify:** la foto sobrevive al reinicio; el script imprime el desglose y sale con 0.

## Order & risks

- **Execution order:** T1 → T2 → T3 → T4 — T1 fija el peso que T2 mide; T3 documenta lo ya decidido.
- **Dependencies:** secuencial.
- **Risks:** el proxy de foto no es una foto real → el script acepta fotos reales y la medición con las del humano es el stop previsible; el build de Docker sigue sin verificarse (sin Docker en esta máquina) → la guía lo dice tal cual.
