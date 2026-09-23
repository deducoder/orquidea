"""La hoja de estilos usa solo tokens de la identidad (ADR-015).

Cada propiedad de `:root` tiene el nombre de un token de `DESIGN.md` (o `--familia`, la pila de
`specimen.md`) y su mismo valor; fuera de `:root` solo hay `var(--…)` declaradas, palabras clave y
los literales de la lista cerrada de ADR-015.
"""

import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).parent.parent
HOJA = RAIZ / "src" / "orquidea" / "web" / "static" / "identidad" / "identidad.css"
DESIGN = RAIZ / "governance" / "identity" / "ui" / "DESIGN.md"
ESPECIMEN = RAIZ / "governance" / "identity" / "specimen.md"

# ADR-015, decisión 2: literal → propiedades donde se admite
ADMITIDOS: dict[str, tuple[str, ...]] = {
    "0": ("*",),
    "100%": ("width", "max-width"),
    "1px": ("border", "border-top", "border-bottom", "border-left", "border-right"),
    "2px": ("outline", "outline-offset"),
    "700": ("font-weight",),
}
LITERAL = re.compile(
    r"#[0-9a-fA-F]{3,8}\b"
    r"|\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\("
    r"|(?<![\w-])-?\d*\.?\d+(?:[a-zA-Z]+|%)?(?![\w-])"
)


def tokens_de_design() -> dict[str, str]:
    """Los tokens del frontmatter de DESIGN.md como propiedades de CSS: `--colors-fondo` → valor."""
    lineas = DESIGN.read_text(encoding="utf-8").split("---")[1].splitlines()
    tokens: dict[str, str] = {}
    ruta: list[str] = []
    for linea in lineas:
        if not linea.strip() or ":" not in linea:
            continue
        nivel = (len(linea) - len(linea.lstrip())) // 2
        clave, _, valor = linea.strip().partition(":")
        ruta = [*ruta[:nivel], clave]
        valor = valor.strip().strip('"')
        if valor and ruta[0] in ("colors", "typography", "spacing"):
            nombre = "-".join(ruta).replace("fontSize", "font-size")
            tokens["--" + nombre.replace("lineHeight", "line-height")] = valor
    return tokens


def pila_del_especimen() -> str:
    texto = ESPECIMEN.read_text(encoding="utf-8")
    pila = re.search(r"```\n(system-ui[^\n]*)\n```", texto)
    assert pila is not None, "specimen.md no declara la pila de familias"
    return pila.group(1)


def reglas(css: str) -> list[tuple[str, list[tuple[str, str]]]]:
    """(selector, [(propiedad, valor)]) de cada regla, sin comentarios."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    salida = []
    for selector, cuerpo in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        declaraciones = [
            (p.strip(), v.strip())
            for p, _, v in (d.partition(":") for d in cuerpo.split(";"))
            if p.strip()
        ]
        salida.append((selector.strip(), declaraciones))
    return salida


def problemas(css: str, tokens: dict[str, str], familia: str) -> tuple[list[str], int]:
    """Lo que no viene de un token, y cuántas propiedades de `:root` se compararon."""
    esperadas = {**tokens, "--familia": familia}
    todas = reglas(css)
    raiz = [d for selector, ds in todas if selector == ":root" for d in ds]
    malos = []
    for propiedad, valor in raiz:
        if propiedad not in esperadas:
            malos.append(f"{propiedad} no es un token de DESIGN.md")
        elif valor != esperadas[propiedad]:
            token = propiedad.removeprefix("--").replace("-", ".", 1)
            malos.append(f"{propiedad} es {valor} y el token {token} es {esperadas[propiedad]}")
    declaradas = {p for p, _ in raiz}
    malos += [f"falta en :root el token {t}" for t in sorted(set(esperadas) - declaradas)]
    for selector, ds in todas:
        if selector == ":root":
            continue
        for propiedad, valor in ds:
            for usada in re.findall(r"var\((--[\w-]+)\)", valor):
                if usada not in declaradas:
                    malos.append(f"var({usada}) no está declarada en :root, en `{selector}`")
            sin_var = re.sub(r"var\([^)]*\)", "", valor)
            for literal in (m.group(0) for m in LITERAL.finditer(sin_var)):
                admitido = ADMITIDOS.get(literal, ())
                if "*" not in admitido and propiedad not in admitido:
                    malos.append(f"literal {literal} fuera de :root, en `{selector}` {propiedad}")
    return malos, len(raiz)


def test_la_hoja_usa_solo_tokens_de_la_identidad() -> None:
    malos, comparadas = problemas(
        HOJA.read_text(encoding="utf-8"), tokens_de_design(), pila_del_especimen()
    )

    assert comparadas > 0, "0 propiedades en :root — nada que comparar"
    assert malos == []


def test_el_lector_de_design_md_encuentra_los_tokens() -> None:
    tokens = tokens_de_design()

    assert tokens["--colors-fondo"] == "#F7F3EA"
    assert tokens["--typography-step-0-font-size"] == "16px"
    assert tokens["--typography-step-2-line-height"] == "36px"
    assert tokens["--spacing-step-6"] == "48px"
    assert not any(t.startswith("--components") for t in tokens)


RAIZ_CHICA = ":root { --colors-fondo: #F7F3EA; --spacing-step-2: 16px; --familia: serif; }\n"
TOKENS_CHICOS = {"--colors-fondo": "#F7F3EA", "--spacing-step-2": "16px"}


@pytest.mark.parametrize(
    ("css", "nombrado"),
    [
        (RAIZ_CHICA.replace("#F7F3EA", "#F7F3EB"), "--colors-fondo es #F7F3EB"),
        (RAIZ_CHICA + ".tarjeta { padding: 10px; }", "literal 10px"),
        (RAIZ_CHICA + ".tarjeta { padding: 0.625rem; }", "literal 0.625rem"),  # forma equivalente
        (RAIZ_CHICA + ".tarjeta { color: rgb(0 0 0); }", "literal rgb("),
        (RAIZ_CHICA + "a { color: #1F3A5F; }", "literal #1F3A5F"),
        (RAIZ_CHICA + "p { line-height: 1.5; }", "literal 1.5"),
        (RAIZ_CHICA + ".x { padding: var(--spacing-step-5); }", "var(--spacing-step-5) no está"),
        (RAIZ_CHICA + "p { border-top: 2px solid var(--colors-fondo); }", "literal 2px"),
        (RAIZ_CHICA.replace(" --spacing-step-2: 16px;", ""), "falta en :root el token"),
        (RAIZ_CHICA.replace("--familia: serif;", "--familia: serif; --otro: 3px;"), "--otro no es"),
    ],
)
def test_lo_que_no_viene_de_un_token_se_nombra(css: str, nombrado: str) -> None:
    malos, _ = problemas(css, TOKENS_CHICOS, "serif")

    assert any(nombrado in m for m in malos), malos


def test_lo_admitido_por_adr_015_pasa() -> None:
    css = RAIZ_CHICA + (
        "a:focus-visible { outline: 2px solid var(--colors-fondo); outline-offset: 2px; }\n"
        "li { border-top: 1px solid var(--colors-fondo); margin: 0 0 var(--spacing-step-2); }\n"
        "img { max-width: 100%; height: auto; } h1 { font-weight: 700; font-style: italic; }\n"
    )

    assert problemas(css, TOKENS_CHICOS, "serif") == ([], 3)


def test_sin_raiz_no_hay_verde() -> None:
    _, comparadas = problemas("a { color: var(--colors-fondo); }", TOKENS_CHICOS, "serif")

    assert comparadas == 0
