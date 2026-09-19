# Epic e3: Specimen photos — Brief

## Hypothesis

Para el coleccionista que quiere reconocer cada una de sus plantas a simple vista,
la foto del ejemplar en Orquídea es un registro visual
ligado a cada planta de su colección.
A diferencia de las fotos sueltas en el teléfono, cada imagen vive junto a su
ejemplar y su especie, se ve en miniatura en las listas y nunca revela dónde se
tomó.

## Success metrics

- **Leading:** subir una foto con GPS en el EXIF y comprobar que la imagen guardada no tiene metadatos y mide ≤ 1600 px de ancho (`must-perf-002`, `must-security-001`).
- **Lagging:** la lista de "mi colección" con miniaturas sigue en ≤ 200 KB en la primera carga (`must-perf-001`), sin contar las fotos a tamaño completo.

## Appetite

M — 5-7 historias. Incluye dividir `orquidea/web/app.py` en routers antes de
añadir rutas: la entrada del parking lot "`orquidea/web/app.py` reúne todas las
rutas…" se unió a la versión v0.2.0.

## Scope boundaries

What the design may not do. **What it will build is not decided here** — the
in-scope list belongs to `scope.md`, written by `epic-design` after the
decomposition.

### No-gos
- Varias fotos por ejemplar o galerías — RF-05 dice una foto por ejemplar.
- Edición de imagen (recortar, rotar) dentro de la app.
- Almacenamiento en servicios externos — las fotos van al disco del servidor (system-context).

### Rabbit holes
- Una tubería de imágenes con varios tamaños y formatos modernos: basta con la imagen reducida y una miniatura.
- Reconocer la orquídea en la foto.
