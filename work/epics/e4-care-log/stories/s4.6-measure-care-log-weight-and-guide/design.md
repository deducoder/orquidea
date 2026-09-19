# Story s4.6: Measure care log weight and guide — Design

> Complexity: moderate

## 1 · What & why

**Problem:** el brief mide que la ficha con 50 registros cargue en ≤ 200 KB (`must-perf-001`), pero nada lo comprueba: el script de e3 solo mide "Mi colección", y el README no dice nada del historial de cuidados.
**Value:** una prueba del gate protege el peso de la ficha aunque el historial llegue al tope, y quien despliega sabe qué guarda el historial, cuánto puede crecer y cómo medirlo.

## 2 · Approach

Sacar del script el montaje de la colección temporal a un administrador de contexto y usarlo desde dos mediciones: la de "Mi colección" (sin cambios de comportamiento) y una nueva, `medir_ficha(riegos, floraciones)`, que inserta los registros por SQL (500+500 en milisegundos) y mide el HTML de la ficha y el JavaScript en gzip, sin fotos, como ya hace la lista. `main` imprime las dos y sale con 1 si cualquiera pasa del presupuesto. Una prueba nueva en `tests/test_medicion.py` fija el presupuesto de la ficha con 50+50 y con el tope. El README gana la sección «Historial de cuidados».

**Components affected:**

- `scripts/medir-primera-carga.py`: modify — `coleccion_temporal()` (contexto), `medir_ficha`, y `main` que mide la lista y la ficha (50+50 y el tope).
- `tests/test_medicion.py`: modify — pruebas de `medir_ficha` y del presupuesto de la ficha.
- `README.md`: modify — sección «Historial de cuidados» y una línea sobre la compresión.
- `tests/test_despliegue.py`: modify — la cifra del tope (`CUIDADOS_MAXIMO`) entra en `test_cada_cifra_de_la_guia_es_la_de_su_constante`, para que guía y código no se separen.
- `records/parking-lot.md`: modify (con `park`) — la aplicación no comprime; el presupuesto es en gzip.

**Legacy sweep:** nada queda huérfano: `medir` conserva su firma y su resultado (`Medicion`) y `main` sigue aceptando los mismos argumentos. Orphaned tests: `test_medicion.py` (cuatro pruebas de `medir`/`main`) y `test_despliegue.py` (guía y variables) se corren; si `main` imprime más líneas, las que afirman sobre la salida se revisan.

## 3 · Interface / examples

### Usage (CLI y API)

```bash
uv run python scripts/medir-primera-carga.py                 # lista (25 fotos) y ficha (50+50 y 500+500)
uv run python scripts/medir-primera-carga.py --presupuesto 1 # sale con 1
```

```python
m = medicion.medir_ficha(riegos=50, floraciones=50)  # Medicion-like: html y javascript en gzip
m.total <= medicion.PRESUPUESTO  # True
```

### Expected output

```
Primera carga de "Mi colección" con 25 ejemplares con foto:
  HTML (gzip)           1.2 KB
  ...
  Total               146.5 KB   presupuesto 200 KB  OK
Primera carga de la ficha con 50 riegos y 50 floraciones:
  HTML (gzip)           ~1.5 KB
  JavaScript (gzip)    16.0 KB
  Total                ~17.5 KB   presupuesto 200 KB  OK
Primera carga de la ficha con 500 riegos y 500 floraciones (el tope):
  ...                             OK
```

### Key data structures

```python
@dataclass(frozen=True)
class MedicionDeFicha:
    riegos: int
    floraciones: int
    html: int  # gzip
    javascript: int  # gzip

    @property
    def total(self) -> int: ...


@contextmanager
def coleccion_temporal() -> Iterator[tuple[TestClient, sqlite3.Connection, str]]:
    """Base y fotos temporales sobre `app.state`, con una sesión iniciada; restaura al salir."""
```

### Gemba: lo medido

Medición de s4.4 (proceso real): la ficha con 500 riegos y 500 floraciones en curso pesa 500 476 bytes sin comprimir y 14 459 en gzip, y responde en 12 ms. El JavaScript (`htmx.min.js`) pesa ~16 KB en gzip: la ficha llena cabe en ~31 KB, un 15 % del presupuesto. **La aplicación no comprime respuestas** (no hay `GZipMiddleware`): el presupuesto se mide en gzip "como lo serviría un proxy" (decisión de e3) y sin compresión en el proxy la ficha llena bajaría 500 KB. Es la observación que s4.4 dejó a esta historia: se documenta en el README y se aparca con su condición de promoción; no se añade compresión (no lo pide ningún criterio y el proxy ya es requisito del despliegue).

## 4 · Acceptance criteria

**Must:**

- `medir_ficha` monta una colección temporal con un ejemplar, inserta `riegos` riegos y `floraciones` floraciones válidos por SQL, pide la ficha con una sesión válida y devuelve el HTML y el JavaScript en gzip.
- La medición no deja rastro: restaura `app.state` y borra el directorio temporal, aunque falle.
- La prueba del gate falla si la ficha con 50+50 o con 500+500 pasa de 200 KB.
- `main` mide la lista y la ficha y sale con 1 si cualquiera pasa del presupuesto; la medición de la lista no cambia.
- El README explica el historial (qué se guarda, fechas de calendario en UTC, tope de 500 por tipo y ejemplar, respaldo con la misma base) y la medición; la cifra del tope sale de `CUIDADOS_MAXIMO` y la prueba de la guía la comprueba.

**Should:**

- El README dice que la aplicación no comprime y que el presupuesto es en gzip; y que la medición con "Slow 3G" en el navegador con datos reales es la que vale.

**Must NOT:**

- No tocar las rutas, la ficha ni la base real: la medición usa su propia base temporal.
- No fijar en la prueba un peso exacto en bytes (frágil): solo el presupuesto y que la medición cuenta algo (`html > 0`, gzip menor que el HTML sin comprimir).

### ASVS L2 (`should-security-002`)

Sin cambios de comportamiento de la aplicación: solo un script y sus pruebas, sin entrada del usuario ni rutas nuevas. V14 (configuración): el README no debe contener secretos ni el hash de ninguna contraseña (la prueba existente de `test_despliegue.py` lo vigila). Los demás capítulos no aplican.

### Deduced criteria

- El script sigue midiendo la lista como antes: confirmed — `medir` conserva su firma y sus resultados; `test_medicion.py` lo prueba.
- La medición no toca la base real: confirmed — usa `app.state` temporal y lo restaura (mismo mecanismo que `medir`, con su prueba).
- Sale con 1 si la ficha pasa del presupuesto: confirmed — `main` compara el total de cada medición.

### Scenarios (delta over the scope)

```gherkin
Given una ficha con el tope de registros
When se mide con --presupuesto 1
Then el script sale con 1 y nombra la ficha que pasó

Given una medición que falla a la mitad
When termina
Then la aplicación conserva su ruta de base y su directorio de fotos originales
```
