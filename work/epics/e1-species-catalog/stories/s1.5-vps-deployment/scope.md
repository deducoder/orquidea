# Story s1.5: VPS deployment — Scope

## User story

As a coleccionista de orquídeas de Chiapas,
I want que la aplicación corra en el VPS y pueda abrirla desde cualquier lugar,
so that consulte el catálogo sin depender de la computadora del equipo.

## Acceptance criteria

```gherkin
@stated
Given el repositorio en GitHub
When Dokploy construye la aplicación con el Dockerfile
Then arranca un solo proceso que sirve la aplicación en el puerto 8000

@deduced
Given la aplicación en marcha
When Dokploy consulta /salud
Then recibe 200 sin depender del catálogo ni de una sesión

@deduced
Given una instalación limpia del paquete (sin el árbol de código)
When arranca la aplicación
Then las plantillas, el htmx y las 100 fichas están disponibles
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| aplicación en marcha | GET /salud | 200, `{"estado": "ok"}` |
| instalación limpia desde el wheel | GET /especies | 200 con 100 enlaces |

## In scope

- Endpoint `/salud` para el healthcheck.
- `uvicorn` como dependencia de ejecución.
- `Dockerfile` y `.dockerignore` para Dokploy sobre Debian 13.
- Guía de despliegue en Dokploy en el README.
- Verificar que el paquete incluye plantillas, estáticos y datos.

## Out of scope

- **La ejecución del despliegue en el VPS:** necesita el push a GitHub, que en esta épica lo hace `epic-close`, y el acceso del humano a su Dokploy; el humano la ejecuta con la guía y `epic-review` deja constancia de que queda pendiente — **not now** (depende del cierre de la épica).
- Autenticación y HTTPS propio: HTTPS lo termina Dokploy (Traefik); la sesión es de e2.
- Construir la imagen aquí: la máquina de desarrollo no tiene un Docker utilizable, así que el Dockerfile no se ejecutó.

## Done when

- [stated] El repositorio queda listo para que Dokploy lo construya y sirva la aplicación (Dockerfile y guía).
- [deduced] `/salud` responde 200; el paquete instalado desde el wheel sirve el catálogo real.
- [deduced] `./scripts/check` en verde.

## Notes

Respuesta del humano al stop P5: "Tengo un VPS Dokploy debian 13". Fila s1.5 de `work/epics/e1-species-catalog/scope.md`. El criterio `[stated]` de la épica (ver la ficha de una especie desplegada en el VPS) no es de esta historia: necesita el push y el acceso del humano, y se verifica con él en `epic-review`.
