# Story s1.2: Catalog schema and loader — Design

> Complexity: moderate

## 1 · What & why

**Problem:** no existe el catálogo: ni la forma de una especie ni cómo cargarla; sin eso, ficha, búsqueda y semilla no tienen contrato.
**Value:** RF-01 y `must-data-001` quedan garantizados en un solo punto: un dato sin fuente o mal formado no entra al catálogo, y el error dice dónde.

## 2 · Approach

Modelos pydantic de la especie (dominio) y una función `cargar_catalogo(directorio)` (datos) que valida todos los JSON, acumula los errores con archivo y campo, y devuelve la lista completa o lanza `CatalogoInvalido` (ADR-002).

**Components affected:**

- `src/orquidea/catalogo/__init__.py`, `src/orquidea/catalogo/modelo.py`: create — `Especie`, `Cuidados`, `Cuidado`.
- `src/orquidea/datos/__init__.py`, `src/orquidea/datos/catalogo.py`: create — `cargar_catalogo`, `CatalogoInvalido`, `DIRECTORIO_CATALOGO`.
- `src/orquidea/datos/catalogo/`: create — directorio de datos del catálogo, vacío por ahora (con `.gitkeep`); los datos reales son s1.6. (Difiere del `catalogo/*.json` en la raíz que el diseño de la épica supuso: dentro del paquete viaja con él, ADR-002.)
- `pyproject.toml`, `uv.lock`: modify — `pydantic` como dependencia directa.
- `tests/test_catalogo_modelo.py`, `tests/test_catalogo_carga.py`: create.

**Legacy sweep:** nada — net-new. Gobernanza: RF-01, RF-03, `must-data-001`, system-design (el dominio no conoce HTTP ni SQL; `orquidea.catalogo` no importa `orquidea.web`), `must-quality-001..003`. Sin dependencias nuevas de instalación (pydantic ya llega con FastAPI). Un directorio de datos con nombre `catalogo` dentro de `datos` y un paquete `orquidea.catalogo` no chocan: rutas y módulos distintos.

## 3 · Interface / examples

### Usage (API / CLI)

```python
from pathlib import Path
from orquidea.datos.catalogo import cargar_catalogo, CatalogoInvalido

especies = cargar_catalogo(Path("src/orquidea/datos/catalogo"))
```

### Expected output (success + error)

```
# éxito: list[Especie], ordenada por id
[Especie(id="epidendrum-radicans", nombre_cientifico="Epidendrum radicans", ...)]

# error: falta la fuente
CatalogoInvalido:
  epidendrum-radicans.json: fuentes: Field required

# error: campo de cuidado ausente
CatalogoInvalido:
  epidendrum-radicans.json: cuidados.riego.fuente: Field required

# error: no es JSON
CatalogoInvalido:
  roto.json: JSON inválido (línea 3, columna 1)

# error: id duplicada
CatalogoInvalido:
  b.json: id: duplicada de a.json ("epidendrum-radicans")
```

`str(CatalogoInvalido)` lista una línea por error; `CatalogoInvalido.errores` es la lista de esas líneas.

### Key data structures (if applicable)

```python
class Cuidado(BaseModel):          # extra="forbid"
    texto: str          # min_length=1
    fuente: str         # min_length=1

class Cuidados(BaseModel):
    luz: Cuidado
    riego: Cuidado
    temperatura: Cuidado
    sustrato: Cuidado

class Especie(BaseModel):
    id: str             # ^[a-z0-9]+(-[a-z0-9]+)*$ (slug para la URL de la ficha)
    nombre_cientifico: str   # min_length=1
    nombres_comunes: list[str] = []
    descripcion: str    # información general, min_length=1
    cuidados: Cuidados
    fuentes: list[str]  # min_length=1 — must-data-001; cada str min_length=1
```

## 4 · Acceptance criteria

- **Must:** un catálogo válido se carga completo y ordenado por `id`; falta de `fuentes` (o lista vacía) se rechaza nombrando archivo y `fuentes`; campo ausente, de tipo incorrecto o desconocido se rechaza nombrando archivo y ruta del campo; todo o nada; JSON inválido e ids duplicadas se rechazan nombrando archivo.
- **Should:** todos los errores de todos los archivos se reúnen en una sola excepción, no solo el primero.
- **Must NOT:** devolver un catálogo parcial; tragar un archivo con `except` amplio; importar `orquidea.web` desde `orquidea.catalogo` o `orquidea.datos`; escribir a disco.

### Deduced criteria

- todo o nada (nunca un catálogo parcial): confirmed — RF-01 y system-design lo exigen ("completo y válido o no se carga").
- JSON inválido → error que nombra el archivo: confirmed.
- ids duplicadas → error que nombra ambos archivos: confirmed — la ficha de s1.3 se dirige por `id`; una duplicada haría ambigua la URL.
- `./scripts/check` en verde: confirmed.

### Scenarios (delta over the scope)

```gherkin
Given un directorio sin archivos JSON
When cargo el catálogo
Then obtengo una lista vacía

Given un directorio que no existe
When cargo el catálogo
Then la carga falla con CatalogoInvalido nombrando el directorio
```
