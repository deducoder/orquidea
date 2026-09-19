# Epic e1: Species catalog — Brief

## Hypothesis

Para coleccionistas de orquídeas de Chiapas que hoy no tienen dónde consultar
qué especies nativas existen ni cómo cuidarlas,
el catálogo de Orquídea es una referencia curada
que reúne cada especie con sus cuidados técnicos y su fuente.
A diferencia de la información dispersa en libros y sitios sueltos, cada dato
cita de dónde viene.

## Success metrics

- **Leading:** el catálogo se carga desde JSON validado y una especie de ejemplo se ve en su ficha, desplegada en el VPS.
- **Lagging:** la primera carga es usable en ≤ 5 s con "Slow 3G" y transfiere ≤ 200 KB (`must-perf-001`), medida sobre el catálogo real.

## Appetite

M — 5-7 historias. Incluye el despliegue temprano al VPS y la entrada del
parking lot "Binding de seguridad sin definir", que se unió a la versión 0.1.0.

## Scope boundaries

What the design may not do. **What it will build is not decided here** — the
in-scope list belongs to `scope.md`, written by `epic-design` after the
decomposition.

### No-gos
- Editar el catálogo desde la interfaz — se mantiene desde código (RF-01).
- Especies fuera de Chiapas — el catálogo cubre solo especies nativas del estado (visión).
- Consumir fuentes de datos externas en tiempo de ejecución — no hay sistemas externos (system-context).

### Rabbit holes
- Capturar ahora el catálogo completo (del orden de 700 especies): esta épica entrega el mecanismo y un conjunto semilla.
- Búsqueda difusa sofisticada: basta con ignorar mayúsculas y acentos (RF-02).
