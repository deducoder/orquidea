# Story s5: Compose species list — Retrospective

Estimated: una parte de la sesión, sin cifra declarada · Actual: de `d7d2c16` a `7c3032a`, unos 45 minutos en las fechas de autor. Creció dos veces: los scripts de la escala y la familia tipográfica.

## Summary

- La escala declara `Font family` y `Font weight` desde el espécimen, y `DESIGN.md` se regeneró con 0.24.0.
- S1 Especies es la primera página generada de la cadena `screens`: el candidato A, elegido entre dos.
- ADR-020 `accepted`.
- La falta de `img` en `page.py` quedó aparcada, y S3 y S4 esperan.

## Finalize

- **Gate:** `./scripts/check` salió 0 antes de cada commit de la rama, con 673 pruebas al final.
- **Pruebas huérfanas:** las que importan `derivar-medidas.py` y `comprobar-medidas.py` son `test_derivar_medidas.py`, `test_comprobar_medidas.py` e `test_identidad_ui.py`, y las tres se tocaron. `test_identidad_hoja.py` lee `DESIGN.md` y también se tocó. No queda ninguna sin resolver.
- **Criterios de aceptación (scope):**
  - ADR en `proposed` con su rojo antes de producir: cumplido. `f85d373` va antes de `c521f89`, y la familia (`3b001d9`) antes de `7053e36`.
  - `DESIGN.md` con peso y familia, idéntico en dos corridas: cumplido.
  - Los dos candidatos con exit 0 y 7:1: cumplido.
  - Juicios con nombre y fecha: cumplido.
  - ADR `accepted`: cumplido.
  - Ningún criterio retractado. W1 creció con aprobación y el diff queda en el ADR.
- **Survival-review:**
  - `precedence` sale PASS en la composición y FAIL en `type-scale.md`. Leído a mano: W1 creció después de la primera pieza que lo cita, que es el mismo mecanismo aparcado en s2.
  - **Firmado por Daniel Efraín Domínguez Urbina el 2026-09-24:** lo que no aplica, `component-contrast` (apoyado en s1) y `target-size` (medido sobre `DESIGN.md`).
- **quality-review:**
  - `tabla_escala` arma sus columnas opcionales en una sola ruta; antes había dos ramas casi iguales.
  - `_columna_de_roles` vuelve a la posición 3 si no hay encabezado. En la práctica no pasa, porque `_filas` ya exigió `Step`.
  - `test_identidad_ui` ahora espera 8 objetivos: los mismos 4 controles medidos dos veces, como decidió s1, con la razón en un comentario.
  - En `:root` conviven `--familia` y `--typography-step-N-font-family` con el mismo valor, y la cadena lo comprueba.
- **security-review:** `uv run bandit -q` sobre los dos scripts no reporta nada. En las pruebas solo saldría B101 (aparcado).

## What went well

- **Las sondas de `page.py` antes de proponer criterios** encontraron los tres bloqueos (sin peso, sin `img` y la regla de pesos por rango) antes de que hubiera un ADR comprometido con la Ficha del ejemplar. La historia cambió de pantalla sin tener que rehacer nada.
- **Ver las capturas antes de pedir el juicio** detectó la letra Times. Un juicio contra "fuentes del sistema" sobre una página en Times habría quedado firmado sin valor.
- **La cadena hoja ↔ `DESIGN.md` de s1 hizo su trabajo:** en cuanto `DESIGN.md` tuvo un token nuevo, la prueba de la hoja lo pidió en `:root`.

## What to improve

- **El recorrido del diseño no leyó quién lee `type-scale.md`.** El diseño decía "ningún código cambia", y en T1 aparecieron dos scripts y cuatro pruebas. Un `grep` del nombre del entregable en `scripts/` y `tests/` al diseñar lo habría dicho antes. Guardado en memoria.
- **Pedir el juicio con razones ya redactadas.** Las tres razones de la elección forzada las escribió el agente y el dueño eligió la opción. Así quedó escrito, pero una razón propuesta pesa más que una pregunta abierta. La próxima vez conviene preguntar abierto primero.
- **La promoción del refactor de lectores de tablas** ("un defecto que aparezca en un lector y no en los otros") se tocó de cerca: `comprobar-medidas.py piso` leía por posición. Aquí solo se arregló ese lector. La entrada sigue abierta, porque los otros lectores no mostraron el defecto. Queda dicho.

## Learned

1. **Sobre el sistema:** `page.py` de 0.24.0 exige `fontWeight`, y sin `fontFamily` la página sale en la letra del navegador. No dibuja imágenes, y un rango no puede pesar menos que el siguiente. `design-md.py` de 0.24.0 lee `Font family`/`Font weight` y escribe `Target` desde los mínimos.
2. **Sobre el proceso:** antes de proponer los criterios de un eslabón que genera algo, se corre el generador con una sonda. Y antes de pedir un juicio visual, se mira la captura.
3. **Capacidad ganada:** cualquier pantalla sin foto puede generarse y medirse ya. S2 es la siguiente candidata.
