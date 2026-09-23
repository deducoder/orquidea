# Docs publishing — Rules

> Restrictions and guards around publishing to the connected docs system.
> The positive shape (templates, the find/create/append procedure) lives
> in [`convention.md`](convention.md).

## R1 — Pages only, never folders

Every node in the tree — grouping or content — is a page. No skill
creates a folder, and none assumes one exists to nest under.

**Why:** a page is the one node type every docs connector offers, and folder
creation is not: a connector's page-creation call can accept an existing
folder as a parent while nothing in its toolset can originate one. Treat that
as the shape to expect rather than as one product's quirk — a tree built only
from pages is portable across connectors, and a tree that needs folders is
not. Revisit only if a connector genuinely offers folder creation, and prefer
pages even then.

## R2 — Never cache a parent page's id

A publish step **always** resolves its parent by searching the docs
space by title (`convention.md`'s "Find or create a parent"). No page id
is stored in `conventions/tracker/instance.md` or anywhere else.

**Why:** `instance.md`'s real template only ever records a docs system's
space key — extending it to cache individual page ids invents new state
that can silently go stale (a page renamed or moved by a human breaks a
cached id with no signal). Publishing is infrequent enough that the extra
search-by-title lookup costs nothing worth trading correctness for.

## R3 — Every title is unique across the whole space, by construction

The epic root's title includes `{EPIC-KEY}`; the project-level root is
the fixed literal `Standalone`. An epic-scoped grouping page
(`Decisions`/`Spikes`) is titled `{EPIC-KEY} — {GroupName}`
(e.g. `e2 — Decisions`), matching the epic root's own `{EPIC-KEY} —
{epic name}` style. A Standalone-scoped grouping page stays bare
(`Decisions`, `Spikes`, `Research`) — Standalone is a single,
always-unique root, so no two Standalone grouping pages of the same name
can ever coexist to collide. `Research` never appears in the epic-scoped
form: it is Standalone-only (`convention.md`'s Research index template).

**Why:** a docs system may enforce title uniqueness across the **whole
space** rather than scoped by parent, and the rule has to hold on one that
does: there, creating a second bare "Decisions" page under a different parent
does not create two pages, it silently renames the new one to "Decisions (2)".
Parent-scoping only helps *find* a page by a correctly-qualified title; it does
not make an *unqualified* title safe to reuse on a system that enforces
uniqueness. With every title unique by construction, the lookup in
`convention.md` needs no `parent =` clause at all — see R2.

## R4 — Append a row, never rewrite the index table

Publishing under a grouping page reads its current body, adds exactly one
row, and writes the full body back — it never regenerates the table from
the local `/work` state.

**Why:** a full-rewrite risks losing rows from a publish that isn't
reflected in whatever local state the rewrite was generated from (a race,
or content published from a different machine/session). One row appended
is always safe; a rewrite is a claim about the whole table's history that
no single publish is positioned to make.

## R5 — Name a `work/` artifact, never cite it by path

Published content that points at anything under `work/` **names** it. It
never writes the path:

| Pointing at | Cite it as |
|---|---|
| A work item (bug, story, epic) | its tracker issue key — `b15`, `s15`, `E2` — or its local id if trackerless |
| A research report | its own name and date: *the {topic} research, {date}* |
| A session log, or any other `work/` artifact | the same way: what it is, and when |

Naming the **directory** while describing the method is not a citation and
stays legal — `work/`, `work/epics/`, `work/{type}/{item}/` in a template.
Those are vocabulary: they name a place, they do not offer evidence.

**Why:** the reader of a published page may never open the repository, so a
path is not a weak citation — it is no citation at all, and the argument
that leans on it becomes an assertion. The rule reaches past work items
because most of what an ADR leans on is **not** one: a research report and a
session log have no tracker key and do not publish, which is exactly why they
have to be named well enough to be recognised without one. Where the artifact
cannot be reached at all, the surrounding text must hold without it — the
reference is provenance, never load-bearing.

## No tracker/docs system connected

If `tracker-bind`'s Docs space binding doesn't exist, every publish step
this convention governs is skipped — best-effort, non-blocking, the same
posture as every other tracker/docs touchpoint in the method. Nothing in
`adr`/`spike`/`epic-close` blocks on a docs system being absent. Skipped
is still said: the step reports **not applicable**, and a binding that
declares a docs system while the page was not created is **not
published**, never a skip (the convention's `When this applies`).
