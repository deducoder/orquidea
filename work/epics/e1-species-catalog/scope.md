# Epic e1: Species catalog — Scope

## Objective

Un coleccionista de orquídeas de Chiapas puede consultar en la aplicación, ya desplegada en el VPS, un catálogo curado de especies nativas con sus cuidados técnicos y la fuente de cada dato.

**Value:** se desbloquea la referencia de cuidados (outcome "Cuidado informado" de la visión) y el mecanismo de catálogo sobre el que e2 (colección personal) ligará sus ejemplares.

## Stories

| ID | Story | Size | Description |
|----|-------|:----:|-------------|
| s1.1 | Esqueleto web | S | Aplicación FastAPI mínima con plantilla base, htmx y una página de inicio, con su prueba y sus gates en verde. |
| s1.2 | Esquema y carga del catálogo | M | Esquema de especie (con fuente obligatoria) y carga de los JSON que rechaza cualquier archivo inválido señalando archivo y campo (RF-01, must-data-001). |
| s1.3 | Ficha de especie | M | Lista de especies y ficha con información general, luz, riego, temperatura, sustrato y la fuente de cada dato (RF-03). |
| s1.4 | Buscar en el catálogo | S | Búsqueda por nombre científico o común, sin distinguir mayúsculas ni acentos (RF-02). |
| s1.5 | Despliegue al VPS | M | La aplicación corre en el VPS y una especie de ejemplo se ve en su ficha en línea (métrica líder del brief). |
| s1.6 | Conjunto semilla | S | Especies reales con sus fuentes cargadas en el catálogo, suficientes para medir must-perf-001 sobre datos reales. |

Dependencias: s1.3 depende de s1.1 y s1.2; s1.4 de s1.3; s1.5 de s1.1; s1.6 de s1.2. Sin ciclos.

## In scope

- **MUST:** esquema y carga validada del catálogo (RF-01); ficha de especie con fuente por dato (RF-03); búsqueda por nombre (RF-02); despliegue al VPS con una especie visible en línea; conjunto semilla con fuentes reales.
- **SHOULD:** medición de must-perf-001 sobre el catálogo semilla, hecha en `epic-review`, sin historia propia.

## Out of scope

- Capturar el catálogo completo (del orden de 700 especies) — está en los rabbit holes del brief; esta épica entrega el mecanismo y un conjunto semilla — **not now**: crecimiento del catálogo, sin épica asignada.
- Búsqueda difusa o por relevancia — rabbit hole del brief; basta ignorar mayúsculas y acentos — **not now**.
- Inicio de sesión y protección de rutas (RF-08) y todo lo de la colección (RF-04 a RF-07) — pertenecen a e2 — **not now**. El catálogo de e1 es de solo lectura y sin sesión hasta que e2 la introduzca.

## Done when

- [stated] El catálogo se carga desde JSON validado y una especie de ejemplo se ve en su ficha, desplegada en el VPS (métrica líder del brief).
- [stated] La primera carga es usable en ≤ 5 s con "Slow 3G" y transfiere ≤ 200 KB gzip, medida sobre el catálogo real (métrica rezagada del brief, `must-perf-001`).
- [deduced] Un JSON que no cumple el esquema o carece de fuente se rechaza con error que nombra archivo y campo, y nunca se carga a medias (RF-01, `must-data-001`).
- [deduced] La búsqueda devuelve la misma especie escribiendo con o sin mayúsculas y con o sin acentos (RF-02).
- [deduced] Cada dato de cuidado de la ficha muestra su fuente (RF-03).
- [stated] All stories complete · docs updated · retrospective done

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| Los datos botánicos y sus fuentes reales no están escritos en ningún artefacto; inventarlos violaría `must-data-001` | H | H | s1.6 y el ejemplo de s1.5 dependen de que el humano aporte especies y fuentes; si no están, esa historia se detiene (P5) en lugar de fabricar datos |
| Los datos del VPS (host, acceso, forma de despliegue) no están escritos en ningún artefacto | H | M | s1.5 lo decide en su diseño con ADR si hay más de una opción; sin datos escritos, se detiene (P5) |
| Se rebasa `must-perf-001` por peso de plantillas, htmx o catálogo | L | M | HTML del servidor con un solo script pequeño (ADR-001); medición en `epic-review` |
