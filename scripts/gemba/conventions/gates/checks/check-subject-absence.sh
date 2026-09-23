#!/usr/bin/env bash
# Verifies: the gates convention, `## Where a project's own checks live` and
# `### A check that cannot find its subject reports success`
#
# Property: a check that cannot find what it was meant to judge says so in
# red. The one green that judges nothing is an opt-out, and it names itself:
# every executable line of a check that leaves with status 0 before the
# check's verdict carries the word `opt-out`, on that line or on the code line
# just before it (an `echo` and its `exit` split in two).
#
# The population is every check the project runs, in three parts: its own,
# found in the location the gates convention beside this check declares on
# its marked `**The location:**` line; the checks shipped beside the method's
# conventions, which sit next to this one wherever it is installed; and any
# file given as an argument, added to the other two.
#
# P0 — the project and the location are found: inside a git work tree, with
#      the convention beside this check carrying its marked line, and a value
#      that is a relative directory under the project (ends in `/`, no `..`,
#      only letters, digits, `.`, `_`, `-` and `/`). Anything else is red:
#      the value is data read from a file, never a pattern or a path to trust.
# P1 — every early `exit 0` is a declared opt-out. A check's verdict leaves
#      with its own status variable, so a literal 0 is a path that skipped
#      judging. A literal 0 written as arithmetic — `exit $((0))`,
#      `exit "$(( 0 ))"` — is the same exit.
#
# A project without its own checks is not red: the location is a directory
# born with the first one, and the verdict counts 0 of them.
#
# DECLARED LIMITS: textual, not a parser, and shell only — a check written in
# another language is outside what it reads. Invisible here: a bare `exit`,
# an `exit "$var"` holding 0, arithmetic that evaluates to 0 without being a
# literal zero (`exit $((1-1))`), and a check that reaches its end green
# without judging. Comments are stripped by a pattern, with a hole: a `#`
# inside quotes, preceded by whitespace, truncates the line. A clause that
# prints "not applicable" and carries on leaves no exit to read, and is a
# review's to catch.
#
# No P1 guard for an empty population: this file is in it, as one of the
# checks shipped beside the conventions.

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
opt=0
for f in "${files[@]}"; do
  [ -f "$f" ] || { echo "P0 FAIL: $f was given and is not a file"; rc=1; continue; }
  report=$(sed 's/[[:space:]]#.*$//; s/^#.*$//' "$f" | awk -v f="$f" '
    /(^|[;&|({[:space:]])exit[[:space:]]+(0|"?\$\(\([[:space:]]*0+[[:space:]]*\)\)"?)([^0-9]|$)/ {
      if ($0 ~ /opt-out/ || prev ~ /opt-out/) opt++
      else print "FAIL " f ":" NR
    }
    /[^[:space:]]/ { prev = $0 }
    END { print "OPT " opt + 0 }')
  while IFS= read -r l; do
    case "$l" in
      "FAIL "*)
        echo "P1 FAIL: ${l#FAIL } leaves green before its verdict without declaring an opt-out —"
        echo "         a missing subject is red; only a population a project starts without is an opt-out, and it says so"
        rc=1 ;;
      "OPT "*) opt=$((opt + ${l#OPT })) ;;
    esac
  done <<< "$report"
done

[ "$rc" -eq 0 ] && echo "check-subject-absence: OK (${#shipped[@]} shipped, ${#own[@]} of the project's own in $loc, $# given; $opt early green exits, every one a declared opt-out)"
exit $rc
