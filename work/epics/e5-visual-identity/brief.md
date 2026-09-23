# Epic e5: Visual identity — Brief

## Hypothesis

Para el coleccionista que consulta y registra su colección en el teléfono, a menudo en campo,
la identidad visual de Orquídea es una paleta, una tipografía y una interfaz derivada de ellas
que hacen legible la ficha y el historial de cada planta bajo el sol y con red lenta.
A diferencia de las plantillas actuales, que no tienen un solo estilo propio,
deja que la foto del ejemplar sea la protagonista y cada valor visual salga de una escala declarada,
con su criterio comprometido antes de producir nada.

## Success metrics

- **Leading:** el criterio del encargo (ADR con las tres adecuaciones aprobadas el 2026-09-22 y el catálogo de supervivencia resuelto) queda commiteado en `proposed`, con los criterios medibles vistos fallar antes de producir la primera pieza.
- **Lagging:** todas las plantillas usan la identidad; `survival-review` pasa sobre cada pieza (`contrast`, `component-contrast`, `target-size`, `provenance`), los recursos de la identidad pesan ≤ 50 KB gzip y la primera carga sigue dentro de `must-perf-001` (≤ 200 KB, ≤ 5 s en Slow 3G).

## Appetite

M — 5-7 historias.

## Scope boundaries

What the design may not do. **What it will build is not decided here** — the
in-scope list belongs to `scope.md`, written by `epic-design` after the
decomposition.

### No-gos
- Logotipo, favicon o ícono de plataforma — decidido por el humano el 2026-09-22: app personal de un solo usuario (RF-08), sin marca que publicar ni registrar; el nombre compuesto en la tipografía elegida basta como encabezado.
- Cambiar el comportamiento de la aplicación — la épica viste lo que existe (RF-01 a RF-08); ninguna pantalla ni flujo nuevo entra por aquí.

### Rabbit holes
- Un tema oscuro o varios temas: una sola paleta basta para probar el criterio.
- Una cadena de construcción de CSS (preprocesador, bundler, generación de tokens): hoy no hay paso de build para el front (ADR-001).
- Una biblioteca de componentes más allá de lo que las plantillas actuales usan.
- Afinar la fuente web (subconjuntos, variantes) antes de saber si el presupuesto de 50 KB la admite.
