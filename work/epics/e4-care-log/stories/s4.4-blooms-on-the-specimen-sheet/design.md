# Story s4.4: Blooms on the specimen sheet — Design

> Complexity: moderate

## 1 · What & why

**Problem:** las floraciones ya se guardan (s4.3) pero ninguna ruta las registra ni las cierra, y la ficha no las muestra.
**Value:** el coleccionista registra cuándo floreció cada planta, cierra la floración cuando termina y ve el historial; cierra RF-07 y completa la ficha que mide el brief.

## 2 · Approach

Tres POST más en el router `cuidados` (registrar, fijar el fin, quitar), con la forma que ya tienen los de riegos: validar con el dominio, llamar a `datos.floraciones`, 303 a la ficha o 422 con el mensaje. La ficha carga el historial de floraciones y `ficha()` cambia el argumento suelto `fecha` por un diccionario `valores` con lo que el usuario escribió, porque ahora hay tres formularios que pueden volver con error y cada uno conserva sus campos.

**Components affected:**

- `orquidea/web/rutas/cuidados.py`: modify — `POST /coleccion/{id}/floraciones`, `.../{floracion}/fin`, `.../{floracion}/quitar`.
- `orquidea/web/rutas/coleccion.py`: modify — `ficha(..., error="", valores=None)` en lugar de `fecha`; el contexto añade `floraciones` (más reciente primero), `inicio`, `fin` y `fecha` desde `valores`.
- `orquidea/web/templates/ejemplar_ficha.html`: modify — sección «Floraciones».
- `tests/test_web_cuidados.py`, `tests/test_web_rutas.py`, `tests/test_recorrido_coleccion.py`: modify.

**Legacy sweep:** el parámetro `fecha` de `ficha` desaparece: su único llamador es `registrar_riego` (`cuidados.py:22`), que pasa a `{"fecha": fecha}`; ningún otro código lo usa. Orphaned tests: `test_web_rutas.py` enumera las rutas y **falla** si no se actualiza (se actualiza aquí); `test_web_proteccion.py` recorre las rutas registradas sin sesión y las cubre solo; `test_web_fotos.py` y `test_web_coleccion.py` pasan por la ficha y se corren.

## 3 · Interface / examples

### Usage (HTTP)

```
POST /coleccion/1/floraciones               inicio=2026-03-01&fin=&csrf=…      -> 303 Location: /coleccion/1
POST /coleccion/1/floraciones               inicio=2026-03-20&fin=2026-03-01   -> 422 «El fin no puede ser anterior al inicio.»
POST /coleccion/1/floraciones/4/fin         fin=2026-03-20&csrf=…              -> 303 Location: /coleccion/1
POST /coleccion/1/floraciones/4/fin         (ya terminada)                     -> 422 «Esa floración ya terminó.»
POST /coleccion/1/floraciones/4/quitar      csrf=…                             -> 303 Location: /coleccion/1
POST /coleccion/1/floraciones/5/quitar      (es del ejemplar 2)                -> 404
POST /coleccion/1/floraciones/5/fin         (es del ejemplar 2)                -> 404
POST /coleccion/999/floraciones             …                                  -> 404
sin sesión / sin token                                                         -> 303 al acceso / 403
```

### Expected output (la sección de la ficha)

```html
<section>
  <h2>Floraciones</h2>
  <p>Aún no hay floraciones.</p>                                  <!-- o la lista -->
  <form method="post" action="/coleccion/1/floraciones">
    <input type="hidden" name="csrf" value="…">
    <label for="inicio">Inicio de la floración</label>
    <input id="inicio" name="inicio" type="date" value="2026-09-19" max="2026-09-19" required>
    <label for="fin">Fin (si ya terminó)</label>
    <input id="fin" name="fin" type="date" max="2026-09-19">
    <button type="submit">Registrar floración</button>
  </form>
  <ul>  <!-- más reciente primero -->
    <li>2026-03-01 — en curso
      <form method="post" action="/coleccion/1/floraciones/4/fin">…<input name="fin" type="date" min="2026-03-01" max="2026-09-19" required><button>Terminar</button></form>
      <form method="post" action="/coleccion/1/floraciones/4/quitar">…<button>Quitar</button></form></li>
    <li>2025-02-01 — 2025-02-20 <form …/quitar>…</form></li>
  </ul>
</section>
```

### Key data structures

```python
def ficha(
    request, conexion, estado, ejemplar, error="", valores: Mapping[str, str] | None = None
) -> HTMLResponse: ...


# valores: {"fecha": …} del riego, {"inicio": …, "fin": …} de la floración; lo que falte cae a hoy
```

Las rutas nuevas reutilizan `validar_floracion(inicio, fin, hoy())` para registrar y `validar_fecha(fin, hoy())` para terminar (el inicio de la floración lo compara `datos.floraciones.terminar`, en una sola sentencia).

### Gemba: lo medido con el tamaño máximo

s4.1 y s4.3 midieron los historiales en el tope (500 riegos: ~97 KB de HTML sin comprimir con un formulario por fila; 500 floraciones con dos formularios cada una: ~210 KB). Aquí «Terminar» solo se dibuja en las que están en curso, así que el peor caso realista es 500 en curso (~210 KB) o 500 terminadas (~100 KB). La página completa con los dos historiales llenos puede rondar 300 KB sin comprimir; el presupuesto de `must-perf-001` es en gzip (s4.6 lo mide y decide). En esta historia se anota la cifra real de la ficha con 500 y 500 (T4, prueba manual).

## 4 · Acceptance criteria

**Must:**

- Registrar valida con `validar_floracion` antes de `agregar`; una floración sin fin queda en curso y con fin, terminada; guarda, redirige (303) y la ficha la muestra.
- Fijar el fin valida con `validar_fecha` y usa `terminar`; una floración ya terminada o con fin anterior vuelve con 422 y el mensaje del dominio; una ajena o inexistente da 404.
- Quitar filtra por ejemplar y floración: una ajena o inexistente da 404 y no se borra.
- Un ejemplar inexistente da 404 en las tres rutas; sin sesión redirige al acceso; sin token CSRF, 403 (dependencia global, con prueba explícita por ruta).
- Todo error vuelve a la misma ficha con 422, sin cambiar la base y con los campos escritos devueltos escapados; el mapa de rutas declarado incluye las tres nuevas.

**Should:**

- El formulario de «Terminar» lleva `min` (el inicio) y `max` (hoy), y el de registrar, hoy por defecto en el inicio: registrar la floración de hoy es un clic.

**Must NOT:**

- No ofrecer «Terminar» en una floración ya terminada.
- No aceptar otros datos del formulario que las fechas: los ids solo vienen de la ruta y siempre con el filtro por ejemplar.
- No dejar `hoy()` duplicado: se reutiliza el de `coleccion.py`.

### ASVS L2 (`should-security-002`), recorrido desde el diseño

- **V4 control de acceso:** cubierto — sesión y CSRF por la dependencia global con pruebas explícitas de las tres rutas; IDOR: floración ajena da 404 en `fin` y `quitar` (prueba con dos ejemplares).
- **V5 validación y codificación de salida:** cubierto — dominio antes de tocar la base; los campos devueltos van con el escape de Jinja; prueba con `"><script>` en `inicio` y en `fin`.
- **V11 lógica de negocio:** cubierto — tope de 500, fecha no futura, fin no anterior al inicio, no terminar dos veces (todo del dominio y de `terminar`).
- **V8/V14:** heredado del middleware (`Cache-Control: no-store`, CSP), sin cambios.
- **V7, V2/V3:** no aplican.
- **Concurrencia y proceso real** (memoria del proyecto): sin estado compartido nuevo en la ruta (tope y `terminar` ya son atómicos, s4.3); la comprobación con `uvicorn` real va en la prueba manual.

### Deduced criteria

- Sin floraciones: «Aún no hay floraciones.»: confirmed.
- Historial de más reciente a más antigua y «Terminar» solo en las que están en curso: confirmed — `listar` ascendente por inicio, la ficha lo invierte; la plantilla condiciona por `fin`.
- Tope con mensaje claro: confirmed — `agregar` lanza `CuidadoInvalido`, la ruta lo devuelve como 422.
- Sin sesión no cambia nada: confirmed — dependencia global; `test_web_proteccion` recorre las rutas nuevas.
- Sin token CSRF se rechaza: confirmed — 403 desde `exigir_sesion`.
- Id inexistente o ajeno da 404: confirmed — `ejemplar_o_404` y `terminar`/`quitar` devuelven `False`.
- Riegos y foto no cambian al tocar floraciones: confirmed — cada ruta toca solo su tabla.

### Scenarios (delta over the scope)

```gherkin
Given una floración cuyo fin se rechazó y el texto "><script>alert(1)</script>
When la ficha vuelve con el error
Then el campo lo muestra escapado y nunca como marcado

Given tres floraciones guardadas en desorden de inicio
When se abre la ficha
Then la lista las muestra de la más reciente a la más antigua

Given una floración ya terminada
When se abre la ficha
Then no ofrece «Terminar» pero sí «Quitar»

Given un ejemplar con floraciones y riegos
When se registra un riego que falla
Then el formulario de riegos conserva lo escrito y el de floraciones muestra sus valores por defecto
```
