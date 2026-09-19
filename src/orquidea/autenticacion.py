import base64
import getpass
import hashlib
import hmac
import secrets

_LONGITUD_SAL = 16
_LONGITUD_HASH = 32


def _derivar(contrasena: str, sal: bytes, n: int, r: int, p: int) -> bytes:
    return hashlib.scrypt(
        contrasena.encode("utf-8"),
        salt=sal,
        n=n,
        r=r,
        p=p,
        maxmem=256 * r * (n + p + 2),
        dklen=_LONGITUD_HASH,
    )


def hashear_contrasena(contrasena: str, n: int = 2**16, r: int = 8, p: int = 2) -> str:
    sal = secrets.token_bytes(_LONGITUD_SAL)
    derivado = _derivar(contrasena, sal, n, r, p)
    return "$".join(
        [
            "scrypt",
            str(n),
            str(r),
            str(p),
            base64.b64encode(sal).decode("ascii"),
            base64.b64encode(derivado).decode("ascii"),
        ]
    )


def verificar_contrasena(contrasena: str, hash_: str | None) -> bool:
    if not hash_:
        return False
    try:
        esquema, n, r, p, sal, esperado = hash_.split("$")
        if esquema != "scrypt":
            return False
        derivado = _derivar(
            contrasena,
            base64.b64decode(sal),
            int(n),
            int(r),
            int(p),
        )
        return hmac.compare_digest(derivado, base64.b64decode(esperado))
    except ValueError:
        return False


class LimiteDeIntentos:
    """Bloquea temporalmente tras varios fallos seguidos; global porque hay un solo usuario."""

    MAXIMO = 5
    BLOQUEO = 300.0

    def __init__(self) -> None:
        self._fallos = 0
        self._hasta = 0.0

    def bloqueado(self, ahora: float) -> bool:
        return ahora < self._hasta

    def fallo(self, ahora: float) -> None:
        self._fallos += 1
        if self._fallos >= self.MAXIMO:
            self._fallos = 0
            self._hasta = ahora + self.BLOQUEO

    def acierto(self) -> None:
        self._fallos = 0


def main() -> None:
    contrasena = getpass.getpass("Contraseña: ")
    if not contrasena:
        raise SystemExit("La contraseña no puede estar vacía")
    if getpass.getpass("Repite la contraseña: ") != contrasena:
        raise SystemExit("Las contraseñas no coinciden")
    print(hashear_contrasena(contrasena))


if __name__ == "__main__":
    main()
