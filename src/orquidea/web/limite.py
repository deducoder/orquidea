from starlette.types import ASGIApp, Message, Receive, Scope, Send


class LimiteDeCuerpo:
    """Corta con 413 una petición cuyo cuerpo pasa de `maximo` bytes, antes de procesarla.

    Va antes del multipart: el formulario se lee entero al resolver las dependencias, y una
    foto no puede llenar el disco ni la memoria antes de que nadie la mire. Se cuentan los
    bytes recibidos y no se confía en `Content-Length`, que puede faltar (chunked) o mentir.
    Al pasarse, la aplicación ve una desconexión (FastAPI convierte cualquier excepción al
    leer el cuerpo en un 422) y su respuesta se sustituye por el 413.
    """

    def __init__(self, app: ASGIApp, maximo: int) -> None:
        self.app = app
        self.maximo = maximo

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        declarado = dict(scope["headers"]).get(b"content-length", b"")
        if declarado.isdigit() and int(declarado) > self.maximo:
            await self._rechazar(send)
            return

        recibidos = 0
        excedido = False
        respondido = False
        empezo = False

        async def contando() -> Message:
            nonlocal recibidos, excedido
            if excedido:
                return {"type": "http.disconnect"}
            mensaje = await receive()
            if mensaje["type"] == "http.request":
                recibidos += len(mensaje.get("body", b""))
                if recibidos > self.maximo:
                    excedido = True
                    return {"type": "http.disconnect"}
            return mensaje

        async def vigilando(mensaje: Message) -> None:
            nonlocal respondido, empezo
            if excedido and not empezo:
                if not respondido:
                    respondido = True
                    await self._rechazar(send)
                return
            if mensaje["type"] == "http.response.start":
                empezo = True
            await send(mensaje)

        try:
            await self.app(scope, contando, vigilando)
        except Exception:
            if not excedido or empezo:
                raise
        if excedido and not empezo and not respondido:
            await self._rechazar(send)

    @staticmethod
    async def _rechazar(send: Send) -> None:
        cuerpo = "La petición es demasiado grande.".encode()
        cabeceras = [
            (b"content-type", b"text/plain; charset=utf-8"),
            (b"content-length", str(len(cuerpo)).encode()),
            (b"connection", b"close"),
        ]
        await send({"type": "http.response.start", "status": 413, "headers": cabeceras})
        await send({"type": "http.response.body", "body": cuerpo})
