#!/bin/sh
# I203-mac: the controls P1 and P2, then the real data, with the frozen method (code wip/i203 0d352f4).
# Run from solver/independent_second_zero of the code checkout; RAW is this repository's clone.
PY=/Users/nathan/venv-qd/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I203-mac
nice -n 10 $PY -I second_zero.py planted --wp 1.095 --seeds 1,2,3,4,5 --out $OUT/P1_wp1.095.json > $OUT/P1_stdout.txt 2>&1
echo "P1 exit $?" >> $OUT/exits.txt
nice -n 10 $PY -I second_zero.py planted --wp 1.15 --seeds 1,2,3,4,5 --out $OUT/P2_wp1.15.json > $OUT/P2_stdout.txt 2>&1
echo "P2 exit $?" >> $OUT/exits.txt
nice -n 10 $PY -I second_zero.py real --dir $RAW/I82-win2 --out $OUT/real.json > $OUT/real_stdout.txt 2>&1
echo "real exit $?" >> $OUT/exits.txt
