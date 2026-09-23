---
type: adr
id: ADR-015
title: "Hoja de estilos de la identidad"
status: accepted
date: 2026-09-22
epic: e5
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-015: Hoja de estilos de la identidad

## Status

Accepted.

## Context

**La pregunta:** ¿cómo lleva la hoja de estilos la identidad decidida (`governance/identity/ui/DESIGN.md`, ADR-013, ADR-014 y `specimen.md`) a las plantillas? Una prueba tiene que poder decir que cada valor viene de un token, y hay que resolver lo que el formato no compone.

**Fuerzas:**
- El done-when de e5 pide que todo valor de la hoja sea un token de `DESIGN.md` y que una prueba se ponga en rojo con un valor inventado.
- El brief descarta una cadena de construcción de CSS: la hoja se escribe a mano.
- `DESIGN.md` no trae bordes ni foco como componentes (están en `colors`), ni peso, cifras tabulares o familia (están en `specimen.md`), ni grosores de trazo, ni `rounded` (ADR-014, huecos).
- La miniatura mide 192 px de lado (`datos/fotos.py`). Hacerla más grande sube el peso de la primera carga (`must-perf-001`) y cambia datos, y eso es no-go del brief.
- s5.6 dejó dos preguntas abiertas: las esquinas, y si el subtítulo de 20 px se distingue del cuerpo.

## Decision

Aprobada por Daniel Efraín Domínguez Urbina el 2026-09-22, con el diseño de s5.7.

1. **Un token, una propiedad personalizada con el nombre de su ruta**, declarada una sola vez en `:root` de `src/orquidea/web/static/identidad/identidad.css`: `--colors-{rol}`, `--typography-step-{n}-font-size`, `--typography-step-{n}-line-height` y `--spacing-step-{m}`. La pila de familias de `specimen.md` va en `--familia`. Fuera de `:root` las reglas solo usan `var(--…)`.
2. **Lista cerrada de literales admitidos fuera de `:root`**, que la prueba de tokens lleva igual:
   - `0`, `100%`, `auto`, `none` e `inherit`: no son medidas de la identidad.
   - `1px`, solo como grosor de un borde (`campo-borde`, `linea`, `error`).
   - `2px`, solo como grosor y separación del anillo de `foco`. WCAG 2.2 SC 2.4.13 (AAA) pide un indicador de al menos el área de un perímetro de 2 px CSS; AA no fija grosor.
   - `700`, `italic` y `tabular-nums`, los valores de `font-weight`, `font-style` y `font-variant-numeric` que declara `specimen.md`.
3. **Esquinas rectas:** ningún `border-radius`.
4. **Lista de ejemplares:** la miniatura se muestra en 96 × 96 junto al texto, como hoy. La foto a todo el ancho es la de la ficha.
5. **El subtítulo se juzga renderizado.** Si en el recorrido no se distingue del cuerpo en negrita, el ajuste va por espacio (un paso de `spacing` como margen) y nunca por tamaño, que es de ADR-014.

## Consequences

**Positive:**
- La prueba compara nombres con nombres. `superficie` y `campo-fondo`, que tienen el mismo `#FFFFFF`, siguen siendo dos tokens distintos en la hoja.
- Un cambio de identidad se hace en el eslabón, se regenera `DESIGN.md` y se cambia una línea de `:root`. La prueba dice cuál falta.

**Negative / costs:**
- Los grosores de trazo son literales admitidos, no tokens. Si un día se quieren derivar, necesitan un eslabón y un ADR nuevos, y la lista se reduce.
- Hay dos fuentes de verdad fuera de `DESIGN.md` para la hoja: `specimen.md` (familia, peso, cifras) y esta lista. La prueba lee las dos.
- La lista de ejemplares no pone la foto a todo el ancho. Si el criterio 3 no se cumple ahí, la salida es una miniatura más grande, con su medición de peso y su ADR.

## Alternatives considered

- **Literales en cada regla, comparados con los valores de `DESIGN.md`:** la prueba no podría decir de qué token viene un `#FFFFFF` ni un `16px`, y dos tokens del mismo valor serían indistinguibles.
- **Tokens de trazo (grosor de borde y de anillo) en un ADR nuevo de s5.6:** reabre una cadena cerrada por dos valores que ninguna regla derivaría.
- **Esquinas redondeadas con un ADR que derive `rounded`:** no hay regla publicada de atributo a radio (lo declara el generador), y una libreta de campo tiene esquinas rectas.
- **La miniatura a todo el ancho de la tarjeta:** se vería borrosa (192 px estirados a unos 330), o pediría miniaturas más grandes y más peso (no-go).
