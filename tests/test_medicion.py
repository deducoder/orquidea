import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

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
