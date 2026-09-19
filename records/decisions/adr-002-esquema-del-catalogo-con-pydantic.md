---
type: adr
id: ADR-002
title: "El esquema del catálogo son modelos pydantic; un archivo por especie"
status: accepted
date: 2026-09-19
epic: e1
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-002: El esquema del catálogo son modelos pydantic; un archivo por especie

## Status

Accepted

## Context

RF-01 exige que el catálogo viva en JSON versionado con un esquema, que un archivo inválido se rechace señalando archivo y campo, y que nunca se cargue a medias; `must-data-001` exige al menos una fuente por especie. e2 (colección) referenciará estas especies, así que la forma de la especie es un contrato del que otras historias dependen. ADR-001 (punto 4) difiere la elección de la pieza de validación a la primera historia que la necesita.

Opciones:

- **(A) Modelos pydantic como esquema.** Pydantic ya viene con FastAPI (dependencia existente); valida tipos, obligatoriedad y longitudes mínimas, y sus errores traen la ruta del campo (`loc`). El esquema es código tipado, coherente con `must-quality-003` (mypy strict).
- **(B) Archivo JSON Schema + biblioteca `jsonschema`.** El esquema es un artefacto de datos independiente del código, editable sin Python. Añade una dependencia, y el resultado validado es un `dict` sin tipos: hace falta un segundo paso para obtener objetos tipados, con dos definiciones de la especie que mantener sincronizadas.
- **(C) Validador escrito a mano.** Sin dependencias, pero reimplementa tipos, obligatoriedad y rutas de error: más código propio que probar para lo mismo.

## Decision

**Opción (A):**

1. La especie se define como modelos pydantic (`Especie`, `Cuidados`, `Cuidado`) en `orquidea.catalogo`, con `extra="forbid"`: un campo desconocido o mal escrito se rechaza.
2. Un archivo JSON por especie en `src/orquidea/datos/catalogo/`, dentro del paquete para que viaje con él.
3. La carga (`orquidea.datos`) valida todos los archivos y reúne los errores como `archivo: campo: mensaje`; si hay alguno, falla sin devolver ninguna especie.
4. `pydantic` se declara como dependencia directa del proyecto.
5. Diferido: exportar el esquema como archivo JSON Schema (`Especie.model_json_schema()`) si algún día un editor o una herramienta externa lo necesita; hoy nadie lo consume.

## Consequences

**Positive:**
- Una sola definición de la especie, tipada, que valida y a la vez es el tipo del dominio.
- Sin dependencias nuevas de instalación (pydantic ya llega con FastAPI).

**Negative / costs:**
- El esquema es código Python: quien mantiene el catálogo no lo lee como archivo aparte. Se acepta porque el catálogo lo mantiene el equipo desde código (RF-01).
- Los mensajes de pydantic están en inglés ("Field required"); el error añade archivo y campo, pero el texto del motivo no se traduce.
- Cambiar la forma de la especie es cambiar código y volver a validar todos los JSON.

## Alternatives considered

- **(B) JSON Schema + `jsonschema`:** duplica la definición (esquema y tipos del dominio) y añade una dependencia sin un consumidor del archivo de esquema.
- **(C) Validador a mano:** más código propio que probar para lo que pydantic ya hace y ya está instalado.
