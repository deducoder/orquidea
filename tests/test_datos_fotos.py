import io

import pytest
from PIL import ExifTags, Image
from PIL.PngImagePlugin import PngInfo

from orquidea.datos.fotos import (
    ANCHO_MAXIMO,
    LADO_MINIATURA,
    TAMANO_MAXIMO,
    FotoInvalida,
    procesar_foto,
)

MARCADOR_XMP = b"http://ns.adobe.com/xap"
COMENTARIO = "coordenadas-secretas-16.75N"


def _jpeg(
    ancho: int = 4000,
    alto: int = 3000,
    *,
    con_metadatos: bool = True,
    orientacion: int | None = None,
) -> bytes:
    imagen = Image.new("RGB", (ancho, alto), (200, 80, 120))
    argumentos: dict[str, object] = {}
    if con_metadatos:
        exif = Image.Exif()
        gps = exif.get_ifd(ExifTags.IFD.GPSInfo)
        gps[ExifTags.GPS.GPSLatitudeRef] = "N"
        gps[ExifTags.GPS.GPSLatitude] = (16.0, 45.0, 30.0)
        gps[ExifTags.GPS.GPSLongitudeRef] = "W"
        gps[ExifTags.GPS.GPSLongitude] = (92.0, 38.0, 15.0)
        if orientacion is not None:
            exif[ExifTags.Base.Orientation] = orientacion
        argumentos = {
            "exif": exif,
            "xmp": MARCADOR_XMP + b"/1.0/ <x:xmpmeta/>",
            "comment": COMENTARIO,
            "icc_profile": b"ICC_PROFILE-falso",
        }
    salida = io.BytesIO()
    imagen.save(salida, "JPEG", **argumentos)
    return salida.getvalue()


def _abrir(datos: bytes) -> Image.Image:
    imagen = Image.open(io.BytesIO(datos))
    imagen.load()
    return imagen


def _sin_rastro(datos: bytes) -> None:
    assert b"Exif" not in datos
    assert MARCADOR_XMP not in datos
    assert COMENTARIO.encode() not in datos
    assert b"ICC_PROFILE" not in datos
    assert len(_abrir(datos).getexif()) == 0
    assert _abrir(datos).format == "JPEG"


def test_la_foto_con_gps_sale_reducida_y_sin_metadatos() -> None:
    foto = procesar_foto(_jpeg(4000, 3000))

    assert _abrir(foto.imagen).size == (ANCHO_MAXIMO, 1200)
    assert _abrir(foto.miniatura).size == (192, 144)
    _sin_rastro(foto.imagen)
    _sin_rastro(foto.miniatura)


def test_una_imagen_pequena_no_se_amplia() -> None:
    foto = procesar_foto(_jpeg(800, 600))

    assert _abrir(foto.imagen).size == (800, 600)
    assert _abrir(foto.miniatura).size == (192, 144)


def test_una_imagen_vertical_respeta_el_lado_mayor_de_la_miniatura() -> None:
    foto = procesar_foto(_jpeg(1200, 2400, con_metadatos=False))

    assert _abrir(foto.imagen).size == (1200, 2400)
    assert max(_abrir(foto.miniatura).size) == LADO_MINIATURA


def test_la_orientacion_exif_se_aplica_a_los_pixeles() -> None:
    # Orientación 6: el archivo guarda 600x800 y hay que girarlo 90° para verlo 800x600.
    foto = procesar_foto(_jpeg(600, 800, orientacion=6))

    assert _abrir(foto.imagen).size == (800, 600)
    _sin_rastro(foto.imagen)


def test_un_png_con_transparencia_se_aplana_sobre_blanco() -> None:
    origen = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    entrada = io.BytesIO()
    origen.save(entrada, "PNG")

    foto = procesar_foto(entrada.getvalue())

    pixel = _abrir(foto.imagen).convert("RGB").getpixel((50, 50))
    assert isinstance(pixel, tuple)
    assert all(canal >= 250 for canal in pixel)
    assert _abrir(foto.imagen).format == "JPEG"


def test_los_bloques_de_texto_de_un_png_no_sobreviven() -> None:
    origen = Image.new("RGB", (100, 100), (10, 20, 30))

    texto = PngInfo()
    texto.add_text("Ubicacion", COMENTARIO)
    entrada = io.BytesIO()
    origen.save(entrada, "PNG", pnginfo=texto)
    assert COMENTARIO.encode() in entrada.getvalue()

    foto = procesar_foto(entrada.getvalue())

    assert COMENTARIO.encode() not in foto.imagen
    assert COMENTARIO.encode() not in foto.miniatura


def test_un_webp_se_convierte_a_jpeg_reducido() -> None:
    entrada = io.BytesIO()
    Image.new("RGB", (3000, 2000), (5, 90, 40)).save(entrada, "WEBP")

    foto = procesar_foto(entrada.getvalue())

    assert _abrir(foto.imagen).size == (ANCHO_MAXIMO, 1067)
    _sin_rastro(foto.imagen)


def test_bytes_que_no_son_una_imagen_se_rechazan() -> None:
    with pytest.raises(FotoInvalida, match="no es una imagen válida"):
        procesar_foto(b"no soy una imagen")


def test_un_formato_no_admitido_se_rechaza() -> None:
    entrada = io.BytesIO()
    Image.new("RGB", (50, 50)).save(entrada, "GIF")

    with pytest.raises(FotoInvalida, match="JPEG, PNG o WebP"):
        procesar_foto(entrada.getvalue())


def test_un_jpeg_truncado_se_rechaza_sin_que_escape_la_excepcion_de_pillow() -> None:
    completo = _jpeg(1000, 800, con_metadatos=False)

    with pytest.raises(FotoInvalida, match="no es una imagen válida"):
        procesar_foto(completo[: len(completo) // 2])


def test_un_archivo_demasiado_grande_se_rechaza_antes_de_abrirlo() -> None:
    with pytest.raises(FotoInvalida, match="10 MB"):
        procesar_foto(b"\xff" * (TAMANO_MAXIMO + 1))


@pytest.mark.filterwarnings("ignore::PIL.Image.DecompressionBombWarning")
def test_una_imagen_con_demasiados_pixeles_se_rechaza_sin_decodificarla() -> None:
    entrada = io.BytesIO()
    Image.new("1", (9000, 9000)).save(entrada, "PNG")  # 81 MP: pesa poco y decodifica mucho
    assert len(entrada.getvalue()) < TAMANO_MAXIMO

    with pytest.raises(FotoInvalida, match="demasiado grande en píxeles"):
        procesar_foto(entrada.getvalue())


def test_una_bomba_de_descompresion_se_rechaza_igual() -> None:
    entrada = io.BytesIO()
    Image.new("1", (12000, 12000)).save(entrada, "PNG")  # 144 MP: Pillow ya la llama bomba

    with pytest.raises(FotoInvalida, match="demasiado grande en píxeles"):
        procesar_foto(entrada.getvalue())


def test_la_miniatura_mide_como_maximo_192_px_por_lado_segun_el_adr_007() -> None:
    assert LADO_MINIATURA == 192
    for ancho, alto in ((4000, 3000), (3000, 4000), (5000, 5000)):
        miniatura = _abrir(procesar_foto(_jpeg(ancho, alto, con_metadatos=False)).miniatura)

        assert max(miniatura.size) == 192
