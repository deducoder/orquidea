# Story s3.6: Deployment and measurement — Scope

## User story

As a coleccionista que despliega su aplicación en su VPS,
I want que las fotos vivan dentro del volumen de datos, que la guía diga cómo respaldarlas y qué límites tienen, y poder medir cuánto pesa "Mi colección" con miniaturas,
so that mis fotos sobrevivan a un redespliegue y la lista siga siendo ligera.

## Acceptance criteria

```gherkin
@stated
Given la colección con miniaturas
When se mide la primera carga de "Mi colección" (HTML, JavaScript y miniaturas, sin las fotos a tamaño completo)
Then transfiere ≤ 200 KB

@deduced
Given la imagen de Docker
When arranca sin `ORQUIDEA_FOTOS`
Then el directorio de fotos queda dentro del volumen `/data`

@deduced
Given la guía de despliegue
When se lee
Then dice que el volumen guarda la base y las fotos y que se respaldan juntas, el tamaño máximo de foto, el ancho al que se reducen, el límite de cuerpo que un proxy delante debe permitir y que las fotos se guardan sin ubicación

@deduced
Given una constante de límite que cambia (foto máxima, ancho, cuerpo, duración de sesión, intentos)
When se corre el gate
Then una prueba falla si la guía ya no dice el mismo número

@deduced
Given fotos de ejemplo con detalle (no de un solo color)
When se mide la lista
Then el script imprime el desglose (HTML, JavaScript, miniaturas, total) y sale con código distinto de cero si pasa de 200 KB

@deduced
Given una miniatura de una foto con detalle
When se genera
Then pesa menos que con el tamaño anterior de 320 px y se ve nítida en la lista a 96 px (2x)
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `uv run python scripts/medir-primera-carga.py` | medir con fotos de ejemplo | tabla con HTML (gzip), JavaScript (gzip), miniaturas y total; código 0 si ≤ 200 KB |
| `uv run python scripts/medir-primera-carga.py mis-fotos/*.jpg` | medir con fotos reales | lo mismo, una miniatura por foto |
| README con "10 MB" y el código con `TAMANO_MAXIMO = 10 MiB` | `./scripts/check` | verde; si una cambia sin la otra, rojo |

## In scope

- La imagen guarda las fotos dentro de `/data` (prueba de deriva con el `Dockerfile`) y la guía lo documenta con respaldo, límites y propietario del volumen.
- Pruebas de deriva guía-constantes para los límites de fotos y para las cifras de la guía de acceso.
- Script de medición de la primera carga y una prueba de presupuesto en el gate con fotos de ejemplo con detalle.
- Miniatura más pequeña, medida y justificada, si la medición lo pide (ADR nuevo que sustituye a ADR-005).

## Out of scope

- Construir la imagen y desplegar en el VPS — depende del humano (sin Docker en esta máquina) — **not now**, ver Risks de la épica.
- La medición con "Slow 3G" en el navegador con las fotos reales — solo la puede hacer el humano — stop previsible en `epic-review` (P4).
- Caché de imágenes en el navegador — fuera de alcance de la épica.

## Done when

- [stated] La lista de "Mi colección" con miniaturas transfiere ≤ 200 KB en la primera carga, sin contar las fotos a tamaño completo, medida por script con fotos de ejemplo con detalle (métrica rezagada del brief, `must-perf-001`); la parte con "Slow 3G" y fotos reales queda para el humano.
- [deduced] Las fotos viven dentro del volumen de la imagen y la guía es exacta en cifras y respaldo.
- [deduced] `./scripts/check` está en verde.

## Notes

Diseño de la épica: `design.md`, componentes `scripts/`, `Dockerfile`, `README.md`. El `@stated` es la métrica rezagada del brief. Esta historia contesta el riesgo que s3.5 dejó abierto: el peso de las miniaturas. La medición con un proxy de foto (ruido fractal) dio ~15 KB por miniatura de 320 px y ~5 KB de 192 px; la lista las muestra a 96 px.
