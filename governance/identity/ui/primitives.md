---
type: primitives
commission: "La identidad visual de la interfaz web de Orquídea: paleta, tipografía y la interfaz derivada de ellas"
identity: "governance/identity/palette.md (ADR-012)"
decision: ADR-013
date: 2026-09-22
---

# Orquídea — Colour primitives

## The criterion this answers

No se repite aquí: vive en `ADR-013`, abierto antes de que existiera cualquiera de los valores de abajo. Esta sección nombra el registro y nada más.

## The rule

**Anclas en OKLCH.** Cada rampa pasa por los roles de la paleta de su tono (las anclas) y por el blanco del escalón 0. Cada rol toma el escalón de la rejilla con la luminosidad más cercana a la suya y lo reemplaza con su valor exacto. Los demás escalones toman la luminosidad de la rejilla; su croma y su tono se interpolan en OKLCH entre las dos anclas que los rodean y, por debajo del ancla más oscura, conservan los de esa ancla. Un color que cae fuera de sRGB conserva luminosidad y tono y pierde croma hasta entrar.

La regla la corre `scripts/derivar-primitivas.py`; las tablas de abajo son su salida sin editar, y una prueba del gate (`tests/test_derivar_primitivas.py`) las regenera con la regla registrada y las compara con este archivo:

```sh
uv run python scripts/derivar-primitivas.py governance/identity/palette.md --regla anclas
```

## The parameters

| Parameter | Value | Stratum | Alternatives it beat, and why each lost |
|-----------|-------|---------|------------------------------------------|
| regla | `anclas` | `judgement` | `oklch` (uniforme): rompe R1 y `component-contrast` — `texto-secundario` sobre `fondo` 6.86:1, `campo-borde` sobre `fondo` 2.76:1 (ADR-013); `hsl` (uniforme): pasa los umbrales, pero cambia `tinta` a `#38342E` y `papel` a `#EEEDEB` (desvío 0.100) y perdió la elección forzada de R3 |
| espacio de color | OKLCH | `judgement` | HSL: su luminosidad no es perceptual, y es lo que movió `tinta` en la regla `hsl`; sRGB lineal: interpolar ahí oscurece y ensucia los medios tonos |
| rampas | `neutro` (hoja, papel, renglón, tinta suave, tinta), `azul` (acento), `rojo` (alerta) | `judgement` | una rampa por rol (siete): los cinco neutros comparten tono y serían cinco rampas casi iguales |
| escalones | doce: `0, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950` | `judgement` | diez (sin `0` ni `950`): sin blanco declarado `hoja` no tiene escalón, y sin `950` la tinta (L ≈ 0.23) cae fuera de la rejilla |
| luminosidad de la rejilla | `1 − i · 0.80 / 11`, de 1 a 0.20 | `judgement` | hasta 0.10: los escalones más oscuros que la tinta no los usa ningún rol; curva no lineal: no hay dato que la pida y la uniforme es la que se puede verificar a ojo |
| gama | conserva L y h, reduce C por bisección (1e-4) | `judgement` | recortar cada canal a [0, 1]: cambia el tono del color recortado |
| asignación | el escalón más cercano; en empate, el más oscuro; ningún escalón compartido | `judgement` | en empate el más claro: puede rebajar el contraste de un texto |
| respaldo | ninguno | `judgement` | desplazar el rol al escalón más cercano que cumpla su umbral: esconde el rojo que la regla causó |
| desvío | ΔE en OKLab | `judgement` | ΔE 2000: pide otra conversión (CIELAB D50) y nada aquí la necesita |

## The primitives

| Step | Value | Ramp |
|---|---|---|
| neutro-0 | #FFFFFF | neutro |
| neutro-50 | #F7F3EA | neutro |
| neutro-100 | #D4CFC4 | neutro |
| neutro-200 | #BDB7AB | neutro |
| neutro-300 | #A7A093 | neutro |
| neutro-400 | #8C8475 | neutro |
| neutro-500 | #7C7568 | neutro |
| neutro-600 | #666055 | neutro |
| neutro-700 | #4A453E | neutro |
| neutro-800 | #3D3933 | neutro |
| neutro-900 | #292723 | neutro |
| neutro-950 | #1E1C19 | neutro |
| azul-0 | #FFFFFF | azul |
| azul-50 | #E3E7EC | azul |
| azul-100 | #C9D0DA | azul |
| azul-200 | #AEB9C8 | azul |
| azul-300 | #94A2B6 | azul |
| azul-400 | #7B8CA4 | azul |
| azul-500 | #637792 | azul |
| azul-600 | #4C6281 | azul |
| azul-700 | #354E70 | azul |
| azul-800 | #1F3A5F | azul |
| azul-900 | #0C274A | azul |
| azul-950 | #001535 | azul |
| rojo-0 | #FFFFFF | rojo |
| rojo-50 | #F3E3E1 | rojo |
| rojo-100 | #E6C7C3 | rojo |
| rojo-200 | #D9ABA6 | rojo |
| rojo-300 | #CB9089 | rojo |
| rojo-400 | #BC756E | rojo |
| rojo-500 | #AC5A53 | rojo |
| rojo-600 | #9C3E38 | rojo |
| rojo-700 | #8A1C1C | rojo |
| rojo-800 | #710009 | rojo |
| rojo-900 | #510004 | rojo |
| rojo-950 | #320002 | rojo |

Todos los valores se reproducen: correr la regla con los parámetros de arriba los devuelve. Los escalones de las anclas:

| Identity role | Identity value | Resolves to | Primitive | Drift |
|---|---|---|---|---|
| hoja | #FFFFFF | neutro-0 | #FFFFFF | 0.000 |
| papel | #F7F3EA | neutro-50 | #F7F3EA | 0.000 |
| renglón | #8C8475 | neutro-400 | #8C8475 | 0.000 |
| tinta suave | #4A453E | neutro-700 | #4A453E | 0.000 |
| tinta | #1E1C19 | neutro-950 | #1E1C19 | 0.000 |
| acento | #1F3A5F | azul-800 | #1F3A5F | 0.000 |
| alerta | #8A1C1C | rojo-700 | #8A1C1C | 0.000 |


## The pairs, measured

Los pares de la aplicación de los roles, en el caso base. Como cada rol resuelve a su valor exacto (desvío 0.000), son los mismos pares, con los mismos valores, que `semantics.md` mide como roles por función — cifras copiadas de `ran:` `uv run python scripts/contraste-de-lectura.py governance/identity/ui/semantics.md` y `ran:` `python3 $G/tokens.py pairs governance/identity/ui/semantics.md`.

| Pair | Ground | Base case | Variant (ninguna declarada) |
|------|--------|-----------|-----------------------------|
| tinta (`neutro-950`) | papel (`neutro-50`) | 15.35:1 | no se compara |
| tinta (`neutro-950`) | hoja (`neutro-0`) | 17.00:1 | no se compara |
| tinta suave (`neutro-700`) | papel | 8.57:1 | no se compara |
| tinta suave (`neutro-700`) | hoja | 9.49:1 | no se compara |
| acento (`azul-800`) | papel | 10.37:1 | no se compara |
| acento (`azul-800`) | hoja | 11.48:1 | no se compara |
| alerta (`rojo-700`) | papel | 8.38:1 | no se compara |
| alerta (`rojo-700`) | hoja | 9.28:1 | no se compara |
| renglón (`neutro-400`) | papel | 3.34:1 (componente) | no se compara |
| renglón (`neutro-400`) | hoja | 3.70:1 (componente) | no se compara |

**Pairs measured:** 10

## How it answers the survival criteria

| Criterion | How this answers it |
|-----------|---------------------|
| `platform-specs` | no aplica, porque no se entrega una marca ni un ícono de plataforma (ADR-009) |
| `minimum-size` | no aplica, porque las primitivas no fijan tamaños; lo resolvió `specimen.md` (16 px) |
| `single-ink` | no aplica, porque es propiedad de una marca y este encargo no tiene marca (ADR-009) |
| `contrast` | los ocho pares de texto de arriba, el más bajo 8.38:1, sobre 4.5:1 y sobre el 7:1 del encargo |
| `prior-art` | no aplica, porque no se entrega marca ni se registra nada (ADR-009) |
| `component-contrast` | `renglón` sobre `papel` 3.34:1 y sobre `hoja` 3.70:1, contra 3:1; los componentes por función los mide `semantics.md` |
| `target-size` | no aplica, porque las primitivas no declaran objetivos interactivos; lo resuelve s5.6 |
| `provenance` | cada valor sale de la regla: la prueba de regeneración lo compara con la salida del script, y `semantics.md` toma cada rol de un escalón de aquí |

## How it answers the fitness criteria

| Criterion, as approved | From | Stratum | How this answers it |
|------------------------|------|----------|----------|
| R1 · texto ≥ 7:1 | commission 2 | `mechanical` | lo mide `semantics.md` sobre los roles; aquí, los ocho pares de texto de las anclas, el más bajo 8.38:1 |
| R2 · reproducible y desde un escalón | este eslabón | `mechanical` | sí — `ran:` `uv run pytest tests/test_derivar_primitivas.py` en verde, incluida la prueba que regenera este archivo |
| R3 · se lee como Cuaderno de campo; el azul, una familia | concept (ADR-010) | `judgement` | sí, para (A) — abajo |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| R3 — el azul sigue siendo una sola familia a lo largo de su rampa, y la regla deja la paleta como se firmó | sí, para (A); no, para (C) | Daniel Efraín Domínguez Urbina, 2026-09-22, en elección forzada entre (A) y (C) sobre la lámina del formulario de alta |

## What was not measured

Nada de lo que solo una interfaz renderizada muestra: cómo se ven los escalones en una pantalla real bajo el sol, zoom, reflujo o foco. Los escalones que ningún rol usa todavía (casi toda la rampa roja y los claros del azul) no se midieron contra ningún fondo: no son pares de nada hasta que un componente los pida. La variante no se compara: la identidad no declara ninguna.

## What was tried and rejected

- **(B) Uniforme en OKLCH:** oscurece el papel (`#EFE6D5`) y aclara la tinta suave (`#534C3E`); `texto-secundario` sobre `fondo` cae a 6.86:1 y `línea` y `campo-borde` sobre `fondo` a 2.76:1.
- **(C) Uniforme en HSL:** pasa los umbrales (mínimos 7.40:1 y 3.30:1), pero la tinta sale `#38342E` y el papel `#EEEDEB`, gris frío; perdió R3.
