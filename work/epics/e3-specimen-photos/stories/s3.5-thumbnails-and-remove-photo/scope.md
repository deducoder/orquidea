# Story s3.5: Thumbnails and remove photo — Scope

## User story

As a coleccionista,
I want ver la miniatura de cada ejemplar en "Mi colección" y poder quitar la foto de uno,
so that reconozca mis plantas a simple vista en la lista y corrija una foto equivocada.

## Acceptance criteria

```gherkin
@stated
Given ejemplares con y sin foto
When abro "Mi colección"
Then cada ejemplar con foto muestra su miniatura, que enlaza a su ficha

@deduced
Given un ejemplar sin foto
When abro "Mi colección"
Then aparece igual que antes, sin imagen rota

@deduced
Given un ejemplar con foto
When quito su foto desde la ficha
Then la ficha vuelve a mostrar "Aún no tiene foto.", el ejemplar sigue en la colección y los dos archivos desaparecen

@deduced
Given un ejemplar sin foto
When se envía quitar la foto
Then no falla y la ficha sigue igual

@deduced
Given una petición de quitar la foto sin CSRF, sin sesión, o de un ejemplar inexistente
When se envía
Then responde 403, redirige al acceso o responde 404, y no cambia nada
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| ejemplar 1 con foto | `GET /coleccion` | `<a href="/coleccion/1"><img src="/coleccion/1/foto/miniatura" alt="…" loading="lazy"></a>` |
| ejemplar 2 sin foto | `GET /coleccion` | sin `<img>` para el 2 |
| `POST /coleccion/1/foto/quitar` con `csrf` | quitar la foto | 303 a `/coleccion/1`; archivos borrados; `foto` nula |

## In scope

- Miniatura enlazada a la ficha en cada fila de "Mi colección" con foto.
- Quitar la foto: botón en la ficha y ruta `POST /coleccion/{id}/foto/quitar`.

## Out of scope

- Página de confirmación para quitar la foto — a diferencia de quitar el ejemplar, se puede volver a subir otra; se pide confirmación solo para la baja del ejemplar completo — **not now**.
- Medir el peso de la lista con miniaturas reales — s3.6.
- Caché de las miniaturas — fuera de alcance de la épica.

## Done when

- [stated] La miniatura del ejemplar se ve en "Mi colección" (RF-05: "en miniatura en las listas").
- [deduced] Quitar la foto borra los archivos y deja el ejemplar intacto.
- [deduced] Sin CSRF, sin sesión o con ejemplar inexistente, quitar la foto no cambia nada.
- [deduced] `./scripts/check` está en verde.

## Notes

Diseño de la épica: `design.md`, componentes `orquidea/web/templates/coleccion.html`, `rutas/coleccion.py`. El `@stated` es RF-05 del PRD. Riesgo para s3.6: una miniatura de 320 px de una foto real pesa decenas de KB y `must-perf-001` cuenta las miniaturas; s3.6 lo mide y, si pasa el presupuesto, baja el tamaño de la miniatura.
