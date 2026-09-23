# Project — Convention

> The top-level tree of a project that adopts the method: which entries it
> has, what governs each one, whether it may be absent, and which step creates
> it.
>
> **Scope:** this convention stops at the first level. What lives inside
> `work/` is fixed by `../work/`, what lives inside `.claude/memory/` by
> `../memory/`, and which artifact each phase writes by `../artifacts/`.

## Entries

| Path | Governed by | Kind | Created by |
|---|---|---|---|
| `CLAUDE.md` | `../core-declarations.md` | required | `install` wires the core into it (or into `.claude/CLAUDE.md`); `project-create` creates it, `project-onboard` only if missing |
| `.claude/settings.json` | `../attribution-hardening.md` | required | `install` merges its entries |
| `README.md` | this convention, `## Two front doors` | required | `project-create` creates it · `project-onboard` only if missing · `epic-close` corrects its Quick start and Structure sections only |
| `governance/` | the project setup skills, `project-create` and `project-onboard` | required | `project-create` creates it · `project-onboard` merges into it |
| `scripts/check` | `../gates/convention.md` | opt-out | `project-create` creates it · `project-onboard` wires it to existing commands · `install` offers it |
| `scripts/gemba/` | `../gates/convention.md` | opt-out | `/gemba:checks` copies into its `conventions/` the checks the plugin ships beside its conventions, replacing that copy whole each run |
| `scripts/checks/` | `../gates/convention.md` | lazy | the project, with its first check of its own; its `scripts/check` runs them |
| `.claude/memory/` | `../memory/` | opt-out | `project-create` and `project-onboard`, symlinked from the harness's per-path memory directory; a project wired by `install` alone has none until one of them runs |
| `conventions/` | `../bindings/convention.md`, one instance binding per domain | per domain | the step that binds that domain |
| `work/` | `../work/` | lazy | the first skill that writes a work log or a session log |
| `records/` | this convention, `## records/` | lazy | the first `adr` or `park` |

Everything else at a project's root — its source, its manifests, its own
documents — belongs to the project and is outside this convention: the table
lists what the method brings, not what a project may keep.

## Kinds

- **required** — present once the project is set up; its absence is a defect.
- **opt-out** — the project may decline it, and its absence means it did:
  nothing is run, nothing fails (see `../gates/convention.md`).
- **per domain** — exists only for a domain that needs it; a project with no
  such domain has none, and nothing asks it to.
- **lazy** — born the first time something writes into it. Its absence before
  then is correct, and no step scaffolds it.

## Two front doors

**`README.md` and `CLAUDE.md` are two front doors for two readers:** the README
for a human arriving at the repo — what it is, how to run it, what is not
obvious from the code — and the CLAUDE.md for an agent working in it, which is
the **gemba core itself**: method only, with this project's six declarations
filled. Neither restates the other, and neither restates governance — this is
the artifacts rules' R1 (one owner per artifact) applied to content: two
sources for the same truth both lose trust the moment they diverge. The method
is not a third source: the core *is* it, which is why nothing else carries a
copy.

## The gate entry point

`scripts/check` is the project's **gate entry point** — the contract every
"run the gates" step refers to (see `../gates/convention.md`; nothing enforces it
automatically until the project wires the shipped hooks). It is created at project setup precisely so a project never
starts life with silent, absent gates — and a project that declines it has
opted out, which `../gates/convention.md` treats as nothing to run rather than a failure.

## `records/`

What the project decides and what it defers. Both files are written by
techniques, and both are born on first use:

| Artifact | Path | Owner |
|---|---|---|
| `adr-{NNN}-{slug}.md` | `records/decisions/` | whoever makes the decision (`adr` technique) |
| `parking-lot.md` | `records/` | appended by whoever defers the work (the artifacts rules' R4) — **created on first append**, not scaffolded |

The shape of a retired parking-lot entry is fixed by `../artifacts/`
(`### The retirement record`), not here.

## The guardrails table

`governance/guardrails.md` holds the project's quality bars as one table, and
a check shipped beside this convention reads it. It finds two columns by their
header — `ID` and `Verification` — so the table may carry others, in any
order. A verification takes one of three shapes:

- **A check of the project's own**, in the location the gates convention
  declares, named by its path; the check claims the row with a
  `# Verifies: {id}` line of its own. The row without that claim, or naming a
  file that does not exist, is red; so is a claim with no row.
- **A check the method ships**, named by its path under
  `conventions/{name}/checks/` wherever it was installed; it cannot claim a
  project's id, so the row names it and the check declares what it verifies.
- **A person's reading**, in words — not a check, and nothing to judge.

A table of only the third shape leaves the check by a declared opt-out; so
does a project that never had the table. One the project committed and then
lost is red.

## An open question: a name that already means something else

A project that adopts the method with a `records/`, a `conventions/` or a
`work/` that already holds something else of its own is not answered here.
Which of the two gives way is a decision for that project, and this convention
does not pretend to have made it.

## Outside this section

- **The adopting project's `conventions/` is not the method's.** The entry
  above is the project's own directory of instance bindings — facts about one
  real tracker or tool. The method's conventions, this file among them, ship
  inside the plugin and are never copied into a project.
- **What lives inside each entry** belongs to the convention in its
  `Governed by` cell: `../work/` for work logs, `../memory/` for the memory
  store, `../bindings/convention.md` for the shape every instance binding has.
- **Which artifact each phase writes, and who owns it,** is `../artifacts/`.
