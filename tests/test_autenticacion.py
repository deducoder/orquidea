import getpass
import hmac
from collections.abc import Iterator

import pytest

from orquidea import autenticacion
from orquidea.autenticacion import LimiteDeIntentos, hashear_contrasena, verificar_contrasena

N_BAJO = 2**4  # costo mínimo para que las pruebas sean rápidas


def test_el_hash_verifica_su_contraseña_y_rechaza_otra() -> None:
    hash_ = hashear_contrasena("orquidea-2026", n=N_BAJO)

    assert verificar_contrasena("orquidea-2026", hash_)
    assert not verificar_contrasena("otra", hash_)
    assert not verificar_contrasena("", hash_)


def test_dos_hashes_de_la_misma_contraseña_difieren_y_ambos_verifican() -> None:
    uno = hashear_contrasena("orquidea-2026", n=N_BAJO)
    otro = hashear_contrasena("orquidea-2026", n=N_BAJO)

    assert uno != otro
    assert verificar_contrasena("orquidea-2026", uno)
    assert verificar_contrasena("orquidea-2026", otro)


def test_el_hash_no_contiene_la_contraseña() -> None:
    assert "orquidea-2026" not in hashear_contrasena("orquidea-2026", n=N_BAJO)


def test_los_parametros_del_hash_viajan_en_la_cadena() -> None:
    hash_ = hashear_contrasena("x", n=2**5)

    assert hash_.startswith("scrypt$32$8$2$")
    assert verificar_contrasena("x", hash_)


def test_los_parametros_por_defecto_son_los_de_owasp() -> None:
    assert hashear_contrasena("x").startswith("scrypt$65536$8$2$")


@pytest.mark.parametrize(
    "malformado",
    [
        None,
        "",
        "basura",
        "scrypt$16$8$2$sal",
        "scrypt$no$8$2$c2Fs$aGFzaA==",
        "scrypt$16$8$2$***$***",
        "bcrypt$16$8$2$c2Fs$aGFzaA==",
        "scrypt$15$8$2$c2Fs$aGFzaA==",
    ],
)
def test_un_hash_ausente_o_malformado_cierra_sin_excepcion(malformado: str | None) -> None:
    assert not verificar_contrasena("orquidea-2026", malformado)


def test_un_hash_con_otro_esquema_no_verifica_aunque_los_datos_sean_validos() -> None:
    hash_ = hashear_contrasena("orquidea-2026", n=N_BAJO)

    assert not verificar_contrasena("orquidea-2026", hash_.replace("scrypt", "otro", 1))


def test_un_hash_con_el_hash_truncado_no_verifica() -> None:
    hash_ = hashear_contrasena("orquidea-2026", n=N_BAJO)
    truncado = hash_.rsplit("$", 1)[0] + "$" + "AAAA"

    assert not verificar_contrasena("orquidea-2026", truncado)


def test_la_comparacion_usa_tiempo_constante(monkeypatch: pytest.MonkeyPatch) -> None:
    llamadas: list[int] = []
    original = hmac.compare_digest

    def espia(a: bytes, b: bytes) -> bool:
        llamadas.append(1)
        return original(a, b)

    monkeypatch.setattr(hmac, "compare_digest", espia)

    verificar_contrasena("x", hashear_contrasena("x", n=N_BAJO))

    assert llamadas


@pytest.fixture
def entradas(monkeypatch: pytest.MonkeyPatch) -> Iterator[list[str]]:
    respuestas: list[str] = []
    monkeypatch.setattr(getpass, "getpass", lambda _msg="": respuestas.pop(0))
    yield respuestas


def test_la_orden_imprime_un_hash_que_verifica(
    entradas: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    entradas.extend(["orquidea-2026", "orquidea-2026"])

    autenticacion.main()

    salida = capsys.readouterr().out.strip()
    assert salida.startswith("scrypt$")
    assert verificar_contrasena("orquidea-2026", salida)
    assert "orquidea-2026" not in salida


def test_la_orden_rechaza_una_confirmacion_distinta(entradas: list[str]) -> None:
    entradas.extend(["una", "otra"])

    with pytest.raises(SystemExit):
        autenticacion.main()


def test_la_orden_rechaza_una_contraseña_vacia(entradas: list[str]) -> None:
    entradas.extend(["", ""])

    with pytest.raises(SystemExit):
        autenticacion.main()


def test_cuatro_fallos_no_bloquean_y_el_quinto_si() -> None:
    limite = LimiteDeIntentos()
    for _ in range(4):
        limite.fallo(ahora=100.0)

    assert not limite.bloqueado(ahora=100.0)

    limite.fallo(ahora=100.0)

    assert limite.bloqueado(ahora=100.0)


def test_el_bloqueo_expira_a_los_cinco_minutos() -> None:
    limite = LimiteDeIntentos()
    for _ in range(5):
        limite.fallo(ahora=100.0)

    assert limite.bloqueado(ahora=100.0 + 299.9)
    assert not limite.bloqueado(ahora=100.0 + 300.0)


def test_un_acierto_reinicia_el_contador() -> None:
    limite = LimiteDeIntentos()
    for _ in range(4):
        limite.fallo(ahora=100.0)
    limite.acierto()
    for _ in range(4):
        limite.fallo(ahora=100.0)

    assert not limite.bloqueado(ahora=100.0)


def test_tras_expirar_el_bloqueo_el_contador_empieza_de_cero() -> None:
    limite = LimiteDeIntentos()
    for _ in range(5):
        limite.fallo(ahora=100.0)
    despues = 100.0 + 300.0
    limite.fallo(ahora=despues)

    assert not limite.bloqueado(ahora=despues)
