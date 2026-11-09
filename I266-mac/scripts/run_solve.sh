#!/bin/bash
# One M = 48 solve of #266 (hp/gamma_m48_gap.py solve), from the worktree root:
#   run_solve.sh STATE PATH TAG [more options]     (PATH gamma | r2 | polish)
PY=/Users/nathan/venv-314/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw/I266-mac
caffeinate -i nice -n 10 $PY -u hp/gamma_m48_gap.py solve $RAW/states "$1" --path="$2" "${@:4}" > $RAW/logs/solve_$3.log 2>&1
echo "solve_$3 exit $?" >> $RAW/logs/exits.txt
