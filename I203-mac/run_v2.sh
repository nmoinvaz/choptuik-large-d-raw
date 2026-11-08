#!/bin/sh
# I203-mac: v2 of the estimator (code wip/i203 3af9d9b): the controls P1 and P2 (seeds 1-5 are the controls,
# seeds 6-10 are extra), then the real data, then a stress family (eps 0.3, information only).
# Run from solver/independent_second_zero of the code checkout.
PY=/Users/nathan/venv-qd/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I203-mac/v2
mkdir -p $OUT
nice -n 10 $PY -I second_zero.py planted --wp 1.095 --seeds 1,2,3,4,5,6,7,8,9,10 --out $OUT/P1_wp1.095.json > $OUT/P1_stdout.txt 2>&1
echo "P1 exit $?" >> $OUT/exits.txt
nice -n 10 $PY -I second_zero.py planted --wp 1.15 --seeds 1,2,3,4,5,6,7,8,9,10 --out $OUT/P2_wp1.15.json > $OUT/P2_stdout.txt 2>&1
echo "P2 exit $?" >> $OUT/exits.txt
nice -n 10 $PY -I second_zero.py real --dir $RAW/I82-win2 --out $OUT/real.json > $OUT/real_stdout.txt 2>&1
echo "real exit $?" >> $OUT/exits.txt
nice -n 10 $PY -I second_zero.py planted --wp 1.1 --eps 0.3 --seeds 1,2,3 --out $OUT/stress_eps0.3_wp1.1.json > $OUT/stress_stdout.txt 2>&1
echo "stress exit $?" >> $OUT/exits.txt
