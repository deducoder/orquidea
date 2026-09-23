# Story s5.4: Typography — Retrospective

Estimated: M · Actual: S (311 s de implementación según `implementation-time.sh develop s5.4`; sin archivos de fuente que integrar, la historia se quedó en documentos y mediciones)

## Summary

La identidad escribe con **la fuente del sistema del teléfono** (`system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif`): cuatro roles (texto 400, énfasis 700, binomio en itálica, fecha con `tabular-nums`) y un piso de legibilidad de 16 px CSS para todo texto. ADR-011 se abrió en `proposed` (`26b3b2f`) antes de medir; se midieron tres familias web en doce combinaciones; el humano eligió (A), pidió verla con fuentes reales y firmó la mitad juzgada; el espécimen quedó en `governance/identity/specimen.md` (`ddb3f5c`, firma en `c1b9728`) y el ADR en `accepted` (`2a17ede`).

### Finalize

- Gate: `./scripts/check` → `✓ gates passed`.
- Orden: `add ADR-011` (22:12:53) → `update` (22:16:09, 22:16:39) → espécimen (22:21:50) → `publish` (22:22:25) → firma (posterior, en el entregable, no en el ADR).
- Pruebas huérfanas: ninguna posible (0 `.py` en el diff).
- Aceptación: los seis escenarios del scope se cumplen; el deducido de "`--identidad` sale con 0 si hay fuente web" no aplica porque no hay fuente web, y queda dicho así, no confirmado.
- Aprobaciones del humano, 2026-09-22: T1–T4 y las cuatro opciones; la elección de (A); la prueba con fuentes reales (a petición suya); la firma de las dos filas juzgadas.
- `quality-review`: PASS (tres observaciones, una a esta retrospectiva). `security-review`: PASS.

## What went well

- **Medir cambió la decisión.** Antes de medir, una fuente web parecía el camino natural para un aspecto propio; los números (61.5–92.3 KB con cuatro estilos, 56.0–93.4 KB variables) dejaron a la negrita sintetizada como precio de cualquier fuente web y a (A) como la única que cumplía todo.
- **Leer el archivo contradijo la etiqueta.** Plex y Source Sans no traen `tnum` y aun así son tabulares por defecto; Atkinson trae `tnum` y es proporcional por defecto. Medir los anchos de avance, no los rasgos, dio la respuesta.
- **La prueba que pidió el humano subió dos filas de `read:` a `ran:`** (Roboto y Segoe UI), y el servidor de prueba se levantó y se apagó por PID como dice la memoria del proyecto.

## What to improve

- **Otra vez una salida escrita antes de correr el comando** (contraejemplo de T2), una hora después de guardar la memoria que lo prohibía. Se corrigió en `proposed`; la memoria ahora dice la regla en general: ninguna salida de comando entra a un registro sin haberla visto.
- **La estimación M suponía archivos de fuente** (descargar, recortar, commitear, medir en el repositorio); con (A) no hubo ninguno. El tamaño debió declararse condicionado a la opción.
- **El piso de 16 px depende de dos parámetros que no se midieron** (35 cm, 160 px/pulgada). Están declarados en el ADR y en el espécimen; si en s5.7 el humano lee cómodo a otra distancia, el piso se revisa con un ADR nuevo, no editando este.

## Learned

1. About the system: sin ninguna fuente enlazada, hoy la aplicación se ve en la serif por defecto del navegador; s5.7 es la primera vez que la interfaz cambia de familia.
2. About the process: en una pieza que se elige entre cosas que ya existen, el contraejemplo mecánico es barato y decisivo (el peso descartó doce combinaciones en un minuto), y lo caro es lo que se lee (qué trae cada sistema), que es donde hay que citar.
3. Capability gained: el procedimiento para medir una fuente web sin agregar dependencias (`uv run --with fonttools --with brotli`) y renderizarla con Pillow a densidad de teléfono, reusable en cualquier elección de tipografía futura.
