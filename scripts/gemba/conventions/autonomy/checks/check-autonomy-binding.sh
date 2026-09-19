#!/usr/bin/env bash
# Verifies: autonomy convention, `### The stops` and `### What the binding answers`
#
# Property: a project that turns unattended mode on does it with a binding that
# only ADDS stops to the shipped list, answers what the convention asks, and has
# somewhere to push the notice a stop sends. Anything else is red; no binding
# at all is the mode off, an opt-out.
#
# A0 — the convention ships beside this check and yields both vocabularies: the
#      shipped stop ids and the labels the binding may answer. A vocabulary
#      this check cannot read is a broken instrument, not an empty one.
# A1 — every label the convention marks required is answered.
# A2 — every top-level label the binding answers is in the convention's
#      vocabulary, compared whole and as data: `Removed stops` is not a
#      spelling of `Added stops`, and a binding has no way to write a removal.
# A3 — no stop the binding adds opens with a shipped stop's id. The shipped
#      stops are read from the convention and never from here, so reusing an
#      id is an attempt to redefine one, however strict its new wording.
# A4 — conventions/notifications/instance.md exists: with the mode on and no
#      notifications binding, a stop pushes its notice nowhere.
#
# WHY NO HISTORY CLAUSE. The lazy-artifact checks beside other conventions turn
# a file the history held and the tree lost red. This one cannot: deleting the
# binding is how the mode is turned off, so an absent binding is an opt-out
# whatever the history says.
#
# WHAT THIS DOES NOT SEE. The shape of the four parts and an empty or
# placeholder value belong to check-binding-shape, which runs over every
# binding including this one. Intent is not read either: an added stop whose
# prose says "except on main" reduces nothing, because nobody reads the list
# from the binding — whether it misleads a reader is judgement, read at review.
#
# Where it runs: shipped beside the autonomy convention, and run by a project's
# own ./scripts/check with the project as the git work tree it runs inside —
# never a path derived from this file's location. The convention sits one
# directory up from here, wherever the copy lives.

set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "A0 FAIL: not inside a git work tree — the binding lives in the project, so no repository is red, not an opt-out"
  exit 1
}
cd "$root" || exit 1

f=conventions/autonomy/instance.md
if [ ! -f "$f" ]; then
  echo "check-autonomy-binding: opt-out — no $f, unattended mode is off"
  exit 0
fi

conv="$here/../convention.md"
[ -f "$conv" ] || { echo "A0 FAIL: $conv is missing — it ships beside this check, so its absence is an incomplete copy, not an opt-out"; exit 1; }

# table SECTION HEADER — the data rows of the table whose header row is exactly
# HEADER, inside the `### SECTION` subsection, cells trimmed and joined by a tab.
table() {
  awk -v s="### $1" -v h="$2" '
    /^```/            { fence = !fence; next }
    fence             { next }
    $0 == s           { in_sec = 1; next }
    in_sec && /^#/    { in_sec = 0 }
    !in_sec           { next }
    $0 == h           { tbl = 1; skip = 1; next }
    tbl && skip       { skip = 0; next }
    tbl && /^\|/      {
      n = split($0, c, "|"); out = ""
      for (i = 2; i < n; i++) { v = c[i]; gsub(/^ +| +$/, "", v); gsub(/`/, "", v); out = out (i > 2 ? "\t" : "") v }
      print out; next
    }
    tbl               { tbl = 0 }
  ' "$conv"
}

ids=$(table 'The stops' '| Id | Stop | Origin |' | cut -f1)
labels=$(table 'What the binding answers' '| Label | Required | Answers |')
[ -n "$ids" ] || { echo "A0 FAIL: $conv yields no shipped stop from \`### The stops\` — a vocabulary this check cannot read is a broken instrument, not an empty one"; exit 1; }
[ -n "$labels" ] || { echo "A0 FAIL: $conv yields no label from \`### What the binding answers\` — a vocabulary this check cannot read is a broken instrument, not an empty one"; exit 1; }
known=$(printf '%s\n' "$labels" | cut -f1)
required=$(printf '%s\n' "$labels" | awk -F'\t' '$2 == "yes" { print $1 }')

rc=0

# The binding's own labels: top-level bullets only. An indented bullet is part
# of the value above it — an added stop, not a label.
answered=$(sed -nE 's/^- \*\*([^*]+):\*\*.*/\1/p' "$f")

# --- A1 ---------------------------------------------------------------------
while IFS= read -r l; do
  [ -n "$l" ] || continue
  grep -Fxq -- "$l" <<< "$answered" || {
    echo "A1 FAIL: $f does not answer \`$l\` — say which stops this project adds, or that it adds none"
    rc=1; }
done <<< "$required"

# --- A2 ---------------------------------------------------------------------
while IFS= read -r l; do
  [ -n "$l" ] || continue
  grep -Fxq -- "$l" <<< "$known" || {
    echo "A2 FAIL: $f answers \`$l\`, which the autonomy convention does not ask — a binding adds stops, it cannot remove or replace one"
    rc=1; }
done <<< "$answered"

# --- A3 ---------------------------------------------------------------------
# The value of `Added stops`: the text on its own line, then every indented
# bullet under it, up to the next top-level bullet or heading.
added=$(awk '
  /^- \*\*Added stops:\*\*/ { in_v = 1; v = $0; sub(/^- \*\*Added stops:\*\* */, "", v); if (v != "") print v; next }
  in_v && (/^- / || /^#/)   { in_v = 0 }
  in_v && /^[[:space:]]+- / { v = $0; sub(/^[[:space:]]+- +/, "", v); print v }
' "$f")
nadded=$(awk '
  /^- \*\*Added stops:\*\*/ { in_v = 1; next }
  in_v && (/^- / || /^#/)   { in_v = 0 }
  in_v && /^[[:space:]]+- / { n++ }
  END { print n + 0 }
' "$f")
while IFS= read -r entry; do
  [ -n "$entry" ] || continue
  first=$(printf '%s' "$entry" | sed -E 's/^[*`_ ]+//; s/^([A-Za-z0-9]+).*/\1/')
  grep -Fxq -- "$first" <<< "$ids" && {
    echo "A3 FAIL: $f redefines shipped stop $first under \`Added stops\` — the shipped stops are read from the convention and cannot be rewritten here"
    rc=1; }
done <<< "$added"

# --- A4 ---------------------------------------------------------------------
[ -f conventions/notifications/instance.md ] || {
  echo "A4 FAIL: unattended mode is on and conventions/notifications/instance.md does not exist — a stop would push its notice nowhere"
  rc=1; }

[ "$rc" -eq 0 ] && echo "check-autonomy-binding: OK ($(printf '%s\n' "$answered" | grep -c .) label(s), $nadded added stop(s), $(printf '%s\n' "$ids" | grep -c .) shipped stops read from the convention, notifications bound)"
exit $rc
