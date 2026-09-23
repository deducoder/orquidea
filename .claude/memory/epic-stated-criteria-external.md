---
name: epic-stated-criteria-external
description: Criterios [stated] que dependen de sistemas o acciones del humano deben preverse como stop en el diseño de la épica
metadata:
  type: feedback
---

Cuando un criterio `[stated]` de un brief depende de algo fuera de la sesión (un VPS del humano, un navegador con devtools, un push que la épica difiere al cierre), marcarlo en `epic-design` y `epic-plan` como un stop previsible (P4 en `epic-review`), y decirlo desde el `scope.md` de la historia que lo toca.

**Why:** en e1 el despliegue y la medición con Slow 3G solo se descubrieron como no cumplibles en `epic-review`, con las seis historias ya hechas.
**How to apply:** en el diseño de una épica, listar qué criterios `[stated]` necesitan al humano y preguntar por adelantado, junto con los datos que falten.

En e5 (2026-09-23) el tiempo con "Slow 3G" se difirió por cuarta épica (e1, e2, e3, e5), aun con el servidor listo y 25 ejemplares con foto. Preverlo como stop no basta. La medición solo significa algo contra el despliegue real, así que queda ligada al primer despliegue en Dokploy (entrada del parking lot) y no se vuelve a pedir en cada `epic-review`.
