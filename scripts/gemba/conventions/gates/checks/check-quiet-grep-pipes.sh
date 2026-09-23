#!/usr/bin/env bash
# Verifies: the gates convention, `## Where a project's own checks live` and
# `### The instrument fails before the check does`
#
# Property: no check the project runs ends a pipe in a quiet grep. Under
# `set -o pipefail` a `grep -q` that finds its line exits at once; if the
# command feeding it is still writing, that command dies of SIGPIPE, the pipe
# exits 141, and the clause reads a match as a failure. The failure it prints
# is false, and it comes and goes with timing.
#
# The population is every check the project runs, in three parts: its own,
# found in the location the gates convention beside this check declares on
# its marked `**The location:**` line; the checks shipped beside the method's
# conventions, which sit next to this one wherever it is installed; and any
# file given as an argument, added to the other two — a project with other
# scripts an agent runs under the same `pipefail` passes them here.
#
# P0 — the project and the location are found: inside a git work tree, with
#      the convention beside this check carrying its marked line, and a value
#      that is a relative directory under the project. Anything else is red.
# P1 — no `grep` given `-q` (alone or in a cluster: `-qx`, `-Fq`), `--quiet`
#      or `--silent` reads from a pipe. A pipe split over two lines (`… |` at
#      the end of one, the grep on the next) is the same pipe. The legal forms
#      read the input to the end: `grep -q "$y" <<<"$x"`, or the grep without
#      `-q` and its output sent to /dev/null.
#
# A project without its own checks is not red: the location is a directory
# born with the first one, and the verdict counts 0 of them.
#
# DECLARED LIMITS: textual, not a parser, and shell only. It reads every
# file, pipefail or not: one without it runs the same form harmlessly today
# and would not once someone adds the option. Other readers that close a pipe
# early — `head`, `grep -m` — fail the same way when their status is tested,
# and are out of reach here. Comments are stripped by a pattern, with a hole:
# a `#` inside quotes, preceded by whitespace, truncates the line.
#
# No P1 guard for an empty population: this file is in it.

set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd -P)
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the project's own checks are found from its root, so no repository is red, not an opt-out"
  exit 1
}
root=$(cd "$root" && pwd -P)
cd "$root" || exit 1

# The location of the project's own checks, read from the convention beside
# this check. The same block, and the same messages, in both checks that read it.
conv="$here/../convention.md"
[ -f "$conv" ] || { echo "P0 FAIL: $conv is missing — the location of the project's own checks is read from it"; exit 1; }
loc=$(awk -v h="## Where a project's own checks live" '/^## /{f=($0==h); next} f' "$conv" \
      | sed -n 's/^\*\*The location:\*\* `\([^`]*\)`.*$/\1/p' | head -n 1)
[ -n "$loc" ] || { echo "P0 FAIL: $conv has no \`**The location:**\` line in \`## Where a project's own checks live\`; the project's own checks cannot be found"; exit 1; }
case "$loc" in
  /*|*..*|*[!A-Za-z0-9._/-]*|*[!/]) echo "P0 FAIL: the location \`$loc\` read from $conv is not a relative directory under the project"; exit 1 ;;
esac

# The shipped half, relative to the project when it is installed inside it.
shipped_root=$(cd "$here/../.." && pwd -P)
case "$shipped_root" in "$root"/*) shipped_root=${shipped_root#"$root"/} ;; esac

shopt -s nullglob
shipped=("$shipped_root"/*/checks/*.sh)
own=("$loc"*.sh)
shopt -u nullglob
files=("${shipped[@]}" "${own[@]}" "$@")

rc=0
for f in "${files[@]}"; do
  [ -f "$f" ] || { echo "P0 FAIL: $f was given and is not a file"; rc=1; continue; }
  # A line whose code ends in a single `|` or in `\` continues on the next:
  # joined, and reported at the line where the pipe starts.
  hits=$(sed 's/[[:space:]]#.*$//; s/^#.*$//' "$f" | awk '
    {
      if (buf == "") { start = NR; buf = $0 } else buf = buf " " $0
      if (buf ~ /(^|[^|])\|[[:space:]]*$/ || buf ~ /\\[[:space:]]*$/) { sub(/\\[[:space:]]*$/, "", buf); next }
      if (buf ~ /(^|[^|])\|&?[[:space:]]*(command[[:space:]]+)?grep([[:space:]]+-[^[:space:]]*)*[[:space:]]+(-[A-Za-z]*q[A-Za-z]*|--quiet|--silent)([[:space:]]|$)/) print start
      buf = ""
    }')
  while IFS= read -r n; do
    [ -n "$n" ] || continue
    echo "P1 FAIL: $f:$n ends a pipe in a quiet grep — under pipefail an early exit reads as a failed match (SIGPIPE, 141)"
    echo "         Read the input to the end: grep -q … <<<\"\$x\", or drop -q and send the output to /dev/null."
    rc=1
  done <<< "$hits"
done

[ "$rc" -eq 0 ] && echo "check-quiet-grep-pipes: OK (${#shipped[@]} shipped, ${#own[@]} of the project's own in $loc, $# given; no quiet grep at the end of a pipe)"
exit $rc
