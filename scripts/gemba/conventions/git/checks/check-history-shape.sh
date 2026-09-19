#!/usr/bin/env bash
# Verifies: git rules R5, R6 and R8; the core's branch forms
#
# Property: the structural trace the git convention's R5, R6 and R8 leave in
# the repository holds for what has not been pushed yet — how work reaches the
# dev branch, which tags exist, and what a branch may be called.
#
# P1 — no behaviour commit sits on {dev-branch}'s own first-parent line within
#      the unpushed range. Work reaches the dev branch through a merge (R5, R6):
#      a story merges --no-ff, a bug ships its own branch, an epic integrates
#      once. A commit of its own on that line means someone committed straight
#      onto {dev-branch} or fast-forwarded a branch away.
# P2 — every tag matches v{semver} and is reachable from {production-branch}.
#      The release tag created at promotion is the one tag this method defines
#      (R8).
# P3 — every local branch is {dev-branch}, {production-branch}, or one of the
#      three work-item forms {story|bug|spike}/{scope}/{slug} (CLAUDE.md,
#      Branches) — or the harness's own transient `worktree-agent-{id}`, the
#      branch an isolated subagent is born on before it switches to its
#      work-item branch. Local branches are shared by every checkout, so
#      without that tolerance a live executor turns the gate red in the
#      dispatching session too. A leftover after cleanup is not caught here:
#      `delegate` verifies none remains as its last step.
#
# Scope of P1, declared: only the four types that change behaviour —
# feat|fix|refactor|test. chore, docs, style, build and ci are deliberately
# OUT: the method's own meta-work (session closes, a container's artifacts,
# the parking lot) commits them straight onto {dev-branch} by convention, and
# judging them would fail correct practice. A behaviour commit made straight
# on the dev branch is the defect this clause exists to catch.
#
# An amend in progress: a pre-commit hook that runs this gate and can tell the
# commit is an `--amend` puts the sha of the HEAD about to be replaced in
# GEMBA_AMENDED_HEAD, and P1 leaves that one commit unjudged, saying so. Such a
# hook runs before the message exists, so P1 only ever judges commits already
# made; without the variable, the commit that turns P1 red could not be
# amended to fix it. An amend that keeps the behaviour type is caught by the
# next commit, as any fresh one is. With no hook setting it the variable is
# empty and every commit is judged.
#
# The two branches are read from the project's OWN DECLARATION in CLAUDE.md
# (or .claude/CLAUDE.md), never from refs/remotes/origin/HEAD. That local ref
# is written once by `git clone` and never refreshed, so it can name a branch
# the server no longer treats as its default.
#
# Where it runs: shipped beside the git convention, and run by a project's own
# ./scripts/check. The project is the git work tree it is run inside, never a
# path derived from this file's location.
#
# sed, not grep -oP: -P is a GNU extension, and a check that cannot parse its
# own input on another platform is red for a reason that is not the property.

set -uo pipefail
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the subject is the project's history, so no repository is red, not an opt-out"
  exit 1
}
cd "$root" || exit 1

decl=CLAUDE.md
[ -f "$decl" ] || decl=.claude/CLAUDE.md
[ -f "$decl" ] || { echo "P0 FAIL: neither CLAUDE.md nor .claude/CLAUDE.md exists — the branches this check reads are declared there, and this project declares them"; exit 1; }

dev=$(sed -n 's/^- \*\*Dev branch:\*\* `\([^`]*\)`.*/\1/p' "$decl" | head -1)
prod=$(sed -n 's/^- \*\*Production branch:\*\* `\([^`]*\)`.*/\1/p' "$decl" | head -1)

[ -n "$dev" ] || { echo "P0 FAIL: $decl declares no dev branch in the form \`- **Dev branch:** \`name\`\` — the declaration is the subject, so an unreadable one is red, not an opt-out"; exit 1; }

rc=0

# --- P1 -----------------------------------------------------------------
behaviour='feat|fix|refactor|test'
p1_count=0
# The summary names what P1 counts — first-parent, non-merge, unpushed — and
# prints no count at all when P1 did not run. A bare "N unpushed commits"
# reads as the whole unpushed range, which is a larger number, and a
# "0 unpushed commits" printed for a skipped P1 reads as a clean one.
p1_sum="P1 skipped"

if ! git show-ref --verify --quiet "refs/heads/$dev"; then
  echo "check-history-shape: no local $dev, P1 skipped"
elif ! git show-ref --verify --quiet "refs/remotes/origin/$dev"; then
  echo "check-history-shape: no origin/$dev, P1 skipped"
else
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    p1_count=$((p1_count+1))
    full=${line%% *}; rest=${line#* }; short=${rest%% *}; subject=${rest#* }
    if [ "$full" = "${GEMBA_AMENDED_HEAD:-}" ]; then
      echo "check-history-shape: HEAD $short is being amended, P1 does not judge it"
      continue
    fi
    printf '%s\n' "$subject" | grep -E "^($behaviour)\(" >/dev/null && {
      echo "P1 FAIL: $short reaches $dev directly: $subject"
      echo "         A behaviour commit reaches the dev branch through a merge, never on its own line (git rules R5, R6)."
      rc=1
    }
  done < <(git log --first-parent --no-merges --format='%H %h %s' "origin/$dev..$dev")
  p1_sum="$p1_count first-parent non-merge commits unpushed on $dev"
fi

# --- P2 -----------------------------------------------------------------
# Tag form, and where a tag may live. Reachability is asked of the LOCAL
# production branch: a tag created on another line is the defect, and
# --is-ancestor answers exactly that. No production branch locally (a fresh
# clone that never fetched it) → the clause is skipped out loud, never
# silently passed.
tag_count=0
p2_sum="P2 skipped"
if [ -z "$prod" ]; then
  echo "check-history-shape: $decl declares no production branch, P2 skipped"
elif ! git show-ref --verify --quiet "refs/heads/$prod"; then
  echo "check-history-shape: no local $prod, P2 reachability skipped"
else
  while IFS= read -r t; do
    [ -n "$t" ] || continue
    tag_count=$((tag_count+1))
    printf '%s\n' "$t" | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+' >/dev/null || {
      echo "P2 FAIL: tag $t is not v{semver}; the release tag is the one tag this method defines (git rules R8)."
      rc=1
      continue
    }
    git merge-base --is-ancestor "$t" "$prod" 2>/dev/null || {
      echo "P2 FAIL: tag $t is not reachable from $prod; a version tag is created on the production branch at promotion (git rules R8)."
      rc=1
    }
  done < <(git tag)
  p2_sum="$tag_count tags"
fi

# --- P3 -----------------------------------------------------------------
# Local branches only. A remote's branches are not this repository's to police,
# and a stale remote-tracking ref would fail a name nobody here can rename.
branch_count=0
while IFS= read -r b; do
  [ -n "$b" ] || continue
  branch_count=$((branch_count+1))
  [ "$b" = "$dev" ] && continue
  [ "$b" = "$prod" ] && continue
  printf '%s\n' "$b" | grep -E '^worktree-agent-[A-Za-z0-9._-]+$' >/dev/null && continue
  printf '%s\n' "$b" | grep -E '^(story|bug|spike)/[A-Za-z0-9.-]+/[a-z0-9-]+$' >/dev/null || {
    echo "P3 FAIL: branch $b is neither $dev, $prod, {story|bug|spike}/{scope}/{slug} (CLAUDE.md, Branches), nor the harness's worktree-agent-*."
    rc=1
  }
done < <(git branch --format='%(refname:short)')

[ "$rc" -eq 0 ] && echo "check-history-shape: OK ($p1_sum, $p2_sum, $branch_count branches)"
exit $rc
