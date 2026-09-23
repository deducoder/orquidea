# Session 2026-09-23 — s1: identidad en el vocabulario de 0.23.0

## Done

- **Survival-review de e5 con gemba-design 0.23.0:** `precedence.py` da PASS en 9 piezas, y `DESIGN.md` sale ilegible (no lleva `decision:`). Con sondas se vio qué puede expresar 0.23.0: acentos, `rounded`, `borderColor` y `minWidth` sí; trazo, elevación, medida e iconografía no.
- **Historia standalone s1, cerrada y publicada** (`origin/develop` = `d6260ff`):
  - ADR-016 `accepted`;
  - tokens en español;
  - radio `recto`, `borderColor` en el campo, mínimos de 48 y las 14 dimensiones del catálogo respondidas;
  - `DESIGN.md` regenerado con 0.23.0, idéntico en dos corridas;
  - dos scripts: `comprobar-dimensiones.py` y `comprobar-medidas.py objetivos`, que ahora lee los mínimos;
  - la cadena de colores atada en el gate (T9);
  - tarjeta solo por tono, enlaces `accion` sin sangría y Acceso con su `<p>`;
  - los dos juicios que e5 dejó `unsigned`, firmados (sí y sí).
- **Parking lot:** tres entradas retiradas (ASCII, interfaz vestida, cadena). Aparcados: `precedence.py` con eslabones recalculados, la sustitución parcial en la técnica `adr` y la documentación de e5 desactualizada.
- **Láminas de juicio:** publicadas como página privada, https://claude.ai/artifact/VzNiVxjwAEr8djdTDSZMws

## Decided

- **ADR-013, 014 y 015 quedan `accepted`, y ADR-016 nombra cada decisión que reemplaza** — **why:** la técnica `adr` solo sustituye registros enteros, y el resto de cada uno sigue en pie.
- **Mínimo de control solo con `minHeight`/`minWidth`** — **why:** es lo que hace la hoja. `height`/`width` declaraban un ancho fijo falso; a cambio, `tokens.py targets` queda sin sujeto, y lo cubre el script propio a 44 px.
- **Medida sin tope, con V3 no cumplido** — **why:** elección del humano. Queda escrito como "no se cumple, se elige igual", sin retocar el criterio.
- **Elevación solo por tono (1.11:1)** — **why:** juicio del humano en V4, papel y tinta sin trazo de más.
- **El refactor de los lectores de tablas va a su propia historia** — **why:** toca cuatro scripts ajenos a s1. Su promoción ya se cumplió.

## Open

- La entrada del refactor de lectores de tablas tiene la promoción cumplida y espera su historia.

## Next

Quitar `'unsafe-inline'` de `style-src` en la CSP (`src/orquidea/web/app.py:46`), con la aserción contraria en `tests/test_web_proteccion.py:225`. Antes, comprobar que htmx no inyecte estilos en línea (`htmx.config.includeIndicatorStyles`).

## State

Branch `develop` · work item in flight: none · tree: clean · `develop` = `origin/develop` (`d6260ff`).
