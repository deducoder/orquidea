# System design: Orquídea

Internal structure — the layers and the modules in each. Stack per ADR-001:
Python con FastAPI, plantillas Jinja y htmx, SQLite, gestionado con uv.

## Layers

| Layer | Modules | Description |
|-------|---------|-------------|
| Web | rutas, plantillas, autenticación | Recibe las peticiones HTTP, protege el acceso con la sesión del único usuario (RF-08) y responde HTML renderizado en el servidor; htmx para las interacciones parciales. |
| Dominio | catálogo, colección, seguimiento | Reglas del negocio: búsqueda de especies, ejemplares (con o sin especie de catálogo), riegos y floraciones. No conoce HTTP ni SQL. |
| Datos | carga del catálogo, persistencia, fotos | Valida y carga los JSON del catálogo; guarda la colección en SQLite; procesa y guarda las fotos en disco (reducción y sin EXIF). |

## Key contracts

- El catálogo se carga completo y válido o no se carga: un JSON que no cumple el esquema detiene la carga con un error explícito (RF-01).
- Un ejemplar referencia a lo sumo una especie del catálogo; sin referencia, lleva nombre propio (RF-04).
- Ninguna foto llega al disco con metadatos EXIF ni con un ancho mayor a 1600 px (must-perf-002, must-security-001).
- Toda ruta, salvo el inicio de sesión, exige la sesión del usuario (RF-08).
