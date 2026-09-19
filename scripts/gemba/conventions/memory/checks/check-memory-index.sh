#!/usr/bin/env bash
# Verifies: memory rules R3, R4 and the half of R1 that lives in the tree; the
# memory convention's flat store
# Property: the always-loaded memory index exists and fits its load budget.
#
# P1 — .claude/memory/MEMORY.md exists. The memory convention is set up in
#      every project at creation or onboarding, and the index is the one
#      memory artifact loaded into every session: without it nothing is
#      recalled, and nothing says so.
# P2 — MEMORY.md is at most 20480 bytes. Past the harness's load limit the
#      index is truncated silently, and a truncated entry is indistinguishable,
#      from inside a session, from a memory nobody wrote. The bound and the
#      remedy — consolidate downward, never raise the bound — are memory
#      rules R4.
#
# P3 — every leaf file is reachable from the index (R3). A memory nobody
#      indexed is a memory nobody recalls, and from inside a session it is
#      indistinguishable from one that was never written.
# P4 — every link in the index resolves to a file that exists. This is the half
#      of R1 that lives in the tree: delete a memory, leave its line, and the
#      reader is pointed at nothing. The other half — that the line and the
#      file move in the SAME commit — needs the history and stays out.
# P5 — no subdirectory under the store. `convention.md` makes flatness a rule,
#      not a placeholder: whether the harness's recall scans subdirectories is
#      undocumented, and being wrong about it disables recall in silence.
#
# Why the byte count is read with `wc -c <`: stat's format flags differ between
# GNU and BSD, and a check that fails to parse its own measurement would be
# red for a reason that is not the property.
#
# Where it runs: shipped beside the memory convention, and run by a project's
# own ./scripts/check. The project is the git work tree it is run inside,
# never a path derived from this file's location.

set -uo pipefail
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the memory store is versioned in the project, so no repository is red, not an opt-out"
  exit 1
}
cd "$root" || exit 1

store=.claude/memory
index=$store/MEMORY.md
bound=20480

if [ ! -f "$index" ]; then
  echo "P1 FAIL: $index is missing — the memory convention is adopted here and the index is its always-loaded tier."
  exit 1
fi

size=$(wc -c < "$index" | tr -d ' ')
rc=0
if [ "$size" -gt "$bound" ]; then
  echo "P2 FAIL: $index is $size bytes; the always-loaded index is bounded at $bound. Consolidate downward (memory rules R4), never raise the bound."
  rc=1
fi

# The link form is the convention's: `- [Title](file.md) — hook`. Extracted
# once and walked in both directions, so the two clauses cannot disagree about
# what an index entry is.
linked=$(grep -oE '\]\([a-z0-9-]+\.md\)' "$index" | tr -d ']()' | sort -u)
leaves=$(find "$store" -maxdepth 1 -name '*.md' ! -name MEMORY.md -exec basename {} \; 2>/dev/null | sort)

leaf_count=0
while IFS= read -r leaf; do
  [ -n "$leaf" ] || continue
  leaf_count=$((leaf_count+1))
  printf '%s\n' "$linked" | grep -x "$leaf" >/dev/null || {
    echo "P3 FAIL: $store/$leaf is not reachable from the index (memory rules R3)."
    rc=1
  }
done <<EOF
$leaves
EOF

entry_count=0
while IFS= read -r target; do
  [ -n "$target" ] || continue
  entry_count=$((entry_count+1))
  [ -f "$store/$target" ] || {
    echo "P4 FAIL: the index points at $store/$target, which does not exist (memory rules R1)."
    rc=1
  }
done <<EOF
$linked
EOF

while IFS= read -r sub; do
  [ -n "$sub" ] || continue
  echo "P5 FAIL: $sub is a subdirectory; the store is flat (memory convention, \"flat is the rule\")."
  rc=1
done < <(find "$store" -mindepth 1 -type d 2>/dev/null)

[ "$rc" -eq 0 ] && echo "check-memory-index: OK (MEMORY.md $size bytes of $bound, $leaf_count leaves, $entry_count entries)"
exit $rc
