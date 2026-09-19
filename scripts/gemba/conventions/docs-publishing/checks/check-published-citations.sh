#!/usr/bin/env bash
# Verifies: docs-publishing rules R5
#
# Property: content that gets PUBLISHED names a work/ artifact instead of
# citing it by path — the docs-publishing convention's R5. Its reader may never
# open the repository, so a path is not a weak citation, it is no citation at
# all, and the argument leaning on it becomes an assertion.
#
# P1 — no publishable document cites a work/ artifact by path.
#
# CITATION vs VOCABULARY, the whole difficulty of this check. R5 declares that
# naming the place stays legal — `work/`, `work/epics/`, `work/{type}/{item}/`
# are vocabulary: they name where something lives, they do not offer evidence.
# The mechanical discriminator is the THIRD segment: present and not starting
# with `{` means a concrete artifact is being pointed at. A naive pattern on
# `work/` would flag the convention's own legal examples: a check wider than
# its rule.
#
# Scope: what is actually published — records/decisions/*.md (published by the
# adr technique) and work/**/docs.md (published by epic-close). A scope.md, a
# plan.md or a retrospective.md is read INSIDE the repository, where a path is
# a useful reference, and work items use them that way on purpose. A check
# over all of work/ would mark correct practice as a defect.
#
# A bare `work/` in a published document is the legal vocabulary, and stays
# green: it is this check's standing positive control.
#
# Where it runs: shipped beside the docs-publishing convention, and run by a
# project's own ./scripts/check. The project is the git work tree it is run
# inside, never a path derived from this file's location — derived from it,
# this check finds nothing published and leaves through its opt-out, green.

set -uo pipefail
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — what is published lives in the project's repository, so no repository is red, not an opt-out"
  exit 1
}
cd "$root" || exit 1

docs=$( { ls records/decisions/*.md 2>/dev/null; find work -name docs.md 2>/dev/null; } | sort -u)
[ -n "$docs" ] || { echo "check-published-citations: opt-out — no decision record and no docs.md yet, nothing published to judge"; exit 0; }

rc=0
count=0

while IFS= read -r f; do
  [ -n "$f" ] || continue
  count=$((count+1))
  while IFS= read -r hit; do
    [ -n "$hit" ] || continue
    line=${hit%%:*}
    path=$(printf '%s' "$hit" | cut -d: -f2-)
    echo "P1 FAIL: $f:$line cites a work/ artifact by path: $path"
    echo "         Published content names it — the issue key, or what it is and when — because its reader may never open the repository (docs-publishing rules R5)."
    rc=1
  done < <(grep -noE 'work/[a-z]+/[A-Za-z0-9][^ )`"]*' "$f" 2>/dev/null)
done <<EOF
$docs
EOF

[ "$rc" -eq 0 ] && echo "check-published-citations: OK ($count publishable documents)"
exit $rc
