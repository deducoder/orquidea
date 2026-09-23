# Gates — the contract, and who wires what enforces it

> What a gate is and where it lives. Every skill step that says "run the
> gates" refers to this. How skills are written is in `../authoring.md`.

## gemba ships the mechanism; the project wires it

Gemba ships the mechanism that enforces the method, and **wiring it is the
project's own act**. What this package provides is the checks it ships
beside some of its conventions (`conventions/{name}/checks/`), which
`/gemba:checks` copies into a project for its own `./scripts/check` to run —
offered, never imposed. Nothing Gemba installs or updates wires any of it,
and no skill step assumes anything is wired.

Until a project wires it, a gate is discipline — the same as everything else
in this method: **written down and followed**, not technically prevented from
being skipped. A project is also free to add a control of its own.

## The contract

A project **opts into gates** by providing an executable entry point:

```
./scripts/check      any language, any toolchain
```

One entry point, deliberately. A project whose gates live in a Makefile points
`scripts/check` at `make check` in a single line — cheaper than every skill
having to know two paths.

Contract rules:

| Rule | Why |
|---|---|
| **Exit 0 = green, non-zero = red** | Keep the signal binary and scriptable, even without a hook consuming it today |
| The project **owns its commands** | Gates are agnostic: they don't know whether this is pytest, vitest or `go test` |
| **No entry point → nothing to run** | A skill or an agent following this convention has nothing to invoke; it is not a failure, it is opt-out |
| **Fast gates only** | Meant to run on *every* commit; if it drags, the discipline gets abandoned |

## Where a project's own checks live

**The location:** `scripts/checks/`

A check the project writes for itself — a property of its own code or
documents that no shipped check covers — lives in `scripts/checks/`, one
executable per property, and the project's `./scripts/check` runs every one
of them. Each follows the contract above: exit 0 green, anything else red.

`scripts/checks/` is the project's; `scripts/gemba/` is the method's.
`/gemba:checks` deletes and rewrites `scripts/gemba/conventions/` every time it
runs, and the adoption marker the hooks command writes sits beside that copy.
A check written there is lost at the next refresh, or mixed with files the
project does not own. The two are run the same way and owned differently.

The directory is born with the project's first check of its own. A project
without it has written none, which is not a defect: a shipped check that
reads the project's own checks treats that absence as a declared opt-out.

Two checks ship beside this convention and judge every check the project
runs — its own, found through the line above, and the method's, vendored
beside them. One turns red on a check that leaves green before its verdict
without saying `opt-out`; the other on a quiet `grep` at the end of a pipe,
whose early exit reads as a failed match under `pipefail`. Both read shell
text, so a check written in another language is outside what they judge.
Both take extra files as arguments, added to what they find on their own.

## What a dispatch asks of the gate

A project that hands a block of work to an isolated executor gets a **second
worktree and a transient branch** for the duration. Both are visible to the
gate, and that is the part worth stating before it bites:

- **Local branches are shared between worktrees.** A gate clause that checks
  the shape of local branch names will see the executor's transient branch and
  go red — not only for the executor, but for whoever dispatched, who never
  created it and cannot make it go away without ending the dispatch.
- **A second checkout means two working trees under one gate.** A clause that
  reasons about "the" working tree is making an assumption a dispatch breaks.

**What this convention asks:** a project whose gate inspects local branches or
the working tree decides, deliberately, what it does while a dispatch is
live — tolerate the transient branch, scope the clause to the current
checkout, or accept that dispatching turns the gate red and say so. Any of the
three is a legitimate answer. Discovering it mid-dispatch is not, and that is
the only outcome this section exists to prevent.

The method ships no clause for this, because what a project's gate checks is
the project's own call, and this is the warning that goes with the freedom.

## Who is expected to run it, absent a hook

The agent, as part of the task discipline each skill already states — a
domain addon's own skills say when to run it, and how often. In a project
that has wired nothing, this is the **only** mechanism — nothing technical
catches a skipped gate. Treat that as a real, standing cost, not a solved
problem. `/gemba:hooks` is how a project that wants more wires the shipped
hooks, after which a red gate refuses the commit.

## Writing a check that does not lie

A check's red is easy to trust: something went wrong and it said so. Its green
is the dangerous half. Green means only that no clause printed a failure, and a
check reaches that state just as easily by judging nothing as by judging well.
The lessons below are the ways a check reports green over nothing, each measured
more than once before it was written down. They apply to a check in any
language, over any subject — code, documents, configuration, history.

### A check that cannot find its subject reports success

Every clause that first locates something and then judges it can fall silent
when the locating fails: the file was moved, the section renamed, the command
reformatted so the pattern no longer recognises it. In a check, silence reads
as approval. The guard that causes it looks harmless — `if the file exists,
then judge it` — and is written thinking of the case where the subject does
not apply. When the subject is something the project ships or has declared,
an absent subject is a rename nobody propagated, and that is exactly what the
check should shout.

A second guard is needed beside the first: the source can be intact while the
population it should judge is empty. A loop over zero items prints the same
verdict as a loop over a hundred good ones.

**How to apply:** enumerate the subjects once, at the top, and make absence
red with its own failure line. Reserve a quiet green for a real opt-out — a
subject any project starts without and this one never declared — and say
`opt-out` in the output, so it can be told from a pass. Print the size of the
population in every green verdict; a verdict that says "0 checked" is visibly
not a pass. And when a precondition rests on a check, run that check with the
subject absent and read its exit code: an opt-out and a pass share one.

### A check is proven by the red it can produce

A new check that passes on its first run is suspect, not reassuring. The only
evidence that an instrument measures is a red it produced on purpose: a forced
mutation, a defect planted in the subject that the check must reject. Three
forms, because each proves something the others do not:

- **The change reverted.** Proves the check sees the defect in the form just
  written — not the defect.
- **An equivalent form.** The same defect written another legal way: the
  command in a fenced block instead of inline, the sentence inverted with the
  same words, the path with a `./` in front. This is the mutation that finds
  holes, because text has many ways to say one thing and the check was
  written against one.
- **The subject removed.** When the check locates something before judging
  it, removing that thing must turn it red rather than leave it silent.

Pair every mutation with its negative twin — a case that must stay green —
or a fix that disables the check is indistinguishable from a fix that repairs
it. Apply each mutation with its outcome confirmed and predict the exact clause
that falls: a mutation that silently failed to apply measures nothing, and a
red from another clause is a finding, not a confirmation. When the red you
expected does not appear, suspect the instrument before the subject. If the
property leaves a trace in history, run the rule over the real history before
the check exists; it holds the forms that actually occur, not the ones its
author imagined.

**How to apply:** write the mutations before trusting the green, run the
baseline green first — with a red baseline every mutation "fails as expected"
and none discriminates — and measure against the single check, never through
the output of the whole gate, which can stop before printing the line you are
looking for.

### A check reads exactly what it judges

A check over code fails by not finding a symbol; a check over prose fails by
finding too much. Natural language repeats its own words in places that are
not the property, and the check approves on the neighbour's sentence. Three
shapes recur:

- **Scope wider than the judgement.** The clause reads the whole file and
  the paragraph next door already contains the words. The locator is inside
  the scope: the heading used to find a section names the very term the
  clause looks for, and satisfies it alone.
- **A value treated as a pattern.** A value read from a file and handed to a
  matcher as a regular expression is data, not a pattern: a row whose value is
  `.*` matches everything, and the membership test approves it. A name with a
  dot in it matches its misspellings.
- **Citing instead of doing.** A clause that requires a document to name the
  source of a fact buys traceability, not freshness; it passes while the
  document reads the fact from a stale cache.

A vocabulary belongs in the document that owns it, and the check reads it
there at run time; a list copied into the check ages silently the day the
document changes.

**How to apply:** read the body of a section, never its heading, and bound
each needle to the smallest unit that holds the property. Before fixing a
scope, search for the needle in that scope *without* the subject: if it is
found, the scope is too wide. Match values read from files as fixed strings,
and test with a metacharacter value, not only with an invented one. Prove a
check reads its vocabulary by changing the source and watching the same text
change verdict.

### The instrument fails before the check does

The commands used to measure a check lie too, and usually more quietly than
the check itself:

- A gate behind a pipe reports the pipe's last command: `check | tail -1 &&
  commit` commits over a red gate.
- A quiet match at the end of a pipe exits as soon as it matches, the writer
  dies of a broken pipe, and under `pipefail` a hit is read as a failure —
  intermittently, with the scheduler.
- A search for a whole sentence misses every copy the line wrap split.
- A range used as a field boundary keeps its terminating line, so a subject
  written just outside the field still counts.
- A needle built with nested quoting expands to nothing; the comparison never
  happens and the verdict is still `OK`, with errors on stderr nobody reads.
- A tool that names the defect in its report can still exit 0; a gate reads
  the exit code, not the report.
- A number written as a measurement, beside the command that would produce
  it, is a guess until the command runs.

**How to apply:** capture the gate's status directly (`./scripts/check > log;
rc=$?`), keep quiet matches off the end of pipes, search wrapped prose with a
fragment that cannot cross a line break, and rerun the positive control after
*any* change to how a check builds or escapes its pattern. Treat output on
stderr during a green run as a sign the green is void. Before adopting an
external tool as a gate, run it on a subject it must reject and read `$?`.

### A shipped check is read from where it is installed

A check written for one repository carries that repository's facts: the
directories it happens to have, the declarations it happens to make, the
exclusions that were true for its first subject. Shipped to others, each of
those becomes an assumption about every project. A presence test that was
right at home is wrong in a project that has not yet created the thing — and
a "does not apply here" written for the first subject silently excludes the
same case everywhere.

Absence means different things in different kinds of project entry. For
something the project must have, absence is red. For something born on first
use, absence before then is correct. For something the project may decline,
absence is an opt-out — unless the project's own history shows it once had
the thing, in which case it was lost, and that is red.

**How to apply:** ask of every path a shipped check reads, "from which
directory will this line be read?" — the answer is the installed copy, not the
source tree. Read the vocabulary from the convention installed beside the
check and find the project through the version-control tool, never from the
source repository's layout. Before shipping, reread every exclusion and every
"does not apply" the check inherited, and measure it on a project of the
*other* shape of each declaration it reads, starting from an empty one:
seeding the subjects first proves only the case that already worked.
