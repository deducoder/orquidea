# Docs publishing — Convention

> The shape of publishing a curated artifact (an ADR, a spike's
> `findings.md`, an epic's `retrospective.md`, a research report) to the
> connected docs system. Shared by `adr`, `spike`, `epic-close`, and
> `research` (see
> [`../authoring.md`](../authoring.md)'s "swapping a tool means editing a
> `references/` file, not the `SKILL.md`" — this doc is that shared
> reference, so none of them restates it). Restrictions and guards
> live in [`rules.md`](rules.md).

## When this applies

Only when a docs system is connected (`tracker-bind`'s "Docs space"
binding exists in the project's `conventions/tracker/instance.md`). That
file is where it is read, and nowhere else: a binding looked for under
another name is not a binding found absent. No docs system → publish steps
are skipped, same as every other best-effort/non-blocking tracker
touchpoint in the method.

Skipped is never silent. Every skill that publishes says, in its output,
which of three outcomes its publish step had, by these names:

- **published** — the page exists, read back; its URL.
- **not applicable** — the binding file declares no docs system; say that
  it was read, and where.
- **not published** — the binding declares a docs system and the page was
  not created: the connector was unreachable, a write failed, or the step
  did not run; say which. This is not a skip, clean or otherwise — it is
  work left undone, reported so the reader of the output (a supervisor, a
  handoff) does not take the close for a published one.

## The five templates

Every page's title always includes its unique key — see `rules.md` R3.
`{…}` placeholders are filled per `authoring.md`'s convention; a
placeholder's *value* follows the project's working language, the
template's own scaffolding never does (`CLAUDE.md`'s `## Language`).

**Epic root** — created the first time anything needs to nest under it:

```
{summary pending — filled in when epic-close writes the real one, 2-3
lines excerpted from retrospective.md's own Summary section}

| Page | Type |
|---|---|
```

**Decisions index** — child of the epic root, or of Standalone:

```
| ADR | Title | Date | Status |
|---|---|---|---|
| [{ADR-NNN}]({link}) | {title} | {date} | {accepted | superseded by ADR-NNN | rejected} |
```

**Spikes index** — child of the epic root, or of Standalone:

```
| Spike | Question | Verdict | Date |
|---|---|---|---|
| [{SPIKE-KEY}]({link}) | {one-line question} | {can we / how / at what cost} | {date} |
```

**Research index** — child of Standalone only; research is never
epic-scoped (identified by `{topic}`, not a work-item key):

```
| Report | Topic | Confidence | Date |
|---|---|---|---|
| [{report}]({link}) | {topic} | {High | Medium | Low} | {date} |
```

**Standalone root** — the project-level home for anything with no epic:

```
Decisions, spikes, and research not tied to a specific epic.
```

## Find or create a parent

Every parent's title is unique across the whole space by construction
(`rules.md` R3), so resolving one is always the same single step,
root or grouping page alike:

1. Build the fully-qualified title: a root page is `{EPIC-KEY} — {epic
   name}` or the literal `Standalone`; a grouping page under an epic
   root is `{EPIC-KEY} — {GroupName}` (e.g. `e2 — Decisions`); a
   grouping page under `Standalone` is the bare `{GroupName}`.
2. Search the space by that exact title.
3. **Found** → use that page's id. **Not found** → create it from the
   matching template above, then use the new page's id.

Never cache the resulting id anywhere (`rules.md` R2) — resolve it fresh
on every publish.

## Publish and append

1. Create the artifact's own page (ADR, spike finding, or epic
   retrospective) as a child of the resolved parent — title follows the
   artifact's own H1 convention (`authoring.md`). The body is the
   artifact's committed content with exactly these changes, and no other —
   nothing added, removed or reworded:
   - **The frontmatter block is stripped**, with the blank line after it:
     it is metadata for the repository, and a page that shows it reads as
     a draft.
   - **The H1 line is stripped**, with the blank line after it: a docs
     system renders the page `title` as its heading, so a body that opens
     with the same H1 duplicates it. Before calling the publish API,
     re-check the assembled body's first line against the title about to
     be sent — if it repeats it, strip that line and the following blank
     line; do not trust that upstream assembly already removed it.
   - **The lines of one paragraph or list item are
     joined into one line**, with a single space: the source is wrapped for
     reading in a terminal, and a docs system can render each of those
     breaks as a hard break in the middle of a sentence.
   - **A mark the target format cannot carry over code closes before the
     code and reopens after it**: bold around a code span becomes bold,
     then the code, then bold again, so the text after the code keeps its
     mark.
   - **Code content passes verbatim**, backslashes and quotes included —
     `tr -d ' \n'` is published with one backslash, never zero, never two.

   The converter this convention ships makes exactly these changes. Run it
   by its path relative to this convention's own directory — a skill of
   another plugin locates the core first — and send what it prints:

   ```sh
   python3 scripts/md-to-html.py {artifact}.md
   ```

   It writes the body to stdout, one block per line, in standard HTML.
   Exit 2 → it met something it does not cover, named on stderr (an
   image, a heading deeper than level 3, an unclosed fence): extend the
   converter before publishing, never hand-write a body around it.

   Write that body in the connector's **structured format** — the one it
   stores as received (HTML, where the connector offers it) — never
   through its **markdown import**, which rewrites the body with rules
   nobody here controls. A connector that offers only markdown is
   published in markdown, and step 4 carries the whole weight. The local,
   git-committed copy keeps its frontmatter, H1 and line breaks
   unconditionally; only the published copy changes.
2. Append **one row** to the parent index's table — read the current
   body, add the row, write the whole body back. Never regenerate the
   table from scratch (`rules.md` R4).
3. Whenever a **new** page is created directly under an epic root as one
   of its **four direct children** — `Decisions`/`Spikes` (found-or-created
   above, as the artifact's own parent) or `Developer Documentation`/
   `Retrospective` (created directly by `epic-close`, no grouping layer
   of their own) — also append one row to the epic root's own index
   table, same append-only discipline as step 2. Scoped to that direct
   child's own first creation, **not per artifact** published under a
   grouping page afterward: an epic's tenth ADR adds a tenth row to
   `Decisions` (step 2), never a new row to the root's own table, since
   `Decisions` itself was only created once.
4. **Read the page back** in the same structured format and compare it
   against the committed source on the changes step 1 lists: no
   frontmatter, no repeated H1, no hard break inside a paragraph, every
   mark around code reopened, every code span character for character.
   Any difference → rewrite the body and republish before going on. The
   step is not done, and nothing records it as done, until the page read
   back matches.
5. Present the published page's URL.

## Publication state, and the population that predates it

An ADR records whether it was published, in its own frontmatter, as a
`published:` key — a date (`YYYY-MM-DD`) when a page was created, or the
literal `no` followed by a reason when one deliberately was not. **No page
id, no URL and no space key is ever written into the repository**: R2
forbids caching a page's identity, and R3 already makes every title unique,
so an artifact's own H1 is the handle anything needs to find it. The key
says only that the step ran.

The obligation reaches **every ADR written from the point a project's docs
binding existed** — not the ones that predate it. A project that adopts
publishing partway through its life has a population of earlier decisions
with no page, and that boundary is a property of the project, recorded
once where its own checks can read it, never re-derived from a list of ids
that goes stale as the corpus grows. State the boundary somewhere a reader
looking for it will land, so an early ADR with no page reads as a recorded
population rather than an oversight.

That place is one line of the docs system's section in the project's
tracker binding, **`Publication starts at`**: the first decision record the
obligation reaches, and why — the date the docs space entered the binding
against the date of the earliest record. Measure both before writing it:
what an early record predates may be the publishing convention rather than
the binding, and then it is inside the obligation and owes a page. A
project whose binding predates every record writes that too — an empty
population is an answer, and a missing line is not.

What this records and what it cannot: a `published:` date is evidence the
publish step ran, never that the page exists today. A page later deleted or
renamed, or a date written while the call actually failed, all read as
green. That ceiling is accepted deliberately — closing it would mean
storing a page id, which R2 forbids for a reason that has not changed.

## Cross-references

When published content needs to reference anything under `work/`, it names
it — a work item by its tracker issue key (`b15`, `s15`, `E2`), a research
report or session log by its own name and date — never a git-relative path
(`rules.md` R5).
