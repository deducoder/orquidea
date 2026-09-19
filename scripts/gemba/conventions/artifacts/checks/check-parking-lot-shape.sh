#!/usr/bin/env bash
# Verifies: artifacts rules R4
#
# Property: the parking lot has the shape the artifacts convention's R4 fixes.
# It is the method's destination for anything named and not opened, the most
# append-only file in the project, and the one several skills write to.
#
# P1 — exactly one "## Open items" and one "## Retired".
# P2 — the archive goes below the live items, so a reader meets deferred work
#      before its archive (R4's own wording).
# P3 — every OPEN entry carries an *Origin:*. An entry belongs to whoever wrote
#      it, and without its origin nobody can weigh it later.
# P4 — every RETIRED record carries a **Why:** and a **Swept:**. The mirror of
#      P3: the archive answers with the two fields the record creates, and the
#      sweep is the one thing git cannot reconstruct once the entry is gone.
# P5 — no retired record carries *Origin:* or *Promotion:*. Those belong to a
#      live entry; carrying them means the entry was moved whole, which is the
#      defect the compact record exists to end — and P4 alone passes on it.
#
# *Promotion:* IS NOT REQUIRED, and that is a decision, not an oversight. R4
# asks for origin and promotion condition, but an entry can be written only so
# that a count is complete, not as deferred work, and it says so in its own
# text instead of naming a promotion. That third kind — the entry of record —
# is one the rule does not contemplate; requiring the field would fail entries
# the convention itself allows.
#
# Why: a merge resolution that keeps both sides of this file leaves two
# "## Retired" sections full of byte-identical duplicates, and nothing sees it
# unless something reads the file's shape.
#
# Where it runs: shipped beside the artifacts convention, and run by a
# project's own ./scripts/check. The project is the git work tree it is run
# inside, never a path derived from this file's location.

set -uo pipefail
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the parking lot is a versioned artifact of the project, so no repository is red, not an opt-out"
  exit 1
}
cd "$root" || exit 1

f=records/parking-lot.md
# The project model makes records/ lazy: the parking lot is born on the first
# park, so a project that never parked anything has none and that is correct.
# One it once committed and no longer holds is a loss — the project's own
# history is what tells the two apart.
if [ ! -f "$f" ]; then
  if [ -n "$(git log -1 --format=%h -- "$f" 2>/dev/null)" ]; then
    echo "P0 FAIL: $f is missing, and this project's history holds it — its deferred findings are lost, not an opt-out"
    exit 1
  fi
  echo "check-parking-lot-shape: opt-out — nothing parked yet, no parking lot in the tree or in its history"
  exit 0
fi

rc=0

open_lines=$(grep -n '^## Open items$' "$f" | cut -d: -f1)
retired_lines=$(grep -n '^## Retired$' "$f" | cut -d: -f1)
n_open=$(printf '%s\n' "$open_lines" | grep -c .)
n_retired=$(printf '%s\n' "$retired_lines" | grep -c .)

# --- P1 -----------------------------------------------------------------
for pair in "Open items:$n_open:$open_lines" "Retired:$n_retired:$retired_lines"; do
  name=${pair%%:*}; rest=${pair#*:}; n=${rest%%:*}; where=${rest#*:}
  if [ "$n" -ne 1 ]; then
    echo "P1 FAIL: $f has $n \"## $name\" sections, at line(s) $(printf '%s' "$where" | tr '\n' ' '); there is exactly one of each (artifacts rules R4)."
    rc=1
  fi
done

# --- P2 -----------------------------------------------------------------
if [ "$n_open" -eq 1 ] && [ "$n_retired" -eq 1 ] && [ "$open_lines" -gt "$retired_lines" ]; then
  echo "P2 FAIL: \"## Retired\" (line $retired_lines) comes before \"## Open items\" (line $open_lines); the archive goes below the live items (artifacts rules R4)."
  rc=1
fi

# --- P3 -----------------------------------------------------------------
# Open entries only: everything above the Retired heading. A retired entry is
# already archived and carries a Swept: record instead.
open_count=0; retired_count=0
# The FIRST Retired heading bounds the open section. Taking $retired_lines
# whole would hold two numbers when P1 is already failing, and the awk
# comparison against that string silently counts retired entries as open —
# measured: the first RED of this clause reported three false P3 failures.
if [ "$n_retired" -ge 1 ]; then
  boundary=$(printf '%s\n' "$retired_lines" | head -1)
else
  boundary=$(wc -l < "$f")
fi

missing=$(awk -v b="$boundary" '
  NR >= b { exit }
  /^- \*\*/ { if (started && !seen) print title; started = 1; seen = 0; title = $0 }
  /^[[:space:]]*\*Origin:\*/ { seen = 1 }
  END { if (started && !seen) print title }
' "$f")
if [ -n "$missing" ]; then
  while IFS= read -r m; do
    [ -n "$m" ] || continue
    echo "P3 FAIL: an open entry carries no *Origin:* — an entry belongs to whoever wrote it, with its origin (artifacts rules R4):"
    printf '         %s\n' "$(printf '%s' "$m" | cut -c1-90)"
    rc=1
  done <<EOF
$missing
EOF
fi

# --- P4 -----------------------------------------------------------------
# Retired records only: everything BELOW the Retired heading — the mirror of
# P3, which asks the live section for *Origin:*. A record answers with Why:
# and Swept: instead. Swept: is the field with a cost attached: an entry is
# often the only place a piece of reasoning lives, so removing it can leave a
# citation aimed at nothing. An empty sweep ("nothing cited it") is an answer;
# an unasked one is not, which is why the field's presence is what is checked
# and never its content.
#
# Scope is the archive alone, on purpose: a live entry carries no Swept: and
# must not be failed for it. Measured in both directions — a record stripped
# of its Swept: fails, and an open entry without one stays green.
incomplete=$(awk -v b="$boundary" '
  NR <= b { next }
  /^### / { if (started && !(why && swept)) print title; started = 1; why = 0; swept = 0; title = $0 }
  /^\*\*Why:\*\*/ { why = 1 }
  /^\*\*Swept:\*\*/ { swept = 1 }
  END { if (started && !(why && swept)) print title }
' "$f")
if [ -n "$incomplete" ]; then
  while IFS= read -r m; do
    [ -n "$m" ] || continue
    echo "P4 FAIL: a retirement record carries no **Why:** or no **Swept:** — the sweep is what retiring creates and git cannot reconstruct (artifacts rules R4):"
    printf '         %s\n' "$(printf '%s' "$m" | cut -c1-90)"
    rc=1
  done <<EOF
$incomplete
EOF
fi

# --- P5 -----------------------------------------------------------------
# No live-entry field survives in the archive. *Origin:* and *Promotion:* belong
# to an entry that is still open; a record that carries them is the whole entry
# moved rather than the compact record R4 prescribes, and P4 passes on it
# happily — measured. *Promotion:* is the sharper signal of the two: it states
# the condition under which the item becomes real work, so a reader meeting one
# below the archive heading cannot tell a closed item from a live one.
#
# Live entries keep both fields and must not be failed for it — the clause reads
# only below the boundary, measured in both directions.
#
# A FIELD IS A LINE THAT STARTS WITH ITS LABEL, after the indentation, and P3
# reads it the same way. A record that names the field in its prose — to count
# how many entries promoted towards something — is not carrying one, and an
# open entry that only names its origin in a sentence has none. Matching the
# label anywhere on the line turned the first red and the second green, both
# measured. DECLARED LIMIT: position is the whole distinction, so a mention
# written at the start of a line reads as a field.
moved=$(awk -v b="$boundary" '
  NR <= b { next }
  /^### / { title = $0 }
  /^[[:space:]]*\*(Promotion|Origin):\*/ { if (title != "" && !(title in seen)) { seen[title] = 1; print title } }
' "$f")
if [ -n "$moved" ]; then
  while IFS= read -r m; do
    [ -n "$m" ] || continue
    echo "P5 FAIL: a retirement record still carries *Origin:* or *Promotion:* — that is the live entry moved, not the record; git already keeps the entry (artifacts rules R4):"
    printf '         %s\n' "$(printf '%s' "$m" | cut -c1-90)"
    rc=1
  done <<EOF
$moved
EOF
fi

open_count=$(awk -v b="$boundary" 'NR >= b { exit } /^- \*\*/ { c++ } END { print c+0 }' "$f")
# A retirement record opens with "### ", not with the "- **" of a live entry:
# the two sections carry different shapes on purpose (artifacts R4). Counting
# retired entries by the live shape reported 0 the moment the records took the
# form the rule prescribes.
retired_count=$(awk -v b="$boundary" 'NR > b && /^### / { c++ } END { print c+0 }' "$f")

[ "$rc" -eq 0 ] && echo "check-parking-lot-shape: OK ($open_count open entries, $retired_count retired)"
exit $rc
