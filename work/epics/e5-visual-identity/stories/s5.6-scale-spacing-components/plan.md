# Story s5.6: Scale, spacing, components and DESIGN.md — Plan

> Size: M
> Pause: none (default) — salvo la parada del ciclo para la elección firmada por el humano (M4)

Aprobación del humano (2026-09-22, en sesión): opción (a) de identificadores ASCII, M1–M4, los componentes de `design.md` y las candidatas (A), (B), (C) de escala y de espaciado, tal como están.

## Container acts around the tasks

- **A0 · Abrir ADR-014** (`records/decisions/adr-014-escala-espaciado-componentes.md`, molde `adr-013-roles-de-color.md`): la pregunta, M1–M4 con su estrato y su origen, y los criterios del catálogo aplicados. También la decisión de identificadores ASCII con sus opciones rechazadas; los componentes con su composición; las seis reglas con **todos sus parámetros fijados** (base, razón, escalones, redondeo, altura de línea, asignación de roles, función de la unidad, pasos, composición de cada control) y "respaldo: ninguno". La rejilla lleva `pending: measured when run` y `## Decision` queda sin resolver. Se commitea antes de cualquier script o valor. `docs(s5.6): add ADR-014`.
- **A1 · Correr las candidatas y ver los rojos** (tras T2): cada regla con el script hacia el scratchpad, con los componentes de cada combinación y su `DESIGN.md` generado ahí. Se corren `comprobar-medidas.py piso` y `objetivos --minimo 44`, `tokens.py targets` y `provenance` y `contraste-de-lectura.py`, y la salida se copia literal.
  - Rojos que se tienen que ver: M1 sobre la escala (C), M2 y `target-size` sobre el espaciado (C), y `provenance` sobre un componente con un literal.
  - M4: "no aplica, no hay oráculo".
  - La rejilla se llena sin tocar criterios ni parámetros. `docs(s5.6): update ADR-014`.
- **A2 · Completar ADR-014** a `accepted` tras T4, en el mismo archivo y con el mismo número. `docs(s5.6): publish ADR-014`.

## Tasks

### T1 · Identificadores de token en ASCII en `semantics.md`

- **Files:** modify `governance/identity/ui/semantics.md`: `línea` → `linea`, `acción-fondo` → `accion-fondo`, `acción-texto` → `accion-texto`, `acción-presionada` → `accion-presionada`, en las tablas `Role | Value`, `Token | Value | From` y `Foreground | Ground | Kind` y en el texto que los cita como identificador. Se añade una nota que cita ADR-014.
- **TDD:** no aplica, porque es un documento; lo verifican los instrumentos.
- **Satisfies:** pregunta 1 (a) del diseño.
- **Mold:** `governance/identity/ui/semantics.md` tal como lo dejó s5.5.
- **Verify:** la propiedad es que los mismos 13 roles con los mismos valores sigan pasando sus umbrales y que ningún identificador de token lleve un carácter fuera de `[a-z0-9-]`.
  - `contraste-de-lectura.py`: 10 pares, 0 bajo 7:1.
  - `tokens.py pairs`: 22 pares, 0 bajo su umbral.
  - `tokens.py provenance` sobre `primitives.md` + `semantics.md`: 13 tokens, 0 fuera de escala.
  - `grep -P` de identificadores no ASCII en las tablas: 0 líneas.
  - Mutación: dejar un `acción-fondo` en una fila de pares hace que `pairs` salga con 2 (rol que no resuelve).
  - Después, `./scripts/check`.
- **Commit:** docs(identity): use ASCII identifiers for the semantic roles

### T2 · Scripts que derivan y comprueban las medidas

- **Files:** create `scripts/derivar-medidas.py`, `scripts/comprobar-medidas.py`, `tests/test_derivar_medidas.py`, `tests/test_comprobar_medidas.py`.
- **TDD:**
  - RED: pruebas de `escala` (tamaños por razón y redondeo declarado, altura de línea como función declarada, roles al escalón que se les asigna, escalón negativo nombrado `-1`), de `espaciado` (unidad como función de la altura de línea, pasos como múltiplos declarados, nombres de paso) y de la salida en las tablas que lee `design-md.py`.
  - RED: pruebas de `piso` (bajo el piso da 1 y nombra rol, escalón y piso; dos escalones con el mismo tamaño dan 1 y se nombran; sin roles de lectura da 2) y de `objetivos --minimo N` (bajo N en una dimensión da 1 y nombra control y dimensión; sin tabla `Target` da 2; exactamente N pasa).
  - Luego GREEN con el mínimo y REFACTOR.
- **Satisfies:** M1, M2, M3.
- **Mold:** `scripts/derivar-primitivas.py` y `tests/test_derivar_primitivas.py` (misma forma de salida, carga por `importlib`, salidas 0/2) y `scripts/contraste-de-lectura.py` (0/1/2 con la población contada).
- **Verify:** las propiedades son que cada tamaño y paso se reproduce de la regla y que las comprobaciones distinguen rojo del criterio (1) de sin sujeto (2). Mutaciones que deben poner rojo:
  - `>=` por `>` en el piso, con una entrada exactamente en el piso.
  - `>=` por `>` en el mínimo, con un objetivo de exactamente 44.
  - Redondear por truncamiento.
  - Contar un colapso solo cuando los tamaños difieren.
  - Devolver 0 con una población vacía.

  Después, `./scripts/check` completo, porque son archivos nuevos que el gate escanea.
- **Commit:** feat(identity): derive and check the type scale and spacing

### T3 · Lámina de juicio para M4

- Tras A1: una página HTML en el scratchpad por combinación que pase M1–M3, con la ficha de un ejemplar (título, binomio, fechas, historial de riegos, botón "Registrar riego") y el formulario de alta, a 360 px, con los colores de `semantics.md`. Se muestra al humano en el navegador.
- **Verify:** cada lámina nombra su combinación de reglas y nada entra al repositorio.
- **Parada:** la elección y la firma de M4 son del humano.
- Sin commit.

### T4 · Escala, espaciado, componentes y DESIGN.md

- **Files:**
  - create en `governance/identity/ui/`: `type-scale.md`, `spacing.md`, `components.md` y `DESIGN.md` generado.
  - modify `tests/test_derivar_medidas.py` con la prueba de regeneración de las tablas de escala y espaciado.
  - create `tests/test_design_md.py`, que lee `DESIGN.md` del repositorio y corre sobre él `comprobar-medidas.py objetivos --minimo 44`. Lee el archivo generado sin volver a generarlo, así que no depende del plugin.
- **TDD:** RED: la prueba de regeneración y la de objetivos fallan porque los archivos no existen. GREEN: escribir las piezas con la salida de los scripts y generar `DESIGN.md`. REFACTOR.
- **Satisfies:** los `@stated` de `DESIGN.md` verificado con los tres instrumentos, el mínimo de 2.5.8 y la firma; M1–M3, y M4 firmada.
- **Mold:** las plantillas de la técnica `ui`, `governance/identity/ui/primitives.md` y `semantics.md`.
- **Verify:** la propiedad es que `DESIGN.md` sale del generador y que sus tablas pasan los instrumentos.
  - Se corren sobre `DESIGN.md`: `tokens.py pairs`, `targets` y `provenance`, `contraste-de-lectura.py` y `comprobar-medidas.py objetivos --minimo 44`. Todos deben salir en 0, con su población.
  - `comprobar-medidas.py piso` sobre `type-scale.md` sale en 0.
  - Mutaciones de la prueba de regeneración: cambiar a mano un tamaño de `type-scale.md` (rojo), cambiar un parámetro sin regenerar (rojo), borrar la tabla (rojo por población cero).
  - Mutación de la prueba de objetivos: bajar a mano en `DESIGN.md` la altura de `boton` a 40 (rojo).
  - Cada pieza lleva una fila por criterio del catálogo, y la mitad juzgada firmada o `unsigned`.
  - Después, `./scripts/check` completo.
- **Commit:** docs(identity): add the type scale, spacing, components and DESIGN.md

### T5 · Prueba de integración manual

- `survival-review` sobre `type-scale.md`, `spacing.md`, `components.md` y `DESIGN.md`. Su `## When` ("after any technique of this addon has produced something") se cumple tras T4.
- Regenerar `DESIGN.md` dos veces desde el árbol limpio con el mismo comando: las dos salidas y el archivo commiteado tienen que ser idénticos (`cmp`).
- Revisar el orden por fecha de autor: `add ADR-014` → T2 → `update ADR-014` → T4 → `publish ADR-014`, y `status: accepted`.
- **Verify:** `cmp` sin diferencias, los instrumentos en 0 con su población y el orden de commits correcto.

## Order & risks

- **Execution order:** A0 → T1 → T2 → A1 → T3 → (elección) → T4 → A2 → T5.
  - T1 va primero porque las candidatas de A1 componen con los nombres ASCII.
  - T2 es la parte arriesgada: dos instrumentos propios cuyo rojo tiene que ser el del criterio.
- **Dependencies:** secuenciales. A0 va antes de T2 porque los parámetros se fijan antes de que exista la herramienta que los corre.
- **Risks:**
  - `design-md.py` rechaza algo que la plantilla de `components.md` pide. Mitigación: la tabla de medición `Component | Text over background` se ignora y se cuenta; que la cuenta salga 1 se comprueba, no se supone.
  - El texto de `DESIGN.md` o de las piezas repite un literal (`16px`) en una celda de prosa que el generador lee. Mitigación: el generador lo rechaza con exit 1. Las columnas de prosa (`Roles`, `Where it is used`) no llevan medidas.
  - M2 a 44 px pide controles grandes, que en 360 px de ancho pueden no caber en fila (los formularios en línea de la ficha). Mitigación: es una consecuencia para s5.7 y se escribe en ADR-014; el criterio no se baja.
  - Escribir una cifra sin correr su comando. Mitigación: cada cifra se copia de la salida vista.
