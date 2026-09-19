"""Lo que la imagen y la guía de despliegue deben decir sobre lo que el código espera."""

import re
from pathlib import Path

RAIZ = Path(__file__).parent.parent
DOCKERFILE = RAIZ / "Dockerfile"


def lineas(dockerfile: Path = DOCKERFILE) -> list[str]:
    """Instrucciones del Dockerfile, con las continuaciones `\\` unidas en una sola."""
    texto = dockerfile.read_text(encoding="utf-8").replace("\\\n", " ")
    return [linea.strip() for linea in texto.splitlines() if linea.strip()]


def indice(lineas_: list[str], patron: str) -> int:
    for numero, linea in enumerate(lineas_):
        if re.match(patron, linea):
            return numero
    raise AssertionError(f"el Dockerfile no tiene una línea que empiece por {patron!r}")


def valor(lineas_: list[str], patron: str) -> str:
    return re.sub(patron, "", lineas_[indice(lineas_, patron)], count=1).strip()


def test_la_base_vive_dentro_de_un_volumen() -> None:
    instrucciones = lineas()
    ruta = Path(valor(instrucciones, r"ENV\s+ORQUIDEA_DB="))
    volumenes = [Path(valor(instrucciones, r"VOLUME\s+"))]

    assert ruta.is_absolute()
    assert any(volumen in ruta.parents for volumen in volumenes)


def test_el_directorio_de_datos_se_crea_y_se_entrega_al_usuario_antes_de_cambiar_de_usuario() -> (
    None
):
    instrucciones = lineas()
    datos = valor(instrucciones, r"VOLUME\s+")
    usuario = indice(instrucciones, r"USER\s+")
    creado = next((n for n, linea in enumerate(instrucciones) if f"mkdir {datos}" in linea), None)
    entregado = next(
        (n for n, linea in enumerate(instrucciones) if f"chown app {datos}" in linea), None
    )

    assert creado is not None and creado < usuario
    assert entregado is not None and entregado < usuario


def test_la_imagen_no_corre_como_root() -> None:
    assert valor(lineas(), r"USER\s+") not in {"root", "0"}


def test_el_healthcheck_sigue_apuntando_a_la_ruta_publica_de_salud() -> None:
    assert "/salud" in valor(lineas(), r"HEALTHCHECK\s+")


def test_el_dockerfile_no_lleva_secretos() -> None:
    assert "scrypt$" not in DOCKERFILE.read_text(encoding="utf-8")
    assert not re.search(r"ORQUIDEA_PASSWORD_HASH\s*=", DOCKERFILE.read_text(encoding="utf-8"))


README = RAIZ / "README.md"


def variables_que_lee_el_codigo(raiz: Path = RAIZ / "src") -> set[str]:
    encontradas: set[str] = set()
    for archivo in raiz.rglob("*.py"):
        encontradas |= set(re.findall(r"ORQUIDEA_[A-Z_]+", archivo.read_text(encoding="utf-8")))
    return encontradas


def test_el_codigo_lee_las_variables_esperadas() -> None:
    assert variables_que_lee_el_codigo() >= {
        "ORQUIDEA_DB",
        "ORQUIDEA_PASSWORD_HASH",
        "ORQUIDEA_COOKIE_SEGURA",
    }


def test_el_readme_documenta_cada_variable_que_lee_el_codigo() -> None:
    texto = README.read_text(encoding="utf-8")

    faltantes = {v for v in variables_que_lee_el_codigo() if v not in texto}

    assert faltantes == set()


def test_una_variable_nueva_sin_documentar_se_detecta(tmp_path: Path) -> None:
    (tmp_path / "nuevo.py").write_text('os.environ["ORQUIDEA_NUEVA_SIN_DOCUMENTAR"]')

    assert "ORQUIDEA_NUEVA_SIN_DOCUMENTAR" in variables_que_lee_el_codigo(tmp_path)
    assert "ORQUIDEA_NUEVA_SIN_DOCUMENTAR" not in README.read_text(encoding="utf-8")


def test_el_readme_ya_no_dice_que_no_hay_variables_de_entorno() -> None:
    assert "No hay variables de entorno" not in README.read_text(encoding="utf-8")


def test_el_readme_explica_el_hash_el_volumen_y_la_cookie() -> None:
    texto = README.read_text(encoding="utf-8")

    assert "python -m orquidea.autenticacion" in texto
    assert "/data" in texto
    assert "Secure" in texto
    assert "HTTPS" in texto


def test_el_readme_no_contiene_un_hash_real() -> None:
    assert not re.search(r"scrypt\$\d+\$\d+\$\d+\$[A-Za-z0-9+/=]{16,}", README.read_text("utf-8"))
