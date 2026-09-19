import io
from dataclasses import dataclass

from PIL import Image, ImageOps

ANCHO_MAXIMO = 1600
LADO_MINIATURA = 320


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


def procesar_foto(datos: bytes) -> FotoProcesada:
    origen = Image.open(io.BytesIO(datos))
    # La orientación vive en el EXIF: se aplica a los píxeles antes de descartarlo.
    girada = ImageOps.exif_transpose(origen)
    if girada.mode in ("RGBA", "LA", "P"):
        fondo = Image.new("RGB", girada.size, (255, 255, 255))
        convertida = girada.convert("RGBA")
        fondo.paste(convertida, mask=convertida.getchannel("A"))
        rgb = fondo
    else:
        rgb = girada.convert("RGB")
    # `Image.info` viaja con la imagen (Pillow copia de ahí el comentario JPEG al guardar):
    # una imagen nueva hecha solo con los bytes de los píxeles no arrastra nada del archivo.
    plana = Image.frombytes("RGB", rgb.size, rgb.tobytes())

    imagen = plana.copy()
    if imagen.width > ANCHO_MAXIMO:
        alto = round(imagen.height * ANCHO_MAXIMO / imagen.width)
        imagen = imagen.resize((ANCHO_MAXIMO, alto), Image.Resampling.LANCZOS)
    miniatura = plana.copy()
    miniatura.thumbnail((LADO_MINIATURA, LADO_MINIATURA), Image.Resampling.LANCZOS)
    return FotoProcesada(imagen=_jpeg(imagen, 85), miniatura=_jpeg(miniatura, 80))
