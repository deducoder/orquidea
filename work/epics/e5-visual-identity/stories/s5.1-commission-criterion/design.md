# Story s5.1: Commission criterion — Design

> Complexity: moderate

## 1 · What & why

**Problem:** los criterios aprobados el 2026-09-22 existen solo en la conversación, y dos de ellos (peso ≤ 50 KB, contraste ≥ 7:1) no tienen instrumento: el script de medición no aísla los recursos de la identidad y el instrumento de contraste del addon fija el umbral en 4.5:1.
**Value:** con ADR-009 commiteado antes que nada y las dos comprobaciones vistas en rojo, cada pieza de e5 puede demostrar con `git log` que su criterio fue anterior, y s5.3 a s5.7 tienen con qué medirse sin escribir nada nuevo.

## 2 · Approach

Seguir la técnica `commission` paso a paso: abrir ADR-009 en `proposed` (rejilla de la convención del ciclo), escribir con TDD las dos comprobaciones en `scripts/` con el mismo contrato que los instrumentos del addon (salida 0/1/2, población contada, sin sujeto es rojo), verlas en rojo sobre sujetos construidos para violarlas, anotar los rojos en el ADR, producir `commission.md` y completar el ADR.

**Components affected:**

- `records/decisions/adr-009-criterio-del-encargo-de-identidad.md`: create — en `proposed` primero (`docs(s5.1): add ADR-009`), actualizado con los rojos (`docs(s5.1): update ADR-009`), completado a `accepted` (`docs(s5.1): publish ADR-009`).
- `scripts/medir-primera-carga.py`: modify — función `medir_identidad(directorio)` y opción `--identidad DIR` que mide solo eso contra 50 KB; el modo por defecto (colección y ficha) no cambia hasta s5.7.
- `scripts/contraste-de-lectura.py`: create — lee las tablas `Foreground | Ground | Kind` y `Role | Value` del mismo formato que `tokens.py pairs` y juzga los pares `Kind = text` contra 7:1.
- `tests/test_medicion.py`: modify — pruebas de `medir_identidad` y `--identidad`.
- `tests/test_contraste_de_lectura.py`: create.
- `governance/identity/commission.md`: create — desde `assets/commission.md` de la técnica.

**Legacy sweep:** nada queda huérfano; la medición existente (`medir`, `medir_ficha`, `main` sin `--identidad`) se conserva intacta y sus pruebas no cambian.

### Decisiones de diseño (sin ADR propio; caben en ADR-009 o son baratas de revertir)

- **Dónde vive la identidad:** `src/orquidea/web/static/identidad/` (CSS y fuentes). La población del criterio 1 es todo archivo de ese directorio; una fuente presente y no usada cuenta igual (conservador). El diseño de la épica decía `static/identidad.css`; s5.7 lo pondrá dentro de ese directorio. Alternativa rechazada: deducir los recursos de los `href`/`src` de la página más los `url()` de la hoja — más código, y dependería de un CSS que aún no existe.
- **Peso en gzip de cada archivo**, como ya cuenta el script el HTML y el JavaScript; una fuente `woff2` no comprime y el gzip le suma unos bytes: la medición queda del lado seguro.
- **Qué es "lectura corrida" para el criterio 2:** todos los pares `Kind = text` (texto de tamaño normal); los `large` (≥ 18 pt o 14 pt negrita) quedan fuera. Es más amplio que la letra del criterio (incluye fechas y fuentes en `<small>`), y es a propósito: ese texto pequeño es justo el que se lee bajo el sol. **Pregunta al humano** (ver al final).
- **La fórmula WCAG se escribe en el proyecto.** El addon la tiene una vez en `contrast.py`, pero vive en la caché del plugin (ruta con versión) y no está vendorizada; importarla por ruta rompería en CI y en otra máquina. La copia son seis líneas y la ata la prueba de control `#767676` sobre blanco = 4.54:1, el mismo caso que el addon.
- **Códigos de salida:** 0 todo pasa, 1 algo bajo el umbral o sobre el tope, 2 nada juzgado (sin sujeto o entrada ilegible) — el contrato de `conventions/mechanical`. El 2 de `argparse` por uso inválido también es "nada juzgado", así que no se confunde con el rojo del criterio.

## 3 · Interface / examples

### Usage (CLI)

```sh
uv run python scripts/medir-primera-carga.py --identidad src/orquidea/web/static/identidad
uv run python scripts/contraste-de-lectura.py governance/identity/palette.md
```

### Expected output (success + error)

```
$ uv run python scripts/medir-primera-carga.py --identidad /tmp/muestra   # un archivo aleatorio de 60 KB
Recursos de la identidad en /tmp/muestra: 1 archivo(s)
  fuente.woff2 (gzip)   60.0 KB
  Total                  60.0 KB   tope 50 KB  PASA DEL TOPE
exit=1

$ uv run python scripts/medir-primera-carga.py --identidad /tmp/vacio
Recursos de la identidad en /tmp/vacio: 0 archivo(s) — nada que medir
exit=2

$ uv run python scripts/contraste-de-lectura.py /tmp/par-gris.md
#767676 sobre #ffffff (texto): 4.54:1  necesita 7:1  NO
1 par(es) de texto juzgado(s), 1 bajo el umbral
exit=1

$ uv run python scripts/contraste-de-lectura.py /tmp/par-oscuro.md
tinta sobre papel (texto): 7.00:1  necesita 7:1  SÍ    # #595959 sobre #ffffff
1 par(es) de texto juzgado(s), 0 bajo el umbral
exit=0

$ uv run python scripts/contraste-de-lectura.py /tmp/sin-tabla.md
0 par(es) de texto juzgado(s) — nada que juzgar
exit=2
```

### Key data structures

```markdown
| Role  | Value   |
|-------|---------|
| tinta | #595959 |
| papel | #ffffff |

| Foreground | Ground | Kind |
|------------|--------|------|
| tinta      | papel  | text |
| #767676    | #ffffff| text |
```

```python
@dataclass(frozen=True)
class MedicionDeIdentidad:
    archivos: tuple[tuple[str, int], ...]  # (nombre, octetos en gzip)

    @property
    def total(self) -> int: ...


TOPE_DE_IDENTIDAD = 50 * 1024
```

## 4 · Acceptance criteria

- **Must:**
  - El commit `docs(s5.1): add ADR-009` precede, por fecha de autor y por orden en la rama, a todo commit que toque `scripts/`, `tests/` o `governance/identity/`.
  - `medir_identidad` cuenta los archivos del directorio, suma su gzip y compara con 51 200 bytes; directorio vacío o inexistente → salida 2, nunca 0.
  - `contraste-de-lectura.py` resuelve roles por nombre desde la tabla `Role | Value`, juzga solo `Kind = text` contra 7:1 y cuenta la población; un rol que no resuelve o un color ilegible → salida 2 nombrando la entrada.
  - Los rojos de la comprobación 1 (muestra de 60 KB) y 2 (`#767676` sobre `#ffffff`) se copian literalmente en ADR-009 antes de escribir `commission.md`.
  - `./scripts/check` en verde con las pruebas nuevas.
- **Should:**
  - La frontera exacta probada: 51 200 bytes pasa, 51 201 no; `#595959` sobre blanco (7.00:1) pasa y `#5a5a5a` (6.90:1) no.
- **Must NOT:**
  - Escribir un color, una fuente, un token o CSS.
  - Cambiar la salida ni el código de salida de `medir-primera-carga.py` sin `--identidad`.
  - Firmar la mitad juzgada en nombre del humano.

### Deduced criteria

- Una comprobación sin nada que medir sale en rojo por población vacía, distinguible del rojo del criterio, y nunca en verde: confirmed — el contrato de `conventions/mechanical` usa 2 para eso y 1 para el criterio; se adopta igual.
- El mismo ADR-009 pasa a `accepted`, mismo archivo y mismo número, una vez escrito `commission.md` y firmada o marcada `unsigned` la mitad juzgada: confirmed — es el paso `record-complete` del ciclo y la etapa 2 de la técnica `adr`.
- Las dos comprobaciones tienen pruebas en `./scripts/check`, incluida la de población vacía: confirmed — `tests/` ya carga `scripts/medir-primera-carga.py` con `importlib`; el script nuevo se prueba igual.
- `commission.md` existe en `governance/identity/` con `decision: ADR-009`: confirmed — la convención `deliverables` fija la raíz y la plantilla trae la clave `decision:`.

## 5 · Pregunta abierta para el humano

**Alcance del criterio 2.** Propongo que "texto de lectura corrida ≥ 7:1" se mida sobre **todo el texto de tamaño normal** (`Kind = text`), no solo sobre los párrafos, porque las fechas, las fuentes y los datos de riego se leen en campo tan pequeños como el cuerpo. La otra lectura, solo el cuerpo de los párrafos, deja el texto pequeño en 4.5:1 (el piso de `contrast`). El criterio lo aprobaste tú: la decisión de ampliarlo también es tuya.
