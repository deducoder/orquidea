# Memory — Rules (restrictions and guards)

> Restrictions that surround the memory store but are not the shape of it —
> where memory lives and how the harness reads it is `convention.md`. These
> govern what must move together.

## R1 — An index entry and its file move in the same commit

`MEMORY.md` is the only memory artifact loaded into every session: a leaf file
is read on recall, its index line is read always. So the line is not a
convenience copy of the file — it is what a reader is told first, and often
all they are told.

Whenever a memory file moves past what its line says — a new instance, a
widened scope, a claim its own file has since qualified — **the line is
rewritten in the same commit**. Not in a follow-up, and not "when someone
notices": an index line has no reader who will discover it is wrong, because
the reader who consults it is precisely the one not opening the file.

This binds the **update** path, which is the one that rots. Creating a memory
already carries an obvious pointer step; refreshing one does not, and a
refresh is the common case.

## R2 — Fix a line by role, never by incrementing its count

An index line that restates a file's contents — "three instances", an
enumeration of ids, a list of the cases covered — has to be re-edited every
time the file grows, and is one edit away from disagreeing with itself. When
such a line is found stale, the fix is to state what the file *is about* and
let the file keep the enumeration, not to bump the number and wait for the
next drift.

The failure this prevents is not hypothetical in either direction: a line
reading "seven confirmed instances" beside an enumeration of six is the
same defect twice — once for being behind, once for being self-contradicting
while behind.

## R3 — Every memory file is reachable from the index, or exempt with a reason

A memory nobody indexed is a memory nobody recalls. Every file in the memory
directory has an index entry, except where a file is deliberately something
other than a fact — a store the index reaches by another route — in which case
the exemption is written down with its reason rather than left as an absence
somebody has to re-derive.

## R4 — The index is bounded by bytes; going over consolidates, never raises the bound

`MEMORY.md` is the **always-loaded tier**. `authoring.md` already draws that
line for skills — light metadata always in context, heavy resources loaded on
demand with no size limit — and the memory store is the same split: the index
is read every session, a leaf file only on recall. An always-loaded artifact
with no load budget is the one gap that split left open.

So the index is bounded at **20,480 bytes**. Where the project provides a
gate entry point, a check over that bound belongs in it; where it does not,
this is a rule with no mechanism behind it — the same opt-out the gates
convention already grants, and the same standing cost it names. The check
ships beside this file, in `checks/check-memory-index.sh`; `/gemba:checks`
copies it into a project whose own `./scripts/check` then runs it. Nothing
runs it for a project that does not.

The bound exists because going over is **silent**. Past the harness's load
limit the index is truncated, and a truncated entry is indistinguishable, from
inside the session, from a memory nobody ever wrote — the reader is told less
than the index says and is not told that.

**When the bound is exceeded, consolidate downward.** Shorten the line to the
file's role, which R2 already requires, and let the leaf file keep the detail: the
on-demand tier has no size limit, so nothing is lost by moving content into it.
**Do not raise the bound to fit.** Raising it belongs to a decision that
supersedes the one below, argued with its own evidence — never to whoever is
standing in front of a red gate.

