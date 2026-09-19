import io
import subprocess
import sys
import textwrap

import pytest
from PIL import Image

# Se mide en un proceso aparte que solo recibe los bytes de la foto: su pico de memoria es el
# de decodificarla y procesarla, sin lo que gastó crearla ni el resto de las pruebas.
PROGRAMA = textwrap.dedent(
    """
    import resource, sys
    from orquidea.datos.fotos import procesar_foto

    procesar_foto(sys.stdin.buffer.read())
    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024)
    """
)
# Pico de un proceso que procesa una foto de 48 MP (el intérprete y Pillow ya gastan unos 60 MB).
# Sin cuidado llegaba a ~1200 MB; lo medido es ~280, 273 y 429 y el pico varía unos ±50 MB.
TOPES_DEL_PICO_MB = {("JPEG", "RGB"): 380, ("PNG", "RGB"): 380, ("PNG", "RGBA"): 520}


def _pico_mb(formato: str, modo: str, ancho: int = 8000, alto: int = 6000) -> int:
    color = (90, 140, 60, 255)[: len(modo)]
    entrada = io.BytesIO()
    Image.new(modo, (ancho, alto), color).save(entrada, formato)
    resultado = subprocess.run(  # noqa: S603
        [sys.executable, "-c", PROGRAMA],
        input=entrada.getvalue(),
        capture_output=True,
        check=True,
    )
    return int(resultado.stdout.decode().strip().splitlines()[-1])


@pytest.mark.parametrize(("formato", "modo"), list(TOPES_DEL_PICO_MB))
def test_procesar_una_foto_de_48_megapixeles_no_dispara_la_memoria(formato: str, modo: str) -> None:
    pico = _pico_mb(formato, modo)

    assert pico < TOPES_DEL_PICO_MB[(formato, modo)], f"{formato} {modo} de 48 MP llegó a {pico} MB"
