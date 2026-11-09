#!/bin/sh
# I214-mac: the controls P1 and P2 on the arc family (ten seeds each), the mutations M1 and M2, the information runs
# (noise 1e-14 and none), then the spread comparison. Run from solver/independent_second_zero of the code checkout.
# $1: a directory holding I82-win2's three sigF_*.json; $2: a directory holding I203-mac/v2's real.json and
# P1_wp1.095.json (from this repository).
PY=/Users/nathan/venv-314/bin/python
OUT=/Users/nathan/Source/choptuik-large-d-raw/I214-mac
S=1,2,3,4,5,6,7,8,9,10
nice -n 10 $PY -I -W ignore arc_family.py "$1" > $OUT/family_check.txt 2>&1
echo "family_check exit $?" >> $OUT/exits.txt
nice -n 10 $PY -I -W ignore second_zero.py planted --family arc --wp 1.095 --seeds $S --out $OUT/P1_wp1.095.json > $OUT/P1_stdout.txt 2>&1
echo "P1 exit $?" >> $OUT/exits.txt
nice -n 10 $PY -I -W ignore second_zero.py planted --family arc --wp 1.15 --seeds $S --out $OUT/P2_wp1.15.json > $OUT/P2_stdout.txt 2>&1
echo "P2 exit $?" >> $OUT/exits.txt
nice -n 10 $PY -I -W ignore mutate_truncate.py 1 --family arc > $OUT/M1_mutate_truncate_seed1.txt 2>&1
echo "M1 exit $? (0 = the mutation fired)" >> $OUT/exits.txt
nice -n 10 $PY -I -W ignore second_zero.py planted --family arc --wp 1.095 --mutate_wshift 0.01 --seeds 1 --out $OUT/M2_wshift0.01.json > $OUT/M2_stdout.txt 2>&1
echo "M2 exit $? (1 = the mutation fired)" >> $OUT/exits.txt
nice -n 10 $PY -I -W ignore second_zero.py planted --family arc --wp 1.095 --noise 1e-14 --seeds 1,2,3,4,5 --out $OUT/info_noise1e-14_wp1.095.json > $OUT/info_noise1e-14_stdout.txt 2>&1
echo "info 1e-14 exit $?" >> $OUT/exits.txt
nice -n 10 $PY -I -W ignore second_zero.py planted --family arc --wp 1.095 --noise 0 --seeds 1 --out $OUT/info_noise0_wp1.095.json > $OUT/info_noise0_stdout.txt 2>&1
echo "info 0 exit $?" >> $OUT/exits.txt
$PY -I spread_compare.py "$2/real.json" "$2/P1_wp1.095.json" $OUT/P1_wp1.095.json $OUT/info_noise1e-14_wp1.095.json $OUT/info_noise0_wp1.095.json > $OUT/spread_compare.md 2>&1
echo "spread_compare exit $? (0 = matches, 2 = does not)" >> $OUT/exits.txt
