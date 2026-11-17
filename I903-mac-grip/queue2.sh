#!/bin/bash
# #903 p_min question: queue2.sh runs the lines of q2.txt one at a time, in order, skipping those in q2done.txt; a line
# is "nn TAG STATE K" (one.sh) or "py NAME SCRIPT ARGS" (python, log NAME.log). The file is re-read after each run, so
# lines can be added while it runs. Stops when none is left, or after 16 runs.
O=$(cd "$(dirname "$0")" && pwd)
PY=/Users/nathan/venv-314/bin/python3
SITE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
touch "$O/q2done.txt"
for n in $(seq 16); do
  line=$(grep -vxF -f "$O/q2done.txt" "$O/q2.txt" | grep -v '^#' | grep . | head -1)
  [ -z "$line" ] && { echo "queue empty $(date -u '+%H:%M')"; exit 0; }
  echo "start $line $(date -u '+%H:%M')"
  set -- $line
  case $1 in
    nn) "$O/one.sh" "$2" "$3" "$4" ;;
    py) name=$2; shift 2; { echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $*"; OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE nice -n 10 "$PY" -u "$@"; echo "exit $?"; } > "$O/$name.log" 2>&1 ;;
  esac
  echo "$line" >> "$O/q2done.txt"
  echo "done $line $(date -u '+%H:%M')"
done
