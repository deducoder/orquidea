# Story s5.3: Palette — Retrospective

Estimated: S · Actual: S (82 s de implementación según `implementation-time.sh develop s5.3`; el resto fue la lámina de juicio y la parada de elección)

## Summary

La paleta es **papel cálido, azul tinta**: `papel` `#F7F3EA`, `hoja` `#FFFFFF`, `tinta` `#1E1C19`, `tinta suave` `#4A453E`, `renglón` `#8C8475`, `acento` `#1F3A5F`, `alerta` `#8A1C1C`; sin variante. ADR-012 se abrió en `proposed` (`5c80399`) sin valores; las tres candidatas se fijaron y midieron en el scratchpad y el rojo se vio sobre `#767676` (`a6a4421`); el humano eligió y firmó sobre una lámina con fotos reales; `palette.md` (`0d7b15d`) y ADR-012 `accepted` (`642da77`).

### Finalize

- Gate: `./scripts/check` → `✓ gates passed`.
- Orden: `add ADR-012` (22:32:41) → `update` (22:34:14) → `palette.md` (22:35:36) → `publish` (22:35:49).
- Medición del entregable: `contraste-de-lectura.py governance/identity/palette.md` → 8 pares de texto, 0 bajo el umbral, exit 0; `tokens.py pairs` del addon → 10 pares (8 texto, 2 componente), 0 bajo su umbral, exit 0 — los dos instrumentos coinciden en las ocho razones de texto.
- Pruebas huérfanas: ninguna posible (0 `.py`).
- Aceptación: los cinco escenarios del scope se cumplen; el deducido (dos tablas legibles y variante declarada) se confirmó en el diseño y se ve en el entregable.
- `quality-review` y `security-review`: PASS (una observación descartada en voz alta: dos tablas `Role`).

## What went well

- **La lámina con fotos reales convirtió P2 en una elección que se podía ver**: el acento verde de (C) junto al follaje de *Cuitlauzina* y *Brassia* no se habría notado en una tabla de hexadecimales.
- **El segundo instrumento confirmó al primero**: `tokens.py pairs` dio las mismas ocho razones que `contraste-de-lectura.py`, lo que también vale como prueba cruzada de la fórmula copiada en s5.1, y midió de paso los dos pares `component` que la comprobación del proyecto no juzga.
- **Ninguna cifra se escribió antes de verla**: las de las candidatas vienen de la salida del instrumento, y las dos que no (1.48 y 3.34) se recalcularon antes del commit.

## What to improve

- **Las tres candidatas pasaron P1 a la primera**, así que el rojo tuvo que construirse (`#767676`). Es legítimo, pero dice que P1 no discriminó entre candidatas: la elección la hizo por completo el juicio. Para s5.5, donde las rampas sí pueden caer bajo el umbral, el contraejemplo saldrá de una candidata real.
- **Dos tablas con encabezado `Role` en un mismo entregable** funcionan por el orden; la plantilla de la técnica pide la tabla descriptiva, y el formato de instrumento pide otra. Si s5.5 tropieza, se unifican.

## Learned

1. About the system: con todo texto a 16 px (ADR-011), el umbral de texto grande nunca aplica, y la tinta suave es la que marca el margen de la paleta (8.57:1).
2. About the process: juzgar un color con el contenido real al lado (fotos del catálogo, bajadas solo al scratchpad con su licencia) cuesta minutos y cambia el veredicto.
3. Capability gained: una lámina de juicio reproducible (Pillow, Roboto de s5.4, fotos de Commons con licencia anotada) para las mitades juzgadas de s5.5 y s5.6.
