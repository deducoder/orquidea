# Memory — Convention

> How a project's assistant memory is versioned. What must move together —
> an index entry and the file it points at — is a restriction rather than a
> shape, so it lives in `rules.md` alongside this file, the same split its
> sibling conventions use.

## The problem this solves

Claude Code's own memory feature creates a per-path directory outside any
repo (`~/.claude/projects/{encoded-path}/memory/`), with no awareness of git.
Left alone, that content is never versioned, never travels with a clone, and
is silently orphaned the moment its directory moves — found during Gemba's
own development, evidenced by hundreds of orphaned memory namespaces for
long-deleted `/tmp` directories.

## Where memory lives

Inside the project's own repo, at **`.claude/memory/`** — versioned exactly
like any other artifact, alongside `records/parking-lot.md` and
`records/decisions/`. `MEMORY.md` and every individual memory file sit flat in
that directory, matching the structure the harness's own memory feature
documents and expects.

The name mirrors the global `~/.claude/` directory on purpose: the
relationship between `~/.claude/projects/{path}/memory/` (global, per-path)
and `.claude/memory/` (local, per-repo) stays symmetric.

## How the harness reads it: a symlink, not a copy

`~/.claude/projects/{encoded-path}/memory` is replaced with a symlink
pointing at `{repo}/.claude/memory` — never a copy that could drift.
Read/Write/Edit tools resolve through the symlink transparently (proven
empirically during Gemba's own development: a write through the harness's
path landed, byte for byte, in the repo's own file, confirmed by reading it
back through a second, independent path).

## Isolation between projects

Each project's `.claude/memory/` lives inside its own repo — there is no
shared or cross-project memory store. A project never reads or references
another project's memory directory.

## Setup

Established once per project, at `project-create` or `project-onboard` time
(see [`../../skills/project/`](../../skills/project/)):

1. Create `.claude/memory/` in the repo, with an empty `MEMORY.md` (or the
   project's existing memory content, in the onboarding case).
2. Replace the harness's per-path memory directory with a symlink into it.
3. Commit `.claude/memory/` like any other artifact.

## Memory files stay flat

Leaf memory files live directly in `.claude/memory/`, never in a
subdirectory. Claude Code's automatic recall is documented to scan file
descriptions; whether that scan reaches subdirectories is **not** publicly
documented, and being wrong about it would silently disable recall for
everything moved there — a worse outcome than the clutter a subfolder tidies
away.

Flat is therefore the rule, not a placeholder. Changing it takes a
demonstration against a live instance, in the project that wants the change.
