# Story s1.5: VPS deployment — Retrospective

Estimated: M · Actual: 3 tareas, una sesión (sin tracker, sin tiempo registrado)

## Summary

`GET /salud` (healthcheck), `uvicorn` como dependencia de ejecución, `Dockerfile` (Python 3.13 slim, `uv sync --frozen --no-dev`, usuario sin privilegios, healthcheck, puerto 8000), `.dockerignore` y una sección "Despliegue con Dokploy" en el README. **El despliegue real no se ejecutó** (ver abajo).

## Acceptance

- `[stated]` el repositorio queda listo para que Dokploy lo construya y sirva la aplicación: Dockerfile y guía escritos; **no verificado con un `docker build`**, porque esta máquina no tiene un Docker utilizable (el `docker` de Windows no está integrado con WSL). Confianza: media.
- `[deduced]` `/salud` responde 200 sin sesión ni catálogo: `test_salud_responde_ok_sin_depender_del_catalogo` (tres mutaciones lo ponen en rojo). Instalación limpia sirve todo: el wheel contiene 5 plantillas, htmx y 100 JSON; instalado en un entorno Python 3.13 nuevo fuera del repositorio (`import orquidea` resuelve a `site-packages`), `/salud`, `/especies` (100 enlaces), una ficha, `?q=orquidea` y htmx respondieron 200. El riesgo de empaquetado de `uv_build` (abierto desde s1.1) queda cerrado.
- Finalize: `./scripts/check` verde (ruff, format, mypy strict, 52 pruebas); tests huérfanos: ninguno (los tests web importan `orquidea.web.app`, que cambió, y pasan); sin tracker, sin registro de tiempo.

## Reviews

- **quality-review — PASS WITH RECOMMENDATIONS.** Recomendación para el humano, no un defecto: el `Dockerfile` es lo único de la épica que no se ejecutó. La versión de `uv` fijada (0.12.7) es la instalada localmente y no se comprobó que exista como paquete en el índice desde la imagen; un fallo de `pip install uv==0.12.7` en el primer build es la causa más probable. Hoy `/salud` es una ruta sin sesión; e2 debe dejarla fuera de la protección (anotado en el diseño).
- **security-review — PASS.** Bandit 1.9.4 sobre los 2 `.py` cambiados: solo B101 en `tests/` (estacionado). Contenedor sin privilegios (uid 10001), un solo puerto, sin secretos ni variables de entorno; `--host 0.0.0.0` es lo normal dentro de un contenedor que Dokploy pone detrás de su proxy con HTTPS. `should-security-002` (ASVS L2) aplica desde e2 (login); `must-security-001` (EXIF), desde las fotos.

## What went well

El riesgo del empaquetado se cerró con un experimento barato (construir el wheel e instalarlo en un entorno limpio), en lugar de suponerlo o de esperar al despliegue.

## What to improve

El primer entorno limpio salió con Python 3.12 porque no pasé `--python 3.13` a `uv venv`; el error de resolución lo delató rápido. Al reproducir un entorno de despliegue hay que fijar la versión de Python, no confiar en la del sistema.

## Learned

1. About the system: `uv_build` empaqueta plantillas, estáticos y JSON que están dentro del paquete, sin configuración extra.
2. About the process: cuando un criterio `[stated]` depende de un sistema externo del humano (aquí, su Dokploy), la historia debe decirlo en su alcance desde el inicio; aquí se dijo en `story-start` y se llevó a `epic-review`.
3. Capability gained: la aplicación se puede desplegar con un Dockerfile y una guía; falta el push (epic-close) y que el humano ejecute el despliegue.
