#!/usr/bin/env bash
# Verifies: the git convention's hooks are reachable wherever a project
# declared them adopted
#
# Property: a project that adopted the method's hooks has them wired —
# `core.hooksPath` points at the hooks shipped beside this check — and a
# project that did not adopt them leaves by a declared opt-out, never by a
# silent green.
#
# Why a marker: `core.hooksPath` lives in `.git/config`, which git does not
# version. A fresh clone of a project that wired the hooks gets the hook files
# and no wiring, with no signal at all — the hooks sit in the tree looking like
# control while controlling nothing. Read from `.git/config` alone, that clone
# and a project that never asked for the hooks are the same. /gemba:hooks
# commits `scripts/gemba/hooks-adopted` when it wires them, so the repository
# itself says which of the two it is.
#
# P0 — inside a git work tree, with the shipped hooks beside this check. Both
#      are shipped or structural, so their absence is red, not an opt-out.
# P1 — the two-entry table:
#        no marker, core.hooksPath unset          → opt-out
#        no marker, another manager's path        → opt-out, naming it
#        no marker, the method's hooks            → red: a fresh clone would
#                                                   be inert with no signal
#        marker, core.hooksPath unset             → red, with the command
#        marker, any other value                  → red
#        marker, the method's hooks               → green, subject to P2
#      "The method's hooks" is the hooks/ directory beside this check,
#      resolved with `pwd -P`: by a relative path, by an absolute one, or — in
#      a linked worktree wired with an absolute path — the main checkout's
#      copy at the same place, since the wiring is one value every worktree
#      shares. The expected path is derived from this file's location, never
#      written in the marker, so the marker cannot drift from where the hooks
#      are.
# P2 — every hook in that directory is executable.
#
# It cannot verify that the hooks work; only that they are reachable. What
# they accept and refuse is verified by running them.
#
# Where it runs: shipped beside the git convention, and run by a project's own
# ./scripts/check — the plugin's source repository, or an adopter's vendored
# copy. The project is the git work tree it is run inside.
set -uo pipefail

here=$(cd "$(dirname "$0")" && pwd -P)
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the hooks are wired through git config, so there is nothing that could carry the wiring; red, not an opt-out"
  exit 1
}
cd "$root" || exit 1
root=$(pwd -P)

hooks=$(cd "$here/../hooks" 2>/dev/null && pwd -P) || {
  echo "P0 FAIL: $here/../hooks is missing — the hooks ship beside the git convention, so a copy without them is a copy nobody finished, not an opt-out"
  exit 1
}
n_hooks=$(find "$hooks" -mindepth 1 -maxdepth 1 -type f | wc -l | tr -d ' ')
[ "$n_hooks" -gt 0 ] || { echo "P0 FAIL: $hooks holds no hook"; exit 1; }

rel=${hooks#"$root/"}
marker=scripts/gemba/hooks-adopted
common=$(cd "$(git rev-parse --git-common-dir)/.." && pwd -P)
configured=$(git config --get core.hooksPath || true)

ours=0
if [ -n "$configured" ]; then
  resolved=$(cd "$root" && cd "$configured" 2>/dev/null && pwd -P) || resolved=""
  if [ -n "$resolved" ] && { [ "$resolved" = "$hooks" ] || [ "$resolved" = "$common/$rel" ]; }; then
    ours=1
  fi
fi

if [ ! -f "$marker" ]; then
  if [ -z "$configured" ]; then
    echo "check-hooks-wiring: opt-out — no $marker and core.hooksPath unset: this project has not adopted the method's hooks"
    exit 0
  fi
  if [ "$ours" -eq 0 ]; then
    echo "check-hooks-wiring: opt-out — no $marker, and core.hooksPath is '$configured': another hook manager's, not the method's"
    exit 0
  fi
  echo "P1 FAIL: core.hooksPath points at the method's hooks but $marker is missing — a fresh clone would get the hooks with no wiring and no signal."
  echo "         Commit the marker: /gemba:hooks writes it."
  exit 1
fi

rc=0
if [ -z "$configured" ]; then
  echo "P1 FAIL: $marker declares the hooks adopted, but core.hooksPath is not set — they are inert."
  echo "         Run: git config core.hooksPath $rel"
  rc=1
elif [ "$ours" -eq 0 ]; then
  echo "P1 FAIL: $marker declares the hooks adopted, but core.hooksPath is '$configured', not $rel"
  rc=1
fi

for h in "$hooks"/*; do
  [ -f "$h" ] || continue
  [ -x "$h" ] || { echo "P2 FAIL: $(basename "$h") is not executable"; rc=1; }
done

[ "$rc" -eq 0 ] && echo "check-hooks-wiring: OK (adopted by $marker, core.hooksPath -> $rel, $n_hooks hooks executable)"
exit "$rc"
