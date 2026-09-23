# Git — Convention

> Git conventions — the shape of every commit, branch and merge in this
> project. Restrictions and guards live in `rules.md`.
> The work item identity (`{scope}`) is the same one used by the tracker
> (`../tracker/`, where the key is born when a tracker exists) and by the
> directory and branch (`../work/`).

## Generic structure

Base: [Conventional Commits](https://www.conventionalcommits.org/), reduced to
**a single line** — no body, no footer.

```
<type>(<scope>): <description>
```

No component references "epic", "story" or "bug" — that is a later
application layer.

**No body, no footer:** the extended detail (acceptance criteria, context,
root cause) already lives in the tracker or in the local scope/plan artifact.
The reference to the parent container needs no footer because the **scope
already encodes it**, or, when the scope is an issue key, because the tracker
already knows the relationship (epic link).

Co-author trailers are discarded by the same simplification: the one-line rule
leaves no room for them, and they are not wanted in the history.

## Type rule

The type describes **the technical nature of the change**, not the work
container. Standard vocabulary:

| Type | When it applies |
|---|---|
| `feat` | New observable functionality |
| `fix` | Correction of incorrect behavior |
| `refactor` | Internal change with no behavior change |
| `test` | Only adds or adjusts tests |
| `docs` | Documentation only |
| `chore` | Process/tooling maintenance (init scope, close with retro, persist state) |
| `style` | Formatting, no logic change |
| `build` / `ci` | Build system or pipelines |

Custom types (`epic`, `bug`) are never invented to signal the container — that
signal lives in the scope.

## Scope rule

The scope is the **unique identifier of the work item**, and the only place
where the parent-child hierarchy lives (there is no footer any more).
Derivation is agnostic to the work item type:

1. If there is a **published** external tracker → the scope is the **issue
   key**. The relationship with the parent is resolved by the tracker (epic
   link).
2. Otherwise → a local identifier that encodes the hierarchy: type prefix +
   epic number + sub-number. `e{N}` (epic), `s{N}.{M}` (story), `b{N}.{M}`
   (bug), `sp{N}.{M}` (spike). The epic number stays embedded.

**Three roles of the scope, depending on the moment:**

1. **Container commits** (opening, triage, plan, close) — work item metadata.
   Scope = work item (issue key or local id).
2. **Task commits** inside a branch that is already associated with a work
   item (`test`/`feat`/`fix`/`refactor` during implement/fix) — the branch
   already identifies the work item, so the scope goes back to its literal
   meaning: **the area of code affected**. Example:
   `fix(payment): guard against duplicate submission on retry`.
3. **Commits with no work item at all** — project setup, session handoffs,
   anything outside a lifecycle. There is no id to name, so the scope is the
   **area affected**, like role 2: `chore(governance): initialize`,
   `chore(session): close 2026-08-03`. The scope is never omitted; `initial
   commit` below is the one total exception in the method.

## Description rule

- **Always in English** — never in Spanish, regardless of the working
  language. The commit lives permanently in the history and is consumed
  outside the project's context.
- Imperative, lowercase, no trailing period. Target ~72 characters.
- Describe the observable effect, not the internal process.

## Derivations by lifecycle moment (type-agnostic)

| Moment | Type | Note |
|---|---|---|
| Opening / scope init | `chore` | Process metadata |
| Classification / triage | `chore` | |
| Task plan | `chore` | |
| Task commit (TDD) | `test`/`feat`/`fix`/`refactor` by phase | Scope = area of code |
| Close with retrospective | `chore` | |
| Integration merge | merge message, not a conventional commit | See below |

### What marks each phase on the work item's branch

The order of a work item's phases is the core's to declare, in its work-items
table, and nowhere else. What this convention adds is how each of those
phases shows on the branch, so that the order can be read back from the
history:

| Phase | Its mark |
|---|---|
| `start` | `chore({scope}): initialize` |
| `implement`, `fix` | a task commit — `test`, `feat`, `fix` or `refactor`, scoped to the area of code |
| `close` | nothing on the branch: the merge into `{dev-branch}` is its mark |
| any other | `chore({scope}): {phase}` |

A task commit is only one of those four types. A `chore` or `docs` commit
scoped to anything but the work item — parking an entry, landing a research,
closing a session — is meta-work done alongside the cycle, not a step of it,
and a decision record's `docs({scope}): …` is the work item's own container
commit. `check-phase-order`, beside this convention, reads this table and the
core's to judge the order.

**Merge:** the message is **git's default, with no embellishment**:
`Merge branch 'story/{scope}/{slug}' into {dev-branch}`. No `Tracker:` line
and no hand-written summary — both are redundant with the branch name.

**Resolving a conflicted merge without an editor takes one extra flag.** Git
prepares a `# Conflicts:` block in the message and relies on the editor pass
to strip it; `git commit --no-edit` skips that pass, so the block survives
and the merge lands with a body this convention forbids. Use
`git commit --no-edit --cleanup=strip`. Measured: `--no-edit` alone produced
a five-line merge message, the same command with `--cleanup=strip` produced
one line.

`{dev-branch}` is the project's integration branch — the one every story, bug
and spike branches from and merges back into. Its actual name (`develop`,
`dev`, `main`…) is a property of the adopting project, declared once in its
`CLAUDE.md`; every skill and rule here refers to it by this placeholder and
never hardcodes a name.

**A phase run again re-emits its commit as `re-{phase}`, and the original
stays.** Rewriting history so a phase looks right the first time deletes the
error, and the error is retrospective material — the same reason a merge keeps
git's own message rather than a tidied summary.

The hyphen is **uniform across every phase**, and the uniformity is the rule's
whole value:

```
re-analyse   re-close   re-design   re-initialize   re-plan   re-review   re-triage
```

The alternative — closing the prefix up where English already has the word
(`redesign`) and hyphenating where it does not (`re-review`) — makes the form
depend on each word's dictionary status. That is a fact nobody can check while
writing a commit message, it differs between `redesign` and `replan` though the
two look alike, and a rule resting on an unverifiable fact per use is one that
gets guessed wrong — the more so while it lives only in prior commit
messages, with nothing written down to check a new one against.

The **type never changes**. A re-emission stays `chore`: it is process
metadata, and `fix` would move the next release's version for an edit that
changes no product.

Commits that predate this rule in any repository **stay as written**, for the
reason the re-emission form exists at all: rewriting them would delete the
evidence that the rule was learned rather than designed.

## Integration mode

**How a branch reaches its target** is the third project declaration, next to
`{dev-branch}` and the tracker mode in the adopting project's `CLAUDE.md`:

- **`request`** — push the branch and open a merge/pull request on the VCS
  host. The team default: the request is where someone else reads the change
  before it lands.
- **`direct`** — merge into the target locally with `--no-ff` and push the
  result. The solo default: with no reviewer on the other side, a request is
  ceremony — the full gate at push time *is* the review, and `--no-ff`
  preserves the same branch history a request would have.

The method never names a host or its CLI: "open a request" binds to whatever
the project uses (GitHub, GitLab, Gitea…), and direct mode needs no host
tooling at all. **If no mode is declared, ask before the first push** — do not
assume either.

The exact message each phase produces is **not listed here**. It lives in the
skill that emits it, which is the only place that can keep it true: a table of
per-flow commit messages in this document would be a second copy of thirteen
skills, and the copy is what goes stale. The rules above are what let you derive
a correct message for a phase this document has never heard of.

## Initial project commit

Right after project setup (scaffolding of `.claude/`, `CLAUDE.md`,
`conventions/`), the first commit of the repository is:

```
initial commit
```

This is a **total exception** to the generic structure — no type and no scope:
it is the "zero" commit, with no work item and no nature of change to
classify.

**It lands on `{production-branch}`, and `{dev-branch}` is created from it.**
A project declaring both branches creates the production one first, commits the
zero commit there, and branches the dev branch off that same commit. The
production branch is therefore the repository's root, and every promotion
afterwards merges into it — which is what gives a release tag a two-parent
commit to sit on. Born the other way round, at the first promotion, that first
tag lands on a single-parent commit and on a shape no later promotion repeats.

`{production-branch}: none` → there is one branch and nothing to create; the
zero commit lands on it.
