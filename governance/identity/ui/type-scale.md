---
type: type-scale
commission: "La identidad visual de la interfaz web de Orquídea: paleta, tipografía y la interfaz derivada de ellas"
derived-from: "governance/identity/specimen.md (ADR-011)"
decision: ADR-014, ADR-020
date: 2026-09-22
---

# Orquídea — Type scale

## The criterion this answers

No se repite aquí: vive en `ADR-014`, abierto antes de que existiera cualquiera de los valores de abajo, y en `ADR-020` para las columnas `Font family` y `Font weight`. Esta sección nombra los registros y nada más.

## The rule

El escalón `n` mide la base por la razón a la `n`, redondeado al entero de px más cercano (medio hacia arriba). La altura de línea es el múltiplo de 4 px más cercano a una vez y media el tamaño (medio hacia arriba). Cada rol del espécimen toma el escalón que se le asigna. La regla la corre `scripts/derivar-medidas.py escala`; la tabla de abajo es su salida sin editar, y `tests/test_derivar_medidas.py` la regenera con los parámetros de abajo y la compara con este archivo.

## The parameters

| Parameter | Value | Stratum | Alternatives it beat, and why each lost |
|-----------|-------|---------|------------------------------------------|
| base | `16` | `judgement` | ninguna menor: el piso del espécimen (ADR-011) es 16 px para todo texto, así que la base no puede bajar de él |
| razon | `1.25` | `judgement` | `1.5`: pasa M1, pero el título sale de 36 px y en 360 px ocupa dos líneas; perdió M4. `1.2` con las fechas un escalón abajo: la fecha cae a 13 px, bajo el piso (M1 en rojo, ADR-014) |
| escalones | `0,1,2` | `judgement` | un escalón `-1` para fechas y notas: queda bajo el piso; más de tres: las plantillas solo tienen cuerpo, `h2` y `h1` |
| roles | `text=0,binomial=0,date=0,subtitulo=1,titulo=2` | `judgement` | `date` un escalón abajo: la costumbre de fechas pequeñas, que el piso prohíbe; la jerarquía de fechas la dan color (`texto-secundario`) y cifras tabulares |
| altura de línea | múltiplo de 4 más cercano a 1.5 veces el tamaño | `judgement` | 1.4 veces sin rejilla: alturas como 22.4 que no caen en la unidad del espaciado; 1.5 exacto sin rejilla: 37.5 para el título |
| redondeo | al entero más cercano, medio hacia arriba | `judgement` | redondeo al par (el de `round`): el mismo tamaño daría otra altura según la paridad; truncar: rebaja un tamaño en casi un px |
| familia | `system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif` | `mechanical` | ninguna: no se elige aquí, se lee de `specimen.md:19`, la pila de sistema que el espécimen decidió (ADR-011); una fuente web contradiría a él y al criterio 1 de ADR-009 (ADR-020) |
| pesos | `0=400,1=700,2=700` | `mechanical` | ninguna: no se elige aquí, se lee de `specimen.md:26-27` (`text` 400; `emphasis` 700 en `h1` y `h2`, que son `titulo` y `subtitulo`). Otro valor contradiría al espécimen (ADR-020) |

## The scale

| Step | Size | Line height | Font family | Font weight | Roles |
|---|---|---|---|---|---|
| 0 | 16px | 24px | system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif | 400 | text, binomial, date |
| 1 | 20px | 32px | system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif | 700 | subtitulo |
| 2 | 25px | 36px | system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif | 700 | titulo |

Cada valor se reproduce: correr la regla con los parámetros de arriba lo devuelve.

## The floor, measured

`ran:` `uv run python scripts/comprobar-medidas.py piso governance/identity/ui/type-scale.md --piso 16 --lectura text,binomial,date` — salida copiada abajo.

| Role | Step it takes | Size | Floor the specimen declares | Held | Collapsed steps |
|------|---------------|------|-----------------------------|------|-----------------|
| text | 0 | 16 | 16, leído por `specimen.md` de Legge y Bigelow (2011) | sí | 0 |
| binomial | 0 | 16 | 16, ídem | sí | 0 |
| date | 0 | 16 | 16, ídem | sí | 0 |

**Steps measured:** 3 · **Reading roles measured:** 3

## How it answers the survival criteria

| Criterion | How this answers it |
|-----------|---------------------|
| `platform-specs` | no aplica, porque no se entrega una marca ni un ícono de plataforma (ADR-009) |
| `minimum-size` | los tres roles de lectura en el escalón 0, igual al piso del espécimen; ningún escalón debajo |
| `single-ink` | no aplica, porque es propiedad de una marca y este encargo no tiene marca (ADR-009) |
| `contrast` | una escala no fija colores; los pares de los componentes los mide `components.md`. Todo texto sigue siendo normal: `subtitulo` y `titulo` en negrita quedan en o sobre el umbral de texto grande, pero se juzgan igual a 7:1 |
| `prior-art` | no aplica, porque no se entrega marca ni se registra nada (ADR-009) |
| `component-contrast` | no aplica, porque una escala no es un componente; lo midió `semantics.md` |
| `target-size` | no aplica, porque una escala no declara objetivos; lo resuelve `spacing.md` |
| `provenance` | cada tamaño sale de la regla: la prueba de regeneración lo compara con la salida del script |

## How it answers the fitness criteria

| Criterion, as approved | From | Stratum | How this answers it |
|------------------------|------|----------|----------|
| M1 · piso y colapso | specimen (ADR-011) | `mechanical` | sí — 3 escalones y 3 roles de lectura medidos, 0 bajo el piso, 0 colapsados (`ran:` arriba); también en el gate (`tests/test_identidad_ui.py`) |
| M3 · reproducible | este eslabón | `mechanical` | sí — `tests/test_derivar_medidas.py` regenera la tabla |
| M4 · una jerarquía | concept (ADR-010) | `judgement` | sí, para (A) — abajo |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| M4 — la escala se lee como una sola jerarquía con peso y espacio | sí, para la escala (A) con el espaciado (A) | Daniel Efraín Domínguez Urbina, 2026-09-22, en elección forzada entre A·A, A·B, B·A y B·B (escala · espaciado) sobre la lámina de la ficha y el formulario de alta a 360 px |

## What was not measured

Que 16 px se lea en el teléfono bajo el sol lo mide el espécimen con sus parámetros declarados (35 cm, 160 px CSS por pulgada), y s5.7 lo revisa en el teléfono real. Aquí no se renderizó nada para probar un tamaño. La familia y el peso (700 en los títulos) los fija `specimen.md`, y desde ADR-020 esta escala los copia en `Font family` y `Font weight`, porque `DESIGN.md` de gemba-design 0.24.0 ya los compone. Las cifras tabulares siguen solo en `specimen.md`: el formato no las compone.

## What was tried and rejected

- **(B) Razón 1.5:** 16, 24, 36 px; pasa M1 y perdió M4 — el título de 36 px domina la pantalla de 360 px.
- **(C) Razón 1.2 con fechas un escalón abajo:** la fecha a 13 px, bajo el piso de 16 (M1 en rojo, ADR-014).
