---
type: adr
id: ADR-006
title: "Las fotos viven en archivos del disco junto a la base, con un nombre aleatorio guardado en el ejemplar"
status: accepted
date: 2026-09-19
epic: e3
published: no — el proyecto no tiene espacio de documentación externo; el ADR vive solo en el repositorio
---

# ADR-006: Las fotos viven en archivos del disco junto a la base, con un nombre aleatorio guardado en el ejemplar

## Status

Accepted

## Context

El system-context descarta el almacenamiento en servicios externos: las fotos van al disco del servidor. ADR-003 guarda la colección en SQLite (ruta `ORQUIDEA_DB`, en producción `/data`, un volumen) con migraciones numeradas. RF-05 admite una sola foto por ejemplar. El despliegue ya monta `/data` como volumen; una foto fuera del volumen se perdería al redesplegar.

Fuerzas:

- **Las fotos deben sobrevivir al redespliegue**, igual que la base.
- **Las fotos son bytes de entrada del usuario**: la ruta en disco no debe depender de nada que el usuario controle.
- **Coherencia**: quitar un ejemplar o reemplazar su foto no debe dejar archivos huérfanos ni filas que apunten a nada.
- **Simplicidad**: dos archivos por ejemplar (imagen y miniatura), sin más.

Opciones:

- **(A) Archivos en un directorio configurable, por defecto junto a la base** (`ORQUIDEA_FOTOS`, por defecto `fotos/` al lado del archivo de la base), con un nombre aleatorio guardado en una columna de `ejemplares`.
- **(B) BLOB en SQLite.** Una sola cosa que respaldar, pero infla la base, ralentiza el listado si se consulta sin cuidado y el servidor no puede entregar el archivo directamente.
- **(C) Nombre derivado del id del ejemplar** (`fotos/{id}.jpg`) sin columna. No necesita migración, pero un id reutilizable o adivinable acopla la ruta al ejemplar y deja fotos huérfanas sin rastro en la base.

## Decision

Opción (A).

1. Migración `0003` añade a `ejemplares` la columna `foto` (texto, nulo si no hay foto): el nombre base aleatorio (`secrets.token_urlsafe`) de la foto actual. La migración `0002` no se edita (ADR-003).
2. Los archivos se guardan como `{directorio}/{foto}.jpg` (imagen) y `{directorio}/{foto}-mini.jpg` (miniatura). El directorio sale de `ORQUIDEA_FOTOS`; sin ella, `fotos/` junto a la base, de modo que en la imagen queda dentro del volumen `/data`. Se crea al arrancar.
3. La ruta de un archivo se forma **solo** con el nombre guardado, validado contra `^[A-Za-z0-9_-]+$`; el id o el nombre de archivo de la petición nunca entran en una ruta.
4. Las fotos se sirven por una ruta propia protegida por la sesión, no como archivos estáticos: sin sesión no hay foto, con las mismas cabeceras de seguridad del resto.
5. Reemplazar la foto escribe la nueva primero, actualiza la fila y borra los archivos anteriores; quitar el ejemplar borra sus archivos. Un archivo que no se puede borrar se registra y no impide la operación (un huérfano es basura, no una fuga).

## Consequences

**Positive:**
- La base sigue pequeña y la foto sobrevive con el volumen ya existente.
- El nombre aleatorio no revela ni depende del id; sin sesión no se accede al archivo.
- Una consulta de "Mi colección" trae solo un texto por ejemplar.

**Negative / costs:**
- Hay dos almacenes que respaldar juntos (base y directorio de fotos); la guía de despliegue debe decirlo.
- Base y disco pueden divergir si el proceso muere entre un paso y otro; el orden (escribir, actualizar, borrar) deja como peor caso un archivo huérfano, nunca una fila rota.
- Servir cada foto desde Python cuesta más que un servidor de archivos estático; con un usuario es irrelevante.

## Alternatives considered

- **(B) BLOB en SQLite:** un solo respaldo, pero mezcla datos pesados con la colección, agranda el archivo de la base en cada foto y obliga a leerlo entero para servir una miniatura.
- **(C) Ruta por id:** ahorra la migración, pero vincula la ruta a un valor que la aplicación no controla del todo y no deja en la base rastro de qué archivo es el vigente.
