#!/usr/bin/env bash
# Verifies: work rules R1, R2 and R3; artifacts rules R2 and R6; the type
# columns of the artifacts convention's canonical table, for epic-only names
#
# Property: the work log's shape is the one its two conventions fix — the
# identity of a work item lives in its path, and the log is versioned like any
# other artifact.
#
# P1 — every work-item directory is {KEY}-{slug}, kebab-case (work rules R1),
#      where {KEY} is a tracker key or a local id (work rules R4).
# P2 — each {KEY} lives in exactly one place (work rules R2). A work item
#      copied instead of moved keeps two logs that drift apart, and the tracker
#      cannot say which is real.
#
# THE KEY IS EITHER FORM R4 ALLOWS: a tracker key (AB-12), or, with no
# tracker, a local id — e{N} for an epic, s/b/sp{N}.{M} for an epic's child,
# s/b/sp{N} standalone. One pattern serves P1 and P2: a key P1 accepts and P2
# cannot extract is a duplicate nobody sees.
# P2 lists the paths of a duplicate by a literal prefix of their LAST
# component: the dot of s1.1 is a wildcard to grep -E, and would have listed
# an s121 beside it; and a match anywhere in the path listed every child of a
# duplicated epic (AB-1-x/stories/AB-2-y under AB-1) as one more copy of it.
# P3 — every artifact inside a work-item directory carries a canonical name
#      (artifacts rules R2). An unnamed "progress log" is an artifact nobody
#      can find.
# P4 — no ignore rule covers work/ or .claude/memory/ (work rules R3,
#      artifacts rules R6). This is the silent one: an ignore rule takes the
#      whole log out of version control with no signal at all.
# P5 — the only loose files in the root of work/ are the ones the artifacts
#      convention declares there, a symlink included: `-type f` let one pass. A file nobody declared has no writer and no
#      reader, which is how the previous backlog died.
# P6 — an artifact the canonical table marks for the epic alone lives only in
#      an epic's own directory, the one directly under work/epics/. A
#      decisions.md or a brief.md inside a story, a bug or a spike — under an
#      epic or standalone — has a writer that never runs there.
#
# P6 READS THE SAME TABLE, BY ITS TYPE COLUMNS: a row whose epic cell is ✓ and
# whose story, bug and spike cells are all — is epic-only. Nothing else is
# judged by type on purpose: the general form (every name against all four
# columns) reddens standalone stories that predate the columns, and deciding
# what to do with those is not this clause's call. A table with no epic-only
# row is P0 red, not a P6 with no subject that reads as green.
#
# THE CANONICAL NAMES ARE READ FROM THE CONVENTION'S OWN TABLE, never written
# here. Add an artifact to `## Canonical table` and it becomes legal without
# touching this file — the same delegation the tracker's status vocabulary
# gets from its binding. The convention sits beside this check, one directory
# up, wherever the copy lives.
#
# Scope: work/{epics,stories,bugs,spikes} for P1–P3, and the root of work/
# for P5. work/sessions/,
# work/research/, work/debug/ and work/problem-shape/ are NOT work items —
# the same convention gives them their own table with their own names
# (report.md, {YYYY-MM-DD}-{slug}.md), so they are out by path, not by
# exemption. A type directory that does not exist is fine: a project without
# spikes is not defective.
#
# P4 asks git check-ignore, not git status: an uncommitted file under work/ is
# an ordinary working state — it happens every time an artifact is written —
# while an ignore rule is permanent and invisible.
#
# AND IT ASKS WITH --no-index. Without that flag check-ignore stays SILENT on a
# path that is already tracked, which work/ and .claude/memory/ both are: the
# first version of this clause reported OK with `work/` sitting in .gitignore,
# and only the forced mutation caught it. The distinction is real and the flag
# picks the right side of it — an ignore rule does not untrack what is already
# committed, but it makes every NEW artifact invisible, which is precisely the
# loss R3 and R6 exist to prevent. The rule itself is the defect, not its
# effect on files that predate it.
#
# AND IT READS ALL THREE ANSWERS. check-ignore exits 0 when the path is
# ignored, 1 when it is not, and 128 when it cannot answer. An `if` over the
# command read 128 as 1 and a `2>/dev/null` hid why, so a P4 that never looked
# printed what a P4 that looked and found nothing prints — measured with a
# `git` that answers 128. Any status but 0 and 1 is red, with git's own words.
#
# Where it runs: shipped beside the artifacts convention, and run by a
# project's own ./scripts/check with the project as the git work tree it runs
# inside — never a path derived from this file's location.

set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the work log is versioned, so no repository is red, not an opt-out"
  exit 1
}
cd "$root" || exit 1

rc=0
key='([A-Z]+-[0-9]+|e[0-9]+|(s|b|sp)[0-9]+(\.[0-9]+)?)'

# --- P4 -----------------------------------------------------------------
for p in work .claude/memory; do
  [ -e "$p" ] || continue
  err=$(git check-ignore --no-index -q "$p" 2>&1)
  st=$?
  case "$st" in
    0) echo "P4 FAIL: $p is covered by an ignore rule; the work log is versioned like any other artifact (work rules R3, artifacts rules R6)."
       rc=1 ;;
    1) : ;;
    *) echo "P4 FAIL: git check-ignore could not answer for $p (exit $st): $err"
       echo "         P4 reads 0 as ignored and 1 as not ignored; anything else is a question that was never answered."
       rc=1 ;;
  esac
done

# P4 runs first because it needs nothing below: an early exit on a missing
# convention or an empty work/ used to skip it, leaving .claude/memory unjudged.
conv="$here/../convention.md"
[ -f "$conv" ] || { echo "P0 FAIL: $conv is missing — it ships beside this check, so its absence is an incomplete copy, not an opt-out"; exit 1; }

canonical=$(sed -n '/^## Canonical table/,/^## /p' "$conv" \
            | sed -n 's/^| [^|]* | `\([a-z-]*\.md\)`.*/\1/p' | sort -u)
[ -n "$canonical" ] || { echo "P0 FAIL: $conv yields no canonical names from its \`## Canonical table\` — a vocabulary this check cannot read is a broken instrument, not an empty one"; exit 1; }

# The cells are compared as literal text: ✓ and — are multibyte, and a
# character class would read them differently under another locale.
epic_only=$(sed -n '/^## Canonical table/,/^## /p' "$conv" | awk -F'|' '
  function t(s) { gsub(/^[ \t]+|[ \t]+$/, "", s); return s }
  NF >= 9 && t($3) ~ /^`[a-z-]*\.md`$/ && t($5) == "✓" \
    && t($6) == "—" && t($7) == "—" && t($8) == "—" {
    n = t($3); gsub(/`/, "", n); print n
  }' | sort -u)
[ -n "$epic_only" ] || { echo "P0 FAIL: $conv yields no epic-only name from its \`## Canonical table\` (epic ✓, story, bug and spike —) — a vocabulary this check cannot read is a broken instrument, not an empty one"; exit 1; }

# --- P5 -----------------------------------------------------------------
# The legal loose names are the rows of `## Artifacts that are not work-item
# artifacts` whose path cell is exactly `work/` — read from the convention, the
# same delegation P3 gives the canonical names. It runs before the opt-out
# below: a work/ holding only loose files has no work-item directory, and an
# early exit there would approve exactly the files this clause exists to see.
loose_ok=$(sed -n '/^## Artifacts that are not work-item artifacts/,/^## /p' "$conv" \
           | sed -n 's/^| `\([^`]*\)` | `work\/` |.*/\1/p' | sort -u)
[ -n "$loose_ok" ] || { echo "P0 FAIL: $conv declares no loose file in work/ under \`## Artifacts that are not work-item artifacts\` — a vocabulary this check cannot read is a broken instrument, not an empty one"; exit 1; }
if [ -d work ]; then
  while IFS= read -r lf; do
    [ -n "$lf" ] || continue
    printf '%s\n' "$loose_ok" | grep -xF -- "$(basename "$lf")" >/dev/null || {
      echo "P5 FAIL: $lf is a loose file in work/; the only ones the convention declares there: $(printf '%s\n' "$loose_ok" | paste -sd' ')"
      rc=1
    }
  done < <(find work -mindepth 1 -maxdepth 1 ! -type d)
fi

roots="work/epics work/stories work/bugs work/spikes"
present=""
for r in $roots; do [ -d "$r" ] && present="$present $r"; done
if [ -z "$present" ]; then
  [ "$rc" -eq 0 ] && echo "check-work-log-layout: opt-out — no work-item directories yet, nothing written to judge (P4 ran)"
  exit $rc
fi

dir_count=0; art_count=0
name_count=$(printf '%s\n' "$canonical" | grep -c .)

# Work-item directories: any directory whose name is not one of the type
# groupings that nest under a container.
dirs=$(find $present -mindepth 1 -maxdepth 3 -type d 2>/dev/null \
       | grep -vE '/(stories|bugs|spikes)$')

# --- P1 -----------------------------------------------------------------
while IFS= read -r d; do
  [ -n "$d" ] || continue
  dir_count=$((dir_count+1))
  printf '%s\n' "$(basename "$d")" | grep -E "^$key-[a-z0-9]+(-[a-z0-9]+)*\$" >/dev/null || {
    echo "P1 FAIL: $d is not {KEY}-{slug} in kebab-case (work rules R1)."
    rc=1
  }
done <<EOF
$dirs
EOF

# --- P2 -----------------------------------------------------------------
while IFS= read -r dup; do
  [ -n "$dup" ] || continue
  echo "P2 FAIL: $dup lives in more than one place, and a work item lives in exactly one (work rules R2):"
  printf '%s\n' "$dirs" | awk -v k="$dup-" '{ n = split($0, p, "/") } index(p[n], k) == 1' \
    | sed 's/^/           /'
  rc=1
done < <(printf '%s\n' "$dirs" | sed -nE "s#.*/$key-[^/]*\$#\\1#p" | sort | uniq -d)

# --- P3 -----------------------------------------------------------------
while IFS= read -r f; do
  [ -n "$f" ] || continue
  art_count=$((art_count+1))
  printf '%s\n' "$canonical" | grep -x "$(basename "$f")" >/dev/null || {
    echo "P3 FAIL: $f is not a canonical artifact name (artifacts rules R2)."
    echo "         The canonical names, from the convention's own table: $(printf '%s' "$canonical" | tr '\n' ' ')"
    rc=1
  }
done < <(find $present -type f -name '*.md' 2>/dev/null)

# --- P6 -----------------------------------------------------------------
while IFS= read -r f; do
  [ -n "$f" ] || continue
  printf '%s\n' "$epic_only" | grep -xF -- "$(basename "$f")" >/dev/null || continue
  [ "$(dirname "$(dirname "$f")")" = work/epics ] && continue
  echo "P6 FAIL: $f is an epic-only artifact outside an epic's own directory (the convention's table marks it for epic alone)."
  echo "         The epic-only names, from the convention's own table: $(printf '%s' "$epic_only" | tr '\n' ' ')"
  rc=1
done < <(find $present -type f -name '*.md' 2>/dev/null)

[ "$rc" -eq 0 ] && echo "check-work-log-layout: OK ($dir_count work item directories, $art_count artifacts, $name_count canonical names)"
exit $rc
