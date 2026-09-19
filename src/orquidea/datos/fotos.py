import io
from dataclasses import dataclass

from PIL import Image, ImageOps

TAMANO_MAXIMO = 10 * 1024 * 1024
PIXELES_MAXIMOS = 64_000_000
ANCHO_MAXIMO = 1600
LADO_MINIATURA = 192
FORMATOS = frozenset({"JPEG", "PNG", "WEBP"})

# Pillow avisa a partir de este tope y lanza `DecompressionBombError` al doble.
Image.MAX_IMAGE_PIXELS = PIXELES_MAXIMOS


class FotoInvalida(ValueError):
    pass


@dataclass(frozen=True)
class FotoProcesada:
    imagen: bytes
    miniatura: bytes


def _jpeg(imagen: Image.Image, calidad: int) -> bytes:
    # Se guarda sin `exif`, `xmp`, `comment` ni `icc_profile`: el archivo se reconstruye
    # solo con los píxeles, así que ningún metadato del original puede sobrevivir.
    salida = io.BytesIO()
    imagen.save(salida, format="JPEG", quality=calidad, optimize=True)
    return salida.getvalue()


def _abrir(datos: bytes) -> Image.Image:
    if len(datos) > TAMANO_MAXIMO:
        raise FotoInvalida(f"La foto no puede pasar de {TAMANO_MAXIMO // (1024 * 1024)} MB.")
    try:
        # Solo lee la cabecera: el tipo sale de lo que Pillow decodifica, no del nombre.
        origen = Image.open(io.BytesIO(datos))
    except Image.DecompressionBombError as fallo:
        raise FotoInvalida("La foto es demasiado grande en píxeles.") from fallo
    except OSError as fallo:
        raise FotoInvalida("El archivo no es una imagen válida.") from fallo
    if origen.format not in FORMATOS:
        raise FotoInvalida("Solo se admiten fotos JPEG, PNG o WebP.")
    if origen.width * origen.height > PIXELES_MAXIMOS:
        raise FotoInvalida("La foto es demasiado grande en píxeles.")
    return origen


def procesar_foto(datos: bytes) -> FotoProcesada:
    origen = _abrir(datos)
    try:
        return _reconstruir(origen)
    except (OSError, SyntaxError, ValueError) as fallo:
        # Un archivo truncado o corrupto solo falla al decodificar los píxeles.
        raise FotoInvalida("El archivo no es una imagen válida.") from fallo


ORIENTACION = 0x0112  # etiqueta EXIF de la orientación
_MODOS_QUE_ESCALAN_BIEN = frozenset({"RGB", "RGBA", "L", "LA"})


def _sobre_blanco(imagen: Image.Image) -> Image.Image:
    if imagen.mode in ("RGBA", "LA"):
        convertida = imagen.convert("RGBA")
        fondo = Image.new("RGB", convertida.size, (255, 255, 255))
        fondo.paste(convertida, mask=convertida.getchannel("A"))
        return fondo
    return imagen.convert("RGB")


def _reconstruir(origen: Image.Image) -> FotoProcesada:
    # Los píxeles de una foto de teléfono (48 MP) son ~150 MB por copia: se reduce antes de
    # copiar, y solo se copia lo que hace falta (ver `test_datos_fotos_memoria.py`).
    # La orientación vive en el EXIF: se aplica a los píxeles antes de descartarlo. Sin
    # orientación no se copia nada (`exif_transpose` siempre copia).
    orientada = (
        ImageOps.exif_transpose(origen) if origen.getexif().get(ORIENTACION, 1) != 1 else origen
    )
    if orientada.mode not in _MODOS_QUE_ESCALAN_BIEN:
        orientada = orientada.convert("RGBA")  # paletas y otros modos se escalan mal
    if orientada.width > ANCHO_MAXIMO:
        alto = round(orientada.height * ANCHO_MAXIMO / orientada.width)
        orientada = orientada.resize(
            (ANCHO_MAXIMO, alto), Image.Resampling.LANCZOS, reducing_gap=2.0
        )
    rgb = _sobre_blanco(orientada)
    # `Image.info` viaja con la imagen (Pillow copia de ahí el comentario JPEG al guardar):
    # una imagen nueva hecha solo con los bytes de los píxeles no arrastra nada del archivo.
    imagen = Image.frombytes("RGB", rgb.size, rgb.tobytes())
    miniatura = imagen.copy()
    miniatura.thumbnail((LADO_MINIATURA, LADO_MINIATURA), Image.Resampling.LANCZOS)
    return FotoProcesada(imagen=_jpeg(imagen, 85), miniatura=_jpeg(miniatura, 75))
