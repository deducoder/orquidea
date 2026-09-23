#!/usr/bin/env bash
# Verifies: the git convention, `### What marks each phase on the work item's branch`; the core's work-items table
#
# Property: the commits of a work item's branch follow the order of its cycle,
# so a task committed before its plan is caught by the project's own gate and
# not by a session that happens to remember the rule.
#
# P0 — what the check reads is there: a git work tree, the dev branch the
#      project declares, the branch kind's row in the work-items table of the
#      project's CLAUDE.md, and the table of phase marks in the convention
#      beside this file. Anything missing is red, never an opt-out.
# P1 — every task commit on the branch has, earlier on it, the mark of the
#      phase the cycle puts just before `implement` (`fix`, in a bug): its plan.
# P2 — the work item's first phase mark is its cycle's first phase, and every
#      phase appears for the first time after every phase its cycle puts later
#      and that already appeared has not. The ORDER is judged, never the
#      presence: the method does not declare which phases a work item may
#      skip — a story may plan with no design — so a phase that never appears
#      is not a finding here.
# P3 — a `re-{phase}` comes after its `{phase}`: a phase can be re-emitted
#      only once it has been emitted.
#
# Where the order comes from: the core's work-items table, wired into the
# project's CLAUDE.md, and only there — this file carries no cycle. What marks
# each phase comes from the table beside it: `start` is `initialize`,
# `implement`/`fix` are task commits of the four types that row names,
# `close` leaves nothing on the branch, and any other phase is
# `chore({scope}): {phase}`.
#
# What is judged: the first-parent commits of the branch that the dev branch
# does not have yet — the dev branch as it stands locally, since a story under
# an epic merges locally and is never pushed before the epic's close. A phase
# mark is looked for in the whole first-parent history of HEAD, so a branch
# whose earlier part already reached the dev branch still finds its plan.
#
# Measured before this check existed, over 142 merged story/ and bug/ branches
# of the repository that builds this plugin: no task before its plan once a
# task is what the table says it is. Counting every commit scoped to something
# other than the work item gave six reds, all of them meta-work — parking an
# entry, landing a research, closing a session — which is why the task types
# are read from the table and not inferred from the scope.
#
# DECLARED LIMITS: the kind and key come from the branch name, so a branch
# not named story/{scope}/{slug} or bug/{scope}/{slug} is not judged — it
# leaves by the opt-out below. Epics have no branch and spikes are deleted
# unmerged, so neither has a history here to judge. The commit being made is
# not judged by the run that precedes it: a hook that runs this before a
# commit sees the one after the offending commit. The dev branch is read
# locally first, then from `origin`.
#
# A task typed `docs` is not a task here. The table says a task commit is one
# of four types, and this check follows the table rather than the practice
# around it: in the same 142 branches, 7 typed their tasks `docs({area})`, so
# a `docs` task committed before its plan would pass unseen. None of the 7 did,
# measured — every `docs` commit scoped to something else before a plan was
# meta-work — but the gap is real, and it closes where the rule is, not here.

set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the order is read from a branch's commits, so no repository is red, not an opt-out"
  exit 1
}
cd "$root" || exit 1

branch=$(git symbolic-ref --quiet --short HEAD 2>/dev/null)
case "$branch" in
  story/?*/?*|bug/?*/?*) ;;
  *) echo "check-phase-order: opt-out — ${branch:-a detached HEAD} is not a story/ or bug/ branch, so there is no cycle to judge"; exit 0 ;;
esac
kind=${branch%%/*}
rest=${branch#*/}
key=${rest%%/*}

decl=CLAUDE.md
[ -f "$decl" ] || decl=.claude/CLAUDE.md
[ -f "$decl" ] || {
  echo "P0 FAIL: neither CLAUDE.md nor .claude/CLAUDE.md exists, so the cycle a $kind/ branch follows cannot be read"
  exit 1
}

# The cycle, from the kind's row of the work-items table: `| **story** | a → b |`.
cycle=$(awk -F'|' -v k="**$kind**" '
  { c = $2; gsub(/^ +| +$/, "", c) }
  c == k { v = $3; gsub(/^ +| +$/, "", v); print v; exit }' "$decl")
[ -n "$cycle" ] || {
  echo "P0 FAIL: $decl has no \`| **$kind** | … |\` row in its work-items table, so the cycle a $kind/ branch follows cannot be read"
  exit 1
}

# The marks, from the convention's table: one "phase<TAB>mark" line per phase
# the table names, and "*" for its catch-all row. A mark is WORD:{word},
# TASK:{types} or NONE.
conv="$here/../convention.md"
marks=$(awk '
  /^#+ / { f = ($0 ~ /^### What marks each phase on the work item.s branch$/); next }
  f && /^\|/ && !/^\| *Phase *\|/ && !/^\|[-| ]+\|$/ {
    split($0, c, "|"); p = c[2]; m = c[3]; mark = "NONE"
    if (m ~ /chore\(\{scope\}\): /) {
      w = m; sub(/.*chore\(\{scope\}\): /, "", w); sub(/`.*/, "", w); mark = "WORD:" w
    } else if (m ~ /task commit/) {
      t = m; types = ""
      while (match(t, /`[a-z]+`/)) { types = types " " substr(t, RSTART + 1, RLENGTH - 2); t = substr(t, RSTART + RLENGTH) }
      mark = "TASK:" substr(types, 2)
    }
    if (p ~ /any other/) { print "*\t" mark; next }
    q = p
    while (match(q, /`[a-z]+`/)) { print substr(q, RSTART + 1, RLENGTH - 2) "\t" mark; q = substr(q, RSTART + RLENGTH) }
  }' "$conv" 2>/dev/null)
[ -n "$marks" ] || {
  echo "P0 FAIL: $conv has no \`### What marks each phase on the work item's branch\` table, so no phase can be recognised on the branch"
  exit 1
}

# The cycle as marks, in order: each phase's word, or TASK for the one the
# task commits stand for; a phase that leaves no mark drops out.
seq=""; types=""
IFS='→' read -ra phases <<< "$cycle"
for ph in "${phases[@]}"; do
  ph=$(printf '%s' "$ph" | tr -d ' ')
  [ -n "$ph" ] || continue
  m=$(printf '%s\n' "$marks" | awk -F'\t' -v p="$ph" '$1 == p { print $2; exit }')
  [ -n "$m" ] || m=$(printf '%s\n' "$marks" | awk -F'\t' '$1 == "*" { print $2; exit }')
  case "$m" in
    "WORD:{phase}") seq="$seq $ph" ;;
    WORD:*) seq="$seq ${m#WORD:}" ;;
    TASK:*) seq="$seq TASK"; types=${m#TASK:} ;;
    *) ;;
  esac
done
seq=${seq# }
case " $seq " in
  *" TASK "*) ;;
  *) echo "P0 FAIL: the $kind cycle in $decl ($cycle) has no phase the table in $conv marks with task commits, so no task can be told apart"; exit 1 ;;
esac

dev=$(sed -n 's/^- \*\*Dev branch:\*\* `\([^`]*\)`.*/\1/p' "$decl" 2>/dev/null | head -1)
[ -n "$dev" ] || {
  echo "P0 FAIL: $decl declares no \`- **Dev branch:** \`name\`\`, so the commits this branch adds cannot be told from the ones it started from"
  exit 1
}
base=""
for b in "refs/heads/$dev" "refs/remotes/origin/$dev"; do
  git show-ref --verify --quiet "$b" && { base=$b; break; }
done
[ -n "$base" ] || {
  echo "P0 FAIL: neither $dev nor origin/$dev exists, so the commits this branch adds cannot be located"
  exit 1
}

inrange=$(git rev-list --first-parent "$base..HEAD" 2>/dev/null)

# The walk, oldest first over HEAD's first-parent history. A mark of this
# work item is `chore({key}): {word}`, compared as data — a local id such as
# `s3.2` carries a dot a pattern would read as any character.
out=$(git log --reverse --first-parent --format='%H %s' HEAD 2>/dev/null | awk \
  -v key="$key" -v kind="$kind" -v cyc="$cycle" -v seq="$seq" -v types="$types" -v r="$inrange" '
  BEGIN {
    n = split(seq, S, " ")
    for (i = 1; i <= n; i++) {
      if (S[i] == "TASK") { before = S[i - 1] } else { known[S[i]] = 1; rank[S[i]] = i; if (first == "") first = S[i] }
    }
    nt = split(types, T, " "); for (i = 1; i <= nt; i++) istype[T[i]] = 1
    nr = split(r, R, "\n"); for (i = 1; i <= nr; i++) if (R[i] != "") inr[R[i]] = 1
  }
  {
    sha = $1; subj = substr($0, length($1) + 2); short = substr(sha, 1, 7)
    if (subj ~ /^chore\([^()]+\): [a-z-]+$/) {
      sc = subj; sub(/^chore\(/, "", sc); sub(/\).*/, "", sc)
      if (sc == key) {
        w = subj; sub(/^[^:]*: /, "", w)
        base = w; if (base ~ /^re-/) base = substr(base, 4)
        if (!(base in known)) next
        if (sha in inr) phases++
        if (w ~ /^re-/ && (sha in inr) && !(base in seen)) {
          printf "P3 FAIL: %s %s re-emits a %s that %s has not committed yet (%s: %s)\n", short, subj, base, key, kind, cyc
          bad = 1
        }
        if (w !~ /^re-/ && !(w in seen)) {
          if (sha in inr && w != first && !(first in seen)) {
            printf "P2 FAIL: %s %s comes before %s%ss %s (%s: %s)\n", short, subj, key, "\047", first, kind, cyc
            bad = 1
          } else if (sha in inr && rank[w] < maxr) {
            printf "P2 FAIL: %s %s comes after %s%ss %s, which its cycle puts later (%s: %s)\n", short, subj, key, "\047", maxw, kind, cyc
            bad = 1
          }
          if (rank[w] > maxr) { maxr = rank[w]; maxw = w }
        }
        seen[w] = 1
        next
      }
    }
    if (!(sha in inr)) next
    ty = subj; sub(/\(.*/, "", ty)
    if ((ty in istype) && subj ~ /^[a-z]+\([^()]+\): /) {
      tasks++
      if (!(before in seen)) {
        printf "P1 FAIL: %s %s is a task before %s%ss %s (%s: %s)\n", short, subj, key, "\047", before, kind, cyc
        bad = 1
      }
    }
  }
  END { printf "COUNTS %d %d\n", phases, tasks; exit bad }')
rc=$?

printf '%s\n' "$out" | sed '/^COUNTS /d'
set -- $(printf '%s\n' "$out" | sed -n 's/^COUNTS //p')
count() { if [ "$1" -eq 1 ]; then printf '1 %s' "$2"; else printf '%s %ss' "$1" "$2"; fi; }
[ "$rc" -eq 0 ] && echo "check-phase-order: OK ($kind $key: $(count "${1:-0}" 'phase commit') and $(count "${2:-0}" task) judged against $cycle, read from $decl)"
exit $rc
