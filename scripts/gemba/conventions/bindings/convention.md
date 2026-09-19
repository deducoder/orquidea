# Bindings — Convention

> The shape of a domain binding: the file in which a project answers, for
> itself, what a shipped convention deliberately leaves open.
>
> **Scope:** this convention fixes the **shape**, never the questions. Which
> questions a domain asks belongs to that domain — to its own convention where
> it has one, and otherwise to the adoption step that asks them. This file
> says how the answers are written down, so that every domain's binding looks
> like every other's.

## Why a shape, and why here

A convention that ships with the method describes what is true of the method.
What is true of **one project's real instance** — which tracker, which
scanner, which channel — cannot ship, because nobody writing the method knows
it. So the method ships the question and the project writes the answer, and
the answer is a binding.

There have been several, and their shape was fixed by reference: each one was
to look like the one before it. That works only for whoever can see the one
before it. An adopter who has the method and not the project that built it has
nothing to look at, invents a shape, and the next adopter invents a different
one — at which point no tool and no reader can treat the two as the same kind
of file. The shape is written here so that it travels.

## Where a binding lives

```
conventions/{domain}/instance.md
```

One directory per domain that needs a binding, in the adopting project and
never in the plugin. A project with no such domain writes none, and nothing
asks it to. The directory exists **because** the domain was bound: one that
holds no `instance.md` is an unfinished binding, not an empty slot.

## The four parts

Every binding has these four, in this order, and nothing is optional:

1. **A title naming the domain.** `# {Domain} — Instance binding`. The domain
   is the directory's own name, capitalised. It reads as the answer to "a
   binding of what?", which is the first thing a reader needs.

2. **A blockquote saying what this project answers, and to whom.** Name the
   step, review or skill that reads the file and would otherwise stop without
   it, and close by saying that what follows are **facts about this instance,
   not a generic rule — which is why the file lives in the project and not in
   the plugin**. That last clause is not decoration: it is what stops the next
   reader from promoting a local answer into a method-wide one.

3. **The facts, one per line, as `- **Label:** the concrete value`.** One
   label per question the domain asks, and the value is what this project
   actually runs, reads or sends — a name, an identifier, a path, a verified
   behaviour. A value may run on for several lines; it may not run out. Where
   the answer has structure of its own, nest it under its label rather than
   inventing a second top-level shape.

4. **`## Last verified`.** That heading, with those words, as the last section
   of the file — then the date, and **what was read live to know it**. Not
   when the file was edited: when the claim was last confirmed against the
   real thing. A binding that does not say when it was true reads as current
   forever, and a stale binding is acted on exactly like a fresh one.

### The four parts, as they look written

```markdown
# Notifications — Instance binding

> What this project answers to the skills that need to say the work stopped.
> Facts about this project, not a generic rule: that is why this file lives
> here and not in the plugin.

- **Channel:** the terminal this method already runs in — no second channel.
- **What is pushed:** only what stops the work; routine progress never.

## Last verified

2026-01-31: a real message sent from a session and seen arrive.
```

## `none` is an answer, and it has a form

For any domain, `none` — no tool, no channel, nothing wired — may be the
honest answer. It becomes a **binding** only when the value cites an accepted
decision record of the adopting project. A line that merely transcribes a
refusal cannot be told apart from nobody having decided, and the two deserve
opposite treatment: the first is respected, the second is a gap someone still
has to close.

An answer of `none` also says what the reader of the binding should do
instead, and under what condition the decision would be revisited.

## Verified live, never guessed

Every value is read from the real instance before it is written. A guessed
binding is worse than an absent one: an absent binding stops whoever needs it,
and a guessed one is believed and acted on. Where a value was not confirmed,
the binding says so in that value's own words rather than leaving the reader
to assume it was.

Re-verification is the same operation as the first: read it live again, and
move the date. Copying a value forward from this file — or from another
project's — is the one thing the shape exists to prevent.

## Outside this section

- **Which questions each domain asks** belongs to that domain, not here. A
  domain with enough of its own to say carries a convention beside this one —
  [`../security/`](../security/convention.md) is the worked example, and
  [`../autonomy/`](../autonomy/convention.md) the one whose binding nobody asks
  for: the human writes it by hand, and its presence is the switch; a domain
  without one has its questions asked by the adoption step that collects them.
- **That a project has a `conventions/` directory at all**, what kind of entry
  it is and who creates it, is declared once in
  [`../project/`](../project/convention.md), which this file does not repeat.
- **Whether a project's gate enforces this shape** is the project's own call,
  the same as everything else it chooses to check. The shape travels as a
  norm, and its check travels beside it, in `checks/`: a project that wants
  its gate to hold the shape copies it in with `/gemba:checks` and runs it
  from its own `./scripts/check`.
