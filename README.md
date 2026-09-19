# Orquídea

Aplicación web personal para llevar una colección de orquídeas nativas de
Chiapas: catálogo de especies con sus cuidados, ejemplares propios con foto, y
registro de riegos y floraciones. El porqué está en
[`governance/vision.md`](governance/vision.md).

## Quick start

```bash
uv sync            # instala Python y las dependencias de desarrollo
./scripts/check    # verifica que todo esté en verde
```

Todavía no hay aplicación que ejecutar: el proyecto está recién gobernado y sin
historias implementadas. Requisitos: [uv](https://docs.astral.sh/uv/) instalado.

## Development

Quality gates. **Run `./scripts/check` before every commit.** Nothing enforces
it — a red check will not stop a commit — so run it yourself while working:

```bash
./scripts/check              # lint · format · types · unit tests (seconds)
```

The gates above do not run a single test. A task's RED step does, so this project's
way to run one lives here too — not a gate, just the command the loop needs:

```bash
uv run pytest tests/test_modulo.py::test_nombre
```

Everything else about how work is organized (branches, commit format, where
artifacts land) is in **Conventions** below.

## Structure

| Path | What lives here |
|------|-----------------|
| `src/orquidea/` | El código de la aplicación |
| `tests/` | Pruebas unitarias |
| `scripts/` | Gate entry points (see Development) |
| `governance/` | Vision, requirements, guardrails, architecture (see below) |
| `conventions/` | Bindings de esta instancia (notificaciones) |
| `work/` | Work in progress — one directory per epic / story / bug / spike |
| `records/decisions/` | ADRs — the decisions and their rationale |
| `records/parking-lot.md` | Hallazgos nombrados y aplazados |

## Governance

The durable answers live here, one question per document:

| Document | Answers |
|----------|---------|
| `governance/vision.md` | Why this exists, and the outcomes it aims for |
| `governance/PRD.md` | What it must do (`RF-XX` requirements) |
| `governance/guardrails.md` | The quality bars, and how each is verified |
| `governance/architecture/system-context.md` | External actors and interfaces |
| `governance/architecture/system-design.md` | Internal layers and modules |

## Conventions

This project follows the gemba method — commits, branches, work items
and gates are defined in
`CLAUDE.md` at the repo root; not repeated here.
