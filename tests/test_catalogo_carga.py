import json
from pathlib import Path
from typing import Any

import pytest

from orquidea.datos.catalogo import CatalogoInvalido, cargar_catalogo


def cuidado(texto: str) -> dict[str, str]:
    return {"texto": texto, "fuente": "Hágsater et al. 2015"}


def especie(id: str = "epidendrum-radicans") -> dict[str, Any]:
    return {
        "id": id,
        "nombre_cientifico": "Epidendrum radicans",
        "descripcion": "Epífita o terrestre de flores anaranjadas.",
        "cuidados": {
            "luz": cuidado("Luz brillante"),
            "riego": cuidado("Regular"),
            "temperatura": cuidado("15 a 28 °C"),
            "sustrato": cuidado("Corteza gruesa"),
        },
        "fuentes": ["Hágsater et al. 2015"],
    }


def escribir(directorio: Path, nombre: str, datos: dict[str, Any]) -> None:
    (directorio / nombre).write_text(json.dumps(datos), encoding="utf-8")


def test_catalogo_valido_se_carga_ordenado_por_id(tmp_path: Path) -> None:
    escribir(tmp_path, "b.json", especie("laelia-anceps"))
    escribir(tmp_path, "a.json", especie("epidendrum-radicans"))

    especies = cargar_catalogo(tmp_path)

    assert [e.id for e in especies] == ["epidendrum-radicans", "laelia-anceps"]


def test_directorio_sin_json_da_lista_vacia(tmp_path: Path) -> None:
    assert cargar_catalogo(tmp_path) == []


def test_sin_fuentes_nombra_archivo_y_campo(tmp_path: Path) -> None:
    datos = especie()
    del datos["fuentes"]
    escribir(tmp_path, "sin-fuentes.json", datos)

    with pytest.raises(CatalogoInvalido) as error:
        cargar_catalogo(tmp_path)

    assert error.value.errores == ["sin-fuentes.json: fuentes: Field required"]


def test_campo_anidado_nombra_la_ruta_completa(tmp_path: Path) -> None:
    datos = especie()
    del datos["cuidados"]["riego"]["fuente"]
    escribir(tmp_path, "x.json", datos)

    with pytest.raises(CatalogoInvalido) as error:
        cargar_catalogo(tmp_path)

    assert error.value.errores == ["x.json: cuidados.riego.fuente: Field required"]


def test_elemento_de_lista_nombra_su_posicion(tmp_path: Path) -> None:
    datos = especie()
    datos["fuentes"] = ["ok", ""]
    escribir(tmp_path, "x.json", datos)

    with pytest.raises(CatalogoInvalido) as error:
        cargar_catalogo(tmp_path)

    assert error.value.errores[0].startswith("x.json: fuentes.1: ")


def test_json_roto_nombra_el_archivo(tmp_path: Path) -> None:
    (tmp_path / "roto.json").write_text("{\n  no es json", encoding="utf-8")

    with pytest.raises(CatalogoInvalido) as error:
        cargar_catalogo(tmp_path)

    assert error.value.errores[0].startswith("roto.json: JSON inválido")


def test_todo_o_nada_con_un_archivo_invalido(tmp_path: Path) -> None:
    escribir(tmp_path, "bueno.json", especie("laelia-anceps"))
    malo = especie()
    del malo["fuentes"]
    escribir(tmp_path, "malo.json", malo)

    with pytest.raises(CatalogoInvalido):
        cargar_catalogo(tmp_path)


def test_reune_los_errores_de_todos_los_archivos(tmp_path: Path) -> None:
    for nombre in ("a.json", "b.json"):
        malo = especie()
        del malo["fuentes"]
        escribir(tmp_path, nombre, malo)

    with pytest.raises(CatalogoInvalido) as error:
        cargar_catalogo(tmp_path)

    assert error.value.errores == [
        "a.json: fuentes: Field required",
        "b.json: fuentes: Field required",
    ]
    assert "a.json" in str(error.value)
    assert "b.json" in str(error.value)


def test_raiz_que_no_es_objeto_nombra_archivo_y_raiz(tmp_path: Path) -> None:
    (tmp_path / "lista.json").write_text("[]", encoding="utf-8")

    with pytest.raises(CatalogoInvalido) as error:
        cargar_catalogo(tmp_path)

    assert error.value.errores[0].startswith("lista.json: (raíz): ")


def test_ids_duplicadas_nombran_ambos_archivos(tmp_path: Path) -> None:
    escribir(tmp_path, "a.json", especie("laelia-anceps"))
    escribir(tmp_path, "b.json", especie("laelia-anceps"))

    with pytest.raises(CatalogoInvalido) as error:
        cargar_catalogo(tmp_path)

    assert error.value.errores == ['b.json: id: duplicada de a.json ("laelia-anceps")']


def test_directorio_inexistente_es_catalogo_invalido(tmp_path: Path) -> None:
    faltante = tmp_path / "no-existe"

    with pytest.raises(CatalogoInvalido) as error:
        cargar_catalogo(faltante)

    assert str(faltante) in error.value.errores[0]
