# Story s4.5: Last watering in my collection — Design

> Complexity: simple

## 1 · What & why

**Problem:** "Mi colección" no dice nada de los riegos; para saber cuándo se regó una planta hay que abrir su ficha, y una consulta por ejemplar haría la lista más lenta cuanto más crece la colección.
**Value:** de un vistazo se ve cuál planta lleva más tiempo sin regarse (RF-06), con un costo fijo de una consulta.

## 2 · Approach

Una función `ultimos(conexion)` que devuelve `{ejemplar_id: fecha}` con `SELECT ejemplar_id, MAX(fecha) FROM riegos GROUP BY ejemplar_id` (la sirve el índice `(ejemplar_id, fecha)` de s4.1); la ruta de la lista la llama una vez y la plantilla busca cada ejemplar en el diccionario.

**Components affected:**

- `orquidea/datos/riegos.py`: modify — `ultimos`.
- `orquidea/web/rutas/coleccion.py`: modify — `mi_coleccion` carga `ultimos` una vez.
- `orquidea/web/templates/coleccion.html`: modify — «Último riego: AAAA-MM-DD» o «Sin riegos» en cada fila.
- `tests/test_datos_riegos.py`, `tests/test_web_cuidados.py`: modify.

**Legacy sweep:** nada — net-new. Orphaned tests: `test_web_coleccion.py` (la lista), `test_web_fotos.py` (miniaturas en la lista) y `test_medicion.py` (peso de la lista con miniaturas) pasan por `coleccion.html`; se corren, y ninguna aserción de ellas cambia porque solo se añade texto a cada fila.

## 3 · Interface / examples

### Usage (API)

```python
from orquidea.datos.riegos import ultimos

ultimos(conexion)  # {1: "2026-09-15", 3: "2026-08-30"}  (el ejemplar 2 no aparece: no tiene riegos)
```

### Expected output (success + error)

```html
<li> … <small>Agregado el 2026-09-19</small> <small>Último riego: 2026-09-15</small> …
<li> … <small>Agregado el 2026-09-19</small> <small>Sin riegos</small> …
```

Sin error posible: es solo lectura; sin riegos la función devuelve `{}`.

### Gemba

`MAX(fecha)` y la ficha (`ORDER BY fecha DESC, id DESC LIMIT 1`) dan la misma fecha: el desempate por id no cambia la fecha. La lista ya recorre todos los ejemplares en Python; el costo nuevo es una consulta agregada sobre un índice. El peso: unos 35 bytes por fila; `test_medicion.py` y el script `medir-primera-carga.py` ya cuentan el HTML de la lista dentro del presupuesto, con mucho margen (s4.6 lo vuelve a medir).

## 4 · Acceptance criteria

**Must:**

- `ultimos` devuelve el mayor `fecha` de cada ejemplar con riegos en una sola sentencia; los ejemplares sin riegos no aparecen.
- La lista carga `ultimos` una sola vez por petición, con independencia del número de ejemplares (prueba que cuenta las llamadas y otra que cuenta las sentencias SQL).
- Cada fila muestra el último de su propio ejemplar o «Sin riegos», y coincide con la ficha.

**Should:**

- El texto usa el mismo formato `AAAA-MM-DD` que el resto de la interfaz.

**Must NOT:**

- No hacer una consulta por ejemplar.
- No añadir entrada del usuario ni rutas nuevas.

### ASVS L2 (`should-security-002`)

Solo lectura por una ruta que ya exige sesión. V4: sin cambios (la dependencia global y sus pruebas cubren `/coleccion`). V5 salida: la fecha viene de la base y va con el escape automático de la plantilla. V7, V8, V11: no aplican.

### Deduced criteria

- Sin riegos dice «Sin riegos»: confirmed.
- Muestra el de mayor fecha, igual que la ficha: confirmed — `MAX(fecha)`; una prueba compara la lista con la ficha.
- Cada fila el suyo: confirmed — `GROUP BY ejemplar_id`.
- Tras quitar un riego, la lista se actualiza: confirmed — se lee de la base en cada petición (`Cache-Control: no-store`).

### Scenarios (delta over the scope)

```gherkin
Given cinco ejemplares con riegos
When se abre "Mi colección"
Then se ejecuta una sola sentencia sobre la tabla de riegos
```
