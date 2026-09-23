# Epic e5: Visual identity — Scope

## Objective

El coleccionista usa Orquídea en el teléfono, en campo, con una interfaz legible bajo el sol y con red lenta, en la que la foto de cada ejemplar es la protagonista, en lugar de las plantillas sin estilo de hoy.

**Value:** la aplicación deja de verse como un prototipo; cada valor visual sale de una escala declarada y juzgada contra un criterio que se commiteó antes de producirla, así que un cambio futuro de color o de tipo se hace en la regla y se vuelve a derivar, no se parcha a mano.

## Stories

| ID | Story | Size | Description |
|----|-------|:----:|-------------|
| s5.1 | Criterio del encargo | S | ADR-009 en `proposed` con el catálogo de supervivencia resuelto y las tres adecuaciones aprobadas el 2026-09-22, las comprobaciones de peso (≤ 50 KB) y de contraste (≥ 7:1) escritas con TDD y vistas fallar, y `governance/identity/commission.md`. |
| s5.2 | Concepto | S | Elige la dirección común de la identidad entre un número de direcciones declarado antes, contra criterios derivados del encargo, y registra por qué cayó cada una (`concept.md`). |
| s5.3 | Paleta | S | Paleta por roles (fondo, texto, acento, estados) producida contra su criterio commiteado antes, con los pares de texto medidos a ≥ 7:1 (`palette.md`). |
| s5.4 | Tipografía | M | Familia o pila de sistema elegida contra su criterio, con itálica verdadera para nombres científicos, glifos es-MX, piso de legibilidad leído de su fuente y licencia registrada (`specimen.md`). |
| s5.5 | Roles de color de la interfaz | S | Primitivas y roles semánticos derivados de la paleta por una regla declarada, con contraste de texto y de componentes medido en los valores reales (`primitives.md`, `semantics.md`). |
| s5.6 | Escala, espaciado, componentes y DESIGN.md | M | Escala tipográfica, espaciado con controles de ≥ 24 px y componentes como composición de referencias; `DESIGN.md` generado y verificado con `pairs`, `targets` y `provenance`. |
| s5.7 | Aplicar la identidad a las plantillas | M | Una hoja de estilos servida desde `/static` que usa solo los tokens de `DESIGN.md`, enlazada en `base.html`, sin estilos en línea, y la medición de la primera carga ampliada con CSS y fuentes. |

Dependencias: s5.2 de s5.1; s5.3 y s5.4 de s5.2 (y entre sí independientes); s5.5 de s5.3; s5.6 de s5.4 y s5.5; s5.7 de s5.6. Sin ciclos. Cada pieza depende de que la anterior esté `complete` (su ADR `accepted`), no solo de que exista el archivo (convención del encargo).

## In scope

- **MUST:** el criterio del encargo commiteado antes de cualquier pieza, con las comprobaciones medibles vistas en rojo; paleta, tipografía y los cinco eslabones de UI, cada uno con su ADR abierto en `proposed` y completado a `accepted`; `DESIGN.md` generado desde las tablas; todas las plantillas vestidas con la hoja de estilos derivada; `survival-review` sobre cada pieza producida; recursos de la identidad ≤ 50 KB gzip y primera carga dentro de `must-perf-001`.
- **SHOULD:** concepto común antes de las piezas (s5.2); la medición de peso de la identidad dentro del gate, no solo como script.

## Out of scope

- Quitar `'unsafe-inline'` de `style-src` en la CSP — al quitar los estilos en línea en s5.7 se vuelve posible, pero es una decisión de seguridad con su propia prueba — **not now**: parking lot.
- Tema oscuro o varios temas — rabbit hole del brief — **not now**.
- Cadena de construcción de CSS o generación automática de la hoja desde `DESIGN.md` — rabbit hole del brief; s5.7 escribe la hoja a mano y una prueba compara sus valores con los tokens — **not now**.
- Biblioteca de componentes más allá de lo que usan las plantillas actuales — rabbit hole del brief — **not now**.
- Logotipo, favicon, ícono de plataforma — no-go del brief — **never**.
- Cualquier cambio de comportamiento (rutas, formularios, datos) — no-go del brief — **never**.
- El título roto de "Mi colección" (el bloque `title` contiene un `<p><a>`, reproducido el 2026-09-22) — es un defecto existente, no parte de vestir la interfaz — va por el flujo de bug antes de s5.1.

## Done when

- [stated] El ADR del encargo está commiteado en `proposed` antes de la primera pieza, y las comprobaciones de los criterios 1 (peso) y 2 (contraste ≥ 7:1) se vieron en rojo sobre un sujeto que los viola (métrica líder del brief).
- [stated] Todas las plantillas usan la identidad; `survival-review` pasa sobre cada pieza (`contrast`, `component-contrast`, `target-size`, `provenance`); los recursos de la identidad pesan ≤ 50 KB gzip y la primera carga sigue dentro de `must-perf-001` (métrica rezagada del brief). El peso en bytes lo mide un script; la medición con "Slow 3G" en el navegador solo la puede hacer el humano: **stop previsible** en `epic-review`.
- [stated] El criterio 3 (la foto es la protagonista) y la mitad juzgada de cada pieza tienen nombre y fecha del humano que los juzgó, o quedan escritos `unsigned` y contados como sin responder: **stop previsible** en cada historia que produce una pieza.
- [deduced] Cada ADR de pieza (s5.1 a s5.6) tiene su commit en `proposed` con fecha de autor anterior a la del primer commit que produce la pieza; se verifica con `git log`, no con la etiqueta.
- [deduced] `DESIGN.md` se genera con `design-md.py` desde las tablas de los entregables; regenerarlo produce el mismo archivo.
- [deduced] Todo valor de la hoja de estilos (color, tamaño, espacio) es un token de `DESIGN.md`; una prueba lo comprueba y se pone en rojo con un valor inventado.
- [deduced] Ninguna plantilla conserva un atributo `style`; ninguna prueba de comportamiento cambia salvo la que afirmaba ese estilo en línea (`tests/test_web_coleccion.py`).
- [deduced] Las fuentes, si las hay, se sirven desde `/static`: la CSP actual (`default-src 'self'`) no cambia.
- [stated] All stories complete · docs updated · retrospective done

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| Una fuente web se come el presupuesto de 50 KB | M | M | El criterio 1 se mide antes de elegir en s5.4; la pila de sistema es una opción real en la rejilla del ADR, no un último recurso |
| Las firmas del humano (criterio 3, mitades juzgadas, elección del concepto) frenan la épica o se firman en automático | H | M | Previstas como stops desde este diseño; pedir pocas y en elección forzada (convención del ciclo); nunca rellenar una firma |
| Los instrumentos del addon viven en la caché del plugin y el de contraste tiene el umbral fijo en 4.5:1 | H | L | La comprobación de 7:1 se escribe en el proyecto con TDD en s5.1; los instrumentos del addon se invocan por su ruta y se anota la versión |
| El contraste ≥ 7:1 deja pocas opciones de acento y la paleta sale apagada | M | L | Se aplica solo al texto de lectura corrida; el acento en componentes responde a `component-contrast` (3:1) |
| La medición con "Slow 3G" depende del humano (pasó en e1 a e4) | H | M | Stop previsto en `epic-review`; el peso en bytes se mide por script en s5.7 |
