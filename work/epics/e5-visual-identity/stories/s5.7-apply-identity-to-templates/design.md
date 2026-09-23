# Story s5.7: Apply the identity to the templates — Design

> Complexity: complex — diez plantillas, una hoja nueva, tres pruebas nuevas y una medición ampliada

## 1 · What & why

**Problem:** las plantillas se sirven sin estilo, con siete atributos `style` sueltos. La identidad existe solo como documentos: `DESIGN.md`, el espécimen y los roles.
**Value:** el coleccionista ve en el teléfono la interfaz decidida: papel cálido, tinta a ≥ 7:1, controles de 48 × 48 y la foto a todo el ancho en la ficha. Una prueba del gate garantiza que cada valor de la hoja es un token, así que un cambio de identidad se re-deriva y no se parcha.

## 2 · Approach

- **La hoja:** `src/orquidea/web/static/identidad/identidad.css`, escrita a mano. En `:root` declara una propiedad personalizada por token, con el nombre de su ruta (`--colors-fondo`, `--typography-step-0-font-size`, `--spacing-step-6`), y el resto de la hoja solo usa `var(--…)`.
- **La prueba de tokens** compara cada propiedad de `:root` con el token de `DESIGN.md` y rechaza cualquier literal de color o medida fuera de `:root` que no esté en una lista cerrada de excepciones declaradas.
- **Plantillas:** `base.html` enlaza la hoja. Los `style` se cambian por clases de la hoja, y ninguna marca cambia de estructura, salvo las clases.
- **Decisión:** hay decisiones con varias respuestas válidas (excepciones, esquinas, la lista de ejemplares), así que van en **ADR-015** antes de escribir la hoja.

**Components affected:**

- `src/orquidea/web/static/identidad/identidad.css`: create.
- `src/orquidea/web/templates/base.html`: modify (`<link>` y las clases de la cabecera). Las otras nueve plantillas: modify, solo clases y los siete `style` quitados.
- `tests/test_identidad_hoja.py`: create. Una prueba compara la hoja con `DESIGN.md` y `specimen.md`; otra confirma que ninguna plantilla lleva `style=`.
- `tests/test_web_titulos.py`: create. Es la prueba de títulos del parking lot.
- `tests/test_web_coleccion.py:250`: modify. Hoy afirma `style="white-space: pre-line"`; pasa a afirmar la clase **en el `<p>` que contiene las notas**, sin buscar la cadena suelta (memoria `afirmar-presencia-no-ve-el-lugar`).
- `scripts/medir-primera-carga.py`: modify. El campo `javascript` ya suma todo lo que cuelga de `/static` por `src` o `href`, así que el CSS entra solo. Lo renombro a `estaticos` y la línea impresa pasa a decir "JavaScript y CSS (gzip)". `tests/test_medicion.py` se ajusta al nombre.
- `records/decisions/adr-015-hoja-de-estilos.md`: create.

**Legacy sweep:** se reemplazan los siete atributos `style` (`coleccion.html:10,28` y `ejemplar_ficha.html:12,18,57,89,96`) por clases, sin coexistencia. La afirmación de `test_web_coleccion.py:250` se sustituye. Nada más queda huérfano.

### Lo que el recorrido encontró

- **El montaje de `/static`** ya existe (`web/app.py:42`), y la CSP (`default-src 'self'; style-src 'self' 'unsafe-inline'`) ya permite una hoja propia. **La CSP no cambia.** Quitar `'unsafe-inline'` va aparte, por la promoción de su entrada al cerrar esta historia.
- **La medición ya contaría el CSS** (`medir-primera-carga.py:133`, `(?:src|href)="(/static/…)"`), pero bajo el nombre `javascript`. Renombrar el campo es lo único honesto.
- **`test_la_lista_no_trae_javascript_nuevo`** cuenta `<script`. Un `<link>` no lo afecta.
- **Lo que `DESIGN.md` no trae** (ADR-014, huecos):
  - Los bordes (`campo-borde`, `linea`, `error`) y el `foco` están en `colors`, pero sin componente.
  - El peso 700, `tabular-nums` y la itálica están en `specimen.md`.
  - La pila de familias está en `specimen.md`: `system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif`.
  - El ancho de un trazo (borde, anillo) no es token de nada.
- **La miniatura mide 192 px de lado** (`datos/fotos.py:9`) y la lista la muestra en 96 × 96 (`coleccion.html:10`). Ponerla a todo el ancho de la tarjeta la estiraría a unos 330 px y se vería borrosa. Hacerla más grande es un cambio de datos y de peso (`must-perf-001`), y eso es no-go del brief. La foto protagonista es la de la **ficha**, que ya es la foto completa.
- **Los formularios en línea de la ficha** (quitar un riego, terminar o quitar una floración) llevan botones que ahora miden 48 × 48. Si caben en fila junto a la fecha a 360 px lo dice el recorrido renderizado; la hoja los deja envolver (`flex-wrap`) en lugar de encogerlos.
- **La prueba de títulos:** `tests/fabricas.py:33 rutas_registradas` enumera las rutas. La prueba recorre una lista declarada de páginas GET que devuelven HTML, cada una con los datos que necesita, y cuenta su población contra las rutas GET registradas menos las exclusiones nombradas (`/static`, foto, miniatura, `/salud`). Así, una página nueva sin título probado la pone en rojo.
- **`pyyaml`** está en `uv.lock` solo como dependencia transitiva. La prueba lee el *frontmatter* de `DESIGN.md` con un lector de dos niveles de sangría, sin depender de él.

### Propuesta que necesita aprobación (ADR-015)

1. **Propiedades personalizadas con el nombre del token.** Cada token entra una vez, en `:root`, y las reglas solo lo usan por `var()`.
   - Alternativa rechazada: literales en cada regla. La prueba tendría que adivinar a qué token corresponde cada `16px`, y dos tokens con el mismo valor (`superficie` y `campo-fondo`, los dos `#FFFFFF`) serían indistinguibles.
2. **Excepciones de literal, lista cerrada, en la prueba y en el ADR:**
   - `0`, `100%`, `auto`, `none` e `inherit`: no son medidas de la identidad.
   - `1px` como grosor de borde y de `linea`, y `2px` como grosor y separación del anillo de `foco` (WCAG 2.2 SC 2.4.13 pide al menos 2 px CSS de perímetro para AAA; AA no fija grosor). Ningún eslabón deriva trazos.
   - `700` y los valores de `font-style` y `font-variant-numeric`, que salen de `specimen.md`.

   Alternativa rechazada: un ADR nuevo de s5.6 con "tokens de trazo". Reabriría una cadena cerrada por dos valores que ninguna regla derivaría.
3. **Esquinas rectas, sin `border-radius`.** Es la pregunta abierta de s5.6. Una libreta de campo tiene esquinas rectas, y así no hace falta un token.
   - Alternativa: un ADR que derive `rounded`. No hay regla publicada de atributo a radio (lo dice el generador).
4. **Lista de ejemplares:** la miniatura queda en 96 × 96 junto al texto, y la foto a todo el ancho va en la ficha.
   - Alternativa: miniatura a todo el ancho de la tarjeta. Se vería borrosa, o pediría miniaturas más grandes y más peso (no-go).
5. **El subtítulo (20 px, 700) contra el cuerpo:** es la otra pregunta abierta. Se juzga en el recorrido renderizado junto con el criterio 3. Si no se distingue, el ajuste va por espacio (margen de `spacing`), no por tamaño, que es de s5.6.

## 3 · Interface / examples

```css
:root {
  --colors-fondo: #F7F3EA;
  --typography-step-0-font-size: 16px;
  --typography-step-0-line-height: 24px;
  --spacing-step-6: 48px;
  --familia: system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif;
}
button { background: var(--colors-accion-fondo); color: var(--colors-accion-texto);
         min-height: var(--spacing-step-6); min-width: var(--spacing-step-6);
         padding: 0 var(--spacing-step-2); border: 0; }
button:active { background: var(--colors-accion-presionada); }
:focus-visible { outline: 2px solid var(--colors-foco); outline-offset: 2px; }
.notas { white-space: pre-line; }
```

```sh
uv run pytest tests/test_identidad_hoja.py
# con `--colors-fondo: #F7F3EB` → FAILED: --colors-fondo es #F7F3EB y el token colors.fondo es #F7F3EA
# con `padding: 10px` en una regla → FAILED: literal 10px fuera de :root, en `.tarjeta`
# con `var(--spacing-step-5)` → FAILED: var(--spacing-step-5) no está declarada en :root
# sin :root → FAILED: 0 propiedades — nada que comparar
uv run python scripts/medir-primera-carga.py --identidad src/orquidea/web/static/identidad
# Identidad (gzip)  1.x KB de 50 KB   OK   → exit 0
uv run python scripts/medir-primera-carga.py
#   JavaScript y CSS (gzip)  …   Total … de 200 KB   OK
```

## 4 · Acceptance criteria

- **Must:**
  - ADR-015 en `accepted` con las cinco decisiones y la lista de excepciones, antes de la hoja.
  - La prueba de tokens pasa y se vio en rojo con cuatro mutaciones: valor distinto, literal fuera de `:root`, `var()` sin declarar y `:root` vacío.
  - Cero atributos `style` en `src/orquidea/web/templates/`, comprobado por una prueba.
  - `--identidad` ≤ 50 KB y la primera carga ≤ 200 KB con el CSS contado, con las cifras copiadas de la salida.
  - La prueba de títulos pasa, cubre todas las páginas GET HTML y se vio en rojo con un `<title>` roto.
- **Should:**
  - El recorrido renderizado a 360 px, con capturas, antes de pedir el juicio.
- **Must NOT:**
  - Cambiar una ruta, un formulario o un dato.
  - Cambiar la CSP.
  - Un literal de color o medida fuera de `:root` que no esté en la lista de excepciones.
  - Cambiar un token.

### Deduced criteria

- La prueba de títulos: **confirmed**. La pide el parking lot con su promoción en s5.7, y `rutas_registradas` permite contar su cobertura.
- La CSP no cambia: **confirmed**. La hoja se sirve desde `/static` bajo `default-src 'self'`, y no hay fuentes web (ADR-011).

### Stated criteria

Ninguno contradicho. Una precisión sobre el de "todo valor es un token": los trazos de 1 y 2 px no lo son, y van como excepción declarada en ADR-015 (decisión 2). Si prefieres que sean tokens, eso reabre s5.6.
