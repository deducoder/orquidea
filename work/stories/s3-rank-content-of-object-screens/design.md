# Story s3: Rank content of object screens — Design

Registro: ADR-018, en `proposed` desde `fda183f`, con su rojo en `9a6a68e`.

## 1 · What & why

**Problema:** las cuatro pantallas de objeto llevan su contenido en el orden en que las historias de e1 a e4 lo fueron agregando. En la ficha del ejemplar, por ejemplo, van el nombre, luego las notas, luego la foto, los riegos y las floraciones. Nadie decidió ese orden contra las tareas.

**Valor:** un orden firmado, rango por rango, atado a las tareas del inventario. Es la entrada de la composición y el lugar donde se juzga el criterio 3 de ADR-009 (la foto como protagonista).

## 2 · Approach

Un entregable, `governance/identity/ui/screens/priority-guide.md`, con la plantilla de la técnica: S1 y S2 comunes, y S3 y S4 con la opción que el dueño elija entre A, B y C de ADR-018. Ningún código cambia.

### Recorrido

- Plantillas `especies.html`, `especie.html`, `coleccion.html` y `ejemplar_ficha.html`: de ahí salen los nombres del contenido, en las palabras del producto. El orden de hoy es la opción C en S4.
- `inventory.md` y `screen-set.md` de s2: las tareas T1 a T7 y las pantallas S1 a S4.
- **Parking lot:** revisé las promociones al diseñar. La entrada "La ficha repite fuentes largas por cada cuidado" (*Promotion:* "cuando se revise el diseño de la ficha") se toca con el rango 2 de S2. La guía decide qué lleva la ficha, no cómo se imprime la cita. Entonces la decisión es del dueño: si la promoción se cumple aquí, el rango 2 dice "los cuidados, con la fuente referida por número" y el rango 5 "las fuentes de la especie, numeradas"; si no, la entrada sigue abierta para la composición.
- Legacy sweep: nada queda huérfano; es nuevo.

## 3 · Interface / examples

```sh
S=~/.claude/plugins/cache/gemba/gemba-design/0.24.0/skills/techniques/screens/scripts
D=governance/identity/ui/screens
python3 $S/inventory-sources.py --repo . $D/inventory.md $D/screen-set.md $D/priority-guide.md
# esperado: OK (… 4 of 9 screens guided, signed by Daniel Efraín Domínguez Urbina, 2026-09-24), exit 0
python3 g2.py $D/inventory.md $D/priority-guide.md    # el comando de G2, extraído de ADR-018
# esperado: serves: 7 tasks, N ranks, 7 served, exit 0
```

Rojo visto en ADR-018: firma sin fecha, tarea inexistente, hueco de rango y T6 sin servir.

## 4 · Acceptance criteria

### Deduced criteria

- Rojo de G1 y G2 antes de producir: confirmado (`9a6a68e`).
- ADR `accepted`, mismo archivo: confirmado.
- `./scripts/check` verde: confirmado.

### Scenarios (delta over the scope)

- **MUST:** las opciones que pierdan en S3 y S4 quedan en *What was tried and rejected* rango por rango, copiadas de ADR-018 sin cambios.
- **MUST NOT:** firmar la guía por el dueño; cambiar un rango de una opción después de abierto el ADR (un cambio es una opción nueva, y se dice).
