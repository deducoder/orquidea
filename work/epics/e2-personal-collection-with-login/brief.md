# Epic e2: Personal collection with login — Brief

## Hypothesis

Para el coleccionista que hoy lleva su colección en notas u hojas de cálculo,
la colección de Orquídea es un registro personal protegido
que liga cada ejemplar que posee a su especie, con sus cuidados a un clic.
A diferencia de una hoja de cálculo, cada ejemplar hereda la ficha técnica de
su especie y admite plantas fuera del catálogo.

## Success metrics

- **Leading:** tras iniciar sesión, agregar un ejemplar del catálogo y verlo en "mi colección".
- **Lagging:** el usuario registra toda su colección real, incluidas plantas fuera del catálogo, sin otra herramienta.

## Appetite

M — 5-7 historias.

## Scope boundaries

What the design may not do. **What it will build is not decided here** — the
in-scope list belongs to `scope.md`, written by `epic-design` after the
decomposition.

### No-gos
- Registro de usuarios o varias cuentas — un solo usuario (RF-08).
- Recuperación de contraseña por correo — no hay sistemas externos (system-context).
- Fotos, riegos y floraciones — pertenecen a la versión 0.2.

### Rabbit holes
- Un sistema de autenticación genérico: es un solo usuario.
- Sincronización sin conexión en el navegador.
