#!/bin/bash
# #899: run.sh NAME SCRIPT ARGS... runs hp/SCRIPT with ARGS from hp/ of the wip/xf-900 worktree (main 1dee59e4,
# #884's 6118a8be and the blend, ea36b6c0) on main 3c35f0c's hpkernel (i599/site2) and writes I899-mac/NAME.log,
# ending "exit N".
HP=/Users/nathan/Source/choptuik-large-d-900/hp
SITE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
PY=/Users/nathan/venv-314/bin/python3
OUT=$(cd "$(dirname "$0")" && pwd)
name=$1
shift
cd "$HP" || exit 9
{
  echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S') UTC, hp at $(git rev-parse --short=8 HEAD)$(git diff --quiet HEAD -- . || echo '+dirty'), $*"
  OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE nice -n 10 "$PY" -u "$@"
  echo "exit $?"
  echo "== end $(date -u '+%Y-%m-%d %H:%M:%S') UTC"
} > "$OUT/$name.log" 2>&1
