# Artifacts — Rules (restrictions and guards)

> Restrictions and guards that surround artifacts but are not their shape —
> that lives in `convention.md`.

## R1 — One artifact, one owner; no chained editing

Each artifact has **exactly one skill that writes it**. The rest **read** it.
The "living document" pattern, where several phases keep piling content into the
same file, is forbidden — that is what leaves an artifact such as the epic's
`scope.md` with no owner and four writers.

If a phase needs to add information, it **emits its own artifact**. If it needs
to correct another phase's artifact, that is a signal the earlier phase came out
wrong, not a licence to edit it.

## R2 — Canonical name per moment, not per type

The name is fixed by the **moment of the cycle** (the table in
`convention.md`), not by the issue type. Forbidden:

- **Per-type variants** of the same moment (`retro.md` vs `retrospective.md`).
- **Identity prefixes** in the name (`s{N}.{M}-plan.md`) — the directory path
  already supplies the identity (`../work/`).
- **Undefined names** — if a skill emits an artifact, it names it. An unnamed
  "progress log" is an artifact nobody can find.

## R3 — Allowed cross-writes, each named explicitly

A cross-write is forbidden by default (R1). Five are declared, each bounded
to one named section of one named file — never open-ended, and never implied
by analogy with these five:

- **`story-close` → the epic's `plan.md` tracking table.** Updated when
  `story-close` closes a story. Bounded to that table.
- **`spike` → the epic's `plan.md` tracking table.** A spike that lives under
  an epic and has a row in that table sets it to `done` in the commit that
  saves its artifacts on the dev branch. Bounded to that one row.
- **`epic-close` → `README.md`'s Quick start and Structure sections.**
  Declared so the repo-root `README.md`'s structural pointers do not drift
  silently across a whole epic's worth of change — no other phase ever
  revisits it once `project-create`/`project-onboard` write it (see
  `convention.md`'s ownership table). Bounded to those two sections; the
  opening paragraph and any other content stay read-only, human-reviewed
  before commit the same way `docs.md` already is.
- **`epic-close` → its own epic's row in `work/roadmap.md`.** Sets that
  row's `Status` to `closed` when the epic closes. Bounded to that one cell of
  that one row (`convention.md`, `### The roadmap`).
- **`release` → its own version's section in `work/roadmap.md`.** Sets the
  section's `State` to `released` when it promotes the version, and renames
  the heading when the number it computed differs from the declared one.
  Bounded to that heading and that line.

Anything else a closing skill believes "needs fixing" in someone else's
artifact is **reported as a finding**, not edited (consistent with the scope
restrictions on `story-close` and `bug-close` in `../../skills/`).

## R4 — Shared documents: append only, entry owned by its author

`records/parking-lot.md` is a shared doc by design: several skills **add** entries
when they defer work. The rule is **append-only** — each entry is owned by
whoever wrote it, with its origin and its promotion condition; nobody rewrites
someone else's entries.

**Retirement is the one declared exception, and it is not a rewrite.** When an
entry's promotion condition fires or its subject stops existing, the entry is
**removed** from the open items and a record of why is appended to the file's
`## Retired` section — newest-first, below the live items, so a reader meets
deferred work before its archive. Retiring is therefore the only operation
that takes something out, and it still writes nothing over anyone's words:
text that moves, moves verbatim. Append-only governs the **entries**; this
governs their end.

**Both operations anchor on the line that is exactly `## Retired`**, never on
the first occurrence of that string: entries that discuss the section carry it
in their prose, and matching that has already split a live entry in half and
left another born retired.

**Retiring sweeps what cited the entry.** Before the record is written, find
what referenced it and say what became of those references in the record's
`Swept:` field — an empty sweep is a legitimate answer, an unasked one is not.
An entry is often the only place a piece of reasoning lives, and something
elsewhere may point at it; a retirement that skips this leaves a citation
aimed at nothing, and the break surfaces only when a reader follows it.

## R5 — Brownfield exception: merge into guardrails

`project-onboard` **merges** the conventions it detected from the code into
`governance/guardrails.md`, instead of creating the doc from scratch. It is the
only update to an existing doc that the convention allows by design, and it has
its own guard: it **never overwrites** the detected conventions — they are the
truth about how that codebase already works.

## R6 — Artifacts are versioned in the repo

They go into git alongside the work (already in `../work/rules.md` R3). They are
not temporary and they are not ignored. An artifact that is not committed is an
artifact lost in the merge.

## R7 — Template ≠ artifact

The template lives in `assets/` of the emitting skill
(`../authoring.md`); the artifact lands in `work/`
(`../work/convention.md`). The two are never conflated: the template is
consulted and does not change, the artifact is produced per work item.

This rule governs **artifacts only**: a written, versioned,
single-owned output. An artifact's template of ~5 lines → **inline in
the `SKILL.md`**, with no separate file; past that, `assets/`. A different
kind, the **presented output** — never written to a file, rendered to the
human as the skill's result — is always inline, under `## Output`,
regardless of length; this threshold does not apply to it.

## R8 — A deferral marker names its ceiling and its trigger

A `parked:` marker (see `convention.md`) is a deliberate simplification, not
a TODO: it names the **ceiling** it accepts and the **trigger** that revisits
it. At harvest, a marker with no trigger is flagged `no-trigger` — a deferral
without a revisit condition is how "later" becomes "never".

The harvest is a **report**: it never edits `records/parking-lot.md` (R4 stays
append-only) and never rewrites markers. Promoting a marker into a parking-lot
entry, a work item, or a fix is a decision its finder makes explicitly.
