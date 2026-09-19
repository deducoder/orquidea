# Story s1.1: Web skeleton — Scope

## User story

As a coleccionista de orquídeas,
I want abrir la aplicación en el navegador y ver una página de inicio,
so that exista la base web sobre la que se construye el catálogo.

## Acceptance criteria

```gherkin
@stated
Given la aplicación FastAPI arrancada
When pido GET /
Then recibo 200 con HTML renderizado en el servidor desde la plantilla base

@stated
Given la página de inicio
When leo su HTML
Then carga htmx y la plantilla base define el bloque que las siguientes historias extienden

@deduced
Given la página de inicio
When leo su HTML
Then no carga ningún recurso de un dominio externo (system-context: no hay sistemas externos)

@deduced
Given un checkout limpio
When corro ./scripts/check
Then sale en verde con la prueba de la página de inicio incluida
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| aplicación en pruebas (TestClient) | GET / | 200, `Content-Type: text/html`, contiene el título "Orquídea" y el script de htmx |

## In scope

- Paquete `src/orquidea/web/` con la aplicación FastAPI, la plantilla base Jinja y la ruta de inicio.
- htmx como archivo servido por la propia aplicación.
- Dependencias de ejecución declaradas en `pyproject.toml` y `uv.lock`.
- Prueba de la página de inicio y gates en verde.

## Out of scope

- Catálogo, ficha y búsqueda — s1.2, s1.3, s1.4.
- Despliegue — s1.5.
- Sesión e inicio de sesión — e2.

## Done when

- [stated] GET / responde 200 con HTML desde la plantilla base que carga htmx.
- [deduced] La página no depende de recursos externos.
- [deduced] `./scripts/check` en verde.

## Notes

Fila s1.1 de `work/epics/e1-species-catalog/scope.md`; sección "Target components" de `design.md`. Stack fijado por ADR-001.
