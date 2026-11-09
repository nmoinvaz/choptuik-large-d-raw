#!/bin/sh
# I214-mac: the family's exact zero and checks, then a pilot on a non-control configuration (w_p 1.105, seed 99).
# Run from solver/independent_second_zero. $1 is a directory holding I82-win2's three sigF_*.json.
PY=/Users/nathan/venv-314/bin/python
OUT=/Users/nathan/Source/choptuik-large-d-raw/I214-mac
nice -n 10 $PY -I -W ignore arc_family.py "$1" > $OUT/family_check.txt 2>&1
echo "family_check exit $?" >> $OUT/exits.txt
nice -n 10 $PY -I -W ignore second_zero.py planted --family arc --wp 1.105 --seeds 99 --out $OUT/pilot_wp1.105_seed99.json > $OUT/pilot_stdout.txt 2>&1
echo "pilot exit $?" >> $OUT/exits.txt
