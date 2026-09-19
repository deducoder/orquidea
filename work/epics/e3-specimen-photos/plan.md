# Epic e3: Specimen photos — Plan

## Sequence

| Order | Story | Strategy | Priority | Component | Depends on | Enables |
|:-----:|-------|----------|----------|-----------|------------|---------|
| 1 | s3.2 | risk-first | — | — | — | s3.3: el procesamiento que garantiza ancho ≤ 1600 px y cero metadatos; la pieza de mayor riesgo de seguridad y la única dependencia nueva (Pillow) |
| 2 | s3.1 | dependency | — | — | — | s3.4: `app.py` dividido en routers antes de que se añada la primera ruta de la épica (brief) |
| 3 | s3.3 | skeleton | — | — | s3.2 (hard) | s3.4: migración, directorio de fotos y borrado coherente; prueba que procesamiento y disco encajan sin HTTP |
| 4 | s3.4 | skeleton | — | — | s3.1 (hard), s3.3 (hard) | s3.5, s3.6: el recorrido de la métrica líder de punta a punta (subir una foto con GPS, verla en la ficha, sin metadatos) |
| 5 | s3.5 | quick-win | — | — | s3.4 (hard) | miniaturas en "Mi colección" y quitar foto; cierra RF-05 y la métrica rezagada |
| 6 | s3.6 | dependency | — | — | s3.4 (hard) | que las fotos sobrevivan a un redespliegue y la medición de `must-perf-001`; al final porque su parte efectiva es del humano |

`Priority` y `Component` quedan en `—`: el proyecto no tiene tracker ni binding que nombre los valores.

**Rationale:** el riesgo mayor es que una foto llegue al disco con metadatos o sin reducir (`must-security-001`, `must-perf-002`) y que la entrada no confiable agote el proceso; por eso s3.2, una función pura sin HTTP, va primero y con las pruebas de GPS, XMP, orientación y límites. s3.1 es refactor puro que el brief exige antes de añadir rutas; no bloquea a s3.2 ni a s3.3, que no tocan `web/`, así que s3.1 va segunda y deja el terreno listo para s3.4. s3.3 une procesamiento y disco con la migración. s3.4 es el esqueleto funcional: cierra la métrica líder de punta a punta. s3.5 es una extensión pequeña sobre la misma ficha y la lista. s3.6 no bloquea código; va al final porque configurar el VPS y medir con "Slow 3G" son del humano.

## Milestones

- [ ] **Walking skeleton** — s3.2, s3.1, s3.3, s3.4 — se sube una foto con GPS en el EXIF a un ejemplar, la ficha la muestra y el archivo guardado mide ≤ 1600 px y no tiene metadatos; sin sesión no se entrega; `./scripts/check` en verde
- [ ] **Core MVP** — s3.1 a s3.5 — además, miniaturas en "Mi colección" y quitar la foto; RF-05 completo
- [ ] **Feature complete** — s3.1 a s3.6 — configuración de despliegue con las fotos en el volumen y script de medición del peso
- [ ] **Epic complete** — done criteria met (el criterio rezagado del brief y `must-perf-001` con "Slow 3G" son del humano: stop previsible en `epic-review`)

No hay checkpoint E2E aparte: la épica es un solo proceso con SQLite y disco; el recorrido completo lo hacen la prueba de extremo a extremo de s3.4 y la manual de `story-implement`.

## Parallel streams

None. s3.1 (`orquidea.web`) y s3.2 (`orquidea.datos.fotos`, `pyproject.toml`) tocan áreas distintas y podrían correr juntas, pero el proyecto no delega sin que el humano lo pida y no hay razón de ritmo para hacerlo.

## Delegation

| Story | Block | Mold | Mode |
|-------|-------|------|------|
| s3.1 | — | — | — |
| s3.2 | — | — | — |
| s3.3 | — | — | — |
| s3.4 | — | — | — |
| s3.5 | — | — | — |
| s3.6 | — | — | — |

## Progress

| Story | Status | Est. | Actual |
|-------|:------:|:----:|:------:|
| s3.1 | done | S | S |
| s3.2 | done | M | M |
| s3.3 | done | M | M |
| s3.4 | done | M | M |
| s3.5 | done | S | S |
| s3.6 | done | S | S |

## Sequencing risks

- Una subida maliciosa o defectuosa agota memoria o CPU, o un contenedor de metadatos sobrevive → s3.2 primero, con pruebas adversas; `security-review` en cada historia y ASVS L2 (subida de archivos) recorrido en el `design.md` de s3.2, s3.3 y s3.4.
- Dividir `app.py` cambia el orden de rutas (`/coleccion/nuevo` frente a `/coleccion/{id}`) → s3.1 se apoya en la suite existente sin editar aserciones, y s3.4 añade una prueba explícita del orden.
- La configuración del VPS (volumen, propietario, límite del proxy) y las mediciones con navegador son del humano → previstas como stop P5/P4; s3.6 va al final para no frenar el código.
- Pillow es una dependencia con extensión nativa: si `uv` no la instala o el wheel de la imagen falla, es P3/P5 en s3.2.
