# Story s5.7: Apply the identity to the templates — Plan

> Size: M
> Pause: none (default) — salvo la parada del recorrido renderizado, donde el humano juzga el criterio 3 de ADR-009 y el subtítulo

Aprobación del humano (2026-09-22, en sesión): las cinco decisiones de `design.md` para ADR-015, tal como están.

## Container acts around the tasks

- **A0 · ADR-015** (`records/decisions/adr-015-hoja-de-estilos.md`, molde `adr-011-sistema-tipografico.md` en su forma aceptada). Se escribe de una vez en `accepted`, porque las decisiones ya están tomadas y aprobadas y ninguna depende de medir candidatas. Lleva las cinco decisiones con sus alternativas y la lista cerrada de excepciones. `docs(s5.7): add ADR-015`.

## Tasks

### T1 · La hoja de estilos y su prueba de tokens

- **Files:** create `src/orquidea/web/static/identidad/identidad.css` y `tests/test_identidad_hoja.py`.
- **TDD:**
  - RED: la prueba lee `DESIGN.md` (lector de *frontmatter* de dos niveles) y la pila de `specimen.md`, y comprueba:
    - cada propiedad de `:root` nombra un token existente y lleva su valor;
    - todo `var(--x)` usado está declarado;
    - fuera de `:root` no hay `#hex` ni medida con unidad, salvo la lista de ADR-015;
    - la población de `:root` no es cero.

    Falla porque la hoja no existe.
  - GREEN: la hoja con los tokens y las reglas de los diez componentes.
  - REFACTOR.
- **Satisfies:** `@stated` de tokens con rojo visto; ADR-015, decisiones 1–3.
- **Mold:** `tests/test_identidad_ui.py` (lee un entregable del repositorio sin regenerarlo); `governance/identity/ui/components.md` (qué compone cada componente).
- **Verify:** la propiedad es que cada valor de la hoja viene de un token o de la lista cerrada. Mutaciones que deben ponerla en rojo:
  - `--colors-fondo` con otro hex;
  - `padding: 10px` en una regla;
  - `var(--spacing-step-5)`;
  - `:root` vaciado, que tiene que dar rojo por población cero, nunca verde;
  - la misma medida escrita de otra forma legal, `0.625rem` en lugar de `10px`.

  Después, `./scripts/check` completo, porque son archivos nuevos que el gate escanea.
- **Commit:** feat(web): add the identity stylesheet derived from DESIGN.md

### T2 · Vestir las plantillas

- **Files:**
  - modify `src/orquidea/web/templates/base.html`: el `<link rel="stylesheet" href="/static/identidad/identidad.css">` y las clases de la cabecera.
  - modify las nueve plantillas restantes: solo clases, y quitar los siete `style`.
  - add en `tests/test_identidad_hoja.py` la prueba "ninguna plantilla lleva `style=`".
  - modify `tests/test_web_coleccion.py:250`: el `<p class="notas">` que contiene las notas, localizado, no la cadena suelta.
- **TDD:** RED: la prueba de `style=` falla con los siete de hoy; la de notas, reescrita para localizar el `<p class="notas">`, falla. GREEN: clases en las plantillas y reglas en la hoja. REFACTOR.
- **Satisfies:** `@stated` de "ninguna plantilla con `style`", "ninguna prueba de comportamiento cambia salvo la del estilo en línea" y "`base.html` enlaza la hoja".
- **Mold:** las plantillas existentes (estructura sin cambios); ADR-015 decisión 4 (lista con miniatura de 96 × 96).
- **Verify:** la propiedad es que ninguna plantilla lleva estilo en línea y que el comportamiento no cambia. Mutaciones:
  - volver a poner un `style="display: inline"`: rojo;
  - poner la clase `notas` en otro elemento, fuera del que contiene las notas: rojo en la prueba de notas;
  - quitar el `<link>`: rojo en una prueba que lo afirme en `base.html` servido.

  `git diff --stat tests/` tiene que mostrar solo `test_web_coleccion.py` y `test_identidad_hoja.py`. Después, `./scripts/check`.
- **Commit:** feat(web): dress the templates with the identity stylesheet

### T3 · Prueba de títulos de todas las páginas

- **Files:** create `tests/test_web_titulos.py`.
- **TDD:** RED: con la lista de páginas incompleta, la prueba de cobertura falla, nombrando las rutas GET que faltan. GREEN: la lista completa, con los datos que cada página necesita (sesión, especie, ejemplar con riego y floración). REFACTOR.
- **Satisfies:** `@deduced` de títulos (parking lot, clase de b1).
- **Mold:** `tests/test_web_proteccion.py` (uso de `rutas_registradas`, sesión de prueba); `tests/fabricas.py`.
- **Verify:** la propiedad es que todo `<title>` de página es texto sin `<` ni `>`, y que ninguna ruta GET HTML queda fuera. Mutaciones:
  - poner un `<a>` dentro del bloque `title` de una plantilla (la forma de b1): rojo, nombrando la página;
  - quitar una página de la lista: rojo por cobertura;
  - la prueba localiza el `<title>` antes de juzgarlo, así que un HTML sin `<title>` tiene que dar rojo, no verde.

  Después, `./scripts/check`.
- **Commit:** test(web): check the title of every page

### T4 · La medición con el CSS contado

- **Files:** modify `scripts/medir-primera-carga.py` (campo `javascript` → `estaticos`, línea "JavaScript y CSS (gzip)") y `tests/test_medicion.py` (el nombre del campo).
- **TDD:** RED: una prueba de `test_medicion.py` afirma que `estaticos` incluye el CSS enlazado, porque es mayor que el solo htmx y la hoja aparece entre lo medido. Falla hasta renombrar. GREEN: el renombre. REFACTOR.
- **Satisfies:** `@stated` de la medición con el CSS contado.
- **Mold:** `scripts/medir-primera-carga.py` tal como está.
- **Verify:** la propiedad es que lo medido incluye la hoja. Mutación: con el patrón de `/static` restringido a `src=`, la hoja deja de contarse: rojo. Después, correr y copiar las salidas: `medir-primera-carga.py --identidad src/orquidea/web/static/identidad` (≤ 50 KB), `medir-primera-carga.py` (≤ 200 KB) y `./scripts/check`.
- **Commit:** feat(medicion): count the stylesheet in the first load

### T5 · Recorrido renderizado y prueba de integración manual

- Levantar la aplicación con `uvicorn` y datos de ejemplo. Recorrer a 360 px de ancho: inicio, acceso, catálogo, especie, colección, ficha con foto, riegos y floraciones, alta y confirmar baja. Capturas al scratchpad.
- Comprobar en lo renderizado lo que ninguna prueba mide:
  - el anillo de foco al tabular;
  - el botón presionado;
  - los formularios en línea de la ficha a 360 px;
  - que la CSP no bloquee la hoja (consola sin errores).
- **Parada:** el humano juzga el criterio 3 de ADR-009 (la foto es la protagonista) y el subtítulo de 20 px frente al cuerpo. Firma o `unsigned`.
- Apagar el servidor por PID y comprobar con `curl` (memoria `pkill-f-mata-su-propio-comando`).
- **Verify:** capturas vistas, consola sin errores de CSP, juicio firmado o `unsigned`.

## Order & risks

- **Execution order:** A0 → T1 → T2 → T3 → T4 → T5. T1 va primero porque es el instrumento del que dependen las demás. T2 es el cambio más ancho: diez plantillas.
- **Dependencies:** T2 depende de T1 (las clases viven en la hoja), T4 de T2 (el `<link>` tiene que existir) y T5 de todo. T3 es independiente.
- **Risks:**
  - La prueba de tokens acepta un literal escrito de otra forma (`rem`, `em`, `%` fuera de la lista, `rgb()`) → mutación de la forma equivalente en T1; el patrón de literales cubre unidades y funciones de color.
  - Un selector de clase cambia algo que una prueba de comportamiento mira → `git diff --stat tests/` en T2.
  - Los formularios en línea no caben a 360 px → la hoja envuelve y no encoge; se ve en T5.
  - El recorrido necesita al humano (el teléfono o el navegador) → las capturas se hacen antes y la parada pide solo el juicio.
