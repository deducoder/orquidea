# Story s3.5: Thumbnails and remove photo — Design

> Complexity: simple

## 1 · What & why

**Problem:** la lista no muestra fotos y una foto equivocada no se puede quitar, solo reemplazar.
**Value:** RF-05 queda completo: foto en la ficha, miniatura en la lista y corrección posible.

## 2 · Approach

En `coleccion.html`, una miniatura enlazada a la ficha por fila con foto (`loading="lazy"` y dimensiones fijas para no mover el diseño), apuntando a la ruta de miniatura de s3.4. Quitar la foto es un `POST /coleccion/{id}/foto/quitar` que llama a `quitar_foto` (s3.3) y redirige a la ficha; el botón vive en la ficha, dentro de un formulario con CSRF. Sin página de confirmación: una foto se sube de nuevo en segundos, a diferencia de la baja del ejemplar (decisión de esta historia; ver Out of scope).

**Components affected:**

- `orquidea/web/templates/coleccion.html`: modify — miniatura enlazada.
- `orquidea/web/templates/ejemplar_ficha.html`: modify — botón "Quitar la foto" cuando hay foto.
- `orquidea/web/rutas/coleccion.py`: modify — `POST /coleccion/{id}/foto/quitar`.
- `tests/test_web_fotos.py`, `tests/test_web_rutas.py`: modify.

**Legacy sweep:** nothing — net-new. `test_web_coleccion.py` prueba el HTML de la lista: se corre entero; los tests de la lista existentes no dependen de la ausencia de `<img>`. `test_web_rutas.py` gana la ruta nueva.

## 3 · Interface / examples

```html
<!-- coleccion.html, por fila con foto -->
<a href="/coleccion/1"><img src="/coleccion/1/foto/miniatura" alt="Foto de Mi rara" loading="lazy" width="96" height="96" style="object-fit: cover"></a>
```

```
POST /coleccion/1/foto/quitar  csrf=<token>  -> 303 /coleccion/1  (archivos borrados, foto nula)
POST /coleccion/1/foto/quitar  (sin foto)     -> 303 /coleccion/1
POST /coleccion/999/foto/quitar               -> 404
POST sin csrf                                 -> 403
```

## 4 · Acceptance criteria

**Must:**

- Cada ejemplar con foto muestra su miniatura enlazada a `/coleccion/{id}`; uno sin foto no lleva `<img>`.
- Quitar la foto borra los dos archivos, deja `foto` nula y conserva el ejemplar y sus notas.
- Sin CSRF 403, sin sesión 303 al acceso, inexistente 404; ninguno cambia nada.
- Quitar la foto de un ejemplar sin foto es idempotente.

**Should:** la miniatura lleva `alt` con el nombre del ejemplar.

**Must NOT:** cambiar la ruta o el tamaño de la miniatura; añadir una página de confirmación.

### ASVS L2

- V4.2 (acceso a objetos) y CSRF: los cubre la dependencia global; se prueban en la ruta real.
- V12: no hay entrada de archivo nueva; el borrado usa `quitar_foto`, que forma rutas solo con el nombre guardado (s3.3).
- Nada más aplica: sin entrada de usuario nueva más allá del `id` entero.

### Deduced criteria

- Ejemplar sin foto aparece igual, sin imagen rota: confirmed
- Quitar la foto la borra y deja el ejemplar: confirmed — `quitar_foto` ya lo hace (s3.3)
- Quitar de un ejemplar sin foto no falla: confirmed — `quitar_foto` lo trata como no-op
- Sin CSRF, sin sesión, inexistente: confirmed

### Scenarios (delta over the scope)

none — scope scenarios stand
