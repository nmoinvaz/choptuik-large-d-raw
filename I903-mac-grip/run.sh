#!/bin/bash
# #903 grip: run.sh NAME SCRIPT ARGS... runs hp/SCRIPT with ARGS from hp/ of the wip/xf-902 worktree (5e8b08db, near_null's
# --ks, as #902) on main 3c35f0c's hpkernel (i599/site2, the build of xfkappa's chain) and writes I903-mac-grip/NAME.log.
HP=/Users/nathan/Source/choptuik-large-d-902/hp
SITE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
PY=/Users/nathan/venv-314/bin/python3
OUT=$(cd "$(dirname "$0")" && pwd)
name=$1
shift
cd "$HP" || exit 9
{
  echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S') UTC, hp at $(git rev-parse --short=8 HEAD)$(git diff --quiet HEAD -- . || echo '+dirty'), $*"
  # The kernel must be site2's: from 07:02 to ~14:40 UTC on 2026-11-17 site2 lacked __init__.py and venv-314's loaded.
  k=$(PYTHONPATH=$SITE "$PY" -c "import hpkernel; print(hpkernel.__file__)" 2>&1)
  echo "hpkernel $k"
  case "$k" in "$SITE"/*) ;; *) echo "hpkernel is not site2's: stop"; echo "exit 7"; exit 7 ;; esac
  OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE nice -n 10 "$PY" -u "$@"
  echo "exit $?"
  echo "== end $(date -u '+%Y-%m-%d %H:%M:%S') UTC"
} > "$OUT/$name.log" 2>&1
