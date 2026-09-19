# Story s2.7: Deployment configuration with persistence — Scope

## User story

As a coleccionista que despliega su aplicación en su VPS con Dokploy,
I want que la imagen guarde la base en un volumen persistente y que la guía diga qué variables de entorno poner y cómo generar el hash de la contraseña,
so that mi colección sobreviva a un redespliegue y solo yo pueda entrar.

## Acceptance criteria

```gherkin
@stated
Given la imagen construida desde el `Dockerfile`
When arranca
Then la base vive en un directorio de datos que es un volumen y que el usuario sin privilegios de la imagen puede escribir

@stated
Given la guía de despliegue
When la sigo
Then sé qué variables de entorno poner (`ORQUIDEA_PASSWORD_HASH`, y las opcionales), cómo generar el hash con la orden del paquete y que debo montar el volumen de datos

@stated
Given un redespliegue de la aplicación
When arranca la versión nueva sobre el mismo volumen
Then la colección sigue ahí y las migraciones nuevas se aplican solas

@deduced
Given cada variable `ORQUIDEA_*` que lee el código
When reviso el README
Then todas están documentadas (nada se lee sin decirlo)

@deduced
Given el README
When lo leo
Then ya no afirma que no hay variables de entorno ni secretos

@deduced
Given el wheel que se instala en la imagen
When lo abro
Then trae las migraciones `.sql` y las plantillas

@deduced
Given el arranque sin `ORQUIDEA_PASSWORD_HASH`
When se documenta
Then la guía dice que sin ella nadie puede entrar (falla cerrado)

@deduced
Given la guía
When habla de HTTPS
Then dice que la cookie de sesión es `Secure` y exige HTTPS (Dokploy lo termina) y que `ORQUIDEA_COOKIE_SEGURA=0` es solo para desarrollo local
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| `uv run python -m orquidea.autenticacion` | generar el hash | una línea `scrypt$65536$8$2$…` para `ORQUIDEA_PASSWORD_HASH` |
| `Dockerfile` | leer la configuración de datos | `ENV ORQUIDEA_DB=/data/orquidea.sqlite3`, `VOLUME /data`, `/data` propiedad del usuario `app` antes de `USER app` |
| wheel de la aplicación | listar contenido | `orquidea/datos/migraciones/0001-sesiones.sql`, `0002-ejemplares.sql` |

## In scope

- `Dockerfile`: directorio de datos `/data`, propietario del usuario de la imagen, `ORQUIDEA_DB` apuntando ahí, `VOLUME`.
- README: variables de entorno, volumen, generación del hash, HTTPS/cookie, actualización de la frase obsoleta y del arranque local.
- Pruebas que impiden la deriva: el `Dockerfile` declara lo que el código espera y el README documenta cada variable `ORQUIDEA_*` que el código lee.
- Verificar que el wheel trae migraciones y plantillas y que la aplicación arranca desde un entorno limpio con una base nueva.

## Out of scope

- El despliegue efectivo al VPS, configurar Dokploy, poner el hash real y montar el volumen allí — acciones del humano, que siguen pendientes desde e1 — **not now**.
- Copias de seguridad de la base — **not now** (el usuario puede respaldar el volumen con lo que ofrezca Dokploy).
- Construir la imagen con Docker: no hay daemon disponible en esta máquina (igual que en e1).

## Done when

- [stated] La imagen declara un volumen de datos escribible por su usuario y la guía dice cómo configurarlo.
- [stated] La guía nombra las variables de entorno y la orden del hash.
- [deduced] El wheel trae las migraciones y una instalación limpia arranca con una base nueva y las aplica.
- [deduced] Las pruebas fallan si el código lee una variable `ORQUIDEA_*` que el README no documenta.

## Notes

ADR-003 punto 3 (`ORQUIDEA_DB` apunta a un volumen persistente) y ADR-004 (hash y cookie por entorno). El `Dockerfile` sigue sin construirse en una máquina con Docker: es un stop previsible del humano (el primer despliegue), no de esta historia.
