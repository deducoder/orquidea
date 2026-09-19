---
type: adr
id: ADR-001
title: "Python con FastAPI, htmx y SQLite, gestionado con uv"
status: accepted
date: 2026-09-19
epic: —
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-001: Python con FastAPI, htmx y SQLite, gestionado con uv

## Status

Accepted

## Context

Orquídea es una aplicación web de un solo usuario que corre en un VPS propio.
Las fuerzas que acotan el stack:

- **Rendimiento en red de baja calidad** (`must-perf-001`): primera carga usable
  en ≤ 5 s con "Slow 3G" y ≤ 200 KB transferidos. Esto favorece HTML renderizado
  en el servidor con muy poco JavaScript; una SPA pesada lo compromete.
- **Un solo usuario con contraseña** (RF-08) y **almacenamiento local simple**:
  basta un proceso único con una base de datos embebida; no se justifica
  infraestructura adicional.
- **TDD y tipado estricto** (`must-test-001`, `must-quality-001..003`): el
  lenguaje debe tener pruebas, linter, formateador y verificación de tipos
  maduros.
- **Catálogo en JSON validado contra esquema** (RF-01).

Options:

- **(A) Python + FastAPI + Jinja + htmx + SQLite** — casi sin JS en el cliente;
  tipado nativo en FastAPI; herramientas maduras (ruff, mypy, pytest). El
  inicio de sesión, las sesiones, CSRF, los formularios y las migraciones se
  arman con piezas propias.
- **(B) Python + Django + htmx + SQLite** — trae de serie autenticación,
  sesiones, CSRF, formularios, ORM y migraciones; menos código propio para
  RF-08. Más marco del que la aplicación usa, y el tipado estricto depende de
  stubs de terceros.
- **(C) TypeScript + Node (Hono/Express) + htmx** — mismas propiedades en el
  cliente que (A); tiene sentido si el equipo trabaja en TypeScript.
- **(D) SvelteKit** — SSR con bundles pequeños, cómodo si la interfaz se vuelve
  rica; exige vigilar el tamaño del bundle frente a `must-perf-001`.

## Decision

**Option (A):**

1. Backend en Python ≥ 3.13 con FastAPI; vistas renderizadas en el servidor con
   Jinja; htmx para interacciones parciales.
2. Persistencia en SQLite; fotos en el disco del VPS.
3. Entorno y dependencias con uv (`pyproject.toml` + `uv.lock`); los gates
   corren con `uv run` (ruff, ruff format, mypy strict, pytest).
4. Las piezas que FastAPI no trae —inicio de sesión, sesión, CSRF, validación
   de formularios, migraciones— se eligen en la historia que las necesite por
   primera vez, con su propio ADR si hay más de una opción razonable.

## Consequences

**Positive:**
- El cliente recibe HTML y un script pequeño: el presupuesto de
  `must-perf-001` es alcanzable sin esfuerzo especial.
- Tipado nativo en rutas y modelos, coherente con `must-quality-003`.
- Despliegue de un solo proceso y un archivo de base de datos en el VPS.

**Negative / costs:**
- La autenticación, la protección CSRF y las migraciones no vienen resueltas:
  son código o dependencias adicionales que habrá que elegir y probar, y un
  error ahí es un riesgo de seguridad (`should-security-002`, ASVS L2). Se
  acepta a cambio de un marco más ligero y de tipado nativo.
- SQLite limita la escritura concurrente; aceptable con un único usuario
  (RF-08), a revisar si algún día hay varias cuentas.

## Alternatives considered

- **(B) Django:** resolvía de serie RF-08 y CSRF, pero se prefirió un marco más
  ligero con tipado nativo; el costo quedó registrado arriba.
- **(C) TypeScript + Node:** sin ventaja sobre (A) para este equipo; no hay
  razón para un segundo lenguaje.
- **(D) SvelteKit:** su fortaleza es la interfaz rica, que la aplicación no
  necesita, a costa de vigilar el bundle frente a `must-perf-001`.
