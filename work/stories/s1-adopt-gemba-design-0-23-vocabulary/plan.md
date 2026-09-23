# Story s1: Adopt the gemba-design 0.23.0 vocabulary — Plan

> Size: L
> Pause: none (default) — salvo las paradas del ciclo: la elección forzada de V3 y V4 (T4) y el recorrido de los dos juicios (T8) son del humano

Aprobación del humano (2026-09-23, en sesión): V1–V4 tal como están en `design.md`, y la sustitución parcial recomendada. ADR-013, ADR-014 y ADR-015 quedan `accepted`; ADR-016 nombra cada decisión que reemplaza, y el hueco del método va al parking lot.

El tamaño es L porque la historia junta el vocabulario nuevo con cuatro entradas del parking lot. No se parte: las cuatro tocan la misma hoja y el mismo `DESIGN.md`, y partirlas regeneraría el archivo dos veces.

## Container acts around the tasks

- **A0 · Abrir ADR-016** (`records/decisions/adr-016-vocabulario-de-gemba-design-0-23.md`, molde `adr-014-escala-espaciado-componentes.md`). Lleva:
  - la pregunta;
  - V1–V4 con su estrato y su origen, y los criterios del catálogo aplicados;
  - las decisiones que reemplaza: la 6 de ADR-014 (ASCII), el `--gap` de bordes de ADR-014 y la 3 de ADR-015 (esquinas sin token);
  - el renombre, con sus opciones rechazadas;
  - las catorce dimensiones con la respuesta propuesta para cada una;
  - las candidatas del diseño con **todos sus parámetros fijados**: mínimo de control (A) fijo, (B) solo mínimo, (C) los dos; medida (A) sin tope, (B) `34em`, (C) `40em`; elevación (A) tono y borde, (B) solo tono, (C) solo borde; sangría (A) sin relleno horizontal fuera de la cabecera, (B) como está; y el nivel único de radio `recto: 0px`.

  La rejilla lleva `pending: measured when run` y `## Decision` queda sin resolver. Se commitea antes de cualquier script o valor. `docs(s1): add ADR-016`.
- **A1 · Correr las candidatas y ver los rojos** (tras T1 y T2), hacia el scratchpad, con la salida copiada literal:
  - V2: `comprobar-medidas.py objetivos` sobre un `DESIGN.md` de la candidata (B) con un mínimo bajado a `spacing.step-4` (32 px).
  - V1: el chequeo de dimensiones sobre un `components.md` al que le falta `measure`.
  - `provenance`: sobre un `DESIGN.md` editado a mano con un `minWidth` que no nombra su escalón.
  - V3 y V4: "no aplica, no hay oráculo"; se juzgan en T4.

  Los rojos y la rejilla se llenan sin tocar criterios ni parámetros. `docs(s1): update ADR-016`.
- **A2 · Completar ADR-016** a `accepted` tras T7, en el mismo archivo y con el mismo número. `docs(s1): publish ADR-016`.

## Tasks

### T1 · `objetivos` mide también los mínimos declarados

- **Files:** modify `scripts/comprobar-medidas.py` y `tests/test_comprobar_medidas.py`.
- **TDD:**
  - RED:
    - una fila `components.boton.minWidth | 48px | spacing.step-6` y otra `…minHeight…` en la tabla `Token | Value | From`, sin tabla `Target`, se cuentan como un objetivo y se juzgan contra el mínimo;
    - un mínimo bajo el umbral sale con 1 y nombra componente y dimensión;
    - un componente que declara solo `minWidth` juzga esa dimensión y dice que la otra no se midió;
    - sin tabla `Target` y sin mínimos, sale con 2 como hoy.
  - GREEN: `objetivos` junta los objetivos de la tabla `Target` y los de los mínimos, agrupados por componente.
  - REFACTOR.
- **Satisfies:** V2, y el escenario del diseño "un componente con `minWidth` y sin `width`".
- **Mold:** `scripts/comprobar-medidas.py::objetivos` y `_filas` (misma forma, mismas salidas 0/1/2 con la población contada), y la tabla `Token | Value | From` que escribe `design-md.py` de 0.23.0 (vista en la sonda: `components.campo.minWidth | 48px | spacing.step-6`).
- **Verify:** la propiedad es que un mínimo declarado bajo el umbral no pasa, y que una población vacía no da verde. Mutaciones que deben poner rojo:
  - revertir el cambio: el objetivo declarado solo con mínimos no se cuenta, y la prueba de población falla;
  - `<` por `<=` en la comparación, con un mínimo de exactamente 44 (la prueba de frontera);
  - leer solo `minWidth` e ignorar `minHeight`, con un `minHeight` de 32;
  - borrar la tabla `Token | Value | From` del caso de prueba: sale con 2, no con 0.

  Después, `uv run pytest tests/test_comprobar_medidas.py` y `./scripts/check`.
- **Commit:** feat(identity): measure the declared control minimums

### T2 · El chequeo de dimensiones (V1)

- **Files:** create `scripts/comprobar-dimensiones.py` y `tests/test_comprobar_dimensiones.py`.
- **TDD:**
  - RED:
    - con un catálogo de prueba de tres dimensiones con destino `ui` y un entregable que responde las tres, sale con 0 y cuenta 3;
    - con una sin responder, o con la celda vacía, sale con 1 y la nombra;
    - una dimensión respondida que el catálogo no tiene sale con 1;
    - un catálogo sin dimensiones `ui` o un entregable sin la tabla sale con 2.
  - GREEN, y REFACTOR.
- **Uso:** `comprobar-dimensiones.py CATALOGO.md ENTREGABLE.md`. Lee las claves con destino `ui` de la tabla `Dimension | … | Destination` del catálogo, y la tabla `Dimension | Answer | Where` del entregable.
- **Satisfies:** V1, y el escenario "sin la respuesta de `measure`".
- **Mold:** `scripts/contraste-de-lectura.py` (0/1/2, población contada, `nada juzgado`) y `tests/test_comprobar_medidas.py` (carga por `importlib`, casos en `tmp_path`).
- **Verify:** la propiedad es que cada dimensión `ui` del catálogo tiene una respuesta no vacía, y que ni una lista vacía ni un catálogo sin sujeto dan verde. Mutaciones que deben poner rojo:
  - revertir el cambio;
  - aceptar una celda de respuesta que solo tiene espacios;
  - comparar solo en un sentido (dimensiones del entregable ⊆ catálogo), con una que falte;
  - quitar la tabla del catálogo de prueba: sale con 2, no con 0.

  Después, `./scripts/check` **completo**, porque son archivos nuevos que el gate escanea.
- **Límite declarado:** el catálogo vive en el plugin, fuera del repositorio. La comparación con el catálogo real se corre a mano con su ruta y la salida se copia en ADR-016, igual que la regeneración de `DESIGN.md` (ADR-014). No se vendoriza una copia de la lista, porque sería una segunda fuente.
- **Commit:** feat(identity): check that every interface dimension is answered

### T3 · Tokens en español

- **Files:**
  - modify `governance/identity/ui/semantics.md`: `linea` → `línea`, `accion-*` → `acción-*` en sus tres tablas y en el texto que los cita como identificador; `decision: ADR-013, ADR-016`;
  - modify `governance/identity/ui/components.md`: las referencias `{colors.accion-*}`; `decision: ADR-014, ADR-016`;
  - regenerar `governance/identity/ui/DESIGN.md` con 0.23.0 y el comando de ADR-014, más `--decision "ADR-016: …"`;
  - modify `src/orquidea/web/static/identidad/identidad.css`: `:root` y cada `var()`.
- **TDD:** RED: con `DESIGN.md` regenerado y la hoja sin tocar, `test_la_hoja_usa_solo_tokens_de_la_identidad` nombra `--colors-linea no es un token` y `falta en :root el token --colors-línea`. GREEN: se renombra la hoja.
- **Satisfies:** el `@stated` de los roles en español, y el `@deduced` de la hoja confirmado en el diseño.
- **Mold:** T1 de s5.6 (`work/epics/e5-visual-identity/stories/s5.6-scale-spacing-components/plan.md`), el mismo renombre en sentido contrario.
- **Verify:** la propiedad es que los mismos 13 roles con los mismos valores pasan sus umbrales, y que ningún identificador ASCII viejo queda en las tablas ni en la hoja.
  - Números esperados: `contraste-de-lectura.py` con 10 y 8 pares y 0 bajo; `tokens.py pairs` con 22 y 8, 0 bajo; `provenance` con 12, 0 fuera.
  - `grep -nE 'colors-linea|accion-(fondo|texto|presionada)|\blinea\b'` sobre la hoja y `governance/identity/ui/`: 0 líneas.
  - Mutaciones que deben poner rojo:
    - dejar `--colors-accion-fondo` en `:root`;
    - dejar un `var(--colors-linea)` en una regla (nombra `var(--colors-linea) no está declarada`);
    - dejar `{colors.accion-fondo}` en `components.md`: el generador sale `refused`, exit 1.

  Después, `./scripts/check`.
- **Commit:** refactor(identity): name the tokens in Spanish

### T4 · Láminas de juicio para V3 y V4

- Tras A1: páginas HTML en el scratchpad, servidas con la hoja real:
  - V3: la ficha de un ejemplar con notas largas, a 1280 y a 360 px, con cada candidata de medida;
  - V4: la colección con tres tarjetas a 360 px, con cada candidata de elevación.

  Se le muestran al humano en el navegador (memoria "Capturas a 360 px en Chrome de Windows").
- **Verify:** cada lámina nombra su candidata, y nada entra al repositorio.
- **Parada:** la elección y la firma de V3 y V4 son del humano. La sangría (A/B) se muestra en la misma lámina de la colección.
- Sin commit.

### T5 · Vocabulario de 0.23.0 en `components.md`, y `DESIGN.md` regenerado

- **Files:**
  - modify `governance/identity/ui/components.md`:
    - una tabla `Level | Value | Where` con `recto | 0px | …`;
    - columnas `rounded` (en `boton`, `boton-presionado`, `campo` y `tarjeta`), `borderColor` (`campo` → `campo-borde`, `tarjeta` → `línea`), y `minHeight`/`minWidth` según la elección de A1 (con la (B), se borran `height`/`width`);
    - la tabla `Dimension | Answer | Where` con las catorce respuestas;
    - la nota de que `error` como borde no tiene componente;
  - regenerar `DESIGN.md`, con un `--gap` por cada dimensión que el formato no lleva (trazo, elevación, medida, retícula y densidad; la iconografía ya la trae el generador);
  - modify `tests/test_identidad_hoja.py`: el lector de tokens aprende `rounded`;
  - modify `identidad.css`: `--rounded-recto` en `:root`, y `border-radius: var(--rounded-recto)` en campo, botón y tarjeta.
- **TDD:**
  - RED: `test_el_lector_de_design_md_encuentra_los_tokens` pide `tokens["--rounded-recto"] == "0px"`; con `DESIGN.md` regenerado, `test_la_hoja_usa_solo_tokens…` nombra `falta en :root el token --rounded-recto`.
  - GREEN: el lector y la hoja.
  - `test_identidad_ui.py` añade la corrida de `comprobar-dimensiones.py` **sobre la tabla del entregable**: 14 filas, 0 vacías. La comparación con el catálogo es la manual de T2.
- **Satisfies:** el `@stated` de radio, `borderColor` y `minWidth`; V1, V2 y la regeneración idéntica.
- **Mold:** la plantilla `assets/components.md` de 0.23.0 (columna `rounded`), la sonda de la survival-review (`rounded.none`, `borderColor`, `minWidth` aceptados) y T4 de s5.6.
- **Verify:** la propiedad es que `DESIGN.md` sale del generador, que cada cifra recalculada coincide con la de e5 o queda anotada en ADR-016, y que el número de propiedades fuera del vocabulario es exactamente el declarado.
  - Sobre lo regenerado, cada uno en 0 con su población:
    - `tokens.py pairs`, `targets` (sin sujeto con la (B): se dice, no se pasa) y `provenance`;
    - `contraste-de-lectura.py`;
    - `comprobar-medidas.py objetivos --minimo 44` y `piso`;
    - `comprobar-dimensiones.py` con el catálogo del plugin.
  - Stderr del generador: `N unrecognised component properties accepted`, con N contado de la tabla (`borderColor` × 2, más los mínimos × 4 × 2 con la (B)).
  - Mutaciones que deben poner rojo:
    - bajar a mano en `DESIGN.md` un `minWidth` a 32 (T1);
    - quitar `measure` de la tabla de dimensiones (T2);
    - escribir `border-radius: 0` en la hoja en lugar del token no la pone en rojo, porque `0` está admitido: **se dice, no se supone**, y queda como límite de la prueba en ADR-016.

  Después, `./scripts/check` completo.
- **Commit:** docs(identity): declare the interface in the 0.23.0 vocabulary

### T6 · Medida, elevación, sangría y el botón de Acceso

- **Files:**
  - modify `identidad.css`: la medida elegida en `main` (`max-width` en `em`) si V3 eligió (B) o (C); la elevación elegida en `.tarjetas > li`; la sangría elegida en `.accion` fuera de la cabecera;
  - modify `tests/test_identidad_hoja.py`: `ADMITIDOS` añade el literal de la medida, solo en `max-width`;
  - modify `src/orquidea/web/templates/acceso.html`: los controles envueltos en `<p>`.
  - Prueba nueva en `tests/`: el formulario de Acceso envuelve su campo en `<p>`.
- **TDD:**
  - RED: la prueba de Acceso falla hoy. La lista cerrada nombra `literal 34em` hasta que ADR-016 lo admita.
  - GREEN, y REFACTOR.
- **Satisfies:** V3 y V4 aplicados; las dos decisiones escritas del parking lot.
- **Mold:** `src/orquidea/web/templates/ejemplar.html:10` (controles en `<p>`) y ADR-015, decisión 2 (lista cerrada de literales).
- **Verify:** la propiedad es que ningún literal entra a la hoja sin estar en la lista de un ADR, y que el campo de Acceso va dentro de un párrafo. Mutaciones que deben poner rojo:
  - revertir la plantilla;
  - envolver el botón en `<p>` pero dejar el campo suelto (una forma equivalente del defecto);
  - admitir el literal de la medida en cualquier propiedad, con `padding: 34em` en un caso de prueba.

  Después, `./scripts/check`.
- **Commit:** fix(web): apply the measure, elevation and spacing adjustments

### T7 · Parking lot

- **Files:** modify `records/parking-lot.md`.
  - Retirar:
    - "`design-md.py` solo acepta referencias ASCII" — su promoción se cumplió con 0.23.0;
    - "La interfaz vestida de e5 tiene dos juicios sin firmar y dos ajustes…" — se retira tras T8, con lo que citaba cada una.
  - Aparcar:
    - `precedence.py` no puede leer el `DESIGN.md` que genera el mismo addon;
    - la técnica `adr` no tiene sustitución parcial.
- **TDD:** no aplica, porque es un documento; lo verifica el chequeo del parking lot del gate.
- **Mold:** la técnica `park` (retirar respondiendo lo que citaba cada entrada) y las entradas de e5 del addon.
- **Verify:** la propiedad es que ninguna entrada sale sin responder quién la citaba. `grep -rn` del texto de cada entrada retirada sobre `work/` y `records/` devuelve solo citas históricas. Después, `./scripts/check`.
- **Commit:** docs(parking-lot): retire the e5 entries and park the addon findings

### T8 · Recorrido del humano, `survival-review` y prueba de integración manual

- **Recorrido a 360 px** con la aplicación corriendo bajo uvicorn (sesión con `curl`, iframe de 360, según las memorias):
  - el humano firma o rechaza el criterio 3 de ADR-009 (la foto como protagonista) y la decisión 5 de ADR-015 (el subtítulo frente al cuerpo);
  - la firma, con nombre y fecha, queda en ADR-016 (antes de A2) y en la sección juzgada de `components.md`;
  - no se firma en nombre del humano.
- **`survival-review`** sobre `semantics.md`, `components.md` y `DESIGN.md`. Su `## When` ("a technique of this addon has produced a piece") se cumple tras T5 y T6. `precedence.py` sobre las piezas que citan ADR-016 tiene que dar PASS; `DESIGN.md` sigue `unreadable`, lo que es el hallazgo aparcado en T7.
- **Regenerar `DESIGN.md` dos veces** desde el árbol limpio: las dos salidas y el archivo commiteado tienen que ser idénticos (`cmp`).
- **Orden por fecha de autor:** `add ADR-016` → T1 → T2 → `update ADR-016` → T5 → `publish ADR-016`.
- **Verify:** `cmp` sin diferencias; los instrumentos en 0 con su población; los dos juicios firmados o rechazados; la aplicación sirve cada página con la hoja y sin errores en consola.

## Order & risks

- **Execution order:** A0 → T1 → T2 → A1 → T3 → T4 (elección) → T5 → T6 → T8 (recorrido y firmas) → A2 → T7 → T8 (resto).
  - T1 y T2 van primero: son los dos instrumentos propios, y sin ellos A1 no tiene con qué ver sus rojos.
  - T3 va antes de T5 para que el vocabulario nuevo se componga ya con los nombres en español.
- **Dependencies:** secuenciales. A0 va antes de T1, porque los parámetros se fijan antes de que exista la herramienta que los mide.
- **Risks:**
  - **Un identificador con acento rompe algo que la sonda no probó**: el lector de la prueba, un `var()` en el navegador, `tokens.py pairs` con el rol en la tabla de pares. Mitigación: T3 corre todos los instrumentos y la hoja se sirve y se ve en T8.
  - **La (B) del mínimo deja a `tokens.py targets` sin sujeto**, así que `target-size` (SC 2.5.8) solo lo mide el script propio. Mitigación: se dice en la pieza y en la review. Si se ve como pérdida, la (C) está en la rejilla.
  - **El chequeo de V1 depende del catálogo del plugin.** Mitigación: corrida manual registrada; el gate prueba el comportamiento y la tabla del entregable.
  - **Escribir una cifra sin correr su comando.** Mitigación: cada cifra se copia de la salida vista (memoria "Cifras de retrospectiva de la salida del comando").
  - **Una mutación de frontera sin entrada exacta sobrevive.** Mitigación: T1 lleva un caso de exactamente 44 (memoria "Mutación de frontera en el predicado").
