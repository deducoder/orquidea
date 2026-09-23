# Epic e5: Visual identity — Retrospective

## Summary

Orquídea tiene identidad visual de punta a punta:

- **Criterio del encargo** (ADR-009) commiteado antes de cualquier pieza.
- **Concepto:** Cuaderno de campo (ADR-010).
- **Tipografía:** fuentes del sistema con piso de 16 px (ADR-011).
- **Paleta:** papel cálido y azul tinta (ADR-012).
- **Interfaz** derivada por reglas que corre un script:
  - roles de color (ADR-013);
  - escala, espaciado y componentes con controles de 48 × 48 (ADR-014);
  - un `DESIGN.md` generado.
- **Hoja de estilos** escrita a mano, con cada valor atado a un token por una prueba (ADR-015), aplicada a las diez plantillas sin un solo `style` en línea.

Lo medible se midió por script. De lo juzgado, casi todo quedó firmado. Dos juicios de la interfaz vestida y el tiempo con "Slow 3G" quedaron sin responder, por decisión del humano, y están abajo.

## Metrics

- Stories: 7 · Estimated: S, S, S, M, S, M, M (s5.1, s5.2, s5.3, s5.4, s5.5, s5.6, s5.7) · Actual: S, S, S, S, S, M, M. Solo s5.4 salió menor: M → S.
- Tiempo de implementación por historia (`implementation-time.sh`, de cada retrospectiva): 438, 210, 82, 311, 737, 743 y 1287 s. Las historias de interfaz (s5.5–s5.7) costaron más que las de identidad, porque cada una escribió instrumentos propios con TDD.
- 87 commits en el rango (`6aeb019^..HEAD`), 79 sin contar los merges. 7 ADR (009–015). 10 entregables en `governance/identity/`. 633 pruebas en el gate al cerrar.
- Instrumentos nuevos del proyecto:
  - `contraste-de-lectura.py` (7:1);
  - `derivar-primitivas.py`;
  - `derivar-medidas.py`;
  - `comprobar-medidas.py` (piso y objetivos ≥ 44);
  - la prueba de la hoja contra los tokens;
  - la prueba de títulos de todas las páginas.
- Lo que no estaba en el plan:
  - la decisión de identificadores ASCII (s5.6), por un límite del generador del addon;
  - quince enlaces sueltos pasados a objetivos de 48 × 48 (s5.7), porque el diseño supuso la excepción *inline*;
  - dos hallazgos del addon aparcados (la columna `Variant` y las referencias ASCII);
  - la segunda prueba de comportamiento tocada (`"<li"` contaba el `<link>`).
- Peso medido por script: identidad 1.6 KB de 50. Primera carga de "Mi colección" con 25 fotos: 148.1 KB de 200. La ficha en su tope: 31.3 KB.

## Scope verification

**In scope (MUST):**

- **Criterio del encargo commiteado antes de cualquier pieza, con las comprobaciones medibles vistas en rojo** → **Fulfilled**. ADR-009 `add` (21:32) antes de `commission.md` (21:39), y los rojos de peso y contraste están escritos en ADR-009 (s5.1).
- **Paleta, tipografía y los cinco eslabones de UI, cada uno con su ADR abierto en `proposed` y completado a `accepted`** → **Fulfilled**. ADR-010 a ADR-014: cada `add` precede por fecha de autor al primer commit de su pieza (comprobado con `git log` en esta revisión), y los cinco están `accepted`.
- **`DESIGN.md` generado desde las tablas** → **Fulfilled**. `governance/identity/ui/DESIGN.md`: el comando está en ADR-014, y se regeneró dos veces idéntico (`cmp`, s5.6 T5).
- **Todas las plantillas vestidas con la hoja de estilos derivada** → **Fulfilled**. `base.html` la enlaza (`b1af4ae`) y cero `style=` en las diez plantillas (`tests/test_identidad_hoja.py`).
- **`survival-review` sobre cada pieza producida** → **Fulfilled, completado en esta revisión**. Corrió en s5.5 y s5.6 y **faltaba en concepto, paleta y espécimen**. Se corrió aquí:
  - Paleta: `contrast` 8/8 PASS y `pairs` 10, 0 bajo el umbral. La invariancia no se comparó: la columna `Variant` con `—` es el hallazgo del addon aparcado.
  - Espécimen y concepto: sin sujeto mecánico.
  - La mitad firmada de las tres la firmó Daniel Efraín Domínguez Urbina el 2026-09-23.
  - `commission.md` es el criterio, no una pieza, y no se revisa como pieza.
- **Recursos de la identidad ≤ 50 KB gzip y primera carga dentro de `must-perf-001`** → **Parcial, diferido por el humano**. El peso se midió por script (1.6 KB y 148.1 KB). El tiempo con "Slow 3G" no se midió: el servidor quedó listo con 25 ejemplares con foto, y el humano pidió cerrar sin medir (2026-09-23). Aparcado con promoción al primer despliegue.

**In scope (SHOULD):**

- **Concepto común antes de las piezas** → **Fulfilled** (ADR-010 antes de ADR-011 y ADR-012).
- **La medición de peso de la identidad dentro del gate, no solo como script** → **Descoped**. `medir-primera-carga.py --identidad` se corre a mano. El gate sí comprueba otras cosas de la identidad (tokens, objetivos, piso, regeneración), pero no el peso. No se abrió trabajo para esto: con 1.6 KB de 50, el margen hace que el riesgo sea bajo.

**Out of scope:**
- `'unsafe-inline'` sigue en la CSP. Su promoción ("al cerrar s5.7, si ninguna plantilla conserva `style`") **se cumple con este cierre** y pasa a ser el siguiente trabajo, con la comprobación de htmx.
- Tema oscuro, cadena de construcción de CSS, biblioteca de componentes, logotipo y cambios de comportamiento: ninguno se hizo.

**Done when:**

- **[stated] ADR del encargo en `proposed` antes de la primera pieza, y rojos de los criterios 1 y 2** → **Fulfilled** (arriba).
- **[stated] Todas las plantillas usan la identidad; `survival-review` pasa sobre cada pieza; ≤ 50 KB y dentro de `must-perf-001`** → **Fulfilled, salvo el tiempo con "Slow 3G", que el humano difirió** (arriba). Era el stop previsto.
- **[stated] El criterio 3 y la mitad juzgada de cada pieza con nombre y fecha, o `unsigned` y contados como sin responder** → **Fulfilled en su forma**. Todas las mitades juzgadas están firmadas, salvo dos, escritas `unsigned` y **contadas como sin responder**: el criterio 3 de ADR-009 sobre la interfaz vestida y el subtítulo frente al cuerpo (ADR-015, decisión 5). Aparcadas.
- **[deduced] Cada ADR de pieza en `proposed` con fecha anterior a su pieza** → **Fulfilled** (fechas de autor, arriba).
- **[deduced] `DESIGN.md` se genera con `design-md.py`, y regenerarlo produce el mismo archivo** → **Fulfilled** a mano (`cmp`). No está en el gate porque el generador vive en el addon (ADR-014).
- **[deduced] Todo valor de la hoja es un token de `DESIGN.md`, y una prueba se pone en rojo con un valor inventado** → **Fulfilled, con la lista cerrada de ADR-015** (trazos de 1 y 2 px, `0`, `100%` y los valores del espécimen). Cinco mutaciones se vieron en rojo (s5.7).
- **[deduced] Ninguna plantilla conserva `style`, y ninguna prueba de comportamiento cambia salvo la del estilo en línea** → **Descoped en su segunda mitad**. Cambió también `test_dos_ejemplares_de_la_misma_especie_aparecen_como_dos_entradas`, porque contaba `"<li"` y el `<link>` nuevo lo contiene. El humano aprobó precisar el localizador, y el comportamiento que afirma no cambió.
- **[deduced] Las fuentes, si las hay, desde `/static`: la CSP no cambia** → **Fulfilled**. No hay fuentes web (ADR-011) y la CSP está intacta.
- **[stated] All stories complete · docs updated · retrospective done** → historias `done` en `plan.md` y esta retrospectiva escrita. Los docs los genera `epic-close`.

**Elimination commitments:** "sin estilos en línea": cumplido. Siete `style` quitados; lo comprueba una prueba.

**Seguridad y calidad a escala de épica:**
- `security-review`: Bandit sobre los `.py` del rango da 324 B101, todos en pruebas, y 0 en los cinco scripts. PASS.
- `quality-review` a escala de épica: PASS WITH RECOMMENDATIONS. **La cadena `semantics.md` → `DESIGN.md` → hoja no está atada en el gate.** Con `accion-fondo` cambiado a mano en `semantics.md`, `./scripts/check` siguió en verde. Aparcado con su arreglo y su promoción.
- Historias delegadas: none dispatched.

## What went well

- **El orden criterio → contraejemplo → pieza se sostuvo en seis ADR** y se puede comprobar por fecha de autor, no por etiqueta. Los contraejemplos casi siempre salieron de candidatas reales: la uniforme en OKLCH (s5.5), la escala con fechas pequeñas y el espaciado compacto (s5.6), la tinta suave `#767676` (s5.3).
- **Cada eslabón escribió su instrumento y lo dejó en el gate.** Al final, un cambio a mano en `primitives.md`, `type-scale.md`, `spacing.md`, `identidad.css`, un control de `DESIGN.md` o un título de plantilla pone el gate en rojo.
- **La paleta firmada llegó intacta a la pantalla**: la regla de anclas (s5.5) la contuvo en lugar de aproximarla.

## What to improve

- **`survival-review` se omitió en tres de siete historias** (s5.2–s5.4) sin que nadie lo notara hasta esta revisión. Estaba en el MUST del scope y en ningún `plan.md` de esas historias. Una historia que produce una pieza de identidad lleva `survival-review` como tarea de su plan, no como supuesto.
- **Los juicios se pidieron tarde y en forma abierta.** En s5.6 y s5.7 el humano firmó lo que se le pidió firmar y cerró sin contestar las preguntas abiertas. Las dos lecciones de memoria (pedir antes y en elección forzada) no se aplicaron en s5.7.
- **El tiempo con "Slow 3G" lleva cuatro épicas diferido** (e1, e2, e3, e5), y en cada una se previó como stop desde el diseño. Preverlo no basta: sin un despliegue real, el humano no lo mide. La entrada del parking lot lo liga ahora al primer despliegue, que es el único momento en que la medición significa algo.
- **Los instrumentos del addon se leyeron tarde dos veces**: la columna `Variant` en s5.5 y las referencias ASCII en s5.6. En s5.6 sí se leyó el código en el diseño, y eso evitó un rojo a mitad de tarea.

## Learned

1. **About the system:** la identidad es una cadena de seis tablas (paleta → primitivas → roles → escala y espaciado → componentes → `DESIGN.md` → hoja). Cada eslabón tiene su prueba, pero no las uniones de roles con primitivas ni de `DESIGN.md` con sus tablas. Un cambio de paleta hoy regenera las primitivas y deja el resto con el valor viejo sin que el gate lo vea. La paleta tiene un solo margen fino: `renglón` sobre `papel`, a 3.34:1.
2. **About the process:** en una épica de juicio, lo que hay que planear no es la firma sino el momento de pedirla. Cada firma se pidió al cerrar la tarea de su pieza, y las que quedaron para el final (s5.7) no se contestaron. Una pregunta abierta al final de una historia larga compite con "cierra" y pierde.
3. **Capability gained:** derivar una interfaz desde una identidad con reglas que corre un script, y comprobar con el gate que cada valor de la hoja viene de ahí. Además, medir contraste a 7:1, objetivos ≥ 44 y el piso de 16 px, y capturar páginas con sesión a 360 px desde WSL.
