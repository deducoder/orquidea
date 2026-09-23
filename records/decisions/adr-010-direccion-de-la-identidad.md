---
type: adr
id: ADR-010
title: "Dirección común de la identidad visual de Orquídea"
status: proposed
date: 2026-09-22
epic: e5
published: pendiente — se resuelve al completar el registro
---

# ADR-010: Dirección común de la identidad visual de Orquídea

## Status

Proposed.

## Context

**La pregunta:** ¿qué apuesta comparten la paleta (s5.3) y la tipografía (s5.4) de Orquídea, elegida entre un número de direcciones declarado antes de desarrollar ninguna?

ADR-009 fijó contra qué se juzga toda la identidad: el catálogo de supervivencia y tres criterios (peso ≤ 50 KB, texto normal ≥ 7:1, la foto como protagonista). Este registro no los repite; deriva de ellos los criterios de esta selección.

Lo que la dirección tiene que vestir (recorrido de s5.2): diez pantallas de consulta y registro — 100 nombres científicos con búsqueda, fichas con cuatro cuidados y su fuente citada larga, "Mi colección" con miniaturas y fechas, la ficha del ejemplar con foto, riegos y floraciones. El catálogo no tiene fotos: lo único saturado que la aplicación muestra son las plantas del usuario.

### Criterios de selección

Aprobados por el humano el 2026-09-22, antes de desarrollar ninguna dirección. S3 fue reformulado a petición del humano.

| # | Criterio | Estrato | From |
|---|-----------|---------|------|
| S1 | Deja la foto del ejemplar como lo único saturado de la pantalla: su firma vive en fondos, tinta y estructura, no en color de marca | `judgement` | commission 3 |
| S2 | Conserva su carácter con texto a ≥ 7:1 y con fuentes del sistema o una sola familia ligera: no depende de medios tonos, de texturas en imagen ni de una fuente de exhibición | `judgement` | commission 1 y 2 |
| S3 | Es una herramienta de registro y consulta pensada primero para el teléfono: toma de las redes la foto a todo el ancho en tarjetas, la navegación al alcance del pulgar y las acciones frecuentes grandes y cerca de su contenido; no toma métricas, seguidores, "me gusta" ni scroll infinito | `judgement` | esta selección (humano, 2026-09-22) |

Los patrones de las redes entran como presentación y navegación de lo que la aplicación ya hace: ningún flujo nuevo (no-go del brief de e5).

### Número de direcciones

**3**, declarado el 2026-09-22, antes de desarrollar la primera.

### Las direcciones

Desarrolladas el 2026-09-22, cada una en su mejor versión. Son apuestas verbales: ninguna fija un valor.

**(A) Cuaderno de campo.** La libreta del naturalista que sale al monte: hoja clara, tinta casi negra, renglones finos, fechas alineadas como en una bitácora. Cada ejemplar es una hoja con su foto pegada a todo el ancho y sus anotaciones debajo.
- *Para el color:* neutros cálidos de papel y una tinta; un solo acento de tinta (azul-negro o sepia oscuro) reservado para acciones y enlaces. La foto es el único color vivo.
- *Para el tipo:* una sans del sistema para la interfaz, cifras tabulares o monoespaciadas para las fechas, itálica verdadera para los nombres científicos. La estructura (renglones, márgenes, etiquetas pequeñas en versalitas) hace el trabajo que en otras direcciones hace el color.
- *En el teléfono:* tarjetas de ejemplar como hojas apiladas, navegación inferior entre Catálogo y Mi colección, el botón de registrar riego grande al pie de su historial.

**(B) Lámina de herbario.** La hoja de herbario de museo: papel crema, el ejemplar montado al centro, la etiqueta de colecta en un recuadro con sus datos (nombre, colector, fecha, localidad), una serif clásica para los binomios.
- *Para el color:* crema, sepia y tinta, con el aire de una colección histórica.
- *Para el tipo:* una serif de texto con itálica real y versalitas; es la tipografía la que dice "herbario".
- *En el teléfono:* la foto como el ejemplar montado, los datos en la etiqueta recuadrada al pie; en pantallas pequeñas la etiqueta se apila en una columna larga.

**(C) Vivero.** El vivero tropical amable: verde hoja como color de marca, esquinas redondeadas, íconos de planta, un tono cercano de app de jardinería.
- *Para el color:* un verde de marca saturado en encabezados, botones y acentos, sobre fondos blancos o verde muy claro.
- *Para el tipo:* una sans redondeada y cálida.
- *En el teléfono:* es la que más se parece a una app de redes: tarjetas grandes, barra inferior con íconos, botones píldora.

### La rejilla

Cada celda es la respuesta del agente a ese criterio para esa dirección; la elección entre las tres es del humano, en elección forzada, y se firma.

| Criterio | Estrato | (A) Cuaderno de campo | (B) Lámina de herbario | (C) Vivero |
|---|---|---|---|---|
| S1 · La foto es lo único saturado | `judgement` | sí — su firma son papel, tinta y renglones; el acento de tinta es oscuro y no compite | sí — crema y sepia no compiten con las flores | **no** — su verde de marca saturado compite con los verdes de la planta y con los amarillos y magentas de las flores en la misma tarjeta |
| S2 · Carácter con ≥ 7:1 y fuentes ligeras | `judgement` | sí — los renglones y las etiquetas son bordes y tamaños de CSS; tinta sobre papel da contraste alto por naturaleza; vive con fuentes del sistema | **no** — su carácter depende de una serif clásica con itálica y versalitas reales (una fuente web que compite por los 50 KB; las serif del sistema en Android no la dan) y de la textura y el tono de papel viejo, que empujan el texto hacia medios tonos sepia | sí — una sans del sistema y un verde oscuro para el texto alcanzan 7:1 |
| S3 · Registro y consulta, primero el teléfono | `judgement` | sí — es una bitácora por definición, y la hoja con la foto a todo el ancho es la tarjeta de las redes | **no del todo** — es registro y consulta, pero la etiqueta recuadrada es una forma de escritorio y de vitrina: en el teléfono se vuelve una columna densa y la acción frecuente (registrar) no tiene lugar natural en una lámina | parcial — primero el teléfono sí, pero su tono de app de jardinería se lee más como tienda o comunidad que como registro con fuentes citadas |

### Contraejemplos

S1, S2 y S3 son `judgement`: **no aplica: no hay oráculo** para ninguno. No existe una medida publicada de "competir con una flor", de "conservar el carácter" ni de "leerse como registro"; inventar una (saturación máxima, distancia de tono, número de fuentes) sería la teatralidad que el paso `counterexample` prohíbe. Se responden en la rejilla, por el agente, y la elección la firma el humano.

## Decision

Sin resolver. Se completa, en este mismo archivo, con la dirección elegida por el humano y `concept.md` escrito.
