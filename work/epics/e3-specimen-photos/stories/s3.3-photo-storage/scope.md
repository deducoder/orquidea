# Story s3.3: Photo storage — Scope

## User story

As a coleccionista,
I want que la foto de cada ejemplar se guarde junto a mi colección y desaparezca con él,
so that mis fotos sobrevivan a un reinicio o redespliegue y no queden archivos sueltos de plantas que ya quité.

## Acceptance criteria

```gherkin
@stated
Given un ejemplar y una foto ya procesada
When se guarda como su foto
Then el ejemplar apunta a un nombre aleatorio, existen los dos archivos (imagen y miniatura) en el directorio de fotos, y el directorio por defecto queda junto a la base

@deduced
Given un ejemplar que ya tiene foto
When se guarda otra
Then el ejemplar apunta a la nueva y los dos archivos anteriores se borran

@deduced
Given un ejemplar con foto
When se quita el ejemplar
Then la fila y los dos archivos desaparecen

@deduced
Given un ejemplar con foto
When se quita solo la foto
Then el ejemplar sigue, sin foto, y los archivos desaparecen

@deduced
Given un identificador de ejemplar que no existe
When se intenta guardar una foto
Then no queda ningún archivo en el directorio

@deduced
Given un nombre de foto con `..`, `/` o vacío
When se pide su ruta
Then se rechaza y nunca se forma una ruta fuera del directorio

@deduced
Given dos subidas simultáneas para el mismo ejemplar
When ambas terminan
Then queda una sola foto vigente y exactamente sus dos archivos en el directorio

@deduced
Given una base migrada a la versión 2 con ejemplares
When se aplica la migración 0003
Then los ejemplares siguen y su foto es nula
```

## Example

| Input | Action | Expected output |
|-------|--------|-----------------|
| ejemplar 1 sin foto, `FotoProcesada` | `poner_foto(conexion, dir, 1, foto)` | `ejemplares.foto = "Xq3…"`; `dir/Xq3….jpg` y `dir/Xq3…-mini.jpg` existen |
| lo mismo con otra foto | `poner_foto(...)` | la fila apunta a la nueva; los archivos de `Xq3…` ya no existen |
| ejemplar 1 con foto | `quitar_con_foto(conexion, dir, 1)` | fila y archivos borrados |
| `"../etc/passwd"` | `ruta_de_foto(dir, nombre, False)` | `NombreDeFotoInvalido` |

## In scope

- Migración `0003` (columna `foto`), `Ejemplar.foto`, `fijar_foto` y las consultas con la columna.
- Módulo de archivos: guardar, borrar y ruta segura; poner o reemplazar, quitar solo la foto y quitar el ejemplar con sus archivos.
- Directorio por `ORQUIDEA_FOTOS`, por defecto `fotos/` junto a la base; creado y comprobado como escribible al arrancar.
- La ruta existente de quitar ejemplar usa el borrado con archivos.

## Out of scope

- Rutas HTTP para subir o servir fotos — s3.4.
- Miniaturas en la lista — s3.5.
- Documentar el volumen y el propietario del directorio — s3.6.

## Done when

- [stated] Las fotos se guardan como archivos en el disco del servidor, junto a la base y por lo tanto dentro del volumen (system-context, ADR-006).
- [deduced] Las pruebas de los criterios anteriores pasan y `./scripts/check` está en verde.
- [deduced] Ninguna ruta de archivo se forma con datos de la petición: solo con el nombre guardado y validado (ADR-006).

## Notes

Diseño de la épica: `design.md`, componentes `orquidea.datos.almacen_fotos`, migración `0003`, `orquidea.datos.ejemplares`, `orquidea.coleccion.modelo`; ADR-006. El único `@stated` es el que dice el system-context (fotos al disco del servidor).
