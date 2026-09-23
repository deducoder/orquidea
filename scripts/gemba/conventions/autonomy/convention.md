# Autonomy — Convention

> What turns a project's unattended mode on, the stops that mode can never run
> past, and what a project answers about it. The mode itself — the
> orchestrator that walks a version, and the human gates that read whether it
> is on — belongs to the skills that implement it; this file stops at what they
> read.

## What turns it on

```
conventions/autonomy/instance.md      in the adopting project, not here
```

**The file being there is the switch.** No file, and the mode is off: every
skill behaves exactly as it does without this convention, and nothing asks the
project to write one. Deleting the file is how the mode is turned off again,
so its absence is never read as a loss — whatever the project's history holds.

A file that is there but incomplete is not "off". It is a declaration nobody
finished, and the gate reads it as red: an empty value or a placeholder by the
shape every binding has ([`../bindings/convention.md`](../bindings/convention.md)),
a missing or unknown label by this convention's own check.

## Who writes it

**The agent, transcribing the human's answer — never on its own initiative.**
Turning the mode on is the one decision this mode exists to keep with a
person, so what a person gives is the decision, and the file is its
transcription. The supervisor of the unattended orchestrator writes it, and
only when the human, in that conversation, asks for an unattended run and
answers what it asks: whether to turn the mode on, which stops to add, and
through which channel a stop reaches them. It quotes the answer in the
binding's `Last verified`, writes nothing on an answer that does not turn the
mode on, and runs this convention's check on what it wrote. No other skill
writes or proposes the file, and an unattended session never creates or edits
it. The adoption steps do not ask for it either — the mode is off by default,
and a project that never wants it is never asked.

## The closed list

A stop is where unattended work halts and waits for a person, whatever the
binding says. The list is closed and shipped: a binding can add to it and never
take anything away. **Nothing reads this list from the binding.** Whoever needs
it reads the table below and adds what the binding declares, so a removal is
not something a binding can express.

### The stops

| Id | Stop | Origin |
|---|---|---|
| P1 | Promoting to `{production-branch}`: `release`, and `integrate`'s pause when its target is `{production-branch}` | never-go of unattended mode |
| P2 | Deleting or cancelling anything in an external system | never-go of unattended mode |
| P3 | A red gate the unattended session does not know how to fix | never-go of unattended mode |
| P4 | A `[stated]` criterion the work contradicts | confirmed by the census below — `story-design`, `epic-review` and `bug-analyse` each hand that question back to a person, because only whoever stated a criterion can drop it |
| P5 | A step the skill itself halts because what it needs is not there: a precondition that does not hold, a declaration that is missing, a dispatch that failed, a cause left unresolved | the rule unattended work already runs under — what is not written down is a stop, never a guess |

The ids are stable: a skill cites a stop by its id, and a new stop takes the
next free one rather than reusing a retired id.

**A decision taken without a person is not a stop.** It is the other never-go,
and it is closed differently: a gate answered without the human writes its
entry in the epic's decisions log before the step goes on, and a decision with
no entry was not taken. That rule belongs to the decisions log, not to this
table.

## The gates of the shipped skills

A shipped skill stops for a person in many places: it asks, it waits for an
acknowledgment, it hands a question back. Unattended work has to know, at each
one, whether it halts or answers. The census below says so, gate by gate. **The
skills are never edited for this mode**: an adopter cannot change them, so the
classification lives here, where the orchestrator reads it.

**The always-loaded core has gates too**, and they are censused the same way:
the unattended session carries the core wired into the project's `CLAUDE.md`
whatever skill it runs, so a pause the core asks for is a gate that session
meets. Its rows name `core` where a skill's rows name the skill, and their text
is a line of the shipped core. A pause read there with no row would be obeyed
the only way left — a question at the end of a turn, outside every stop and
every entry of the decisions log.

Each row names a skill, or `core`, a fragment of one line of its `SKILL.md`
or of the core exactly as written, and a class:

- **a stop id** (`P1`…) — the work halts there, as the stop says;
- **`decision`** — the orchestrator answers it, and writes the entry in the
  epic's decisions log **before** the step goes on. The entry's shape belongs
  to the decisions log's own convention, not to this table. An executor that
  meets a `decision` gate inside a dispatched block does not answer it: it
  stops and reports, and the orchestrator decides and writes. The log keeps
  one writer, because the orchestrator is the session that holds the
  development branch and runs every close;
- **`not a gate`** — the wording looks like a gate and is not one: the
  missing earlier phase a skill tells you to run first, which unattended work
  runs, or a step that says outright it does not wait.

### The gates

| Skill | Gate (exact text, one line of the SKILL.md or the core) | Class |
|---|---|---|
| bug-analyse | If it does not, **stop** and run | not a gate |
| bug-analyse | equally likely, **stop and escalate to a human** with the two strongest | P5 |
| bug-analyse | take it to the human as a question. | P4 |
| bug-close | If any is missing, **stop** and run the phase that produces it. | not a gate |
| bug-close | → **stop** and report | P5 |
| bug-close | the message to the human. Neither merge nor push | P5 |
| bug-close | stop and report it, because `-D` would destroy them. | P5 |
| bug-fix | If it does not, **stop** and run | not a gate |
| bug-fix | the fix is a specified delta: ask the human | decision |
| bug-fix | escalate to a human with the partial state documented. | P3 |
| bug-fix | ## 4 · Commit each task, pause for review | decision |
| bug-fix | Then pause and show the human | decision |
| bug-fix | say what it contains and let the human decide. | decision |
| bug-fix | no-longer-reproduces confirmation. It gets no artifact | not a gate |
| bug-plan | it does not, **stop** and run `bug-analyse` | not a gate |
| bug-review | If any of the three is not true, **stop** and | not a gate |
| bug-review | the human's approval if the plan was | not a gate |
| bug-triage | If it does not, **stop** and run | not a gate |
| bug-triage | analysis — do not wait for an answer. | not a gate |
| epic-close | present them and let the human choose | decision |
| epic-close | **Do not proceed until resolved** | decision |
| epic-close | Then ask the human what a developer new to the code would still find | decision |
| epic-close | missing — added failure modes are the most valuable. Human-reviewed before | decision |
| epic-close | nothing has drifted, say so and change nothing. Human-reviewed before | decision |
| epic-close | sections only — human-reviewed, never any other section | decision |
| epic-close | Human reviewed `docs.md` before shipping. | decision |
| epic-design | If it does not, **stop** and run | not a gate |
| epic-plan | If it does not, **stop** and run `epic-design` | not a gate |
| epic-plan | Present it to the human before starting the first story. | decision |
| epic-review | If any is still `todo`/`doing`, **stop** and resolve it | P5 |
| epic-review | stop and take it to the human, who stated it | P4 |
| epic-start | a tracker → stop and report it | P5 |
| security-review | **No binding declared → stop and say so.** | P5 |
| security-review | declaration and let the human decide whether to bind a tool | P5 |
| story-design | If it does not, **stop** and run | not a gate |
| story-design | a criterion the scope marks stated, take it to the human as a question | P4 |
| story-implement | If it does not, **stop** and run | not a gate |
| story-implement | ask the human once whether to | decision |
| story-implement | restate its intent in 2-3 sentences and confirm with the | decision |
| story-implement | stop and escalate with the partial state documented. | P3 |
| story-implement | Then show the human what changed and wait for acknowledgment | decision |
| story-implement | say what it contains and let the human decide. | decision |
| story-implement | and the acceptance confirmation. | not a gate |
| story-implement | fix it or escalate. | P3 |
| story-implement | Stop on the first defect; never accumulate errors | P3 |
| story-plan | If it does not, **stop** and run | not a gate |
| story-review | If either is not true, **stop** and finish `story-implement` | not a gate |
| story-review | acceptance confirmation, and the human's approval | not a gate |
| story-start | **stop and report** which key still blocks | P5 |
| spike | unreadable, **stop and report** which | P5 |
| spike | **stop and report** the mismatch rather than start it | P5 |
| bug-start | unreadable, **stop and report** which | P5 |
| bug-start | **stop and report** the mismatch rather than start it | P5 |
| story-close | → **not merging**; return it as a finding to the human | P5 |
| integrate | Fetch the target, then ask whether it carries content | not a gate |
| integrate | pause and ask for explicit human | P1 |
| integrate | confirmation before doing anything below** | P1 |
| integrate | target paused for explicit confirmation before | P1 |
| integrate | A **presented output**: rendered to the human, never written to a | not a gate |
| integrate | declares none, ask** — do not assume either. | P5 |
| release | Promote {dev-branch} to {production-branch} on demand | P1 |
| release | into step 4's confirmation; nothing is renamed before it. | P1 |
| release | its target-keyed confirmation pause | P1 |
| release | **A declared version that differs goes into the confirmation.** | P1 |
| release | confirmation → nothing ships, and nothing is renamed or marked. | P1 |
| release | full gate, confirmation pause, | P1 |
| release | **stop and report** that it is not a hotfix | P5 |
| release | Stop and report it: the promotion, the tag and the | P5 |
| release | A **presented output**: rendered to the human, never written to a file. | not a gate |
| debug | respect the box (escalate if exceeded) | P3 |
| debug | time-box respected — escalate if exceeded. | P3 |
| quality-review | A **presented output**: rendered to the human as this review's | not a gate |
| security-review | A **presented output**: rendered to the human as this review's result, | not a gate |
| research | independent confirmations | not a gate |
| research | Fewer than 3 confirmations means lower the | not a gate |
| architecture-review | has not decided its rung. Questions for the | decision |
| architecture-review | A **presented output**: rendered to the human as this review's | not a gate |
| adr | complete it to `accepted` once the decision exists | decision |
| delegate | never delegate on your own initiative without asking first. | decision |
| delegate | considering delegating unprompted — then **ask first** | decision |
| delegate | ask, and do nothing below until the answer is yes. | decision |
| delegate | otherwise stop and ask this session to set `none` in the plan it wrote | decision |
| delegate | contract is not met by any installed addon: **stop and say so** | P5 |
| delegate | prints `{sha}`. If it fails, stop and report. | P5 |
| delegate | prints `{base}`. If it fails, stop and report. | P5 |
| delegate | blocker — stop and report. | P5 |
| delegate | Blocked → stop and report; do not improvise past it. | P5 |
| delegate | every item: one notification per executor | not a gate |
| delegate | and wait for at most {limit}, the limit the dispatching technique names, in | not a gate |
| delegate | this skill stops and reports to | P5 |
| delegate | Stop, name the files, and do not merge either until the human has looked | P5 |
| delegate | stop, report it as a finding for the epic's review, never resolve it by hand | P5 |
| color | ## 2 · Propose the fitness criteria, then stop | decision |
| typography | ## 2 · Propose the fitness criteria, then stop | decision |
| logo | ## 2 · Propose the fitness criteria, then stop | decision |
| ui | ## 2 · Propose the fitness criteria, then stop | decision |
| core | show the work, explain the reasoning, let the human | not a gate |
| core | stop on incoherence, ambiguity or drift | P5 |
| core | ask before expensive | decision |
| core | conflict to surface to the human before the first commit it would | P5 |
| core | undeclared → ask before the first push. | P5 |
| core | **Stop on defects.** Do not accumulate; a red gate is fixed, not bypassed. | P3 |
| core | **Pause for human review by default** after significant work | decision |

### Skills outside the mode

The orchestrator walks a version a person already declared. It adopts no
project and opens or closes no session, so it never runs these, and their
gates stay the person's:

| Skill | Why |
|---|---|
| project-create | adoption, once per project |
| project-onboard | adoption, once per project |
| tracker-bind | a binding is verified live by a person |
| problem-shape | shaping a problem precedes any version |
| version-plan | declaring the version is what the mode walks, not part of the walk |
| session-start | a session belongs to the person who opens it |
| session-close | a session belongs to the person who closes it |
| orchestrate | the mode itself: its stops are the closed list, not gates the mode walks |

## The binding's two questions

Two, and only the first is required. The switch is the file itself and the
stops are shipped, so a binding is asked what it **adds** to a closed list and
nothing about narrowing it. The second is optional because its absence has to
mean the safe answer, which is the paragraph after the table:

### What the binding answers

| Label | Required | Answers |
|---|---|---|
| Added stops | yes | The stops this project adds to the shipped list, or that it adds none |
| Delegated approvals | no | Whether the orchestrator may approve fitness criteria on the person's behalf. Absent, it may not |

A label outside this table is red, whatever it says: `Removed stops`,
`Disabled stops` or a bare `Stops` have no meaning here, and reading one as a
harmless extra would let a binding appear to narrow the list.

**Without `Delegated approvals`, the fitness approval halts the run, and no
new rule had to be written to say so.** The census classifies that pause
`decision`, and a decision the orchestrator answers on the person's behalf
needs this binding to say that it may. Left unanswered, the declaration that
decision needs is not there — which is already `a declaration that is
missing`, P5 by its own wording in `### The stops` above. That is the
asymmetry, and it is why this label **supplies a declaration** instead of
removing a stop: a binding still has no way to narrow the closed list, and a
project that says nothing keeps the behaviour it has today.

**Approving is not signing.** The label authorises answering the approval
pause. It does not make a judgement of the `judgement` stratum signed: a
judgement with no person behind it is still written `unsigned` and still named
among the criteria left unanswered. Two distinct acts, and a binding that
delegates the first delegates nothing of the second.

**Write text on the label's own line.** The shape every binding has reads a
value up to its first structural line, and a nested bullet is one: a
`- **Added stops:**` with nothing after it and its stops in bullets below reads
as an empty answer. Say how many, then list them:

```markdown
# Autonomy — Instance binding

> What this project answers to the unattended orchestrator and to every human
> gate that reads whether unattended mode is on: it is, and these are the stops
> it adds. Facts about this project, not a generic rule: that is why this file
> lives here and not in the plugin.

- **Added stops:** one, beyond the shipped list.
  - Any change under `governance/`.

## Last verified

2026-01-31: a real notice sent through the notifications binding and seen arrive.
```

An added stop never opens with a shipped id. Writing `P1 only when …` under
`Added stops` is an attempt to redefine P1, and the check reads it as one.

## What else it needs

**A notifications binding** (`conventions/notifications/instance.md`). A stop
pushes a notice so that someone knows to come back; with the mode on and no
channel bound, the work halts and nobody learns it did. The check reads the
two together and turns red when the autonomy binding is there without the
notifications one.

**A harness that lets a background session edit the project's checkout.**
The unattended session works on the development branch in the project's own
checkout, and a harness may guard against exactly that: Claude Code refuses
every edit a background session makes there until it moves to a worktree,
unless `.claude/settings.json` carries `"worktree": {"bgIsolation": "none"}`.
Like the autonomy binding, the supervisor writes that switch only from the
human's answer — lifting a harness guard is a decision about the project, not
something the mode grants itself — merged into the settings the project
already has, and the unattended session halts before touching anything when
it is missing.

## Outside this section

- **What a skill does at a stop** — how it halts, what it reports, how the
  notice is worded — belongs to the skills that implement the mode.
- **The shape of a decisions-log entry** belongs to the decisions log's own
  convention; `### The gates` only says which gates write one.
- **Whether a project's gate enforces the binding** is the project's own call.
  The binding's check travels beside this file, in `checks/`: a project that
  wants its gate to hold it copies it in with `/gemba:checks` and runs it from
  its own `./scripts/check`. The census of the gates is checked where the
  skills are written, not in an adopting project, which does not carry them.
