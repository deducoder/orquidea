import asyncio
from collections.abc import Iterator

from fastapi.testclient import TestClient
from starlette.types import Message, Receive, Scope, Send

from orquidea.web.app import LIMITE_DE_CUERPO
from orquidea.web.limite import LimiteDeCuerpo

MAXIMO = 100


async def _aplicacion(scope: Scope, receive: Receive, send: Send) -> None:
    total = 0
    while True:
        mensaje = await receive()
        total += len(mensaje.get("body", b""))
        if not mensaje.get("more_body", False):
            break
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": str(total).encode()})


def _llamar(cabeceras: list[tuple[bytes, bytes]], trozos: list[bytes]) -> tuple[int, bytes, int]:
    """Devuelve (estado, cuerpo, cuántos mensajes de cuerpo leyó la aplicación)."""
    pendientes = list(trozos)
    leidos = 0
    enviados: list[Message] = []

    async def receive() -> Message:
        nonlocal leidos
        leidos += 1
        cuerpo = pendientes.pop(0) if pendientes else b""
        return {"type": "http.request", "body": cuerpo, "more_body": bool(pendientes)}

    async def send(mensaje: Message) -> None:
        enviados.append(mensaje)

    scope: Scope = {"type": "http", "method": "POST", "path": "/", "headers": cabeceras}
    asyncio.run(LimiteDeCuerpo(_aplicacion, maximo=MAXIMO)(scope, receive, send))
    return enviados[0]["status"], enviados[1]["body"], leidos


def test_un_cuerpo_dentro_del_limite_pasa_intacto() -> None:
    estado, cuerpo, _ = _llamar([(b"content-length", b"100")], [b"a" * 60, b"b" * 40])

    assert (estado, cuerpo) == (200, b"100")


def test_un_content_length_excedido_responde_413_sin_leer_el_cuerpo() -> None:
    estado, _, leidos = _llamar([(b"content-length", b"101")], [b"x" * 101])

    assert estado == 413
    assert leidos == 0


def test_un_cuerpo_sin_content_length_que_se_pasa_responde_413() -> None:
    estado, _, _ = _llamar([], [b"a" * 60, b"b" * 60])

    assert estado == 413


def test_un_content_length_que_miente_no_evita_el_conteo() -> None:
    estado, _, _ = _llamar([(b"content-length", b"10")], [b"a" * 60, b"b" * 60])

    assert estado == 413


def test_un_content_length_ilegible_no_rompe_y_se_cuenta_igual() -> None:
    assert _llamar([(b"content-length", b"abc")], [b"a" * 10])[0] == 200
    assert _llamar([(b"content-length", b"abc")], [b"a" * 200])[0] == 413


def test_un_mensaje_que_no_es_http_pasa_sin_tocarse() -> None:
    visto: list[str] = []

    async def aplicacion(scope: Scope, receive: Receive, send: Send) -> None:
        visto.append(scope["type"])

    async def recibir() -> Message:
        return {"type": "lifespan.startup"}

    async def enviar(_: Message) -> None:
        return None

    scope: Scope = {"type": "lifespan"}
    asyncio.run(LimiteDeCuerpo(aplicacion, maximo=1)(scope, recibir, enviar))

    assert visto == ["lifespan"]


def test_la_aplicacion_rechaza_con_413_un_cuerpo_gigante_con_content_length(
    anonimo: TestClient,
) -> None:
    respuesta = anonimo.post("/acceso", content=b"x" * (LIMITE_DE_CUERPO + 1))

    assert respuesta.status_code == 413


def test_la_aplicacion_rechaza_con_413_un_cuerpo_chunked_gigante(anonimo: TestClient) -> None:
    def trozos() -> Iterator[bytes]:
        for _ in range(LIMITE_DE_CUERPO // 1024 + 2):
            yield b"x" * 1024

    respuesta = anonimo.post(
        "/acceso",
        content=trozos(),
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert respuesta.status_code == 413


def test_un_formulario_normal_no_se_ve_afectado(anonimo: TestClient) -> None:
    assert anonimo.get("/acceso").status_code == 200
