#!/usr/bin/env bash
# Verifies: the project convention, `## The guardrails table`
#
# Property: a guardrail that declares a check has one, and that check claims
# it explicitly; a check that claims a guardrail has its row.
#
# The table is governance/guardrails.md. Its ID and Verification columns are
# found by their header, never by position, so a table with another column or
# another order is read right. The project's own checks live where the gates
# convention's marked `**The location:**` line says; the checks the method
# ships are named by their path, whatever directory they were installed under.
#
# P0 — the subject is found. A table this project committed and then lost is
#      red; one it never had is a declared opt-out. The header names the ID
#      and Verification columns, or no clause can tell which cell to read. The
#      location of the project's own checks is read from the gates convention
#      and is a relative directory under the project.
# P1 — every row whose Verification names the location has a check there that
#      carries `# Verifies: {id}`, and every check the cell names by path
#      exists. The two are not one assertion: the claim is about the id, so a
#      row keeps passing it while the file it names is renamed or deleted.
# P2 — every row that names a check shipped beside a convention
#      (`…conventions/{name}/checks/check-*.sh`) points at a file that exists
#      and carries a `# Verifies:` line. A shipped check cannot claim a
#      project's id, so the coupling runs the other way.
# P3 — every id a check in the location claims has a row. Mentioning the id
#      in another row's prose is not having a row.
# P4 — every row has as many cells as the header. A row that does not is
#      reported here and skipped by P1 and P2, which would read another cell.
#
# A table whose rows name no check, with nothing claiming an id, leaves by a
# declared opt-out that counts its rows: a guardrail may be verified by a
# person, and a table of those has nothing for this check to judge — which is
# not the same as having judged it.
#
# The claim is a declared marker, never any mention: a first version grepped
# the bare id and passed on its own comment, which cited the ids it existed
# for. Ids and paths come out of the table and are matched as data, never as
# patterns: without -F a row named `must-x-00.` passes the claim for
# `must-x-004`.

set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd -P)
root=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "P0 FAIL: not inside a git work tree — the table and its absence are read from the project, so no repository is red, not an opt-out"
  exit 1
}
cd "$root" || exit 1

file=governance/guardrails.md
if [ ! -f "$file" ]; then
  last=$(git log -1 --format=%h -- "$file" 2>/dev/null)
  if [ -n "$last" ]; then
    echo "P0 FAIL: $file is missing and was committed before ($last) — it was lost, not declined"
    exit 1
  fi
  echo "check-guardrails: opt-out — this project has never had a $file"
  exit 0
fi

# The location of the project's own checks, read from the gates convention
# beside this one. The same block as the checks shipped beside that convention.
conv="$here/../../gates/convention.md"
[ -f "$conv" ] || { echo "P0 FAIL: $conv is missing — the location of the project's own checks is read from it"; exit 1; }
loc=$(awk -v h="## Where a project's own checks live" '/^## /{f=($0==h); next} f' "$conv" \
      | sed -n 's/^\*\*The location:\*\* `\([^`]*\)`.*$/\1/p' | head -n 1)
[ -n "$loc" ] || { echo "P0 FAIL: $conv has no \`**The location:**\` line in \`## Where a project's own checks live\`; the project's own checks cannot be found"; exit 1; }
case "$loc" in
  /*|*..*|*[!A-Za-z0-9._/-]*|*[!/]) echo "P0 FAIL: the location \`$loc\` read from $conv is not a relative directory under the project"; exit 1 ;;
esac
loc_re=$(printf '%s' "$loc" | sed 's/\./\\./g')

# Read one cell of a row, honouring the `\|` escape: `awk -F'|'` splits on an
# escaped pipe too, so a row that escapes its pipes — correct for GFM — would
# lose its alignment and every clause would read the wrong cell. The escape is
# neutralised before the split and restored after. The row arrives on stdin,
# never through `awk -v`, where an undefined escape such as `\|` is
# implementation-defined.
cell() {  # cell {n} {line}
  printf '%s' "$2" | awk -v n="$1" '{
    gsub(/\\\|/, "\001")
    m = split($0, a, "|")
    if (n > m) exit
    v = a[n]
    gsub(/\001/, "\\|", v)
    gsub(/^ +| +$/, "", v)
    print v
  }'
}
ncells() {  # ncells {line}
  printf '%s' "$1" | awk '{ gsub(/\\\|/, "\001"); print split($0, a, "|") }'
}

# The header: the first table line with a cell `ID` and a cell `Verification`.
header=""; col_id=0; col_ver=0
while IFS= read -r line; do
  n=$(ncells "$line"); i=2; ci=0; cv=0
  while [ "$i" -lt "$n" ]; do
    case "$(cell "$i" "$line")" in
      ID) ci=$i ;;
      Verification) cv=$i ;;
    esac
    i=$((i+1))
  done
  if [ "$ci" -gt 0 ] && [ "$cv" -gt 0 ]; then header=$line; col_id=$ci; col_ver=$cv; break; fi
done < <(grep -E '^\|' "$file")
if [ -z "$header" ]; then
  echo "P0 FAIL: $file has no header naming the columns ID and Verification, so no clause can tell which cell to read"
  exit 1
fi
want=$(ncells "$header")

claimed=""
[ -d "$loc" ] && claimed=$(grep -rhoE '^# Verifies: [a-z]+-[a-z]+-[0-9]{3}' "$loc" | awk '{print $3}' | sort -u)
nclaimed=$(printf '%s\n' "$claimed" | grep -c . || true)

rc=0; count=0; shipped=0; unautomated=0; nrows=0; ids=""
while IFS= read -r line; do
  id=$(cell "$col_id" "$line")
  case "$id" in must-*|should-*) ;; *) continue ;; esac
  nrows=$((nrows+1)); ids="$ids$id"$'\n'
  # P4 — the row's shape, before any clause reads a cell by position.
  got=$(ncells "$line")
  if [ "$got" -ne "$want" ]; then
    echo "P4 FAIL: $id has $got cells where the header has $want — no verdict about this row can be read off the right cell"
    rc=1
    continue
  fi
  verification=$(cell "$col_ver" "$line")
  paths=$(printf '%s' "$verification" | grep -oE '[A-Za-z0-9_./-]*conventions/[A-Za-z0-9_.-]+/checks/check-[A-Za-z0-9_-]+\.sh' || true)
  automated=0
  # P1 — a row that names the location.
  case "$verification" in
    *"$loc"*)
      automated=1; count=$((count+1))
      grep -Fx -- "$id" <<<"$claimed" >/dev/null || {
        echo "P1 FAIL: $id declares a check in $loc but no check claims it"
        rc=1
      }
      for p in $(printf '%s' "$verification" | grep -oE "${loc_re}[A-Za-z0-9_-]+(\\.[A-Za-z0-9]+)?" || true); do
        [ -f "$p" ] || { echo "P1 FAIL: $id names $p, which does not exist"; rc=1; }
      done ;;
  esac
  # P2 — a row that names a shipped check by its path.
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    automated=1; shipped=$((shipped+1))
    if [ ! -f "$p" ]; then
      echo "P2 FAIL: $id names the shipped check $p, which does not exist"
      rc=1
    elif ! grep -qE '^# Verifies: ' "$p"; then
      echo "P2 FAIL: $id names $p, which declares nothing it verifies (no \`# Verifies:\` line)"
      rc=1
    fi
  done <<< "$paths"
  [ "$automated" -eq 1 ] || unautomated=$((unautomated+1))
done < <(grep -E '^\|' "$file")

# P3 — every claimed id has its row.
while IFS= read -r id; do
  [ -n "$id" ] || continue
  grep -Fx -- "$id" <<<"$ids" >/dev/null || {
    echo "P3 FAIL: $id is claimed by $(grep -rlF -- "# Verifies: $id" "$loc" | xargs -n1 basename | tr '\n' ' ')but has no row in $file"
    rc=1
  }
done <<< "$claimed"

if [ "$rc" -eq 0 ]; then
  if [ "$count" -eq 0 ] && [ "$shipped" -eq 0 ] && [ "$nclaimed" -eq 0 ]; then
    echo "check-guardrails: opt-out — $file has $nrows rows and none names a check"
  else
    echo "check-guardrails: OK ($count declared in $loc, $shipped shipped by path, $nclaimed claimed ids each with its row, $unautomated declaring no check file)"
  fi
fi
exit $rc
