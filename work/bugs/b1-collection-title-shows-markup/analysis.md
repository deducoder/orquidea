# Bug b1: Collection title shows markup — Analysis

## Method: git bisect (introducing change conocido) + 5 Whys

No hizo falta correr `git bisect`: `git log -S` sobre la línea defectuosa nombra un solo commit, `8d5b985 feat(web): agregar plantas que no están en el catálogo` (e2, 2026-09-19).

### Root cause
El mismo commit que agregó el enlace a `/coleccion/nuevo` en el cuerpo de "Mi colección" lo insertó también, por segunda vez, dentro del bloque `title`, y la única prueba que cubre ese enlace busca la subcadena `href="/coleccion/nuevo"` en toda la página, así que pasa igual con el enlace en el título que en el cuerpo. Ninguna prueba afirma el título de esa página.

1. ¿Por qué la pestaña muestra marcado? — `ran:` porque `<title>` contiene `<p><a …>…</a></p>` y es RCDATA: el navegador lo muestra como texto (reproducido en `scope.md`).
2. ¿Por qué el título contiene ese marcado? — `ran:` `git show 8d5b985 -- src/orquidea/web/templates/coleccion.html` cambia la línea 2 de `{% block title %}Mi colección — Orquídea{% endblock %}` a la misma con el `<p><a>` antes del `{% endblock %}`.
3. ¿Por qué no era el enlace buscado? — `ran:` `git show 8d5b985:src/orquidea/web/templates/coleccion.html | grep -n coleccion/nuevo` da dos líneas, la 2 (título) y la 27 (cuerpo): el enlace del cuerpo es el que la historia pedía, el del título es un duplicado.
4. ¿Por qué pasó la prueba? — `ran:` `tests/test_web_coleccion.py:202` es `assert 'href="/coleccion/nuevo"' in client.get("/coleccion").text`, que no distingue dónde está el enlace; y `grep -rn "<title>" tests/` solo encuentra `test_web_inicio.py:13`, que afirma el título de la página de inicio.
5. ¿Por qué el duplicado entró al editar? — `read: unverified` no queda rastro de cómo se hizo la edición; lo accionable es el punto 4: una afirmación de "el enlace existe en la página" no puede ver un enlace en el lugar equivocado.

### Evidence
- `ran:` `GET /coleccion` con sesión → 200 y `<title>Mi colección — Orquídea<p><a href="/coleccion/nuevo">Agregar una planta que no está en el catálogo</a></p>\n</title>` (script de reproducción de `bug-start`, en la rama del bug).
- `ran:` `git log -S` sobre la línea defectuosa → solo `8d5b985`.
- `ran:` el enlace del cuerpo (línea 27 en `8d5b985`) sigue en la línea 37 de hoy; el del título es el único que sobra.
- `ran:` `grep -rn "block title" src/orquidea/web/templates/` → ninguna otra plantilla tiene un bloque `title` partido en varias líneas ni con marcado.

### Done when
confirmed — `GET /coleccion` debe dar `<title>Mi colección — Orquídea</title>` y la página conservar **exactamente un** enlace a `/coleccion/nuevo`; el "exactamente uno" es lo que la prueba actual no podía ver.

### Fix approach
Una prueba de regresión que afirme el `<title>` exacto de "Mi colección" y que la página tenga un solo `href="/coleccion/nuevo"`, y quitar el `<p><a>…</a></p>` sobrante del bloque `title` de `coleccion.html`, dejándolo en una línea como en las otras plantillas.
