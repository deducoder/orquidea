#!/usr/bin/env bash
# Verifies: git rules R1 and R3; the git convention's re-{phase} forms
#
# Property: every commit not yet pushed respects the mechanical shape the git
# convention fixes, so a malformed message is caught before it reaches origin
# rather than by a human reading the log afterwards.
#
# P1 — the message is a single line: no body, no footer, no trailer.
# P2 — a non-merge subject matches `type(scope): description`, with type in the
#      closed vocabulary, a non-empty scope, a lowercase description and no
#      trailing period.
# P3 — a merge subject is git's own default, `Merge ...`. Merges are exempt
#      from type and scope because the convention mandates that default
#      message, which carries neither — but P1 applies to them in full.
# P4 — a phase run again re-emits its commit as `re-{phase}`: within the range,
#      only the first plain `chore(scope): phase` of a pair may lack the prefix.
#      The vocabulary is read from the convention, never written here.
#
# Scope of the check, declared: English, the imperative mood, "describe the
# observable effect", and the choice between scope-as-work-item-id and
# scope-as-area are NOT verified. They are judgement — a check wider than the
# rule it verifies is as broken as a rule with no check.
#
# The range is origin/{dev-branch}..HEAD, with {dev-branch} read from the
# project's declaration (CLAUDE.md, or .claude/CLAUDE.md): what has not reached
# the remote yet, which is exactly the property. {dev-branch}..HEAD would miss
# commits made straight on the dev branch, such as session closes. Never from
# refs/remotes/origin/HEAD: `git clone` points it at the server's default
# branch — usually the production one — and never refreshes it, so a fresh
# clone would judge everything not yet released. A dev branch not yet on the
# remote falls back to origin/{production-branch}, the branch it was cut from;
# neither on the remote is red.
#
# Where it runs: shipped beside the git convention, and run by a project's own
# ./scripts/check — this plugin's source repository, or an adopter's vendored
# copy. The project is the git work tree it is run inside, never a path derived
# from this file's location; the convention it reads IS beside this file, in
# the directory above, wherever the copy lives.
#
# DECLARED LIMIT: the remote is `origin`. The method declares no remote name.

set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the range is a set of commits, so no repository is red, not an opt-out"
  exit 1
}
cd "$root" || exit 1

types='feat|fix|refactor|test|docs|chore|style|build|ci'

# P4's vocabulary is READ FROM THE CONVENTION, never written here: the line
# that lists the re-emitted forms. Add a phase there and this check counts it
# without being touched — the same delegation the status vocabulary already
# gets from the tracker binding.
#
# The line is identified structurally: EVERY token on it is a `re-` form, and
# there are at least two. Scanning the whole file for `re-[a-z]+` instead reads
# the prose too — `re-emits` and `re-emission` yielded the phantom phases
# `emits` and `emission`, a vocabulary wider than the property. Measured.
conv="$here/../convention.md"
phases=$(awk 'NF >= 2 { for (i = 1; i <= NF; i++) if ($i !~ /^re-[a-z]+$/) next
                        for (i = 1; i <= NF; i++) print substr($i, 4) }' \
         "$conv" 2>/dev/null | sort -u)

decl=CLAUDE.md
[ -f "$decl" ] || decl=.claude/CLAUDE.md
dev=$(sed -n 's/^- \*\*Dev branch:\*\* `\([^`]*\)`.*/\1/p' "$decl" 2>/dev/null | head -1)
prod=$(sed -n 's/^- \*\*Production branch:\*\* `\([^`]*\)`.*/\1/p' "$decl" 2>/dev/null | head -1)
[ -n "$dev" ] || {
  echo "P0 FAIL: neither CLAUDE.md nor .claude/CLAUDE.md declares \`- **Dev branch:** \`name\`\` — the range is that branch's unpushed commits, so an unreadable declaration is red, not an opt-out"
  exit 1
}
base=""
for b in "$dev" "$prod"; do
  [ -n "$b" ] && git show-ref --verify --quiet "refs/remotes/origin/$b" && { base="origin/$b"; break; }
done
[ -n "$base" ] || {
  echo "P0 FAIL: neither origin/$dev nor origin/${prod:-<no production branch declared>} exists, so the unpushed range cannot be located —"
  echo "         the commits exist whether or not the instrument finds them. Push the production branch first."
  exit 1
}

range="$base..HEAD"
rc=0; count=0

while read -r sha; do
  [ -n "$sha" ] || continue
  count=$((count+1))
  subject=$(git log -1 --format=%s "$sha")
  short=$(git log -1 --format=%h "$sha")

  # P1 — a single non-blank line, whatever the commit is.
  if [ "$(git log -1 --format=%B "$sha" | grep -c '[^[:space:]]')" -gt 1 ]; then
    echo "P1 FAIL: $short carries a body or trailer: $subject"
    rc=1
  fi

  # P3 — merges take git's default message and are exempt from type and scope.
  if [ "$(git log -1 --format=%P "$sha" | wc -w)" -gt 1 ]; then
    case "$subject" in
      Merge*) ;;
      *) echo "P3 FAIL: $short is a merge but does not carry git's default message: $subject"; rc=1 ;;
    esac
    continue
  fi

  # P2 — type(scope): description
  printf '%s\n' "$subject" \
    | grep -E "^($types)\([^()]+\): [a-z0-9\`].*[^.]$" >/dev/null || {
    echo "P2 FAIL: $short does not match type(scope): description — $subject"
    rc=1
  }
done < <(git rev-list "$range" 2>/dev/null)

# P4 — only the FIRST plain `chore(scope): phase` of a pair may lack `re-`.
# Walked oldest-first, because "first" is a question about order and
# `git rev-list` answers newest first. A `re-` form is never counted: the
# convention defines no `re-re-`, so repeating it is legal. A word outside the
# vocabulary is not a phase at all — `dispatch` repeats legitimately every time
# a second block is archived.
if [ -z "$phases" ]; then
  echo "P4 FAIL: $conv lists no re-{phase} vocabulary, so a repeat cannot be judged"
  echo "         The phase vocabulary is read from that line and from nowhere else,"
  echo "         so its absence leaves nothing to read, not nothing to check."
  rc=1
else
  seen=""
  while read -r sha; do
    [ -n "$sha" ] || continue
    [ "$(git log -1 --format=%P "$sha" | wc -w)" -gt 1 ] && continue
    subject=$(git log -1 --format=%s "$sha")
    scope=$(printf '%s\n' "$subject" | sed -n 's/^chore(\([^()]*\)): .*/\1/p')
    phase=$(printf '%s\n' "$subject" | sed -n 's/^chore([^()]*): \([a-z-]*\)$/\1/p')
    [ -n "$scope" ] && [ -n "$phase" ] || continue
    printf '%s\n' "$phases" | grep -xF -- "$phase" >/dev/null || continue
    key="$scope|$phase"
    if printf '%s\n' "$seen" | grep -xF -- "$key" >/dev/null ; then
      echo "P4 FAIL: $(git log -1 --format=%h "$sha") repeats $scope's \`$phase\` without re-: $subject"
      rc=1
    else
      seen=$(printf '%s\n%s' "$seen" "$key")
    fi
  done < <(git rev-list --reverse "$range" 2>/dev/null)
fi

[ "$rc" -eq 0 ] && echo "check-commits: OK ($count commits ahead of $base, dev branch from $decl, $(printf '%s' "$phases" | wc -w) phases read from the convention)"
exit $rc
