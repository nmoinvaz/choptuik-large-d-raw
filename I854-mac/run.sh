#!/bin/bash
# #854: run.sh NAME SCRIPT ARGS... runs hp/SCRIPT with ARGS from hp/ of a worktree (WT: 854, the wip/m752-854 worktree,
# 394e45b0 or later, by default; 839, the wip/i839 worktree at main 4617f876, for the code before #854) on main 3c35f0c's
# hpkernel build (i599/site2, as #713, #777 and #839), and writes I854-mac/NAME.log, ending "exit N".
WT=${WT:-854}
HP=/Users/nathan/Source/choptuik-large-d-$WT/hp
SITE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
PY=/Users/nathan/venv-314/bin/python3
OUT=$(cd "$(dirname "$0")" && pwd)
name=$1
shift
cd "$HP" || exit 9
if [ "$WT" = 854 ]; then
  git merge-base --is-ancestor 394e45b0 HEAD || { echo "worktree is older than 394e45b0" > "$OUT/$name.log"; exit 9; }
else
  [ "$(git rev-parse --short=8 HEAD)" = 4617f876 ] || { echo "worktree $WT is not at 4617f876" > "$OUT/$name.log"; exit 9; }
fi
{
  echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S') UTC, hp at $(git rev-parse --short=8 HEAD) ($WT), $*"
  echo "# hpkernel $(PYTHONPATH=$SITE "$PY" -c 'import hpkernel; print(hpkernel.__file__)')"
  OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE nice -n 10 "$PY" -u "$@"
  echo "exit $?"
  echo "== end $(date -u '+%Y-%m-%d %H:%M:%S') UTC"
} > "$OUT/$name.log" 2>&1
