# Bug b1: Collection title shows markup — Scope

WHAT:      el `<title>` de "Mi colección" contiene `<p><a href="/coleccion/nuevo">Agregar una planta que no está en el catálogo</a></p>`, y el navegador lo muestra como texto literal en la pestaña y en el historial
WHEN:      siempre, con sesión iniciada, al pedir `GET /coleccion` (reproducido el 2026-09-22 con `TestClient`: 200 y el marcado dentro de `<title>`)
WHERE:     `src/orquidea/web/templates/coleccion.html:2`, bloque `title`
EXPECTED:  el título es `Mi colección — Orquídea`, sin marcado; el enlace para agregar una planta fuera del catálogo sigue en el cuerpo de la página
DONE WHEN: [deduced] `GET /coleccion` devuelve `<title>Mi colección — Orquídea</title>` y la página conserva exactamente un enlace a `/coleccion/nuevo`, fijado por una prueba de regresión vista en rojo antes del arreglo

Base:      develop
