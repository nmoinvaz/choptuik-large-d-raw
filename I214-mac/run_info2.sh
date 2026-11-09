#!/bin/sh
# I214-mac: information runs added after the controls (not in the criteria). The P1 arc family with noise 3e-12 and
# 1e-11 (seeds 1-5), to find the noise at which its spread matches the real data's, then the spread comparison again.
# Run from solver/independent_second_zero. $1: a directory holding I203-mac/v2's real.json and P1_wp1.095.json.
PY=/Users/nathan/venv-314/bin/python
OUT=/Users/nathan/Source/choptuik-large-d-raw/I214-mac
for NZ in 3e-12 1e-11; do
  nice -n 10 $PY -I -W ignore second_zero.py planted --family arc --wp 1.095 --noise $NZ --seeds 1,2,3,4,5 --out $OUT/info_noise${NZ}_wp1.095.json > $OUT/info_noise${NZ}_stdout.txt 2>&1
  echo "info $NZ exit $?" >> $OUT/exits.txt
done
$PY -I spread_compare.py "$1/real.json" "$1/P1_wp1.095.json" $OUT/P1_wp1.095.json $OUT/info_noise1e-14_wp1.095.json $OUT/info_noise0_wp1.095.json $OUT/info_noise3e-12_wp1.095.json $OUT/info_noise1e-11_wp1.095.json > $OUT/spread_compare_all.md 2>&1
echo "spread_compare_all exit $? (verdict line is P1's, as before)" >> $OUT/exits.txt
