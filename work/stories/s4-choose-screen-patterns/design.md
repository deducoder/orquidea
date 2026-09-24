# Story s4: Choose screen patterns — Design

Registro: ADR-019, en `proposed` desde `e97d219`, con su rojo y las tres opciones medidas en `29fb5ba`, antes de producir.

## 1 · What & why

**Problema:** las pantallas de Orquídea tienen hoy la forma que les dio cada plantilla. Ninguna se eligió contra una tabla de formas.

**Valor:** una forma por pantalla, elegida con la regla de una fuente y citada con la fecha de lectura. Es lo que `page.py` necesita, junto con la guía, para generar la página de cada pantalla en la composición.

## 2 · Approach

Un entregable, `governance/identity/ui/screens/screen-pattern.md`, con la plantilla de la técnica: los valores comunes de ADR-019 más la opción que el dueño elija para S3 y S4. Ningún código cambia.

### Recorrido

- **Fuente:** Android Developers, "Canonical layouts" (actualizada el 2026-09-22 y leída el 2026-09-24). m3.material.io no entregó texto. La regla de elección está citada en ADR-019.
- **Guía de ADR-018:** S3 pone la miniatura primero, y S4 la foto primero, sin los cuidados de la especie. Eso es lo que P4 compara.
- **Parking lot:** revisé las promociones y ninguna se cumple. La de las fuentes largas espera a la composición de S2.
- **Legacy sweep:** nada queda huérfano; es nuevo.

## 3 · Interface / examples

```sh
S=~/.claude/plugins/cache/gemba/gemba-design/0.24.0/skills/techniques/screens/scripts; D=governance/identity/ui/screens
python3 $S/inventory-sources.py --repo . $D/inventory.md $D/screen-set.md $D/priority-guide.md $D/screen-pattern.md
# esperado: OK (…; 9 of 9 screens with a pattern), exit 0
```

## 4 · Acceptance criteria

### Deduced criteria

- Rojo antes de producir: confirmado (`29fb5ba`).
- ADR `accepted`, mismo archivo: confirmado.
- `./scripts/check` verde: confirmado.

### Scenarios (delta over the scope)

- **MUST:** `source-read` en el frontmatter nombra la URL que se leyó, no la que nombra el catálogo, y la fecha de lectura.
- **MUST NOT:** firmar P3 o P4 por el dueño.
