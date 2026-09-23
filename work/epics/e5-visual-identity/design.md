# Epic e5: Visual identity — Design

## Gemba findings

- **No hay identidad que extraer.** `src/orquidea/web/static/` solo tiene `htmx.min.js` (50 917 bytes); ninguna plantilla enlaza CSS, y `base.html` no tiene un solo estilo. El criterio entra al ciclo **propuesto**, no extraído: seguir la entrada `proposed` de la convención del ciclo.
- **Diez plantillas, 287 líneas**, todas heredan de `base.html` (`header` con navegación y botón "Salir", `main`). Una sola hoja enlazada en `base.html` llega a todas: extender ese patrón, no añadir estilos por plantilla.
- **Estilos en línea en cuatro sitios**: `white-space: pre-line` en las notas (`coleccion.html`, `ejemplar_ficha.html`), `max-width: 100%` en la foto de la ficha, `object-fit: cover` en la miniatura y `display: inline` en los formularios de quitar/terminar. Pasan a la hoja en s5.7.
- **`/static` ya se sirve** con `StaticFiles` y queda fuera de `Cache-Control: no-store` (`app.py`). Reutilizar para la hoja y las fuentes.
- **La CSP** es `default-src 'self'; style-src 'self' 'unsafe-inline'`: una hoja propia y fuentes servidas desde `/static` caben sin tocarla; una fuente de un CDN externo, no. `tests/test_web_proteccion.py` afirma `'unsafe-inline'` en `style-src`.
- **La medición de peso ya existe**: `scripts/medir-primera-carga.py` cuenta HTML y JavaScript en gzip más miniaturas contra 200 KB, con pruebas en `tests/test_medicion.py`. El criterio 1 extiende ese script, no escribe otro.
- **Instrumentos del addon** (`gemba-design` 0.21.0): `contrast.py` fija el umbral en 4.5:1, así que el ≥ 7:1 del criterio 2 se escribe en el proyecto; `pairs`, `targets` y `provenance` se corren sobre el `DESIGN.md` generado por `design-md.py`.
- **Nombres científicos** ya van en `<i>` en `especie.html`, `especies.html`, `coleccion.html` y `ejemplar_ficha.html`: la tipografía necesita una itálica verdadera, o se verá una oblicua sintética.
- **Defecto encontrado en el recorrido**: el bloque `title` de `coleccion.html` contiene `<p><a href="/coleccion/nuevo">…</a></p>` (desde `8d5b985`, e2); reproducido con `TestClient`, la pestaña muestra el marcado como texto. Destino: flujo de bug antes de s5.1.

## Target components

| Component | Change | Purpose |
|-----------|--------|---------|
| `records/decisions/adr-009…` a `adr-01N…` | create | un ADR por pieza, abierto en `proposed` antes de producirla y completado a `accepted` (`s5.1`, `s5.2`, `s5.3`, `s5.4`, `s5.5`, `s5.6`) |
| `governance/identity/` | create | entregables del encargo: `commission.md`, `concept.md`, `palette.md`, `specimen.md` (`s5.1`, `s5.2`, `s5.3`, `s5.4`) |
| `governance/identity/ui/` | create | `primitives.md`, `semantics.md`, `type-scale.md`, `spacing.md`, `components.md` y `DESIGN.md` generado (`s5.5`, `s5.6`) |
| `scripts/medir-primera-carga.py` | modify | cuenta los recursos de la identidad (CSS y fuentes) contra 50 KB y los suma a la primera carga (`s5.1`, `s5.7`) |
| comprobación de contraste ≥ 7:1 (script del proyecto) | create | criterio 2 del encargo, que el instrumento del addon no cubre (`s5.1`, `s5.3`, `s5.5`) |
| `src/orquidea/web/static/identidad.css` (y fuentes, si las hay) | create | la hoja que viste la interfaz con los tokens de `DESIGN.md` (`s5.7`) |
| `src/orquidea/web/templates/*.html` | modify | enlazar la hoja en `base.html`, quitar estilos en línea, clases donde haga falta (`s5.7`) |
| `tests/test_medicion.py`, `tests/test_web_coleccion.py` | modify | medición con CSS y fuentes; la prueba que afirmaba el estilo en línea (`s5.1`, `s5.7`) |

## Key contracts

- Una pieza se deriva de otra solo cuando el ADR de la anterior está `accepted` (convención del encargo: un insumo cuenta cuando su fase está `complete`).
- El ADR de cada pieza se commitea en `proposed` antes del primer commit que la produce; los criterios y sus estratos no cambian después sin dejar su diff.
- Cada criterio de pieza declara de dónde viene: derivado de un criterio del encargo (por su número) o propio de la pieza.
- `contrast` nunca se mide sobre una marca; aquí no hay marca (no-go del brief).
- Toda comprobación escrita para el encargo cuenta la población que midió y se pone en rojo si es cero.
- Cada mitad juzgada lleva nombre y fecha del humano, o se escribe `unsigned`; el agente nunca la firma.
- `DESIGN.md` se genera, nunca se edita a mano; un cambio va a la regla o a un parámetro y se regenera.
- La hoja de estilos usa solo valores que son tokens de `DESIGN.md`.
- Ninguna ruta, formulario ni dato cambia: la suite de comportamiento sigue verde sin tocarla (salvo la afirmación del estilo en línea).
- Las fuentes se sirven desde `/static`; la CSP no cambia.

## Decisions (ADRs)

- Ninguno a nivel de épica. Las decisiones de esta épica son las de cada pieza, y cada una tiene su propio ADR abierto por su historia (ADR-009 en s5.1; los siguientes números los toma cada historia en orden). Cómo se escribe y se comprueba la hoja de estilos (a mano con prueba de tokens, frente a generarla) se decide en el diseño de s5.7, la única historia que depende de ello.

## Legacy sweep

- Los cuatro estilos en línea de las plantillas desaparecen en s5.7.
- `tests/test_web_coleccion.py:239` afirma `style="white-space: pre-line"`: es la única prueba que queda huérfana, y s5.7 la cambia para afirmar el comportamiento (las notas conservan sus saltos de línea) en lugar del estilo.
- `'unsafe-inline'` en `style-src` deja de ser necesario cuando no quedan estilos en línea; se aparca y no se quita en esta épica.
