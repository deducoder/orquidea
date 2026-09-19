# Story s2.7: Deployment configuration with persistence — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · La imagen guarda la base en un volumen escribible

- **Files:** modify `Dockerfile`; create `tests/test_despliegue.py`
- **TDD:** RED pruebas que leen el `Dockerfile`: existe `ENV ORQUIDEA_DB=` con una ruta; esa ruta está dentro del directorio de un `VOLUME`; el directorio se crea (`mkdir`) y se entrega (`chown app`) antes de la línea `USER app`; `USER` no es `root`; el `HEALTHCHECK` sigue apuntando a `/salud`; ninguna línea contiene `scrypt$` (sin secretos) → GREEN Dockerfile → REFACTOR
- **Satisfies:** scenario 1 y los deltas del Dockerfile
- **Mold:** none
- **Verify:** quitar el `VOLUME` (rojo); poner `ORQUIDEA_DB` fuera de `/data` (rojo); mover el `chown` después de `USER app` (rojo); quitar el `mkdir` (rojo); `USER root` (rojo); cambiar el `HEALTHCHECK` a otra ruta (rojo); luego `./scripts/check` completo (archivo nuevo)
- **Commit:** feat(despliegue): volumen de datos escribible para la base de la colección

### T2 · La guía documenta cada variable y el volumen

- **Files:** modify `README.md`, `tests/test_despliegue.py`
- **TDD:** RED pruebas: por cada `ORQUIDEA_[A-Z_]+` que aparece en `src/**/*.py` (la lista no puede estar vacía), el README contiene su nombre; el README no contiene "No hay variables de entorno"; menciona `python -m orquidea.autenticacion`, `/data` y `Secure`; no contiene un hash real (`scrypt$65536$8$2$` seguido de base64 de sal) → GREEN README → REFACTOR
- **Satisfies:** scenarios 2, 4, 5, 7, 8 y el delta del hash de ejemplo
- **Mold:** T1
- **Verify:** quitar del README una de las tres variables (rojo); volver a escribir la frase obsoleta (rojo); añadir una variable nueva en el código sin documentarla (rojo: se comprueba con un archivo temporal en la prueba); pegar un hash real (rojo); luego `./scripts/check`
- **Commit:** docs(despliegue): variables de entorno, volumen y hash de la contraseña en la guía

### T3 · Manual integration test

- Con `uv build --wheel`: listar el wheel y comprobar migraciones, plantillas y estáticos; instalarlo en un entorno limpio (`python -m venv` + `pip install`), arrancar `uvicorn` con `ORQUIDEA_DB` en un directorio nuevo y `ORQUIDEA_PASSWORD_HASH` generado con la orden, iniciar sesión, agregar un ejemplar, parar, volver a arrancar (simulando el redespliegue sobre el mismo "volumen") y comprobar que sigue y que una migración nueva (`0003-…`) se aplica sola.
- **Verify:** el wheel trae `0001`/`0002`, el entorno limpio arranca y crea la base, la colección sobrevive al reinicio y la migración nueva se aplica; `docker` no está disponible (sin daemon) y se dice.

## Order & risks

- **Execution order:** T1 → T2 → T3 — la imagen, la guía, y la verificación que las junta.
- **Dependencies:** secuenciales, acíclicas.
- **Risks:** el `Dockerfile` sigue sin construirse (no hay daemon Docker aquí): el humano lo comprobará en el primer despliegue, previsto desde el diseño del épico; `uv_build` podría no incluir los `.sql` → T3 lo comprueba en el wheel real y, si no, es un defecto de esta historia; una prueba que lee texto del README es frágil pero es justo lo que evita la deriva, y solo comprueba nombres de variables.
