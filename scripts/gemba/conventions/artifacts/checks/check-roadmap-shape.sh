#!/usr/bin/env bash
# Verifies: artifacts convention, `### The roadmap`
#
# Property: work/roadmap.md has the shape the artifacts convention fixes. Four
# parties in two plugins write or read it — the version-planning technique,
# epic-close, release and session-start — each with its own script, so one
# shape checked in one place is what keeps them agreeing.
#
# P1 — every `## ` section (one per version) carries exactly one `State:` line
#      whose value is in the convention's state vocabulary.
# P2 — every section carries exactly one table headed `| Epic | Status |`,
#      with its separator row. Without one, the line under the header is a
#      data row, and skipping it on trust left a row unjudged — measured.
# P3 — every row of that table carries a key (a tracker key, or an epic's local
#      id) and a status in the convention's status vocabulary.
# P4 — a key is a row of one section only: an epic belongs to one version.
#
# THE TWO VOCABULARIES ARE READ FROM THE CONVENTION'S OWN TABLES, never written
# here, the same delegation check-work-log-layout gives the canonical names.
# Each is the first cell of every row of the table that follows its heading
# line. A vocabulary this check cannot read is red, not empty.
#
# P0 — work/roadmap.md is lazy: a project that never had one is an opt-out.
#      One whose own history holds it and whose tree does not has lost its
#      planned versions, and that is red — the project's history is what tells
#      the two apart, as check-parking-lot-shape reads it.
#
# Where it runs: shipped beside the artifacts convention, and run by a
# project's own ./scripts/check with the project as the git work tree it runs
# inside — never a path derived from this file's location. The convention sits
# one directory up from here, wherever the copy lives.

set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the roadmap is a versioned artifact of the project, so no repository is red, not an opt-out"
  exit 1
}
cd "$root" || exit 1

f=work/roadmap.md
if [ ! -f "$f" ]; then
  if [ -n "$(git log -1 --format=%h -- "$f" 2>/dev/null)" ]; then
    echo "P0 FAIL: $f is missing, and this project's history holds it — the planned versions are lost, not an opt-out"
    exit 1
  fi
  echo "check-roadmap-shape: opt-out — this project has never had a $f"
  exit 0
fi

conv="$here/../convention.md"
[ -f "$conv" ] || { echo "P0 FAIL: $conv is missing — it ships beside this check, so its absence is an incomplete copy, not an opt-out"; exit 1; }

# vocab HEADER — the first cell of every data row of the table whose header
# row is exactly HEADER, inside the convention's `### The roadmap` subsection.
vocab() {
  awk -v h="$1" '
    /^```/                     { fence = !fence; next }
    fence                      { next }
    /^### The roadmap$/        { in_sec = 1; next }
    in_sec && /^##/            { in_sec = 0 }
    !in_sec                    { next }
    $0 == h                    { tbl = 1; skip = 1; next }
    tbl && skip                { skip = 0; next }
    tbl && /^\|/               { c = $0; sub(/^\| *`?/, "", c); sub(/`? *\|.*/, "", c); print c; next }
    tbl                        { tbl = 0 }
  ' "$conv"
}
states=$(vocab '| Section `State` | Written by |')
statuses=$(vocab '| Row `Status` | Written by |')
[ -n "$states" ] || { echo "P0 FAIL: $conv yields no state vocabulary under \`### The roadmap\` — a vocabulary this check cannot read is a broken instrument, not an empty one"; exit 1; }
[ -n "$statuses" ] || { echo "P0 FAIL: $conv yields no status vocabulary under \`### The roadmap\` — a vocabulary this check cannot read is a broken instrument, not an empty one"; exit 1; }

report=$(awk -v states="$(printf '%s\n' $states | paste -sd' ')" -v statuses="$(printf '%s\n' $statuses | paste -sd' ')" '
  function flush() {
    if (sec == "") return
    if (nstate != 1)      { print "P1 FAIL: " sec " carries " nstate " `State:` lines, and a version carries exactly one"; bad = 1 }
    if (ntable != 1)      { print "P2 FAIL: " sec " has " (ntable ? ntable " tables" : "no table") " headed `| Epic | Status |`, and a version has exactly one"; bad = 1 }
  }
  function isin(v, list,   a, n, i) { n = split(list, a, " "); for (i = 1; i <= n; i++) if (a[i] == v) return 1; return 0 }
  BEGIN { bad = 0; versions = 0; epics = 0 }
  /^## / {
    flush(); sec = $0; versions++; nstate = 0; ntable = 0; intable = 0; next
  }
  sec == "" { next }
  /^State:/ {
    nstate++; st = $0; sub(/^State: */, "", st); sub(/ *$/, "", st)
    if (!isin(st, states)) { print "P1 FAIL: " sec " has `State: " st "`; the convention declares: " states; bad = 1 }
    next
  }
  /^\| *Epic *\| *Status *\| *$/ { ntable++; intable = 1; sep = 1; next }
  intable && sep {
    sep = 0
    if ($0 ~ /^\|( *:?-+:? *\|)+ *$/) next
    # No separator: this line is a row, and it is judged as one below.
    print "P2 FAIL: " sec " has a `| Epic | Status |` table with no separator row under its header"; bad = 1
  }
  intable && /^\|/ {
    n = split($0, cell, "|"); key = cell[2]; status = cell[3]
    gsub(/^ +| +$/, "", key); gsub(/^ +| +$/, "", status)
    if (key !~ /^([A-Z]+-[0-9]+|e[0-9]+)$/) { print "P3 FAIL: " sec ", row `" $0 "`: `" key "` is not a tracker key or an epic local id"; bad = 1 }
    else {
      epics++
      if (seen[key] != "") { dup[key] = dup[key] ", " sec } else { seen[key] = sec; dup[key] = sec }
      cnt[key]++
    }
    if (!isin(status, statuses)) { print "P3 FAIL: " sec ", row " key ": `" status "` is not a status; the convention declares: " statuses; bad = 1 }
    next
  }
  intable { intable = 0 }
  END {
    flush()
    for (k in cnt) if (cnt[k] > 1) { print "P4 FAIL: " k " is planned in more than one version: " dup[k]; bad = 1 }
    if (versions == 0) { print "P1 FAIL: work/roadmap.md declares no version — a roadmap without a `## ` section plans nothing"; bad = 1 }
    print "#counts " versions " " epics
    exit bad
  }
' "$f")
rc=$?
counts=$(printf '%s\n' "$report" | sed -n 's/^#counts //p')
printf '%s\n' "$report" | grep -v '^#counts ' || true
[ "$rc" -eq 0 ] && echo "check-roadmap-shape: OK (${counts%% *} versions, ${counts##* } epics, $(printf '%s\n' "$states" | grep -c .) states and $(printf '%s\n' "$statuses" | grep -c .) statuses read from the convention)"
exit $rc
