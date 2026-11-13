#!/bin/bash
# #713: run.sh NAME SCRIPT ARGS... runs hp/SCRIPT with ARGS from hp/ and writes I713-mac/NAME.log, ending "exit N".
# RAW is this file's repository root; HP the choptuik-large-d checkout's hp/; SITE the kernel build.
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a7cb7a3b927c2e92a/hp
SITE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
PY=/Users/nathan/venv-314/bin/python3
OUT=$(cd "$(dirname "$0")" && pwd)
name=$1
shift
cd "$HP" || exit 9
{
  echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S') UTC, hp at $(git rev-parse --short=8 HEAD), $*"
  OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE nice -n 10 "$PY" -u "$@"
  echo "exit $?"
  echo "== end $(date -u '+%Y-%m-%d %H:%M:%S') UTC"
} > "$OUT/$name.log" 2>&1
