---
name: afirmar-presencia-no-ve-el-lugar
description: "`assert x in html` no distingue dónde está x ni cuántas veces; un duplicado en el lugar equivocado pasa"
metadata:
  type: feedback
---

Una prueba de página que afirma `'href="/…"' in html` pasa igual si el elemento está en el cuerpo, dentro de `<title>` o repetido. En b1 (2026-09-22) un enlace duplicado vivió en el `<title>` de "Mi colección" desde e2 porque la única prueba buscaba la subcadena en toda la página.

Patrón: defecto de plantilla + origen Code → las afirmaciones de presencia no ven la ubicación.

**Why:** RCDATA (`<title>`, `<textarea>`) muestra el marcado como texto y nada falla; solo un humano mirando la pestaña lo ve.

**How to apply:** al probar HTML, localizar el elemento antes de juzgarlo (regex o parser sobre el contenedor) y contar cuando "exactamente uno" es el requisito; incluir en las mutaciones forzadas "el sujeto quitado" para que la localización no pase en vacío. Al correr las mutaciones, ver [[mutation-checks-stale-bytecode]].

La misma clase apareció al revés en s5.7 (2026-09-23): `html.count("<li") == 3` también contaba el `<link rel="stylesheet">` nuevo, y la prueba se rompió sin que cambiara el comportamiento. Contar una subcadena de una etiqueta cuenta también las etiquetas que empiezan igual: localizar con límite de nombre (`<li[\s>]`) o dentro del contenedor.
