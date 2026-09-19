---
type: adr
id: ADR-004
title: "Autenticación de un solo usuario: contraseña con scrypt en el entorno y sesión guardada en el servidor"
status: accepted
date: 2026-09-19
epic: e2
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-004: Autenticación de un solo usuario: contraseña con scrypt en el entorno y sesión guardada en el servidor

## Status

Accepted

## Context

RF-08 pide un único usuario con contraseña, sin registro ni varias cuentas; el system-design exige que toda ruta, salvo el inicio de sesión, requiera sesión. `should-security-002` fija la línea base OWASP ASVS nivel 2 porque la aplicación tiene inicio de sesión. ADR-001 (punto 4) difiere a esta épica la elección de las piezas de sesión, CSRF y validación, y avisa que un error aquí es un riesgo de seguridad. El system-context excluye sistemas externos (sin correo): no hay recuperación de contraseña (no-go del brief).

Fuerzas:

- **Un solo usuario**: la contraseña no necesita tabla de usuarios; es configuración del despliegue.
- **Sin dependencias innecesarias**: cada dependencia de seguridad es superficie a mantener.
- **ASVS L2**: contraseñas con hash lento y sal, tokens de sesión aleatorios y de suficiente entropía, cookie `HttpOnly`/`Secure`/`SameSite`, cierre de sesión que invalida la sesión, protección contra CSRF, límite a los intentos de acceso.
- **El humano pone la contraseña en el despliegue**: el hash y el secreto llegan por el entorno del VPS (Dokploy); no pueden estar en el repositorio.

Opciones para el hash de la contraseña:

- **(A) `hashlib.scrypt` de la biblioteca estándar**, con sal aleatoria y parámetros explícitos. Sin dependencias; aceptado por ASVS como función de derivación de claves.
- **(B) argon2-cffi.** El recomendado actual de OWASP; añade una dependencia con extensión nativa.
- **(C) bcrypt.** Dependencia con extensión nativa y límite de 72 bytes.

Opciones para la sesión:

- **(D) Sesión guardada en el servidor (tabla `sesiones` en SQLite, ADR-003) con un identificador aleatorio en la cookie.** Se puede invalidar al cerrar sesión; la cookie no lleva datos.
- **(E) Cookie firmada sin estado (`SessionMiddleware` de Starlette).** Necesita `itsdangerous`; no se puede invalidar en el servidor al cerrar sesión, solo esperar a que caduque.

## Decision

1. **Contraseña:** opción (A). El hash (scrypt, sal aleatoria, parámetros dentro de la cadena guardada) llega por la variable de entorno `ORQUIDEA_PASSWORD_HASH`; la comparación es en tiempo constante. Una orden de línea de comandos del propio paquete genera ese valor a partir de una contraseña, para que el humano lo pegue en el despliegue. Sin la variable, la aplicación no permite ningún inicio de sesión (falla cerrado).
2. **Sesión:** opción (D). Un identificador de `secrets.token_urlsafe` en la cookie; en la tabla, su hash SHA-256 (un volcado de la base no entrega sesiones válidas), la fecha de creación y de caducidad, y un token CSRF de la sesión. Cookie `HttpOnly`, `SameSite=Lax` y `Secure` cuando el despliegue es HTTPS (configurable para desarrollo local). Cerrar sesión borra la fila. La sesión caduca por inactividad y por antigüedad máxima.
3. **CSRF:** todo `POST` exige el token CSRF de la sesión en el formulario (o en el encabezado de htmx); sin él, 403. `SameSite=Lax` es una segunda barrera, no la única.
4. **Límite de intentos:** los fallos consecutivos de inicio de sesión retrasan o bloquean temporalmente nuevos intentos (contador en memoria del proceso; basta con un proceso único, ADR-001).
5. **Protección de rutas:** una dependencia de FastAPI aplicada al conjunto de rutas; están exentos solo el formulario de acceso, `/salud` (lo usa el healthcheck de Docker) y `/static`. Un sin sesión en una ruta HTML redirige al formulario.
6. **Cabeceras de seguridad** (`X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`/CSP acotada) en todas las respuestas.
7. Diferido: recuperación o cambio de contraseña desde la interfaz — es un no-go del brief; cambiarla es cambiar la variable de entorno.

## Consequences

**Positive:**
- Sin dependencias nuevas.
- Cerrar sesión invalida de verdad; un volcado de la base no da acceso.
- No hay tabla de usuarios ni registro que proteger: cumple RF-08 con la menor superficie.

**Negative / costs:**
- Autenticación, CSRF y límite de intentos son código propio que probar con cuidado; un error es un riesgo de seguridad (lo compensa `security-review` en cada historia).
- Cambiar la contraseña exige acceso al entorno del VPS y reiniciar; asumido porque no hay recuperación por correo (no-go).
- El contador de intentos en memoria se reinicia con el proceso y no sirve con varios procesos; se acepta con un proceso único y se revisará si eso cambia.
- Cada petición autenticada consulta la base para validar la sesión.

## Alternatives considered

- **(B) argon2-cffi:** mejor función que scrypt, pero una dependencia nativa más para un solo usuario; scrypt cumple ASVS. Reevaluar si un `security-review` lo pide.
- **(C) bcrypt:** dependencia nativa y límite de 72 bytes, sin ventaja sobre scrypt de la biblioteca estándar.
- **(E) Cookie firmada sin estado:** no se puede invalidar en el servidor al cerrar sesión y añade `itsdangerous`; la tabla de sesiones ya existe por ADR-003.
