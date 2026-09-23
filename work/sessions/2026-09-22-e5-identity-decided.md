# Session 2026-09-22 — e5: identidad decidida

## Done

- b1 (título de "Mi colección" con un `<p><a>` dentro) de punta a punta, publicado a `origin/develop` (`3f05425`), con prueba de regresión que localiza el `<title>` y cuenta el enlace.
- Épica e5 · Visual identity abierta, diseñada y planeada (7 historias); CSP `'unsafe-inline'` y prueba de títulos de todas las páginas, aparcadas para s5.7.
- s5.1 encargo: ADR-009 (peso ≤ 50 KB, texto normal ≥ 7:1, la foto protagonista) y dos instrumentos nuevos — `medir-primera-carga.py --identidad DIR` y `scripts/contraste-de-lectura.py`, ambos con salida 0/1/2.
- s5.2 concepto: ADR-010, **Cuaderno de campo**.
- s5.4 tipografía: ADR-011, **fuentes del sistema** (`system-ui…`), 0 KB, piso de 16 px para todo texto.
- s5.3 paleta: ADR-012, **papel cálido, azul tinta** (`#F7F3EA`, `#FFFFFF`, `#1E1C19`, `#4A453E`, `#8C8475`, `#1F3A5F`, `#8A1C1C`).
- Hito "identidad decidida" alcanzado; `governance/identity/` tiene commission, concept, specimen y palette, todos con la mitad juzgada firmada por el humano.

## Decided

- Encargo completo en una épica, no pieza suelta — **why:** el humano quiso traza y rama; el encargo da un criterio común a las cuatro piezas.
- Criterio 2 aplica a todo texto de tamaño normal — **why:** el texto pequeño (fechas, fuentes) es el que se lee bajo el sol.
- S3 del concepto: mobile first con patrones de redes (foto a todo el ancho, navegación al pulgar, acciones grandes), sin métricas ni scroll infinito — **why:** pedido del humano; ningún flujo nuevo por el no-go del brief.
- Fuentes del sistema en lugar de una fuente web — **why:** ninguna web cabe en 40 KB con negrita propia (56–93 KB medidos); el carácter lo pone la estructura.
- Enlaces subrayados — **why:** con tinta casi negra y un acento a 7:1, acento contra tinta da 1.48:1.
- b1 hecho en sesión, no delegado — **why:** R1 solo deja delegar la ejecución de un bug, y aquí era una línea.

## Open

- El piso de 16 px depende de dos parámetros no medidos (35 cm, 160 px CSS/pulgada); se revisa con un ADR nuevo si en s5.7 la lectura en el teléfono dice otra cosa.
- Siguen del 2026-09-19: regla de popularidad y cuidados por género del catálogo; primer `docker build` y despliegue en Dokploy con la medición en Slow 3G.

## Next

Arrancar s5.5 (roles de color de la interfaz) con `story-start`: primitivas y roles semánticos derivados de `governance/identity/palette.md` por una regla declarada, técnica `ui` de gemba-design.

## State

Branch `develop` · work item in flight: none (e5 abierta, s5.1–s5.4 cerradas) · tree: clean · `develop` con 41 commits locales sin push, que viajan con `epic-close` de e5.
