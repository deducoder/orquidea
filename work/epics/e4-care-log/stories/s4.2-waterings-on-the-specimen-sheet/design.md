# Story s4.2: Waterings on the specimen sheet — Design

> Complexity: moderate

## 1 · What & why

**Problem:** los riegos ya se guardan (s4.1) pero ninguna ruta los registra y la ficha del ejemplar no los muestra.
**Value:** el coleccionista registra un riego en la ficha y ve el historial y la fecha del último; es la métrica líder del brief (RF-06) de punta a punta.

## 2 · Approach

Un router `cuidados` nuevo con dos POST (registrar, quitar) que validan la fecha con `validar_fecha`, llaman a `datos.riegos` y redirigen (303) a la ficha; y la ficha existente carga el historial y el último riego. Los errores vuelven a la misma ficha con 422, como ya hacen las fotos. Sin htmx: formularios y redirección, el patrón de e3.

**Components affected:**

- `orquidea/web/rutas/cuidados.py`: create — `POST /coleccion/{id}/riegos` y `POST /coleccion/{id}/riegos/{riego}/quitar`.
- `orquidea/web/rutas/coleccion.py`: modify — `_ficha` y `_ejemplar_o_404` pasan a ser públicos (`ficha`, `ejemplar_o_404`) porque `cuidados` los reutiliza; `ficha` recibe la conexión y añade `riegos` (más reciente primero), `ultimo` y `hoy` al contexto.
- `orquidea/web/app.py`: modify — monta el router.
- `orquidea/web/templates/ejemplar_ficha.html`: modify — sección «Riegos».
- `tests/test_web_cuidados.py`: create; `tests/test_web_rutas.py`: modify (mapa de rutas declarado); `tests/test_recorrido_coleccion.py`: modify (métrica líder de punta a punta).

**Legacy sweep:** nada queda huérfano. `_ficha` y `_ejemplar_o_404` cambian de nombre y de firma (la primera): sus llamadores están en `coleccion.py` (`ficha_del_ejemplar`, `subir_foto`) y en `cuidados.py`. Orphaned tests: `test_web_fotos.py` y `test_web_coleccion.py` pasan por la ficha; `test_web_rutas.py` enumera las rutas y **falla** si no se actualiza (se actualiza aquí); `test_web_proteccion.py` recorre las rutas registradas sin sesión y las cubre solo.

## 3 · Interface / examples

### Usage (HTTP)

```
POST /coleccion/1/riegos                 fecha=2026-09-15&csrf=…   -> 303 Location: /coleccion/1
POST /coleccion/1/riegos                 fecha=2026-09-25&csrf=…   -> 422 ficha con «La fecha no puede ser posterior a hoy.»
POST /coleccion/1/riegos/7/quitar        csrf=…                    -> 303 Location: /coleccion/1
POST /coleccion/1/riegos/7/quitar        (riego 7 es del ejemplar 2) -> 404
POST /coleccion/999/riegos               fecha=2026-09-15&csrf=…   -> 404
POST /coleccion/1/riegos                 sin sesión                -> 303 Location: /acceso
POST /coleccion/1/riegos                 sin token CSRF            -> 403
```

### Expected output (la sección de la ficha)

```html
<section>
  <h2>Riegos</h2>
  <p>Último riego: <strong>2026-09-15</strong></p>     <!-- o «Aún no hay riegos.» -->
  <form method="post" action="/coleccion/1/riegos">
    <input type="hidden" name="csrf" value="…">
    <label for="fecha">Fecha del riego</label>
    <input id="fecha" name="fecha" type="date" value="2026-09-19" max="2026-09-19" required>
    <button type="submit">Registrar riego</button>
  </form>
  <ul>  <!-- más reciente primero -->
    <li>2026-09-15 <form method="post" action="/coleccion/1/riegos/7/quitar">…<button>Quitar</button></form></li>
  </ul>
</section>
```

### Key data structures

```python
def hoy() -> date:  # una sola definición, en cuidados.py
    return datetime.now(UTC).date()


def ficha(request, conexion, estado, ejemplar, error="", fecha="") -> HTMLResponse: ...
```

`hoy` sale de la ruta y se pasa a `validar_fecha`; el dominio no llama al reloj (s4.1). El campo de la fecha se rellena con `fecha` si la validación falló y con `hoy` si no.

## 4 · Acceptance criteria

**Must:**

- Registrar con una fecha válida guarda el riego, redirige a la ficha y la ficha muestra ese riego y «Último riego».
- Una fecha inválida, inexistente o futura, o el tope, vuelve a la ficha con 422 y el mensaje, sin cambiar la base; la ficha conserva lo que el usuario escribió, escapado.
- Quitar filtra por ejemplar y riego: un riego ajeno o inexistente da 404 y no se borra; tras quitar, el último se recalcula.
- Un ejemplar inexistente da 404 en ambas rutas; sin sesión redirige al acceso; sin token CSRF, 403 (dependencia global, con una prueba explícita de cada ruta).
- El mapa de rutas declarado incluye las dos rutas nuevas y `/coleccion/nuevo` sigue registrándose antes que `/coleccion/{id}`.

**Should:**

- El campo de fecha es `type="date"` con `max` de hoy y valor por defecto hoy: registrar el riego de hoy es un clic.

**Must NOT:**

- No usar htmx ni JavaScript nuevo.
- No aceptar otro dato del formulario que la fecha: el id del ejemplar y del riego solo vienen de la ruta y siempre acompañados del filtro por ejemplar.
- No dejar `date.today()` ni `datetime.now()` dispersos: `hoy()` es único.

### ASVS L2 (`should-security-002`), recorrido desde el diseño

- **V4 control de acceso:** cubierto — sesión y CSRF por la dependencia global (`exigir_sesion`), prueba de las dos rutas nuevas sin sesión y sin token; IDOR: riego de otro ejemplar da 404 (prueba con dos ejemplares).
- **V5 validación y codificación de salida:** cubierto — `validar_fecha` antes de `agregar`; el valor devuelto en el campo va con el escape de Jinja; prueba con `"><script>` que no aparece sin escapar.
- **V11 lógica de negocio:** cubierto — tope de 500 (mensaje claro, 422) y fecha no futura.
- **V8/V14 (protección de datos, cabeceras):** cubierto por el middleware existente (`Cache-Control: no-store`, CSP); las rutas nuevas lo heredan; sin cambios.
- **V7 registro de eventos:** no aplica — registrar o quitar un riego no es un evento de seguridad; los rechazos por sesión y CSRF ya los tratan sus dependencias.
- **V2/V3 (contraseñas, sesión):** no aplica a esta historia.
- **Concurrencia y proceso real** (memoria del proyecto): no hay estado compartido nuevo en la ruta (el tope ya es atómico, s4.1); la comprobación con `uvicorn` real se hace en la prueba manual.

### Deduced criteria

- Sin riegos: «Aún no hay riegos.» y sin «Último riego»: confirmed.
- Tope de riegos rechazado con mensaje claro: confirmed — `agregar` lanza `CuidadoInvalido`, la ruta lo devuelve como 422.
- Sin sesión no se registra ni se quita nada: confirmed — dependencia global; además la prueba de `test_web_proteccion` recorre las rutas nuevas.
- Sin token CSRF se rechaza: confirmed — 403 desde `exigir_sesion`.
- Id inexistente o ajeno da 404: confirmed — `ejemplar_o_404` y `quitar` devuelve `False`.
- Un ejemplar no afecta a otro: confirmed — todo filtra por `ejemplar_id`.

### Scenarios (delta over the scope)

```gherkin
Given un riego cuya fecha se rechazó y el texto "><script>alert(1)</script>
When la ficha vuelve con el error
Then el campo lo muestra escapado y nunca como marcado

Given tres riegos guardados en desorden de fechas
When se abre la ficha
Then la lista los muestra del más reciente al más antiguo y «Último riego» es el mayor

Given un ejemplar con foto
When se registra un riego
Then la foto y sus formularios siguen en la ficha sin cambios
```
