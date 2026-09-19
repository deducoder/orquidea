# Epic e1: Species catalog — Retrospective

## Summary

La aplicación ya tiene un catálogo de especies nativas de Chiapas que se carga desde JSON validado (esquema pydantic con fuente obligatoria, ADR-002), se explora en una lista, se busca ignorando mayúsculas y acentos, y abre una ficha con luz, riego, temperatura y sustrato cada uno con su fuente. Trae 100 especies reales respaldadas por una investigación, un healthcheck y un `Dockerfile` con guía para Dokploy. **No está desplegada**: eso queda para el humano tras dar acceso de Dokploy al repositorio.

## Metrics

- Stories: 6 (s1.1 a s1.6) · Estimated: S, M, M, S, M, S · Actual: iguales a lo estimado en tamaño; s1.6 fue mucho más grande de lo que "S" sugiere por la investigación (lo grande no fue el código, sino conseguir datos con fuente real).
- 52 pruebas, `./scripts/check` verde, 1 ADR (ADR-002), 1 informe de investigación (`work/research/chiapas-orchid-seed/`).
- Surgió a mitad de la épica y no estaba planeado: un re-plan (s1.4 antes que s1.5; s1.5 depende de s1.6), una investigación de 100 especies, y la corrección de los ids locales (`s1.n`, no `e1.n`).

## Scope verification

Cada elemento de "In scope" y "Done when" de `scope.md`, releído contra el código (los commits son los de `git log` de la épica):

- **MUST — esquema y carga validada del catálogo (RF-01)** → **Fulfilled**: `src/orquidea/catalogo/modelo.py` y `src/orquidea/datos/catalogo.py`, pruebas `test_catalogo_carga.py` y `test_catalogo_modelo.py`.
- **MUST — ficha de especie con fuente por dato (RF-03)** → **Fulfilled**: `src/orquidea/web/app.py` y `templates/especie.html`, `test_web_especies.py`.
- **MUST — búsqueda por nombre (RF-02)** → **Fulfilled**: `src/orquidea/catalogo/busqueda.py` y `/especies?q=`.
- **MUST — despliegue al VPS con una especie visible en línea** → **Not fulfilled**, diferido por el humano ("Dile que lo cierre, regreso para darle acceso a dokploy al repo": `decisions.md`, entrada Answered de `epic-review`). Hecho: `Dockerfile`, `.dockerignore`, `/salud`, guía en el README y wheel verificado en un entorno limpio. No hecho: `docker build` (sin Docker aquí), push y despliegue en Dokploy.
- **MUST — conjunto semilla con fuentes reales** → **Fulfilled** con reservas: 100 JSON en `src/orquidea/datos/catalogo/`, `test_catalogo_real.py`. Reservas que el humano debe revisar: los cuidados son de género, no de especie (cada dato lo dice), y "conocidas y populares" se midió como más observadas en iNaturalist.
- **SHOULD — medición de `must-perf-001`** → **Parcial**: peso medido (lista 1,884 B, ficha 1,035 B, htmx 16,356 B con gzip); tiempo con "Slow 3G" no medido.
- **[stated] catálogo cargado desde JSON validado y una especie de ejemplo en su ficha, desplegada en el VPS** → **Not fulfilled** en su parte "desplegada"; diferido por el humano (misma respuesta). La parte de carga y ficha, **Fulfilled**.
- **[stated] primera carga ≤ 5 s con Slow 3G y ≤ 200 KB sobre el catálogo real** → **Parcial**: ≤ 200 KB medido; tiempo con Slow 3G **not measured**, diferido por el humano.
- **[deduced] rechazo con archivo y campo y nunca a medias** → **Fulfilled** (`test_todo_o_nada_con_un_archivo_invalido` y compañeras).
- **[deduced] la búsqueda ignora mayúsculas y acentos** → **Fulfilled** (`test_catalogo_busqueda.py`).
- **[deduced] cada dato de cuidado con su fuente en la ficha** → **Fulfilled** (`test_ficha_muestra_datos_generales_y_cada_cuidado_con_su_fuente`, `test_catalogo_real.py`).
- **[stated] all stories complete · docs updated · retrospective done** → stories y retrospectiva hechas; `docs.md` lo escribe `epic-close`.

No hay compromisos de eliminación. Revisión de rango: `quality-review` sin críticos (recomendación: unificar en un `conftest.py` la fixture que sustituye y restaura `app.state.catalogo`, hoy repetida en dos archivos de prueba); `security-review` PASS WITH FINDINGS con solo B101 en `tests/` (estacionado) y la observación de que aún no hay cabeceras de seguridad ni sesión, materia de e2 (`should-security-002`).

## What went well

- El esquema con fuente obligatoria hizo imposible sembrar datos sin sustento: la investigación tuvo que dar una fuente por dato o no había ficha.
- Las mutaciones (sin bytecode) encontraron pruebas que pasaban en vacío en varias historias.
- Detener el trabajo en P5 al llegar a s1.6 y s1.5, con ambas preguntas juntas, ahorró idas y vueltas; la respuesta trajo el VPS y la decisión de investigar.

## What to improve

- Se escribió `e1.n` para las historias durante el diseño y se corrigió después: leer el esquema de ids del proyecto (`s{N}.{M}`) antes de escribir el primer artefacto.
- Un criterio `[stated]` que depende de un sistema externo del humano (aquí el Dokploy) debió señalarse en `epic-design` como un stop previsible; se descubrió en `epic-review`.
- La ficha repite una cita larga cuatro veces (estacionado en el parking lot).
- El `Dockerfile` nunca se construyó: confirmar en el primer despliegue que `pip install uv==0.12.7` existe y que la imagen arranca.

## Learned

1. About the system: la AOS publica una tarjeta de cuidados por género que encaja con el esquema; los cuidados por especie de Chiapas no están en una fuente abierta y uniforme; `uv_build` empaqueta plantillas, estáticos y datos sin configuración extra.
2. About the process: distinguir pronto qué criterios `[stated]` dependen de acciones del humano o de sistemas fuera de la sesión; y correr las mutaciones sin caché de bytecode.
3. Capability gained: catálogo de 100 especies con fuentes, listo para que e2 (colección) enlace ejemplares a `Especie.id`, y una aplicación empaquetable y desplegable con `Dockerfile`.
