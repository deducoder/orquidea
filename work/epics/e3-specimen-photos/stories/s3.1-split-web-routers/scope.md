# Story s3.1: Split web routers — Scope

## User story

As a desarrollador de la aplicación,
I want que `orquidea/web/app.py` solo construya la aplicación y que las rutas vivan en un router por área,
so that las rutas de fotos de esta épica (y las de riegos y floraciones de la siguiente) se añadan sin engordar un solo archivo.

## Acceptance criteria

```gherkin
@stated
Given la aplicación de antes de dividir y la de después
When se listan sus rutas (método y ruta)
Then son exactamente las mismas, y la suite de e1 y e2 pasa sin cambiar ninguna aserción

@deduced
Given una petición sin sesión a cualquier ruta que no es pública
When se envía
Then sigue redirigiendo al acceso (o 401 con htmx), y toda ruta nueva de un router nace protegida por la dependencia global

@deduced
Given la ruta `/coleccion/nuevo` y la ruta `/coleccion/{id}/editar`
When se piden
Then siguen resolviendo a sus vistas y el orden de registro entre `nuevo` y una ruta futura `/coleccion/{id}` está fijado por una prueba

@deduced
Given `uvicorn orquidea.web.app:app`
When arranca
Then sigue funcionando con la misma orden (el Dockerfile y el README no cambian)

@deduced
Given un catálogo inválido
When se importa `orquidea.web.app`
Then el arranque se detiene con `CatalogoInvalido`, como hasta ahora
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `[(m, r.path) for r in app.routes]` antes y después | comparar | conjuntos iguales |
| `from orquidea.web.sesion import RUTAS_PUBLICAS` | importar | `{"/acceso", "/salud"}` |

## In scope

- Módulo `sesion` (dependencia de sesión y CSRF, cookie, conexión) y módulo de plantillas compartido.
- Un `APIRouter` por área: acceso, catálogo (con el inicio) y colección.
- `app.py` reducido a construir la aplicación: ciclo de vida, middleware de cabeceras, manejador de errores y montaje.
- Actualizar las pruebas que apuntan a nombres movidos (destino de un `monkeypatch`, import de `RUTAS_PUBLICAS`).
- Retirar del parking lot la entrada de `app.py` (`park`).

## Out of scope

- Cambiar comportamiento, rutas, plantillas o cabeceras — es refactor puro.
- Las rutas de fotos — s3.4.
- Mover `/salud` fuera de `app.py`.

## Done when

- [stated] `app.py` deja de reunir rutas, sesión y cabeceras; las rutas quedan en routers por área (brief y parking lot).
- [deduced] El conjunto de rutas es idéntico y toda la suite pasa con solo cambios de destino de `monkeypatch` e imports.
- [deduced] `./scripts/check` está en verde.

## Notes

Diseño de la épica: `design.md`, componentes `orquidea.web.*`. El único `@stated` es el que declara el brief ("dividir `orquidea/web/app.py` en routers antes de añadir rutas").
