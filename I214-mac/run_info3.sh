#!/bin/sh
# I214-mac: information runs added after the controls (not in the criteria). #203's sens_noise.py on the real data
# with relative noise 1e-12 and 3e-12, to see whether noise at the level that matches the arc family's spread to the
# data's also costs the real data approximants (the real data admits 70/70 at every node).
# Run from solver/independent_second_zero. $1: a directory holding I82-win2's three sigF_*.json.
PY=/Users/nathan/venv-314/bin/python
OUT=/Users/nathan/Source/choptuik-large-d-raw/I214-mac
for NZ in 1e-12 3e-12; do
  for SD in 1 2; do
    nice -n 10 $PY -I -W ignore sens_noise.py "$1" $NZ $SD > $OUT/real_sens_noise${NZ}_seed$SD.txt 2>&1
    echo "real sens_noise $NZ seed $SD exit $?" >> $OUT/exits.txt
  done
done
