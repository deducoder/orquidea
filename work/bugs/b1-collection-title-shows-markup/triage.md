# Bug b1: Collection title shows markup — Triage

## Severity: Minor
Es cosmético: la pestaña, el historial y los marcadores de "Mi colección" muestran marcado como texto, pero la página carga, el enlace para agregar una planta sigue en el cuerpo y ningún dato ni flujo se ve afectado. No hay ejecución: `<title>` es RCDATA y el navegador no interpreta lo que contiene.
**Overturned by:** que el contenido del bloque llegue a interpretarse como HTML en algún contexto (p. ej., un lector de pantalla que lea el título y deje al usuario sin saber en qué página está), o que el texto dentro del título provenga de datos del usuario.

## Priority: —
Derived mechanically from Severity per the tracker convention's R8 — no
independent rationale. Sin tracker ni binding, no hay valor que nombrar; el rung es el último (`Minor`).

## Origin: Code
El síntoma es un fragmento del cuerpo de la página puesto dentro del bloque equivocado de la plantilla: el requisito (RF-04, agregar una planta sin especie) y el diseño de la página son correctos, y el enlace también existe donde debe.
**Overturned by:** que el diseño de la historia que lo introdujo pidiera ese enlace en el encabezado o en el título, lo que lo convertiría en un defecto de `Design`.
