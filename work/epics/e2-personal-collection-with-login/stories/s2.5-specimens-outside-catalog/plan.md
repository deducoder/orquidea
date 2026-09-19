# Story s2.5: Specimens outside the catalog — Plan

> Size: S
> Pause: none (default)

## Tasks

### T1 · Validación del ejemplar propio y alta sin especie

- **Files:** modify `src/orquidea/coleccion/modelo.py`, `src/orquidea/datos/ejemplares.py`, `tests/test_coleccion_modelo.py`, `tests/test_datos_ejemplares.py`
- **TDD:** RED pruebas: `validar_ejemplar_propio` recorta el nombre, acepta 120 y rechaza 121, rechaza vacío y solo espacios, acepta notas de 2000 y rechaza 2001, normaliza `\r\n` a `\n`; `agregar_sin_especie` guarda `especie_id` NULL con nombre y notas y `listar` lo devuelve → GREEN → REFACTOR
- **Satisfies:** scenarios de validación, límites y recorte
- **Mold:** `orquidea.datos.ejemplares.agregar` (T1 de s2.4)
- **Verify:** límites `>` por `>=` en el borde 120/121 y 2000/2001 (rojo con las pruebas de borde); no recortar (rojo); aceptar el vacío (rojo); no normalizar saltos (rojo); guardar el nombre sin recortar en el repositorio (no aplica: recorta el dominio); luego `./scripts/check` completo
- **Commit:** feat(coleccion): validar y guardar plantas fuera del catálogo

### T2 · Formulario, rutas y lista

- **Files:** modify `src/orquidea/web/app.py`, `src/orquidea/web/templates/coleccion.html`, `tests/test_web_coleccion.py`; create `src/orquidea/web/templates/nuevo_ejemplar.html`
- **TDD:** RED pruebas con `client`: `GET /coleccion/nuevo` trae el formulario con `csrf`, sin JS nuevo; `POST` válido → 303 y fila sin especie con nombre y notas recortados; nombre vacío → 422 con el mensaje, campos conservados y nada guardado; nombre y notas excesivos → 422; sin token → 403; anónimo → 303 al acceso; la lista muestra el ejemplar propio sin enlace, con notas (saltos conservados) y el enlace "no está en el catálogo" desde "Mi colección"; HTML en nombre o notas escapado; un ejemplar sin notas no trae bloque vacío → GREEN → REFACTOR
- **Satisfies:** scenarios 1 a 3, los deducidos y los deltas del diseño
- **Mold:** rutas y plantillas de s2.4 (`agregar_a_mi_coleccion`, `coleccion.html`)
- **Verify:** no validar en la ruta (rojo); redirigir con 200 en error (rojo); no conservar lo escrito (rojo); `|safe` en las notas (rojo con HTML); enlazar al ejemplar propio a una ficha (rojo); quitar el campo `csrf` del formulario (rojo, aserción acotada al `<form>`); luego `./scripts/check` completo
- **Commit:** feat(web): agregar plantas que no están en el catálogo

### T3 · Manual integration test

- Con `uvicorn` real: acceder, abrir el formulario, enviar uno válido y uno vacío, ver "Mi colección" con una entrada del catálogo y una propia con notas de varias líneas, reiniciar y volver a verla.
- **Verify:** la entrada propia sin enlace y con sus saltos de línea, el error visible con lo escrito conservado, persistencia tras el reinicio, `./scripts/check` en verde.

## Order & risks

- **Execution order:** T1 → T2 → T3 — el dominio primero; la web usa su validación.
- **Dependencies:** secuenciales, acíclicas.
- **Risks:** el `CHECK` de la base solo asegura `trim(nombre) > 0`; los límites de longitud viven solo en el dominio (una fila metida por otra vía no los cumpliría) → aceptable, no hay otra vía de escritura; `white-space: pre-line` en un atributo `style` depende de que la CSP permita estilos en línea (lo hace `style-src 'unsafe-inline'`, s2.3).
