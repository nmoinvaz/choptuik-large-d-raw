#!/bin/bash
# #777: run.sh NAME BUILD SCRIPT ARGS... runs hp/SCRIPT with ARGS from hp/ of main 8e10d127 (newton_od's full_drop for
# the own test) and writes I777-mac/NAME.log, ending "exit N". BUILD: "old" is venv-314's hpkernel (before #523's exact
# freeze projector, the build #742 and #752 ran on), "new" the i599/site2 build of main 3c35f0c (after #523, #713's).
HP=/Users/nathan/Source/choptuik-large-d-777/hp
SITE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
PY=/Users/nathan/venv-314/bin/python3
OUT=$(cd "$(dirname "$0")" && pwd)
name=$1
build=$2
shift 2
cd "$HP" || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "8e10d127" ] || { echo "worktree is not at 8e10d127" > "$OUT/$name.log"; exit 9; }
PP=""
[ "$build" = new ] && PP=$SITE
{
  echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S') UTC, hp at $(git rev-parse --short=8 HEAD), build $build, $*"
  OPENBLAS_NUM_THREADS=1 PYTHONPATH=$PP nice -n 10 "$PY" -u "$@"
  echo "exit $?"
  echo "== end $(date -u '+%Y-%m-%d %H:%M:%S') UTC"
} > "$OUT/$name.log" 2>&1
