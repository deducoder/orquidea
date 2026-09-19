# Story s2.7: Deployment configuration with persistence — Retrospective

Estimated: S · Actual: S

## Summary

La imagen guarda la base en un volumen: `Dockerfile` crea `/data`, se lo entrega al usuario `app` antes de `USER app`, fija `ORQUIDEA_DB=/data/orquidea.sqlite3` y declara `VOLUME /data`. El README dejó de decir que no hay variables de entorno: documenta el volumen (con la nota de propietario para carpetas montadas), la tabla de configuración (`ORQUIDEA_PASSWORD_HASH`, `ORQUIDEA_DB`, `ORQUIDEA_COOKIE_SEGURA`), la orden que genera el hash, HTTPS y la cookie `Secure`, y el arranque local con las variables. Once pruebas de deriva (`tests/test_despliegue.py`) atan el `Dockerfile` y la guía a lo que el código espera. Dos commits de tarea.

## Finalize (reportado por story-implement)

- **Gate:** `./scripts/check` en verde, 246 pruebas (235 al cierre de s2.6 + 11), ruff, ruff format, mypy strict.
- **Orphaned-test check:** la historia no cambió código de `src/`; el único archivo de prueba que lee `Dockerfile` o `README.md` es el nuevo. Ningún test existente depende de lo modificado. Limpio.
- **Acceptance:** los tres escenarios `@stated` y los cinco `@deduced` se cubren así: `Dockerfile` (prueba), variables y guía (prueba), wheel y redespliegue (prueba manual, abajo). **Prueba manual (T3):** `uv build --wheel` genera un wheel con `0001-sesiones.sql`, `0002-ejemplares.sql`, las ocho plantillas, `htmx.min.js` y el catálogo; instalado en un entorno virtual limpio y ejecutado desde otro directorio, `uvicorn` arrancó con `ORQUIDEA_DB` en una carpeta inexistente (la creó), acceso 303, alta 303, `user_version` 2; al parar, añadir una migración `0003` al paquete instalado (simulando una versión nueva) y volver a arrancar sobre el mismo archivo, la colección seguía (1 ejemplar) y `user_version` pasó a 3 con la tabla nueva. **No verificado:** `docker build` y `docker run`; el cliente de Docker existe pero el daemon no responde en esta máquina, igual que en e1. Es el primer despliegue del humano.
- **Plan con `> Pause: none`:** sin aprobación humana por tarea; el despacho se decidió en `decisions.md`.
- **Tiempo de implementación:** sin tracker; derivable de la rama, no registrado.

## Reviews

- **quality-review:** sin críticos. Observaciones: (1) las pruebas del README solo comprueban nombres de variables y no la exactitud de lo que se dice (por ejemplo "12 horas" o "cinco minutos"): se aceptó, decirlo en prosa es más legible que una tabla generada, y esas cifras las prueba `test_datos_sesiones.py` y `test_autenticacion.py`; si cambian, la guía quedará vieja sin que nada falle. Queda como riesgo anotado. (2) El `Dockerfile` sigue sin construirse.
- **security-review:** PASS. Sin `.py` cambiado en `src/`; Bandit no aplica a esta historia (solo el archivo de prueba nuevo, con B101 de siempre). Guardrails `should-security-002`, recorridos en el diseño: el secreto (`ORQUIDEA_PASSWORD_HASH`) llega por el entorno, no vive en la imagen ni en el repositorio (probado: el `Dockerfile` y el README no contienen un hash ni asignan la variable), la imagen no corre como root (probado), la cookie `Secure` es el valor por defecto y la guía dice que desactivarla es solo para local.

## What went well

- Instalar el wheel en un entorno limpio desde otro directorio comprobó lo que ninguna prueba unitaria ve: que `uv_build` empaqueta las migraciones `.sql`, las plantillas y el catálogo, y que la aplicación no depende de estar dentro del repositorio.
- La prueba de deriva del README encontró de inmediato (en ROJO) que las tres variables no estaban documentadas, y una mutación con una variable nueva en `src/` la vuelve roja: el próximo `ORQUIDEA_*` sin documentar no pasará el gate.
- Simular el redespliegue con una migración nueva en el paquete instalado probó el requisito "las migraciones nuevas se aplican solas" sin Docker.

## What to improve

- Sigue sin verificarse `docker build`/`docker run` (segunda épica seguida). Si hay Docker Desktop en el equipo del humano, arrancar el daemon antes de la próxima sesión permitiría probar la imagen; anotado en el parking lot.
- Las cifras de la guía (12 h, 30 min, 5 intentos, 5 minutos) están escritas a mano; una constante importada de `datos.sesiones`/`autenticacion` en una prueba las ataría al código (también en el parking lot).

## Learned

1. About the system: `uv venv` + `uv pip install` sobre el wheel funciona donde `python -m venv` no trae `pip`; un volumen con nombre de Docker hereda el propietario del directorio de la imagen y una carpeta montada no, por eso la guía pide el `chown`; `VOLUME` se declara después de crear y entregar el directorio.
2. About the process: la deriva entre código, `Dockerfile` y guía se evita con una prueba pequeña que compara nombres, no prosa; verificar el artefacto empaquetado (wheel limpio) es la comprobación que faltaba en e1.
3. Capability gained: una imagen configurada para persistir la colección, una guía completa de despliegue y una defensa automática contra que una variable de entorno nueva quede sin documentar.
