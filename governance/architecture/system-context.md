# System context: Orquídea

The external actors and systems this project talks to, and how.

| Interface | Direction | Actor / System | Protocol | Purpose |
|-----------|-----------|----------------|----------|---------|
| Interfaz web | in | Coleccionista (único usuario), desde el navegador | HTTPS (HTML renderizado en el servidor + htmx) | Consultar el catálogo, llevar su colección, subir fotos, registrar riegos y floraciones |
| Catálogo | in | Equipo de desarrollo, desde el repositorio | Archivos JSON versionados, validados contra su esquema al cargar | Mantener las especies nativas de Chiapas y sus fuentes |

No hay sistemas externos: ni servicios de terceros, ni correo, ni fuentes de
datos remotas. La aplicación corre en un VPS propio.
