import io
from typing import Any

from fastapi.routing import APIRoute
from PIL import ExifTags, Image

from orquidea.catalogo.modelo import Especie


def especie(id: str = "epidendrum-radicans", nombre: str = "Epidendrum radicans") -> Especie:
    def cuidado(nombre_cuidado: str) -> dict[str, str]:
        return {
            "texto": f"texto de {nombre_cuidado}",
            "fuente": f"fuente de {nombre_cuidado}",
        }

    datos: dict[str, Any] = {
        "id": id,
        "nombre_cientifico": nombre,
        "nombres_comunes": ["orquídea de fuego"],
        "descripcion": "Epífita de flores anaranjadas.",
        "cuidados": {
            "luz": cuidado("luz"),
            "riego": cuidado("riego"),
            "temperatura": cuidado("temperatura"),
            "sustrato": cuidado("sustrato"),
        },
        "fuentes": ["Hágsater et al. 2015"],
    }
    return Especie.model_validate(datos)


def rutas_registradas(rutas: Any) -> list[tuple[str, str]]:
    """Pares (método, ruta) de una aplicación, entrando en los routers incluidos."""
    pares: list[tuple[str, str]] = []
    for ruta in rutas:
        if isinstance(ruta, APIRoute):
            pares.extend((metodo, ruta.path) for metodo in sorted(ruta.methods or set()))
        elif hasattr(ruta, "original_router"):
            pares.extend(rutas_registradas(ruta.original_router.routes))
    return pares


MARCADOR_XMP = b"http://ns.adobe.com/xap"


def imagen_jpeg(ancho: int = 4000, alto: int = 3000, *, con_gps: bool = True) -> bytes:
    """Un JPEG de un color; con GPS en el EXIF, XMP y comentario cuando `con_gps`."""
    argumentos: dict[str, Any] = {}
    if con_gps:
        exif = Image.Exif()
        gps = exif.get_ifd(ExifTags.IFD.GPSInfo)
        gps[ExifTags.GPS.GPSLatitudeRef] = "N"
        gps[ExifTags.GPS.GPSLatitude] = (16.0, 45.0, 30.0)
        gps[ExifTags.GPS.GPSLongitudeRef] = "W"
        gps[ExifTags.GPS.GPSLongitude] = (92.0, 38.0, 15.0)
        argumentos = {"exif": exif, "xmp": MARCADOR_XMP + b"/1.0/", "comment": "gps-secreto"}
    salida = io.BytesIO()
    Image.new("RGB", (ancho, alto), (200, 80, 120)).save(salida, "JPEG", **argumentos)
    return salida.getvalue()
