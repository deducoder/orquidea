# Story s2.7: Deployment configuration with persistence — Design

> Complexity: simple

## 1 · What & why

**Problem:** la imagen de e1 no tiene dónde guardar la base (el sistema de archivos del contenedor se pierde al redesplegar, y el usuario `app` no puede escribir en cualquier ruta) y la guía dice que no hay variables de entorno ni secretos, lo cual dejó de ser cierto.
**Value:** la colección sobrevive a un redespliegue y quien despliega sabe exactamente qué configurar; cierra el criterio "la colección persiste" de la épica sin depender de que el humano adivine.

## 2 · Approach

`/data` como directorio de datos: creado y de la propiedad de `app` antes de `USER app`, declarado `VOLUME`, con `ORQUIDEA_DB=/data/orquidea.sqlite3` por defecto en la imagen. El README documenta cada variable. Dos pruebas de deriva impiden que `Dockerfile`, código y guía se separen.

**Components affected:**

- `Dockerfile`: modify — `mkdir /data && chown app`, `ENV ORQUIDEA_DB`, `VOLUME /data`.
- `README.md`: modify — sección de despliegue con variables, volumen, hash, HTTPS; arranque local con variables; quitar la frase obsoleta.
- `tests/test_despliegue.py`: create — el `Dockerfile` y el README se ajustan a lo que lee el código.

**Legacy sweep:** la frase "No hay variables de entorno ni secretos: el catálogo viaja dentro de la imagen" del README queda falsa y se reemplaza; el `Dockerfile` de e1 se amplía sin quitar nada. Nada más se orfana.

**Gobernanza:** ADR-003 (punto 3: `ORQUIDEA_DB` a un volumen), ADR-004 (hash y cookie por entorno; `Secure` por defecto), system-context (un VPS propio, sin sistemas externos), ASVS V14.1 (configuración segura y documentada: el secreto llega por entorno y no vive en la imagen ni en el repositorio). `must-perf-001`: sin efecto.

## 3 · Interface / examples

### Usage (API / CLI)

```dockerfile
RUN uv sync --frozen --no-dev \
    && useradd --system --uid 10001 app \
    && mkdir /data && chown app /data

ENV ORQUIDEA_DB=/data/orquidea.sqlite3
VOLUME /data
USER app
```

```bash
uv run python -m orquidea.autenticacion       # imprime el valor de ORQUIDEA_PASSWORD_HASH
```

### Expected output (success + error)

```
docker run -v orquidea-datos:/data -e ORQUIDEA_PASSWORD_HASH='scrypt$…' orquidea   -> arranca, crea /data/orquidea.sqlite3 y aplica las migraciones
(sin ORQUIDEA_PASSWORD_HASH)                                                        -> la aplicación arranca, pero nadie puede iniciar sesión (401 siempre)
```

Las pruebas de deriva:

- `Dockerfile`: la variable `ORQUIDEA_DB` cae dentro del directorio declarado `VOLUME`; ese directorio se crea y se entrega a `app` antes de `USER app`.
- README: para cada `ORQUIDEA_[A-Z_]+` que aparece en `src/`, el README lo menciona; no contiene "No hay variables de entorno".

## 4 · Acceptance criteria

- **Must:** volumen de datos escribible por `app`; `ORQUIDEA_DB` por defecto dentro del volumen; guía con variables, hash, volumen y HTTPS; wheel con migraciones y plantillas.
- **Should:** pruebas de deriva; guía de arranque local con las variables.
- **Must NOT:** poner un hash o secreto en el `Dockerfile`, el repositorio o el README con un valor real; ejecutar la aplicación como root; quitar el `HEALTHCHECK`.

### Deduced criteria

- Cada variable `ORQUIDEA_*` que lee el código está en el README: confirmed — por prueba
- El README ya no dice que no hay variables de entorno: confirmed — por prueba
- El wheel trae migraciones y plantillas: confirmed — se verifica en la prueba manual con `uv build` (no es una prueba automatizada: construir el wheel es lento y depende de la red)
- Sin `ORQUIDEA_PASSWORD_HASH` nadie entra, y la guía lo dice: confirmed — el comportamiento ya está probado en s2.2; la guía lo documenta
- La guía dice que la cookie es `Secure` y exige HTTPS, y que `ORQUIDEA_COOKIE_SEGURA=0` es solo para local: confirmed

### Scenarios (delta over the scope)

```gherkin
Given el Dockerfile
When lo reviso
Then el HEALTHCHECK sigue apuntando a /salud (ruta pública)

Given el README
When lo reviso
Then el ejemplo de hash no contiene un hash real, solo el formato
```
