#!/usr/bin/env bash
# Verifies: the bindings convention, `## The four parts` and `## Last verified`
# Property: EVERY instance binding this project writes carries the four parts
# of the shape the core ships, its verification section is named as the shape
# names it and carries a date, and no value it answers is left unresolved or
# empty.
#
# The population is the group — every `conventions/{domain}/` — and never a
# list of domains written here: a fourth domain must be watched the day it
# lands, not the day someone remembers to add it. The count is printed so a run
# over zero directories cannot read as green; a check with no subjects is
# watching nothing.
#
# P0 — `conventions/` exists, holds at least one domain, and every domain
#      directory carries an `instance.md`. A domain directory exists because
#      the domain was bound, so one without its binding is RED, never "nothing
#      to check": a clause that cannot find its subject otherwise reads as
#      approval.
# P1 — the four parts of the shape, one clause each, because three of four is
#      what a single clause accepts:
#      P1a the H1 `# {Domain} — Instance binding`;
#      P1b a blockquote as the first thing after it, which is where a binding
#          says what this project answers and to whom;
#      P1c at least one fact written as `- **Label:** value`;
#      P1d a `## Last verified` section carrying a date.
# P2 — no value is an unresolved placeholder or empty.
#
# WHY P1d IS TWO CONDITIONS, AND NAMED SO. The heading has to be present AND
# carry a date, because the two failures are the same defect written two legal
# ways: a real adoption wrote its date section as `## Verificación en vivo`
# instead, and a section can equally keep the right name and say nothing about
# when. A binding that does not say when it was true reads as current forever.
# The heading is matched whole and exact: the shape names this section, and a
# check that accepted any heading with a date in it would approve the rename
# that motivated it.
#
# A VALUE IS THE WHOLE BULLET, continuation lines included. Measured while
# writing this: a tracker binding answered `- **Parent link:**` over three
# lines, and reading only the first missed everything after it. Folding is what
# makes P2 read the value the author wrote rather than its first line.
#
# CODE SPANS ARE STRIPPED BEFORE P2 LOOKS FOR A PLACEHOLDER, and that is not a
# convenience. Measured: a tracker binding writes `` `parent = {PARENT-KEY}` ``
# as a fact — a real answer that quotes the syntax of a query — and a check
# that read braces anywhere would turn a correct file red. A placeholder inside
# a code span is being quoted, not left unanswered.
#
# DECLARED LIMIT, and it is the one the scope was rewritten around: this sees a
# value that is ABSENT or still in template notation, never one that is merely
# vague. Telling "the harness notification this method runs under" from "some
# channel" is judgement, and it is read by a person at review. A proxy for
# concreteness was measured and rejected: across three real, correct bindings
# the share of fact lines carrying a backtick ran from most to none, so any
# such proxy reddens good files.
#
# Why: a binding's shape was fixed by reference — "the same shape the one above
# uses" — and lived in no shipped document and in no check. The first adoption
# that went looking for it produced a file with another structure and another
# name for its date section.

# Where it runs: shipped beside the bindings convention, and run by a
# project's own ./scripts/check with the project as the git work tree it runs
# inside — never a path derived from this file's location. It reads nothing
# from the convention: its clauses are the shape.

set -uo pipefail
top=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the bindings live in the project, so no repository is red, not an opt-out"
  exit 1
}
cd "$top" || exit 1

root=conventions

# P0 — the group itself is a subject, once the project has had one. The
# project model makes `conventions/` per domain: born when a domain is bound,
# so a project that never bound one has none and that is correct. What tells
# the two apart is the project's own history: a binding it once committed and
# no longer holds is a loss, and red.
if [ ! -d "$root" ]; then
  if [ -n "$(git log -1 --format=%h -- "$root/*/instance.md" 2>/dev/null)" ]; then
    echo "P0 FAIL: $root/ does not exist, and this project's history holds instance bindings — they were bound and are gone"
    exit 1
  fi
  echo "check-binding-shape: opt-out — no domain bound yet, no instance binding in the tree or in its history"
  exit 0
fi

# Each `- **Label:** value` bullet folded onto one line, continuation lines
# included. A blank line, a new bullet, or any other structural line ends it.
fold() {
  awk '
    /^[[:space:]]*- \*\*[^*]+:\*\*/ { if (b != "") print b; b = $0; next }
    /^[[:space:]]*$/                { if (b != "") { print b; b = "" } next }
    /^[[:space:]]*[-*|#>]/          { if (b != "") { print b; b = "" } next }
    b != ""                         { sub(/^[[:space:]]+/, " "); b = b $0 }
    END { if (b != "") print b }
  ' "$1"
}

rc=0
n=0
nvalues=0

for dir in "$root"/*/; do
  [ -d "$dir" ] || continue
  n=$((n + 1))
  domain=$(basename "$dir")
  f="${dir}instance.md"

  if [ ! -f "$f" ]; then
    echo "P0 FAIL: $root/$domain/ carries no instance.md — the directory exists because the domain was bound, so a missing binding is the defect and not the absence of one"
    rc=1
    continue
  fi

  # --- P1a — the H1 ---------------------------------------------------------
  head -n 1 "$f" | grep -E '^# .+ — Instance binding$' >/dev/null || {
    echo "P1a FAIL: $f does not open with \`# {Domain} — Instance binding\` (found: $(head -n 1 "$f"))"
    rc=1; }

  # --- P1b — the blockquote, first thing after the H1 -----------------------
  firstline=$(tail -n +2 "$f" | grep -m1 -vE '^[[:space:]]*$')
  case "$firstline" in
    '>'*) ;;
    *) echo "P1b FAIL: $f has no blockquote after its H1 — that is where a binding says what this project answers and to whom, and that these are facts rather than a generic rule"
       rc=1 ;;
  esac

  # --- P1c — the facts ------------------------------------------------------
  nf=$(grep -cE '^[[:space:]]*- \*\*[^*]+:\*\*' "$f" || true)
  [ "$nf" -ge 1 ] || {
    echo "P1c FAIL: $f answers nothing as \`- **Label:** value\` — a binding with no facts in it binds nothing"
    rc=1; }

  # --- P1d — the verification section, named and dated ----------------------
  if ! grep -qx '## Last verified' "$f"; then
    last=$(grep -E '^## ' "$f" | tail -n 1)
    echo "P1d FAIL: $f has no \`## Last verified\` section${last:+ (its last section is \`$last\`)} — the shape names this section, and a binding that does not say when it was true reads as current forever"
    rc=1
  elif ! awk '/^## Last verified$/ { s = 1; next } s' "$f" | grep -E '[0-9]{4}-[0-9]{2}-[0-9]{2}' >/dev/null ; then
    echo "P1d FAIL: $f has a \`## Last verified\` section with no date in it — the heading without the date is the same defect written a legal way"
    rc=1
  fi

  # --- P2 — no value unresolved or empty ------------------------------------
  while IFS= read -r v; do
    [ -n "$v" ] || continue
    nvalues=$((nvalues + 1))
    label=$(printf '%s' "$v" | sed -nE 's/^[[:space:]]*- \*\*([^*]+):\*\*.*/\1/p')
    if printf '%s' "$v" | grep -E '^[[:space:]]*- \*\*[^*]+:\*\*[[:space:]]*$' >/dev/null ; then
      echo "P2 FAIL: $f answers \`$label\` with nothing — an empty value is a question nobody came back to"
      rc=1
      continue
    fi
    if printf '%s' "$v" | sed 's/`[^`]*`//g' | grep -E '\{[^}]*\}' >/dev/null ; then
      echo "P2 FAIL: $f answers \`$label\` with a placeholder still in template notation — a binding is read and acted on, so an unfilled field is worse than an absent one"
      rc=1
    fi
  done < <(fold "$f")
done

[ "$n" -eq 0 ] && { echo "P0 FAIL: $root/ holds no domain — the check would be watching nothing"; rc=1; }

[ "$rc" -eq 0 ] && echo "check-binding-shape: OK ($n binding(s), $nvalues values: P1 the four parts with a dated \`## Last verified\`, P2 none unresolved or empty)"
exit $rc
