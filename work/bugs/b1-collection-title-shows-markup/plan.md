# Bug b1: Collection title shows markup — Plan

> Pause: none (default)

## Tasks

### T1 · Quitar el enlace duplicado del título de "Mi colección"
- **Files:** modify `tests/test_web_coleccion.py` (prueba de regresión junto a `test_mi_coleccion_enlaza_al_formulario_de_plantas_fuera_del_catalogo`); modify `src/orquidea/web/templates/coleccion.html` (bloque `title`, línea 2).
- **TDD:** RED una prueba que extrae el `<title>` de `GET /coleccion` y afirma que es exactamente `Mi colección — Orquídea`, y que la página tiene exactamente un `href="/coleccion/nuevo"`; se ve fallar → GREEN dejar el bloque en `{% block title %}Mi colección — Orquídea{% endblock %}` en una línea → REFACTOR ninguno: el enlace del cuerpo ya existe y la prueba anterior de "enlaza al formulario" queda cubierta por la nueva, pero se conserva porque nombra otro comportamiento.
- **Mold:** `tests/test_web_inicio.py:13` (afirmación sobre `<title>`), y el bloque `title` de una línea de las demás plantillas (`especies.html`, `especie.html`).
- **Verify:** el título de "Mi colección" es texto sin marcado y el enlace a `/coleccion/nuevo` aparece una sola vez — forced mutations, each of which must flip it: el arreglo revertido (el `<p><a>` de vuelta en el título); una forma equivalente (otro marcado en el título, p. ej. `Mi colección — Orquídea <b>x</b>`); el sujeto quitado (el `<title>` ausente de `base.html`: la prueba no debe pasar por no encontrarlo) y el enlace del cuerpo quitado (cero enlaces tampoco es uno); then `uv run pytest tests/test_web_coleccion.py -q` y `./scripts/check`.
- **RED observed:**
- **Commit:** fix(web): remove the duplicated link from the collection page title
