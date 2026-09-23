# Story s5.7: Apply the identity to the templates — Retrospective

Estimated: M · Actual: M. Fueron 4 tareas y 2 arreglos, 1287 s de implementación (`implementation-time.sh`) y 10 commits en la rama antes de la revisión.

## Summary

- `src/orquidea/web/static/identidad/identidad.css`: todos los tokens de `DESIGN.md` y la pila de `specimen.md` en `:root`, y solo `var()` fuera, salvo la lista cerrada de ADR-015. Pesa 1.6 KB en gzip.
- `base.html` enlaza la hoja, y ninguna plantilla conserva un `style`. Los siete atributos se cambiaron por clases (`notas`, `foto`, `miniatura`, `tarjetas`, `historial`, `en-linea`), y quince enlaces fuera de una frase llevan `accion`, el componente `enlace-navegacion` de 48 × 48.
- Pruebas nuevas:
  - `tests/test_identidad_hoja.py`, 18 pruebas: la hoja contra los tokens, ningún `style=`, el `<link>` en el `<head>`, la hoja servida como `text/css` y todo enlace suelto con `accion`.
  - `tests/test_web_titulos.py`: los `<title>` de las nueve páginas, con la cobertura contada contra `rutas_registradas`.
- `medir-primera-carga.py` pasa a contar `estaticos`, que ahora es JS y CSS. Primera carga de "Mi colección" con 25 fotos: 148.1 KB de 200. La ficha en su tope: 31.3 KB. Identidad: 1.6 KB de 50. Cifras copiadas de la salida.
- ADR-015 en `accepted`, con sus cinco decisiones. La CSP no cambió.

**Finalize (reportado por `story-implement`):**
- Gate en verde, 633 pruebas.
- Pruebas huérfanas: los módulos que se tocaron (`medir-primera-carga.py` y las plantillas) los leen `tests/test_medicion.py`, `test_web_coleccion.py` y las pruebas web. Esas pruebas se leyeron y siguen en verde, y se ajustaron las dos que tenían que cambiar (abajo).
- Aceptación: siete de los ocho escenarios se cumplen. El del criterio 3 queda **`unsigned`**, como el escenario permite, y cuenta como sin responder.
- **Dos pruebas de comportamiento cambiaron, no una.** El scope esperaba solo `test_web_coleccion.py:250`, la del estilo en línea, que ahora localiza `<p class="notas">`. La segunda es `test_dos_ejemplares_de_la_misma_especie_aparecen_como_dos_entradas`: contaba `"<li"`, que también cuenta el `<link>` nuevo. El humano aprobó precisar el localizador (`<li[\s>]`) antes de tocarla. El comportamiento que afirma no cambió.

**Recorrido renderizado (T5):** las nueve páginas se capturaron a 360 px (en el scratchpad). La foto de la ficha va a todo el ancho, y el formulario de la floración en curso envuelve en lugar de encoger. La hoja se sirve con la CSP intacta. **Juicios sin respuesta:** el criterio 3 de ADR-009 y el subtítulo frente al cuerpo quedan `unsigned`, porque el humano pidió cerrar sin responder. Van al parking lot con dos ajustes visuales sin decidir (la sangría de los enlaces `accion` y el botón pegado en Acceso). La medición en "Slow 3G" sigue siendo el stop previsto de `epic-review`.

**`quality-review`:** PASS WITH RECOMMENDATIONS. Dos hallazgos:
- **Aplicado en `035f9ce`:** el diseño dio a los enlaces sueltos la excepción *inline* de SC 2.5.8 y 2.5.5, y no les toca. Medían 24 px de alto contra el 44 de M2. Lo reveló el recorrido renderizado, no una prueba; ahora hay una prueba que se vio en rojo.
- **Aplicado en `efb090b`:** `test_un_titulo_con_marcado_o_ausente_no_pasa` solo ejercitaba un helper de la propia prueba (muda). El rojo real se vio mutando las plantillas.
- **Observación que se deja fuera, dicha en voz alta:** `.foto` lleva `width: 100%` y `max-width: 100%`, y la primera hace redundante a la segunda. No es un defecto.

**`security-review`:** Bandit (`conventions/security/instance.md`) sobre los `.py` cambiados dio 216 hallazgos B101 (`assert` de pytest), todos en `tests/`, y 0 en `scripts/medir-primera-carga.py`. PASS. Guardrails: `must-security-001` no aplica. La CSP no se relajó, y quitar `'unsafe-inline'` queda aparcado con su promoción, que se cumple con este cierre.

**Incidente, dicho al humano en el momento:** al bajar la foto de prueba de Wikimedia Commons, puse su correo en el User-Agent de `curl`. Salió en una sola petición. Va a memoria como regla.

## What went well

- **La prueba de tokens compara nombres, no valores.** `superficie` y `campo-fondo` (los dos `#FFFFFF`) siguen siendo distintos. Cinco mutaciones sobre la hoja real, incluida la forma equivalente `0.625rem`, se vieron en rojo, cada una nombrando la regla.
- **La medición ya contaba el CSS.** El recorrido del diseño lo vio en `medir-primera-carga.py:133`, así que el cambio fue un renombre honesto y no una función nueva.
- **El recorrido renderizado encontró lo que ninguna prueba veía:** el tamaño de los enlaces sueltos.

## What to improve

- **La excepción *inline* se supuso en el diseño en lugar de clasificar los 19 enlaces.** Se hizo la clasificación en T5, y debió hacerse en el recorrido del diseño con `grep "<a "`.
- **Las primeras capturas engañaron:** Chrome en Windows no baja de unos 500 px, y la página parecía desbordarse a 360. Se resolvió con un `iframe` de 360. Va a memoria.
- **Los datos de ejemplo con `curl -d` y acentos** guardaron "dÃa". Se comprobó que era de `curl` y no de la aplicación antes de seguir.
- **El dato personal en el User-Agent**, arriba.
- **Los juicios se pidieron al final de T5, junto con tres preguntas**, y el humano cerró sin responderlos. En la memoria de s5.6 ya estaba "pedir el juicio antes y en elección forzada". Aquí se pidió en forma abierta, otra vez.

## Learned

1. **About the system:** la hoja tiene dos fuentes fuera de `DESIGN.md` (`specimen.md` y la lista de ADR-015), y la prueba lee las dos. Un cambio de identidad que toque el peso o la familia pasa por `specimen.md`, no por el generador. La CSP ya no necesita `'unsafe-inline'` para las plantillas; falta comprobar htmx.
2. **About the process:** en una historia que viste plantillas, clasificar cada elemento interactivo en el diseño (objetivo, en una frase, imagen) decide qué componente le toca. Suponer la excepción de WCAG fue más barato en el diseño y más caro al renderizar.
3. **Capability gained:** capturas de páginas con sesión a 360 px desde WSL, y una prueba de hoja contra tokens que se puede reusar si la identidad cambia.
