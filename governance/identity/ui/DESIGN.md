---
version: alpha
name: Orquídea
colors:
  fondo: "#F7F3EA"
  superficie: "#FFFFFF"
  texto: "#1E1C19"
  texto-secundario: "#4A453E"
  enlace: "#1F3A5F"
  error: "#8A1C1C"
  línea: "#8C8475"
  campo-fondo: "#FFFFFF"
  campo-borde: "#8C8475"
  acción-fondo: "#1F3A5F"
  acción-texto: "#FFFFFF"
  acción-presionada: "#0C274A"
  foco: "#1F3A5F"
typography:
  step-0:
    fontSize: 16px
    lineHeight: 24px
    fontWeight: 400
  step-1:
    fontSize: 20px
    lineHeight: 32px
    fontWeight: 700
  step-2:
    fontSize: 25px
    lineHeight: 36px
    fontWeight: 700
rounded:
  recto: "0px"
spacing:
  step-1: 8px
  step-2: 16px
  step-3: 24px
  step-4: 32px
  step-6: 48px
components:
  pagina:
    backgroundColor: "{colors.fondo}"
    textColor: "{colors.texto}"
    typography: "{typography.step-0}"
  tarjeta:
    backgroundColor: "{colors.superficie}"
    textColor: "{colors.texto}"
    typography: "{typography.step-0}"
    rounded: "{rounded.recto}"
    padding: "{spacing.step-2}"
  titulo:
    backgroundColor: "{colors.fondo}"
    textColor: "{colors.texto}"
    typography: "{typography.step-2}"
  subtitulo:
    backgroundColor: "{colors.fondo}"
    textColor: "{colors.texto}"
    typography: "{typography.step-1}"
  boton:
    backgroundColor: "{colors.acción-fondo}"
    textColor: "{colors.acción-texto}"
    typography: "{typography.step-0}"
    rounded: "{rounded.recto}"
    padding: "{spacing.step-2}"
    minHeight: "{spacing.step-6}"
    minWidth: "{spacing.step-6}"
  boton-presionado:
    backgroundColor: "{colors.acción-presionada}"
    textColor: "{colors.acción-texto}"
    typography: "{typography.step-0}"
    rounded: "{rounded.recto}"
    padding: "{spacing.step-2}"
    minHeight: "{spacing.step-6}"
    minWidth: "{spacing.step-6}"
  campo:
    backgroundColor: "{colors.campo-fondo}"
    textColor: "{colors.texto}"
    typography: "{typography.step-0}"
    rounded: "{rounded.recto}"
    padding: "{spacing.step-1}"
    borderColor: "{colors.campo-borde}"
    minHeight: "{spacing.step-6}"
    minWidth: "{spacing.step-6}"
  enlace-navegacion:
    backgroundColor: "{colors.fondo}"
    textColor: "{colors.enlace}"
    typography: "{typography.step-0}"
    minHeight: "{spacing.step-6}"
    minWidth: "{spacing.step-6}"
  aviso:
    backgroundColor: "{colors.fondo}"
    textColor: "{colors.error}"
    typography: "{typography.step-0}"
  fecha:
    backgroundColor: "{colors.superficie}"
    textColor: "{colors.texto-secundario}"
    typography: "{typography.step-0}"
---

# Orquídea

Generated from the tables of the deliverables by the generator of the UI technique. Nobody edits this file: change the rule or a parameter and generate it again.

## Overview

The values are the tokens above and are normative; this text cites them by reference and never repeats a value.

## Colors

- {colors.fondo}
- {colors.superficie}
- {colors.texto}
- {colors.texto-secundario}
- {colors.enlace}
- {colors.error}
- {colors.línea}
- {colors.campo-fondo}
- {colors.campo-borde}
- {colors.acción-fondo}
- {colors.acción-texto}
- {colors.acción-presionada}
- {colors.foco}

## Typography

- {typography.step-0}: text, binomial, date
- {typography.step-1}: subtitulo
- {typography.step-2}: titulo

## Layout

- {spacing.step-1}: 1 unidad
- {spacing.step-2}: 2 unidades
- {spacing.step-3}: 3 unidades
- {spacing.step-4}: 4 unidades
- {spacing.step-6}: 6 unidades; tamaño de control

## Elevation & Depth

Not derived: see Known Gaps.

## Shapes

- {rounded.recto}: botones, campos y tarjetas

## Components

- pagina: backgroundColor is {colors.fondo}, textColor is {colors.texto}, typography is {typography.step-0}
- tarjeta: backgroundColor is {colors.superficie}, textColor is {colors.texto}, typography is {typography.step-0}, rounded is {rounded.recto}, padding is {spacing.step-2}
- titulo: backgroundColor is {colors.fondo}, textColor is {colors.texto}, typography is {typography.step-2}
- subtitulo: backgroundColor is {colors.fondo}, textColor is {colors.texto}, typography is {typography.step-1}
- boton: backgroundColor is {colors.acción-fondo}, textColor is {colors.acción-texto}, typography is {typography.step-0}, rounded is {rounded.recto}, padding is {spacing.step-2}, minHeight is {spacing.step-6}, minWidth is {spacing.step-6}
- boton-presionado: backgroundColor is {colors.acción-presionada}, textColor is {colors.acción-texto}, typography is {typography.step-0}, rounded is {rounded.recto}, padding is {spacing.step-2}, minHeight is {spacing.step-6}, minWidth is {spacing.step-6}
- campo: backgroundColor is {colors.campo-fondo}, textColor is {colors.texto}, typography is {typography.step-0}, rounded is {rounded.recto}, padding is {spacing.step-1}, borderColor is {colors.campo-borde}, minHeight is {spacing.step-6}, minWidth is {spacing.step-6}
- enlace-navegacion: backgroundColor is {colors.fondo}, textColor is {colors.enlace}, typography is {typography.step-0}, minHeight is {spacing.step-6}, minWidth is {spacing.step-6}
- aviso: backgroundColor is {colors.fondo}, textColor is {colors.error}, typography is {typography.step-0}
- fecha: backgroundColor is {colors.superficie}, textColor is {colors.texto-secundario}, typography is {typography.step-0}

## Do's and Don'ts

- Do use a token by reference and never by its value.
- Do not edit this file: it is generated.

## Verifiable constraints

Generated from the same tokens as the frontmatter, for the instruments of the mechanical stratum to read. Nobody edits these tables.

| Role | Value |
|------|-------|
| fondo | #F7F3EA |
| superficie | #FFFFFF |
| texto | #1E1C19 |
| texto-secundario | #4A453E |
| enlace | #1F3A5F |
| error | #8A1C1C |
| línea | #8C8475 |
| campo-fondo | #FFFFFF |
| campo-borde | #8C8475 |
| acción-fondo | #1F3A5F |
| acción-texto | #FFFFFF |
| acción-presionada | #0C274A |
| foco | #1F3A5F |

| Foreground | Ground | Kind |
|------------|--------|------|
| texto | fondo | text |
| texto | superficie | text |
| acción-texto | acción-fondo | text |
| acción-texto | acción-presionada | text |
| texto | campo-fondo | text |
| enlace | fondo | text |
| error | fondo | text |
| texto-secundario | superficie | text |

| Target | Width | Height |
|--------|-------|--------|
| boton | 48 | 48 |
| boton-presionado | 48 | 48 |
| campo | 48 | 48 |
| enlace-navegacion | 48 | 48 |

| Step | Value |
|------|-------|
| spacing.step-1 | 8px |
| spacing.step-2 | 16px |
| spacing.step-3 | 24px |
| spacing.step-4 | 32px |
| spacing.step-6 | 48px |

| Token | Value | From |
|-------|-------|------|
| components.tarjeta.padding | 16px | spacing.step-2 |
| components.boton.padding | 16px | spacing.step-2 |
| components.boton.minHeight | 48px | spacing.step-6 |
| components.boton.minWidth | 48px | spacing.step-6 |
| components.boton-presionado.padding | 16px | spacing.step-2 |
| components.boton-presionado.minHeight | 48px | spacing.step-6 |
| components.boton-presionado.minWidth | 48px | spacing.step-6 |
| components.campo.padding | 8px | spacing.step-1 |
| components.campo.minHeight | 48px | spacing.step-6 |
| components.campo.minWidth | 48px | spacing.step-6 |
| components.enlace-navegacion.minHeight | 48px | spacing.step-6 |
| components.enlace-navegacion.minWidth | 48px | spacing.step-6 |

## Decisions

- ADR-013: roles de color de la interfaz
- ADR-014: escala tipográfica, espaciado y componentes
- ADR-016: la identidad en el vocabulario de gemba-design 0.23.0
- ADR-020: el peso de cada paso de la escala

## Known Gaps

- Radius, elevation and motion are not derived: no rule from an attribute to a value is published.
- Whatever needs a rendered interface is not measured: zoom, reflow, text spacing and focus.
- Iconography has nowhere to declare a family or a style: neither `Dimension` nor `number`, the only types the spec gives a token, hold a name like "Material Symbols" or "outlined".
- El anillo de foco (rol foco) no tiene componente: el formato no compone estados de foco.
- Las cifras tabulares de date viven en specimen.md: el formato no las compone en typography.
- Los enlaces dentro de un párrafo se apoyan en la excepción inline de WCAG 2.2 SC 2.5.8 y 2.5.5; no son objetivos declarados.
- Trazo: 1 px en el borde del campo y en los separadores, 2 px en el anillo de foco (components.md); el formato no tiene grosores.
- Elevación: dos planos separados solo por tono, superficie sobre fondo (components.md); el formato no tiene elevación.
- Retícula: una columna con margen lateral de spacing.step-2 (components.md); el formato no tiene retícula.
- Medida: sin tope, el renglón ocupa el ancho de la página menos su margen (components.md, ADR-016); el formato no tiene medida.
