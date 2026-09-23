---
type: specimen
commission: "La identidad visual de la interfaz web de Orquídea: paleta, tipografía y la interfaz derivada de ellas"
decision: ADR-011
date: 2026-09-22
---

# Orquídea — Type specimen

## The criterion this answers

No se repite aquí: vive en `ADR-011`, abierto antes de medir ninguna familia. Esta sección nombra el registro y nada más.

## The system

Una sola familia: **la del sistema del teléfono**, por la pila

```
system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif
```

Ningún archivo de fuente se sirve.

| Role | Family | Weights and styles | Where it is used |
|------|--------|--------------------|------------------|
| text | la pila de arriba | 400 | cuerpo, descripciones, cuidados, citas de fuentes, etiquetas de formulario |
| emphasis | la pila de arriba | 700 | títulos (`h1`, `h2`), `strong` (el último riego) |
| binomial | la pila de arriba | 400 itálica | nombres científicos (`<i>`) |
| date | la pila de arriba | 400 con `font-variant-numeric: tabular-nums` | fechas de riegos, floraciones y altas, alineadas en columna |

Lo que se ve según el sistema: Roboto (Android), San Francisco (iOS, macOS), Segoe UI (Windows); Noto Sans o la sans del navegador en el resto.

## The scale

No se fija aquí: la escala de la interfaz es la regla del eslabón `type scale` de s5.6, que lee de este espécimen los roles y el piso. Lo único que este espécimen fija es que **ningún rol de texto baja del piso** (abajo).

## The legibility floor

| Role | Smallest size it holds | Proved how | Source of the range, and when it was read |
|------|------------------------|------------|-------------------------------------------|
| todos los roles de texto (text, binomial, date; también el de `<small>`) | **16 px CSS** | en pantalla: Roboto (la fuente de Android, desde su versión web `@fontsource/roboto` 5.3.0) renderizada con Pillow a 3 px físicos por px CSS, a 16 y 14 px; y la pila real en Chrome sobre Windows (Segoe UI) a 16 y 14 px. En papel: no aplica — la aplicación no se imprime | Legge y Bigelow (2011), «Does print size matter for reading?», *Journal of Vision* 11(5):8, doi:10.1167/11.5.8 — tamaño crítico de 0.2° de altura de x; leído el 2026-09-22 |

De 0.2° a 16 px: con el teléfono a 35 cm y 160 px CSS por pulgada (parámetros declarados, no medidos) la altura de x mínima es 7.7 px CSS; Roboto (x/em 0.528, `ran:`) la alcanza a 14.6 px. Se declara 16 px para todas porque la altura de x de San Francisco y de Segoe UI no se midió en esta máquina y porque 16 px cubre hasta una x/em de 0.48. San Francisco no se renderizó: se prueba en un iPhone en s5.7 si hay uno a mano.

## Licence

| Family | Licence | What it permits | What it costs |
|--------|---------|-----------------|---------------|
| Fuentes del sistema (Roboto, San Francisco, Segoe UI, Noto Sans) | la del sistema operativo que la trae | que el navegador la use para mostrar la página; Orquídea no copia, recorta ni distribuye ningún archivo | nada |

## How it answers the survival criteria

| Criterion | How this system answers it |
|-----------|----------------------------|
| `platform-specs` | no aplica, porque esta pieza no entrega una marca ni un ícono de plataforma (ADR-009) |
| `minimum-size` | piso declarado de 16 px CSS para todo texto, leído de Legge y Bigelow (2011) el 2026-09-22 y probado renderizando (arriba) |
| `single-ink` | no aplica, porque es propiedad de una marca y este encargo no tiene marca (ADR-009) |
| `contrast` | no se resuelve aquí: lo miden s5.3 (pares de la paleta) y s5.5 (roles) con la comprobación de ≥ 7:1 para texto normal; este espécimen solo declara que todo texto es tamaño normal — a 16 px ninguno llega al umbral de texto grande (18 pt, o 14 pt en negrita = 24 px o 18.7 px) salvo los títulos que s5.6 ponga por encima |
| `prior-art` | no aplica, porque no se entrega marca ni se registra nada (ADR-009) |
| `component-contrast` | no aplica a esta pieza, porque un sistema de tipos no es un componente; lo resuelve s5.5 y s5.6 |
| `target-size` | no aplica a esta pieza, porque no declara objetivos interactivos; lo resuelve s5.6 |
| `provenance` | la familia y los estilos salen de la pila declarada arriba; los tamaños saldrán de la escala de s5.6, cuyo único dato de aquí es el piso |

## How it answers the fitness criteria

| Criterion, as approved | From | How this system answers it | How that was established |
|------------------------|------|----------------------------|--------------------------|
| T1 · fuentes ≤ 40 KB gzip | commission 1 | 0 KB: no se sirve ningún archivo | `ran:` `medir-primera-carga.py --identidad` no aplica sin archivos; las tres opciones web con 4 estilos dieron 61.5–92.3 KB (ADR-011) |
| T2 · itálica verdadera y glifos es-MX | esta pieza | sí en los tres sistemas principales | `ran:` Roboto — archivo itálico propio y glifos, renderizado; Segoe UI — renderizado en Chrome (¿ ¡ « » — á ó, itálica diseñada) · `read:` San Francisco — Wikipedia y Apple Developer, 2026-09-22 |
| T3 · cifras tabulares | concept (ADR-010) | sí, con `font-variant-numeric: tabular-nums` en el rol `date` | `ran:` Roboto — un solo ancho de 0–9 (1151) por defecto; Segoe UI — fechas alineadas en Chrome con `tabular-nums` · `read:` San Francisco — Wikipedia, 2026-09-22 |
| T4 · licencia libre para servir y recortar | esta pieza | no aplica: no se sirve ni se recorta nada | `read:` — la fuente la pone el sistema del usuario |

## What was judged, and by whom

| Judged | Verdict | Judged by, and when |
|--------|---------|---------------------|
| Whether the pairing has character of its own | no por sí sola: el carácter lo pone la estructura del Cuaderno de campo (ADR-010), no la familia | `unsigned` — propuesto por el agente; pendiente de la firma del humano |
| Whether it suits this commission | sí: 0 KB, negrita e itálica diseñadas y la tipografía de las apps del teléfono (S3) | Daniel Efraín Domínguez Urbina, 2026-09-22, al elegir (A) |

## What was tried and rejected

- **(B) Atkinson Hyperlegible:** cabe con regular e itálica (34.7 KB), pero sin negrita propia (sintetizada), cifras proporcionales por defecto (solo con `tnum`) y más ancha: en pantalla estrecha parte más las líneas. El cero tachado ayudaba a las fechas.
- **(C) IBM Plex Sans:** falla T1 aun con solo regular e itálica (45.8 KB > 40).
- **(D) Source Sans 3:** la mejor itálica y cabe con dos estilos (30.8 KB), pero con negrita sintetizada y 31 KB más en cada primera carga; la alternativa si se quiere el mismo aspecto en todos los teléfonos.
- **Versiones variables** de (B), (C) y (D): 56.0–93.4 KB, todas sobre T1.
