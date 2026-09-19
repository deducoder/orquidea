#!/usr/bin/env bash
# Verifies: git rules R10
#
# Property: no tracked file carries a conflict marker. A merge, a rebase, a
# cherry-pick or a `stash pop` that stops on a conflict writes its markers into
# the file, and nothing else in the gate reads them: they are text, and every
# other check judges the text around them.
#
# Population: every file `git ls-files` lists, read from the working tree —
# what the next commit records. Binary files are skipped (`git grep -I`).
#
# P0 — there is something to judge: at least one tracked file. This check runs
#      inside a project that versions its own gate, so none is a checkout
#      nobody can read, not a clean one. Outside any git work tree there is no
#      population at all, and that is red too.
# P1 — no line STARTS with a marker: `<<<<<<< `, `>>>>>>> `, the diff3 base
#      `||||||| ` (each with its label, or alone on the line), or `=======`
#      alone on the line. git writes its markers at column 0 and never
#      anywhere else, so a marker quoted inside a sentence, or indented in an
#      example, is not one and is not judged. The separator is judged on its
#      own because a conflict resolved halfway — the two outer markers deleted
#      by hand — leaves exactly that line behind.
#
# Why a check and not `git diff --check`: that knows markers, but only on the
# lines a diff ADDS. A marker already committed passes the diff of every later
# change, so it can survive commit after commit with the gate green.
#
# Where it runs: shipped beside the git convention, and run by a project's own
# ./scripts/check. The project is the git work tree it is run inside, never a
# path derived from this file's location.
#
# DECLARED LIMITS: textual. A setext heading underlined with exactly seven `=`
# is refused — the method writes headings with `#`. A marker size other than
# seven (the `conflict-marker-size` attribute) is not seen.

set -uo pipefail
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the population is the tracked files, so no repository is red, not an opt-out"
  exit 1
}
cd "$root" || exit 1

total=$(git ls-files | wc -l | tr -d ' ')

rc=0
if [ "$total" -eq 0 ]; then
  echo "P0 FAIL: git ls-files lists no tracked file — this check judges the tracked tree, so an empty one is a checkout nobody can read, not a clean one"
  rc=1
fi

while IFS= read -r hit; do
  [ -n "$hit" ] || continue
  loc=${hit%%:*}; rest=${hit#*:}; line=${rest%%:*}; text=${rest#*:}
  echo "P1 FAIL: $loc:$line starts with a conflict marker (\`${text:0:7}\`) — a merge, rebase or stash left it unresolved and it was committed (git rules R10)"
  rc=1
done < <(git grep -I -nE '^(<{7}|>{7}|\|{7})( |$)|^={7}$' 2>/dev/null)

[ "$rc" -eq 0 ] && echo "check-conflict-markers: OK ($total tracked files, no conflict marker at the start of any line)"
exit $rc
