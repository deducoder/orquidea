import gzip
import importlib.util
import os
from pathlib import Path
from types import ModuleType

import pytest

from orquidea.coleccion.modelo import CUIDADOS_MAXIMO
from orquidea.web.app import app

SCRIPT = Path(__file__).parent.parent / "scripts" / "medir-primera-carga.py"


def _cargar() -> ModuleType:
    spec = importlib.util.spec_from_file_location("medir_primera_carga", SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


medicion = _cargar()


def test_la_coleccion_de_ejemplo_cabe_en_el_presupuesto_de_200_kb() -> None:
    m = medicion.medir(n=25)

    assert m.cantidad == 25
    assert m.html > 0 and m.javascript > 0
    assert 25 * 1024 < m.miniaturas < 150 * 1024  # se cuentan, y son de fotos con detalle
    assert m.total <= medicion.PRESUPUESTO == 200 * 1024


def test_cada_miniatura_cuenta_la_miniatura_y_no_la_foto_a_tamano_completo() -> None:
    m = medicion.medir(n=10)

    assert m.miniaturas / m.cantidad < 20 * 1024


def test_medir_deja_la_aplicacion_como_estaba() -> None:
    antes = (app.state.ruta_base, app.state.directorio_fotos)

    medicion.medir(n=2)

    assert (app.state.ruta_base, app.state.directorio_fotos) == antes


def test_el_script_sale_con_1_si_pasa_del_presupuesto_y_con_0_si_no(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert medicion.main(["--n", "3", "--presupuesto", "1"]) == 1
    assert "PASA DEL PRESUPUESTO" in capsys.readouterr().out

    assert medicion.main(["--n", "3"]) == 0
    salida = capsys.readouterr().out
    assert "3 ejemplares" in salida and "OK" in salida and "HTML (gzip)" in salida


def test_el_script_mide_las_fotos_reales_que_se_le_dan(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    for nombre in ("a.jpg", "b.jpg"):
        (tmp_path / nombre).write_bytes(medicion.foto_con_detalle())

    codigo = medicion.main([str(tmp_path / "a.jpg"), str(tmp_path / "b.jpg")])

    assert codigo == 0
    assert "2 ejemplares" in capsys.readouterr().out


def test_la_ficha_con_50_riegos_y_50_floraciones_cabe_en_el_presupuesto() -> None:
    m = medicion.medir_ficha(riegos=50, floraciones=50)

    assert (m.riegos, m.floraciones) == (50, 50)
    assert m.html > 0 and m.javascript > 0
    assert m.total <= medicion.PRESUPUESTO == 200 * 1024


def test_la_ficha_con_el_tope_de_registros_cabe_en_el_presupuesto() -> None:
    m = medicion.medir_ficha(riegos=CUIDADOS_MAXIMO, floraciones=CUIDADOS_MAXIMO)

    assert (m.riegos, m.floraciones) == (CUIDADOS_MAXIMO, CUIDADOS_MAXIMO)
    assert m.total <= medicion.PRESUPUESTO


def test_la_medicion_de_la_ficha_cuenta_gzip_y_todos_los_registros() -> None:
    m = medicion.medir_ficha(riegos=30, floraciones=20)

    assert m.filas == 50  # una fila del historial por cada registro insertado
    assert m.html_sin_comprimir > m.html  # gzip comprime: el peso que se cuenta no es el crudo


def test_medir_la_ficha_deja_la_aplicacion_como_estaba() -> None:
    antes = (app.state.ruta_base, app.state.directorio_fotos)

    medicion.medir_ficha(riegos=2, floraciones=2)

    assert (app.state.ruta_base, app.state.directorio_fotos) == antes


def test_medir_la_ficha_restaura_la_aplicacion_aunque_falle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    antes = (app.state.ruta_base, app.state.directorio_fotos)

    def falla(*_: object, **__: object) -> None:
        raise RuntimeError("falla a la mitad")

    monkeypatch.setattr(medicion.gzip, "compress", falla)
    with pytest.raises(RuntimeError):
        medicion.medir_ficha(riegos=2, floraciones=2)

    assert (app.state.ruta_base, app.state.directorio_fotos) == antes


def test_el_script_mide_tambien_la_ficha_y_sale_con_1_si_esta_pasa_del_presupuesto(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert medicion.main(["--n", "3", "--presupuesto", "1"]) == 1
    salida = capsys.readouterr().out

    assert "Primera carga de la ficha con 50 riegos y 50 floraciones" in salida
    assert f"con {CUIDADOS_MAXIMO} riegos y {CUIDADOS_MAXIMO} floraciones (el tope)" in salida
    assert salida.count("PASA DEL PRESUPUESTO") == 3  # la lista y las dos fichas


def test_sin_argumentos_el_script_sale_con_0_y_mide_la_lista_y_las_dos_fichas(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert medicion.main(["--n", "3"]) == 0
    salida = capsys.readouterr().out

    assert salida.count("OK") == 3
    assert "PASA DEL PRESUPUESTO" not in salida


def test_una_ficha_que_pasa_del_presupuesto_basta_para_salir_con_1(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    lista_chica = medicion.Medicion(cantidad=1, html=1, javascript=1, miniaturas=1)
    ficha_grande = medicion.MedicionDeFicha(
        riegos=500,
        floraciones=500,
        filas=1000,
        html_sin_comprimir=2_000_000,
        html=300 * 1024,
        javascript=1,
    )
    monkeypatch.setattr(medicion, "medir", lambda *_, **__: lista_chica)
    monkeypatch.setattr(medicion, "medir_ficha", lambda *_, **__: ficha_grande)

    codigo = medicion.main(["--n", "1"])

    salida = capsys.readouterr().out
    assert codigo == 1
    assert salida.count("PASA DEL PRESUPUESTO") == 2  # las dos fichas; la lista está dentro
    assert "OK" in salida


def test_medir_identidad_suma_el_gzip_de_cada_archivo_del_directorio(tmp_path: Path) -> None:
    hoja = b"body { color: #222; }\n" * 200
    (tmp_path / "identidad.css").write_bytes(hoja)
    (tmp_path / "fuentes").mkdir()
    (tmp_path / "fuentes" / "texto.woff2").write_bytes(os.urandom(4096))

    m = medicion.medir_identidad(tmp_path)

    assert [nombre for nombre, _ in m.archivos] == ["fuentes/texto.woff2", "identidad.css"]
    assert dict(m.archivos)["identidad.css"] == len(gzip.compress(hoja))
    assert m.total == sum(octetos for _, octetos in m.archivos)


def test_la_identidad_cuenta_en_gzip_no_sin_comprimir(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "identidad.css").write_bytes(b" " * (60 * 1024))  # 60 KB que comprimen a casi nada

    assert medicion.main(["--identidad", str(tmp_path)]) == 0
    assert "OK" in capsys.readouterr().out


def test_la_identidad_sobre_el_tope_sale_con_1(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "fuente.woff2").write_bytes(os.urandom(60 * 1024))

    codigo = medicion.main(["--identidad", str(tmp_path)])

    salida = capsys.readouterr().out
    assert codigo == 1
    assert "1 archivo(s)" in salida and "PASA DEL TOPE" in salida


def test_el_tope_de_la_identidad_incluye_la_frontera(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "fuente.woff2").write_bytes(os.urandom(8 * 1024))
    total = medicion.medir_identidad(tmp_path).total

    assert medicion.TOPE_DE_IDENTIDAD == 50 * 1024
    monkeypatch.setattr(medicion, "TOPE_DE_IDENTIDAD", total)
    assert medicion.main(["--identidad", str(tmp_path)]) == 0
    monkeypatch.setattr(medicion, "TOPE_DE_IDENTIDAD", total - 1)
    assert medicion.main(["--identidad", str(tmp_path)]) == 1


@pytest.mark.parametrize("vacio", [True, False])
def test_sin_recursos_de_identidad_no_hay_verde(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], vacio: bool
) -> None:
    directorio = tmp_path / "identidad"
    if vacio:
        directorio.mkdir()

    codigo = medicion.main(["--identidad", str(directorio)])

    assert codigo == 2
    assert "nada que medir" in capsys.readouterr().out
