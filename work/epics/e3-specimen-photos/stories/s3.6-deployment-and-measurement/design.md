# Story s3.6: Deployment and measurement — Design

> Complexity: moderate

## 1 · What & why

**Problem:** la guía y el `Dockerfile` no dicen nada de las fotos; nadie ha medido cuánto pesa "Mi colección" con miniaturas, y `must-perf-001` cuenta las miniaturas en sus 200 KB; y las cifras de la guía se escriben a mano y pueden envejecer sin que nada falle (parking lot).
**Value:** las fotos sobreviven a un redespliegue dentro del volumen, la guía es exacta y una prueba vigila el presupuesto de peso.

## 2 · Approach

Tres piezas pequeñas. (1) El `Dockerfile` no cambia de comportamiento: `ORQUIDEA_FOTOS` sin definir cae en `/data/fotos` (junto a la base); una prueba de deriva lo fija y el README lo explica. (2) Pruebas de deriva que importan las constantes (foto máxima, ancho, cuerpo, sesión, intentos) y las buscan en el README. (3) Un script `scripts/medir-primera-carga.py` con la lógica en una función `medir` que la suite también llama: monta una colección temporal con fotos con detalle, pide `/coleccion`, los estáticos y todas las miniaturas y suma bytes (HTML y JavaScript en gzip; las miniaturas ya son JPEG). La medición dio ~15 KB por miniatura de 320 px con ruido fractal (proxy de foto) y la lista las muestra a 96 px: se baja la miniatura a 192 px (2x) y calidad 75 (ADR-007 sustituye a ADR-005).

**Components affected:**

- `scripts/medir-primera-carga.py`: create — `medir(fotos, n)` y `main`; sale con 1 si pasa de 200 KB.
- `orquidea/datos/fotos.py`: modify — `LADO_MINIATURA` 192 y calidad de la miniatura 75.
- `README.md`: modify — volumen con base y fotos, respaldo, límites, proxy, sin ubicación, medición.
- `Dockerfile`: modify — solo un comentario que ata `ORQUIDEA_FOTOS` al volumen (sin cambio de comportamiento).
- `records/decisions/adr-007-...`, `adr-005-...`: create / status.
- `tests/test_despliegue.py`, `tests/test_medicion.py`, `tests/test_datos_fotos.py`: modify/create.
- `records/parking-lot.md`: modify — retirar "Las cifras de la guía de despliegue están escritas a mano" (`park`).

**Legacy sweep:** `test_datos_fotos.py` fija el tamaño de la miniatura con la constante y con literales `320`/`240` para 800x600: se actualizan al nuevo tamaño (aserciones sobre el tamaño de la miniatura, no de comportamiento). `test_web_fotos.py` usa `<= 320` para la miniatura y sigue valiendo. El scope de s3.2 dice "lado mayor ≤ 320": 192 lo cumple. ADR-005 queda `superseded by ADR-007`.

## 3 · Interface / examples

```
$ uv run python scripts/medir-primera-carga.py
Primera carga de "Mi colección" con 25 ejemplares con foto:
  HTML (gzip)              2.1 KB
  JavaScript (gzip)       15.9 KB   (/static/htmx.min.js)
  Miniaturas (25)        118.0 KB   (4.7 KB c/u)
  Total                  136.0 KB   presupuesto 200 KB  OK

$ uv run python scripts/medir-primera-carga.py ~/fotos/*.jpg     # con fotos reales
$ echo $?   # 0 dentro del presupuesto, 1 si lo pasa
```

```python
def medir(fotos: list[bytes] | None = None, n: int = 25) -> Medicion: ...


PRESUPUESTO = 200 * 1024
```

## 4 · Acceptance criteria

**Must:**

- La imagen guarda las fotos dentro del volumen: una prueba con el `Dockerfile` (`ORQUIDEA_DB` bajo `VOLUME`) y `directorio_de_fotos` lo comprueba.
- La guía dice: `/data` guarda base y fotos y se respaldan juntas; foto máxima "10 MB" y "1600 px"; el proxy debe permitir cuerpos de "11 MiB"; las fotos se guardan sin ubicación; el propietario del directorio del volumen. Una prueba compara cada cifra con su constante.
- La medición de la colección de ejemplo (25 ejemplares con foto con detalle) da ≤ 200 KB y la prueba lo exige; el script sale con 1 si no.
- La miniatura nueva mide ≤ 192 px de lado mayor, sin metadatos, y pesa menos que la de 320 px para la misma foto.

**Should:** el script acepta rutas de fotos reales; la guía dice cómo medir con "Slow 3G".

**Must NOT:** cambiar el tamaño de la imagen a tamaño completo (1600 px); tocar el comportamiento del `Dockerfile`; afirmar en la guía que el build de Docker se verificó.

### ASVS L2 / seguridad

- Nada de entrada de usuario nueva. La guía no incluye secretos ni el hash.
- V12.4: el directorio de fotos sigue dentro del volumen y fuera de `/static`; la guía lo aclara.
- V8 (datos guardados): fotos sin EXIF ni ubicación, comprobado en s3.2/s3.4; la guía lo dice.

### Deduced criteria

- Fotos dentro del volumen sin definir `ORQUIDEA_FOTOS`: confirmed — `directorio_de_fotos` cae en `{base}/../fotos` y la base está en `/data`
- La guía dice respaldo, límites, proxy y ubicación: confirmed
- Prueba de deriva de cada cifra: confirmed
- El script imprime el desglose y sale con 1 si se pasa: confirmed
- Miniatura más ligera y nítida a 2x: confirmed — 192 px para una imagen mostrada a 96 px; la medición con el proxy lo respalda (15.5 KB → 5.2 KB)

### Scenarios (delta over the scope)

```gherkin
Given una colección de 25 ejemplares con foto con detalle
When se mide con el proxy de foto
Then las miniaturas suman menos de 150 KB y el total menos de 200 KB

Given `ORQUIDEA_FOTOS` definida
When arranca la aplicación
Then las fotos van a ese directorio y la guía advierte que debe estar dentro de un volumen
```
