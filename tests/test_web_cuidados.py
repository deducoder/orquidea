import re
import sqlite3
from datetime import UTC, date, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from httpx2 import Response

from orquidea.coleccion.modelo import CUIDADOS_MAXIMO
from orquidea.datos.almacen_fotos import poner_foto
from orquidea.datos.base import conectar
from orquidea.datos.ejemplares import agregar_sin_especie
from orquidea.datos.fotos import procesar_foto
from orquidea.datos.riegos import agregar as agregar_riego
from orquidea.datos.sesiones import Sesion
from orquidea.web.app import app
from tests.fabricas import imagen_jpeg

AHORA = 1_780_000_000


def _conexion() -> sqlite3.Connection:
    return conectar(app.state.ruta_base)


def _ejemplar(nombre: str = "Mi rara") -> int:
    conexion = _conexion()
    try:
        return agregar_sin_especie(conexion, nombre, "", AHORA).id
    finally:
        conexion.close()


def _con_riegos(id: int, *fechas: str) -> None:
    conexion = _conexion()
    try:
        for fecha in fechas:
            assert agregar_riego(conexion, id, fecha) is not None
    finally:
        conexion.close()


def _riegos_guardados(id: int) -> list[str]:
    conexion = _conexion()
    try:
        filas = conexion.execute(
            "SELECT fecha FROM riegos WHERE ejemplar_id = ? ORDER BY fecha, id", (id,)
        ).fetchall()
        return [fila[0] for fila in filas]
    finally:
        conexion.close()


def _posicion(patron: str, texto: str) -> int:
    coincidencia = re.search(patron, texto)
    assert coincidencia is not None, patron
    return coincidencia.start()


def _hoy() -> date:
    return datetime.now(UTC).date()


def _registrar(client: TestClient, csrf: str, id: int, fecha: str) -> Response:
    return client.post(
        f"/coleccion/{id}/riegos", data={"csrf": csrf, "fecha": fecha}, follow_redirects=False
    )


def test_la_ficha_sin_riegos_lo_dice_y_ofrece_registrar_uno(client: TestClient) -> None:
    id = _ejemplar()

    respuesta = client.get(f"/coleccion/{id}")

    assert respuesta.status_code == 200
    assert "Aún no hay riegos." in respuesta.text
    assert "Último riego" not in respuesta.text
    assert f'action="/coleccion/{id}/riegos"' in respuesta.text
    assert 'name="fecha"' in respuesta.text
    assert 'type="date"' in respuesta.text
    assert f'max="{_hoy().isoformat()}"' in respuesta.text


def test_registrar_un_riego_lo_guarda_y_la_ficha_muestra_el_ultimo(
    client: TestClient, sesion: Sesion
) -> None:
    id = _ejemplar()

    respuesta = _registrar(client, sesion.csrf, id, "2026-09-15")

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == f"/coleccion/{id}"
    assert _riegos_guardados(id) == ["2026-09-15"]
    assert "Último riego: <strong>2026-09-15</strong>" in client.get(f"/coleccion/{id}").text


def test_la_ficha_lista_los_riegos_del_mas_reciente_al_mas_antiguo(client: TestClient) -> None:
    id = _ejemplar()
    _con_riegos(id, "2026-09-10", "2026-09-15", "2026-09-01")

    texto = client.get(f"/coleccion/{id}").text

    posiciones = [
        _posicion(rf"<li>\s*{fecha}", texto) for fecha in ("2026-09-15", "2026-09-10", "2026-09-01")
    ]
    assert posiciones == sorted(posiciones)
    assert "Último riego: <strong>2026-09-15</strong>" in texto


def test_el_riego_de_hoy_se_acepta(client: TestClient, sesion: Sesion) -> None:
    id = _ejemplar()

    assert _registrar(client, sesion.csrf, id, _hoy().isoformat()).status_code == 303


@pytest.mark.parametrize(
    ("fecha", "mensaje"),
    [
        ("19/09/2026", "formato AAAA-MM-DD"),
        ("2026-02-30", "no existe"),
        ("", "obligatoria"),
        ((_hoy() + timedelta(days=2)).isoformat(), "posterior a hoy"),
    ],
)
def test_una_fecha_rechazada_vuelve_a_la_ficha_sin_guardar_nada(
    client: TestClient, sesion: Sesion, fecha: str, mensaje: str
) -> None:
    id = _ejemplar()

    respuesta = _registrar(client, sesion.csrf, id, fecha)

    assert respuesta.status_code == 422
    assert mensaje in respuesta.text
    assert 'role="alert"' in respuesta.text
    assert _riegos_guardados(id) == []


def test_la_fecha_rechazada_se_devuelve_escapada(client: TestClient, sesion: Sesion) -> None:
    id = _ejemplar()

    respuesta = _registrar(client, sesion.csrf, id, '"><script>alert(1)</script>')

    assert respuesta.status_code == 422
    assert "<script>alert(1)" not in respuesta.text
    assert "&lt;script&gt;alert(1)" in respuesta.text


def test_el_tope_de_riegos_se_rechaza_con_un_mensaje(client: TestClient, sesion: Sesion) -> None:
    id = _ejemplar()
    conexion = _conexion()
    try:
        conexion.executemany(
            "INSERT INTO riegos (ejemplar_id, fecha) VALUES (?, '2026-01-01')",
            [(id,)] * CUIDADOS_MAXIMO,
        )
    finally:
        conexion.close()

    respuesta = _registrar(client, sesion.csrf, id, "2026-09-15")

    assert respuesta.status_code == 422
    assert "500 riegos" in respuesta.text
    assert len(_riegos_guardados(id)) == CUIDADOS_MAXIMO


def test_registrar_en_un_ejemplar_inexistente_da_404(client: TestClient, sesion: Sesion) -> None:
    assert _registrar(client, sesion.csrf, 999, "2026-09-15").status_code == 404


def test_registrar_un_riego_deja_intacta_la_foto(client: TestClient, sesion: Sesion) -> None:
    id = _ejemplar()
    conexion = _conexion()
    try:
        assert poner_foto(
            conexion, app.state.directorio_fotos, id, procesar_foto(imagen_jpeg(800, 600))
        )
    finally:
        conexion.close()

    _registrar(client, sesion.csrf, id, "2026-09-15")

    texto = client.get(f"/coleccion/{id}").text
    assert f'src="/coleccion/{id}/foto"' in texto
    assert f'action="/coleccion/{id}/foto/quitar"' in texto
    assert re.search(r"Último riego: <strong>2026-09-15</strong>", texto)


def _id_del_riego(id: int, fecha: str) -> int:
    conexion = _conexion()
    try:
        fila = conexion.execute(
            "SELECT id FROM riegos WHERE ejemplar_id = ? AND fecha = ?", (id, fecha)
        ).fetchone()
        return int(fila[0])
    finally:
        conexion.close()


def _quitar(client: TestClient, csrf: str, id: int, riego: int) -> Response:
    return client.post(
        f"/coleccion/{id}/riegos/{riego}/quitar", data={"csrf": csrf}, follow_redirects=False
    )


def test_quitar_un_riego_lo_borra_y_recalcula_el_ultimo(client: TestClient, sesion: Sesion) -> None:
    id = _ejemplar()
    _con_riegos(id, "2026-09-01", "2026-09-15")

    respuesta = _quitar(client, sesion.csrf, id, _id_del_riego(id, "2026-09-15"))

    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == f"/coleccion/{id}"
    assert _riegos_guardados(id) == ["2026-09-01"]
    assert "Último riego: <strong>2026-09-01</strong>" in client.get(f"/coleccion/{id}").text


def test_la_ficha_ofrece_quitar_cada_riego(client: TestClient) -> None:
    id = _ejemplar()
    _con_riegos(id, "2026-09-01")

    texto = client.get(f"/coleccion/{id}").text

    assert f'action="/coleccion/{id}/riegos/{_id_del_riego(id, "2026-09-01")}/quitar"' in texto


def test_quitar_el_riego_de_otro_ejemplar_da_404_y_no_lo_borra(
    client: TestClient, sesion: Sesion
) -> None:
    uno, otro = _ejemplar("Uno"), _ejemplar("Otro")
    _con_riegos(otro, "2026-09-01")

    respuesta = _quitar(client, sesion.csrf, uno, _id_del_riego(otro, "2026-09-01"))

    assert respuesta.status_code == 404
    assert _riegos_guardados(otro) == ["2026-09-01"]


def test_quitar_un_riego_inexistente_da_404(client: TestClient, sesion: Sesion) -> None:
    assert _quitar(client, sesion.csrf, _ejemplar(), 999).status_code == 404


def test_quitar_en_un_ejemplar_inexistente_da_404(client: TestClient, sesion: Sesion) -> None:
    assert _quitar(client, sesion.csrf, 999, 1).status_code == 404


def test_quitar_un_riego_no_cambia_los_de_otro_ejemplar(client: TestClient, sesion: Sesion) -> None:
    uno, otro = _ejemplar("Uno"), _ejemplar("Otro")
    _con_riegos(uno, "2026-09-01")
    _con_riegos(otro, "2026-09-01", "2026-09-02")

    _quitar(client, sesion.csrf, uno, _id_del_riego(uno, "2026-09-01"))

    assert _riegos_guardados(uno) == []
    assert _riegos_guardados(otro) == ["2026-09-01", "2026-09-02"]


def test_sin_sesion_no_se_registra_ni_se_quita_ningun_riego(anonimo: TestClient) -> None:
    id = _ejemplar()
    _con_riegos(id, "2026-09-01")
    riego = _id_del_riego(id, "2026-09-01")

    registrar = anonimo.post(
        f"/coleccion/{id}/riegos", data={"fecha": "2026-09-15"}, follow_redirects=False
    )
    quitar = anonimo.post(f"/coleccion/{id}/riegos/{riego}/quitar", follow_redirects=False)

    assert (registrar.status_code, registrar.headers["location"]) == (303, "/acceso")
    assert (quitar.status_code, quitar.headers["location"]) == (303, "/acceso")
    assert _riegos_guardados(id) == ["2026-09-01"]


def test_sin_token_csrf_no_se_registra_ni_se_quita_ningun_riego(client: TestClient) -> None:
    id = _ejemplar()
    _con_riegos(id, "2026-09-01")
    riego = _id_del_riego(id, "2026-09-01")

    registrar = client.post(
        f"/coleccion/{id}/riegos", data={"fecha": "2026-09-15"}, follow_redirects=False
    )
    quitar = client.post(f"/coleccion/{id}/riegos/{riego}/quitar", follow_redirects=False)
    equivocado = client.post(
        f"/coleccion/{id}/riegos",
        data={"fecha": "2026-09-15", "csrf": "otro"},
        follow_redirects=False,
    )

    assert (registrar.status_code, quitar.status_code, equivocado.status_code) == (403, 403, 403)
    assert _riegos_guardados(id) == ["2026-09-01"]
