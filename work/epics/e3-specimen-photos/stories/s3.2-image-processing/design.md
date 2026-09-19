# Story s3.2: Image processing — Design

> Complexity: moderate

## 1 · What & why

**Problem:** hoy no hay nada que decodifique ni reduzca una imagen, y una foto de teléfono llega con GPS en el EXIF, hasta 12 MP y con la orientación solo en los metadatos.
**Value:** `must-perf-002` y `must-security-001` pasan de ser una frase del guardarraíl a una función probada: lo que sale de ella no lleva metadatos y no pasa de 1600 px.

## 2 · Approach

Una función pura `procesar_foto(datos: bytes) -> FotoProcesada` en `orquidea.datos.fotos` que abre la imagen con Pillow, comprueba tamaño y píxeles, aplica la orientación EXIF, aplana la transparencia sobre blanco y reconstruye dos JPEG desde los píxeles: la imagen (ancho máximo 1600 px, sin ampliar) y la miniatura (lado mayor ≤ 320 px). Sin archivos, HTTP ni SQL (ADR-005).

**Components affected:**

- `src/orquidea/datos/fotos.py`: create — `procesar_foto`, `FotoProcesada` (dataclass congelada con `imagen: bytes` y `miniatura: bytes`), `FotoInvalida(ValueError)` y las constantes de límites.
- `pyproject.toml` / `uv.lock`: modify — dependencia `pillow`.
- `tests/test_datos_fotos.py`: create.

**Legacy sweep:** nothing — net-new. Ningún test existente importa un módulo cambiado (solo se añade una dependencia).

## 3 · Interface / examples

### Usage (API / CLI)

```python
from orquidea.datos.fotos import FotoInvalida, procesar_foto

foto = procesar_foto(open("orquidea.jpg", "rb").read())   # 4000x3000 con GPS
Image.open(io.BytesIO(foto.imagen)).size                  # (1600, 1200)
Image.open(io.BytesIO(foto.miniatura)).size               # (320, 240)
Image.open(io.BytesIO(foto.imagen)).getexif()             # vacío
```

### Expected output (success + error)

```
procesar_foto(jpeg 4000x3000 con GPS)   -> FotoProcesada(imagen=<JPEG 1600x1200>, miniatura=<JPEG 320x240>)
procesar_foto(jpeg 800x600)              -> imagen 800x600 (sin ampliar)
procesar_foto(b"no soy una imagen")     -> FotoInvalida("El archivo no es una imagen válida.")
procesar_foto(gif)                       -> FotoInvalida("Solo se admiten fotos JPEG, PNG o WebP.")
procesar_foto(>10 MB)                    -> FotoInvalida("La foto no puede pasar de 10 MB.")
procesar_foto(imagen de 20000x20000)     -> FotoInvalida("La foto es demasiado grande en píxeles.")
```

### Key data structures (if applicable)

```python
TAMANO_MAXIMO = 10 * 1024 * 1024      # bytes del archivo subido
PIXELES_MAXIMOS = 64_000_000           # ancho x alto; un teléfono de 50 MP cabe
ANCHO_MAXIMO = 1600
LADO_MINIATURA = 320
FORMATOS = frozenset({"JPEG", "PNG", "WEBP"})

@dataclass(frozen=True)
class FotoProcesada:
    imagen: bytes
    miniatura: bytes
```

## 4 · Acceptance criteria

**Must:**

- Ninguna de las dos salidas contiene EXIF, GPS, XMP, comentario ni perfil ICC (`must-security-001`); se comprueba leyendo los bytes de salida, no confiando en la API.
- La imagen mide ≤ 1600 px de ancho y la miniatura tiene su lado mayor ≤ 320 px, conservando la proporción y sin ampliar (`must-perf-002`).
- La orientación EXIF se aplica a los píxeles antes de descartar los metadatos.
- El tipo se decide por lo que Pillow decodifica; se rechaza lo que no sea JPEG, PNG ni WebP, y lo que exceda tamaño o píxeles **antes** de cargar los píxeles.
- Todo rechazo es `FotoInvalida` con mensaje en español; nunca escapa una excepción de Pillow.

**Should:**

- La calidad JPEG de la imagen es 85 y la de la miniatura 80, con `optimize=True`.

**Must NOT:**

- Escribir archivos o leer el disco; conservar el original; ampliar imágenes pequeñas; tomar el tipo del nombre o del `Content-Type`.

### ASVS L2 recorrido al diseñar (subida de archivos y entrada no confiable)

- V12.1.1 (tamaño máximo del archivo): cubierto aquí con `TAMANO_MAXIMO`; el límite del cuerpo de la petición es de s3.4/s3.6.
- V12.2.1 (tipo verificado, no confiado): cubierto — se decide por el decodificador y se reconstruye la salida.
- V12.3 (nombres de archivo): no aplicable aquí; s3.3 no usa el nombre subido (ADR-006).
- V12.4 (almacenamiento fuera de la raíz web) y V12.5 (descarga con tipo y cabeceras correctos): diferidos a s3.3 y s3.4.
- V5.2 (sanitización de entrada compleja): cubierto — la imagen no se reenvía, se reconstruye.
- V13/DoS por recursos: tope de píxeles y de bytes; `Image.MAX_IMAGE_PIXELS` se fija igual al tope y `DecompressionBombError` se trata como rechazo.
- Bandit: la función no usa `assert` ni `subprocess`.

### Deduced criteria

- Una imagen de 800x600 no se amplía: confirmed
- Un JPEG con orientación 6 sale girado y sin EXIF: confirmed
- Un PNG con alfa se aplana a JPEG sobre blanco: confirmed
- XMP, comentario e ICC no sobreviven: confirmed — la salida se reconstruye desde píxeles, con `save` sin esos argumentos
- Bytes que no son imagen o un formato no admitido → error de dominio en español: confirmed
- Tamaño o píxeles excedidos → mismo error antes de decodificar: confirmed — `Image.open` solo lee la cabecera; el tamaño de bytes se comprueba antes de abrir

### Scenarios (delta over the scope)

```gherkin
Given una imagen WebP de 3000x2000
When se procesa
Then se devuelve un JPEG de 1600x1067 y una miniatura, ambos sin metadatos

Given un JPEG truncado (cabecera válida, datos cortados)
When se procesa
Then se lanza FotoInvalida y no escapa OSError de Pillow

Given un PNG de 100x100 con un bloque de texto de metadatos
When se procesa
Then la salida no contiene ese texto (buscado en los bytes)
```
