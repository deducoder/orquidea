# Story s5.6: Scale, spacing, components and DESIGN.md — Retrospective

Estimated: M · Actual: M. Fueron 5 tareas y 3 actos de contenedor, con 743 s de implementación (`implementation-time.sh`) y 10 commits en la rama antes de la revisión.

## Summary

- **Scripts nuevos**, con 53 pruebas entre los dos más `tests/test_identidad_ui.py`:
  - `scripts/derivar-medidas.py` produce la escala y el espaciado.
  - `scripts/comprobar-medidas.py` juzga `piso` (M1) y `objetivos --minimo N` (M2).
- **Piezas** en `governance/identity/ui/`, con la regla elegida, escala (A) y espaciado (A):
  - `type-scale.md`: 16/24, 20/32 y 25/36.
  - `spacing.md`: unidad de 8, controles de 48 × 48.
  - `components.md`: diez componentes, todos compuestos de referencias.
  - `DESIGN.md`: generado con `design-md.py --spec-version alpha`, con 21 tokens, 10 componentes, 8 pares y 4 objetivos.
- **Identificadores ASCII:** `semantics.md` pasó a `linea` y `accion-*` (ADR-014), sin cambiar roles ni valores.
- **Sobre `DESIGN.md`:** `pairs` da 8/0, `targets` 4/0, `provenance` 12/0 y el contraste a 7:1 da 8/0 (el más bajo 8.38:1). M1 da 3/3/0/0 y M2 4/0. Invariancia sin sujeto.
- **Gate:** M1, M2 y la regeneración de las tablas de escala y espaciado corren en él.
- **ADR-014** siguió `proposed` → `update` con los rojos → `accepted`. Orden por fecha de autor comprobado: el registro se abrió antes de los scripts y de cualquier valor.

**Finalize (reportado por `story-implement`):**
- Gate: `./scripts/check` en verde, 602 pruebas; 604 tras el arreglo de la revisión.
- Pruebas huérfanas: ninguna. Solo `tests/test_derivar_medidas.py`, `test_comprobar_medidas.py` y `test_identidad_ui.py` leen lo que cambió, y los tres son de esta historia.
- Aceptación: los ocho escenarios del scope se cumplen. Los cuatro `@deduced` los confirmó el diseño. Uno quedó confirmado solo en parte, con su razón: "regenerar `DESIGN.md` da el mismo archivo" se comprobó en la integración manual (`cmp` de dos regeneraciones y del archivo commiteado), no como prueba del gate, porque el generador vive fuera del repositorio.
- El plan existió.

**`survival-review`:** el bloque mecánico salió en verde (arriba) y la invariancia sin sujeto. Los "no aplica" de `platform-specs`, `single-ink` y `prior-art`, y la excepción *inline* de los enlaces dentro de un párrafo (`target-size`), los firmó Daniel Efraín Domínguez Urbina el 2026-09-22. **Dos preguntas quedaron sin respuesta** y pasan a s5.7, donde la interfaz se renderiza:
- ¿Distingue la distancia 20/16 al subtítulo del cuerpo en negrita?
- ¿Las esquinas van rectas sin token, o se decide `rounded` con un ADR nuevo?

**`quality-review`:** PASS WITH RECOMMENDATIONS, aplicada en `9da6948`. Con una fila corta, `comprobar-medidas.py` salía con 1 por un `IndexError` sin capturar, que se lee igual que un control bajo el mínimo. Ahora sale con 2, y lo cubren dos pruebas.

Observación que se deja fuera, dicha en voz alta: `piso` toma la primera tabla `Step`. Sobre un archivo que tenga antes la de espaciado, sale con 2, no con un verde falso, así que no se aparca.

**`security-review`:** Bandit (`conventions/security/instance.md`) sobre los cinco `.py` cambiados: 47 hallazgos, todos B101 (`assert` de pytest) en las pruebas, y 0 en los scripts. PASS. Los guardrails no aplican, porque no se tocó código de la aplicación ni entradas del usuario.

## What went well

- **Los rojos salieron de las candidatas.** La escala (C) puso la fecha en 13 px. El espaciado (C) dejó los cuatro controles en 20 × 20, en rojo para M2 y para `target-size`. Solo `provenance` necesitó muestras construidas: el generador rechazó un literal y el instrumento marcó una edición a mano.
- **El bloqueo del generador apareció en el diseño, no al producir.** Leer `design-md.py` antes de proponer mostró que las referencias con acento se rechazan y que `primitives.md` no se le puede pasar. Por eso hubo una pregunta para el humano en lugar de un rojo a mitad de T4.
- **La memoria de s5.5 se aplicó:** "respaldo: ninguno" en el ADR desde el primer commit, y las piezas en `governance/identity/ui/` desde el scope.

## What to improve

- **Una mutación sobrevivió a ocho casos de redondeo:** `round()` redondea al par, y todos los .5 probados tenían parte entera impar. Se cerró con el caso de 12 px y va a memoria.
- **El contrato 0/1/2 se probó con tablas ausentes y valores ilegibles, pero no con filas cortas.** Lo encontró la revisión, no las pruebas. Va a memoria como lista de entradas que todo script 0/1/2 debe recibir.
- **Invoqué mal `--escalones=-1,…` una vez al correr las candidatas.** El script salió con 2 sin tabla, como debe, y no llegó a la rejilla.
- **Las dos preguntas del juicio quedaron sin respuesta.** Se pidieron junto con las firmas, y la respuesta firmó todo sin contestarlas. En s5.7 conviene hacerlas antes de pedir firmas, o como elección forzada.

## Learned

1. **About the system:** el formato `DESIGN.md` compone fondo, texto, tipografía, relleno y dimensiones, pero no bordes, foco, peso ni cifras tabulares. s5.7 tiene que tomar esos valores de `colors` y de `specimen.md` por token, y la prueba que compare la hoja con los tokens tiene que contarlos. Los formularios en línea de la ficha con botones de 48 × 48 probablemente no quepan en fila a 360 px.
2. **About the process:** leer el código del instrumento del addon en el diseño (su expresión regular, qué tablas lee y por qué celdas) decidió la historia antes de escribir una línea. La pregunta de los identificadores ASCII no se habría visto leyendo solo su cabecera.
3. **Capability gained:** `derivar-medidas.py` y `comprobar-medidas.py` con su regeneración en el gate, y M1 y M2 como pruebas que se ponen en rojo si una edición baja un control o un rol de lectura.
