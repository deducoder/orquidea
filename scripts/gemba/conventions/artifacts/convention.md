# Artifacts — Convention

> Artifact conventions — what each skill emits, what it is called, and who
> owns it. Where those files live is set by `../work/`; what each skill does is
> defined by `../../skills/`. Restrictions and guards live in `rules.md`.

## The two principles

1. **Every phase its own file.** Each moment of the cycle emits **its own**
   artifact. A document shared across phases is never edited in a chain.
2. **One moment, one name; one artifact, one owner.** The name derives from the
   **moment of the cycle**, not from the issue type — the same moment never has
   two names. And each artifact has **exactly one skill that writes it**; the
   rest read it.

The content **does** vary by type (an epic's `scope.md` looks nothing like a
bug's). It is the name and the owner that are unified, not the content.

**Both tables below list artifacts only** — written, versioned outputs. A
skill's **presented output** (a review's findings, `integrate`'s result)
appears in neither: it is never written to a file, so it has no path and no
owner row here. Being outside the canonical table does not make
something a presented output, either — `debug`'s `analysis.md` is a file
artifact and still lives in the second table below, not the first.

## Canonical table — name, owner and types

| Moment | Artifact | Owner (single writer) | epic | story | bug | spike |
|---|---|---|:---:|:---:|:---:|:---:|
| Definition / bet | `brief.md` | `epic-start` | ✓ | — | — | — |
| Scope and done when | `scope.md` | `epic-design` · `*-start` | ✓ | ✓ | ✓ | ✓ |
| Classification | `triage.md` | `bug-triage` | — | — | ✓ | — |
| Root cause analysis | `analysis.md` | `*-analyse` · `debug` | — | — | ✓ | — |
| Design | `design.md` | `*-design` | ✓ | ✓ | — | — |
| Task plan | `plan.md` | `*-plan` | ✓ | ✓ | ✓ | — |
| Dispatch record | `dispatch.md` | `delegate` | — | ✓ | ✓ | — |
| Decisions log | `decisions.md` | the epic session of the software addon's `orchestrate` technique | ✓ | — | — | — |
| Experiment outcome / kept finding | `findings.md` | `spike` · `*-fix` | — | — | opt. | ✓ |
| Generated documentation | `docs.md` | `epic-close` | ✓ | — | — | — |
| Retrospective | `retrospective.md` | `*-review` | ✓ | ✓ | ✓ | — |

A spike has no retrospective of its own: its `findings.md` **is** the retro.

A bug's `findings.md` is a different thing wearing the same name, and optional:
something worth keeping that is **not** the root cause — an unfiled upstream
report, a reproduction someone else will need, evidence for a decision that
lands elsewhere. The cause belongs in `analysis.md`; if the finding *is* the
cause, it has no `findings.md`.

## Who owns the `scope.md`, by type

There is a **deliberate** asymmetry here between epic and everything else:

- **Epic:** `epic-start` emits **only `brief.md`** (the bet: hypothesis,
  appetite, limits). The `scope.md` is owned by **`epic-design`**, because an
  epic's scope *is* a product of design — you cannot list its stories before
  decomposing it. Seeding a scope at start with "planned stories" only forces
  design to rewrite it.
- **Story / bug / spike:** the `scope.md` is owned by its `*-start`, because
  what bounds them arrives given — from the epic's story list, from the bug
  report, or from the spike's question. Not everything a story's or a bug's
  scope holds does: an acceptance criterion or a done-when outcome written
  before any phase has read the code is often deduced by whoever writes the
  scope. Each one carries a mark, so the two are never read alike — see
  `## Criterion marks` below.

## The user story lives inside the story's `scope.md`

`story-start` emits **a single artifact**: `scope.md`, which holds the user
story and its limits together:

- User story — *"As a {role}, I want {capability}, so that {benefit}"*.
- Acceptance criteria (Gherkin), each marked, and one concrete example.
- In scope / Out of scope.
- Done when (observable outcomes, each marked).

They are the same moment (opening the story and stating what it is and how far
it goes); two files for that was ceremony. An epic **does** split `brief.md`
from `scope.md`, because there the bet and the scope are distinct decisions,
taken by different skills at different moments.

## Criterion marks

Criterion marks: `[stated]` · `[deduced]`

A story's or a bug's scope marks every commitment it makes with one of the
two, in that order of authority:

- **`[stated]`** — the human said it, or the source that opened the work item
  carries it (the epic's story row, the bug report). It stands until the human
  changes it.
- **`[deduced]`** — inferred by whoever wrote the scope. It stands only once
  the phase that reads the code has confirmed it: the story's design, which
  confirms or retracts each one, or the bug's analysis, which confirms, narrows
  or retracts its done-when — always with the reason. **When in doubt,
  deduced.**

In a Gherkin block the mark is a tag on the line above the scenario
(`@stated`, `@deduced`); in a list it opens the item. A stated criterion the
code contradicts is not retracted by the phase that found it: it goes back to
the human as a question. A criterion with no mark predates the marks and reads
as stated.

An epic's scope marks its `## Done when` the same way, with one difference in
who resolves it. That scope is written by `epic-design`, the phase that reads
the code, so there is no later phase to confirm a deduction before the work
is built:

- **`[stated]`** — the human said it, or the epic's brief carries it.
- **`[deduced]`** — the design inferred it. A measurement the design did not
  run itself, inherited from a spike or from earlier work, is deduced however
  factual it reads.

`epic-review` resolves them when it re-verifies the scope. A deduced criterion
the code does not fulfil is descoped with its reason. A stated one goes to the
human.

## The epic's progress lives in its `plan.md`

The epic's `plan.md` holds the tracking table (story sequence, status,
estimated vs actual). When a story closes, **`story-close` updates that table**
— not the `scope.md` — and a spike that has a row there sets it when it
saves its artifacts. These are the only two writers of that table (see
`rules.md` R3): progress belongs to the plan, which is where the sequencing
hypothesis lives, not to the scope, which is a stable declaration.

## The epic's decisions log

With the unattended mode on ([`../autonomy/convention.md`](../autonomy/convention.md)),
the gates a person answers today are answered by the version orchestrator
instead, and each answer is a decision nobody saw being taken. `decisions.md`
is where they are read afterwards: one per epic, in the epic's own directory,
never in a story, a bug or a spike.

- **What goes in:** a gate answered in the human's place, a stop the
  unattended work halted at, and the answer that stop received — and nothing
  else. A stop is written here because this file is what the human reads
  after an unattended run; the stop's question, left anywhere else, is one
  more place to look. The decisions an executor takes inside its own block —
  a story's design, a plan's order — stay in that block's artifacts.
- **The rule it closes:** the entry is written **before** the step goes on. A
  gate answered with no entry was not answered: the decision was not taken.
  This is the never-go the closed stop list leaves to this file.
- **Who writes it:** the epic session of the `orchestrate` technique alone —
  the session that holds `{dev-branch}`. An executor never writes it: it
  reports what it decided, and the orchestrator records it.
- **It only grows.** An entry is never rewritten or removed. A later decision
  that reverses one is a new entry that names the one it reverses.
- **It may be absent.** With the mode off there is nothing to record, and an
  epic with no `decisions.md` is complete.

**The shape of an entry** — a gate answered, a stop, the answer to a stop — is
the software addon's to write, and lives in one place: the `assets/` of its
`orchestrate` technique, the log's one writer, where `rules.md` R7 puts a
template. This section keeps the rule; the asset keeps the shape.

## Artifacts that are not work-item artifacts

| Artifact | Path | Owner |
|---|---|---|
| `analysis.md` | `work/debug/{name}/` | `debug` (tiers S, M and L — XS leaves only a commit line) |
| `report.md` | `work/research/{topic}/` | `research` |
| `problem-brief.md` | `work/problem-shape/{slug}/` | `problem-shape` |
| `{YYYY-MM-DD}-{slug}.md` | `work/sessions/` | `session-close` (written) · `session-start` (read) |
| `roadmap.md` | `work/` | the version-planning technique (sections and rows) · `epic-close` and `release` (the cross-writes `rules.md` R3 declares) · the human (everything else) |
| `session-pointer.md` | `.claude/memory/` | `session-close` (written) · `session-start` (read) |

The project's first-level entries — which exist, what governs each, whether it
may be absent and who creates it — are declared by `../project/`, not here.

### The roadmap

`work/roadmap.md` holds the versions a project has planned: one section per
version, in the order they were planned, each naming the epics that make up its
functional scope. It is a hypothesis that changes while the versions are built,
which is why it lives in the work log and not in the governance.

```markdown
# Roadmap

## v0.3.0

State: planned

Customers can book, change and cancel an appointment, and receive a reminder.

| Epic | Status |
|---|---|
| AB-12 | closed |
| AB-15 | open |
```

A section is headed `## {name}`, where the name is the number the version is
expected to carry: provisional until `release` computes the real one from the
commits, and renamed then if the two differ. Under the heading, exactly one
`State:` line, one line of functional scope in the project's working language,
and exactly one `| Epic | Status |` table. A row's first cell is the epic's key
— its tracker key, or its local id (`e{N}`) where no tracker is connected — and
an epic is a row of one section only.

The state of a section, and who writes it:

| Section `State` | Written by |
|---|---|
| `planned` | the version-planning technique, when it creates the section |
| `released` | `release`, when it promotes the version |

The status of a row, and who writes it:

| Row `Status` | Written by |
|---|---|
| `open` | the version-planning technique, when it adds the row |
| `closed` | `epic-close`, on its own epic's row |

**Writers.** The version-planning technique creates a section and its rows.
`epic-close` changes one cell, its own epic's `Status`, and `release` changes
its own section's heading and `State` — the two cross-writes `rules.md` R3
declares. Everything else belongs to the human: adding, removing or reordering
a version or an epic is a decision, not an event.

**Readers.** `session-start` reconciles the version in progress — the first
section whose `State` is `planned` — against the real state of its epics, and
reports without blocking. `release` compares what a section declared with what
landed. The version-planning technique reads the whole file before it declares
the next version.

**What it never holds.** No dates: a date in an artifact nobody owns ages in a
week and nobody corrects it. No "someday" section: what fits no declared version
is parking-lot work, which already has a shape and a promotion condition.

### The retirement record

An entry that is retired leaves a record in `parking-lot.md`'s `## Retired`
section, at the end of the file, newest-first. The live items come first
because they are what the file is for; the archive is what it accumulated.

```markdown
### {YYYY-MM-DD} · {work item key, or "direct fix" and why it was not one} · {what was retired}
**Why:** {what changed — the promotion condition fired, the subject stopped
existing, or the decision was taken elsewhere}
**Swept:** {what cited the entry and what became of those citations, or
"nothing cited it" — an empty sweep is an answer, an unasked one is not}
```

`Swept:` is the field with a cost attached: an entry is often
the only place a piece of reasoning lives, so removing it can leave a citation
elsewhere aimed at nothing. R4 makes the sweep an obligation of retiring; this
is where its answer is written down.

**The form reaches every record, including those written before this
convention existed.** Two forms in one archive leave a reader no way to tell
which one to expect. Moving an entry's text verbatim is not rewriting it, and
its own words survive in the commit that removed them, so converting a record
neither loses an author's text nor touches the entry R4 protects.

`analysis.md` shares its name between `bug-analyse` and `debug` on purpose:
same moment of the cycle (finding the root cause), same name.

## The in-code deferral marker

`records/parking-lot.md` catches what someone remembers to write down; a corner
cut **deliberately** in code is marked where it happens, so the deferral stays
greppable next to the code it describes:

```
{comment leader} parked: {ceiling}, {upgrade trigger}
```

```python
# parked: O(n²) pairwise scan, fine to ~1k items — spatial index past that
```

The harvest is one grep, run by `architecture-review` at epic scope or on
demand:

```
grep -rnE '(#|//|<!--) ?parked:' . --exclude-dir=.git --exclude-dir=node_modules
```

Each hit is one ledger row; the footer counts them: `{N} markers, {M} with no
trigger`. A marker that names no upgrade trigger is flagged `no-trigger` —
those are the ones that silently rot (see `rules.md` R8).

The **session log is the source of truth** for where work stood; the memory
entry `session-close` refreshes alongside it is only a pointer (date, next
action, path), regenerated on every close so the two cannot meaningfully drift.
A session log is dated and append-only as a set — unlike a work item's
artifacts, past entries are never rewritten.

## Templates

Each artifact's template lives as **`assets/` of the skill that emits it** (see
`../authoring.md`). The emitted artifact lands in `work/`
according to `../work/convention.md`. A template and an artifact are different
things: one is consulted, the other is produced.

This governs **artifacts** — a skill's **presented output** (a review's
findings, `integrate`'s result to the developer) is never written to a file,
so it has no template in `assets/`: its shape stays inline, under `## Output`.
