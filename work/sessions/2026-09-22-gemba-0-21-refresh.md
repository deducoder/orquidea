# Session 2026-09-22 — actualización a Gemba 0.21

## Done

- `CLAUDE.md` refrescado al core 0.21.0: cambió `## Gates` y la sección de gemba-design (la interfaz derivada de la identidad como `DESIGN.md`, y el ciclo con dos entradas: criterio propuesto o extraído).
- Checks vendorizados refrescados de 0.17.0 a 0.21.0; entran las convenciones `gates` y `project`, y en `git` los checks `check-hooks-wiring` y `check-phase-order`. Gate en verde.
- Hooks del método cableados: `core.hooksPath` → `scripts/gemba/conventions/git/hooks`, marcador `scripts/gemba/hooks-adopted` commiteado; `commit-msg` rechaza mensajes fuera de convención y `pre-commit` corre `./scripts/check`.

## Decided

- Poner al día el método antes de empezar la UI — **why:** la sesión de diseño debe correr con el core y la sección de gemba-design vigentes, y la nueva sección cambia cómo entra un criterio al ciclo.
- Adoptar los hooks — **why:** el gate dejaba de ser solo disciplina; desde ahora un commit con el gate en rojo o con mensaje malformado se rechaza (cada commit tarda lo que tarda `./scripts/check`).

## Open

- Siguen del 2026-09-19: revisar la regla de popularidad y los cuidados por género del catálogo; primer `docker build` y despliegue en Dokploy con la medición en Slow 3G.

## Next

Abrir sesión nueva (para cargar el core 0.21.0) y empezar la UI con gemba-design por **color**: comprometer su criterio antes de producir nada.

## State

Branch `develop` · work item in flight: none · tree: clean · `develop` con 8 commits locales sin push (los de esta sesión y la anterior); viajan con la próxima integración. En un clon nuevo hay que volver a correr `/gemba:hooks`: `.git/config` no se versiona.
