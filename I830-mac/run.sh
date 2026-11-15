#!/bin/bash
# #830: run.sh NAME SCRIPT ARGS... runs hp/SCRIPT with ARGS from hp/ of the wip/i830 worktree (01c5df20 or later) on
# the new build (main 3c35f0c's hpkernel, i599/site2, which #713 and #777's rerun used), and writes I830-mac/NAME.log,
# ending "exit N".
HP=/Users/nathan/Source/choptuik-large-d-830/hp
SITE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
PY=/Users/nathan/venv-314/bin/python3
OUT=$(cd "$(dirname "$0")" && pwd)
name=$1
shift
cd "$HP" || exit 9
git merge-base --is-ancestor 01c5df20 HEAD || { echo "worktree is older than 01c5df20" > "$OUT/$name.log"; exit 9; }
{
  echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S') UTC, hp at $(git rev-parse --short=8 HEAD), $*"
  echo "# hpkernel $(PYTHONPATH=$SITE "$PY" -c 'import hpkernel; print(hpkernel.__file__)')"
  OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE nice -n 10 "$PY" -u "$@"
  echo "exit $?"
  echo "== end $(date -u '+%Y-%m-%d %H:%M:%S') UTC"
} > "$OUT/$name.log" 2>&1
