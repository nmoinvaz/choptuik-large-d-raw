#!/bin/sh
# I214-mac: the arc family's fit to the data (no zero computed). Run from solver/independent_second_zero.
# $1 is a directory holding I82-win2's three sigF_w1.0x_K45_J1500_p1280.json.
PY=/Users/nathan/venv-314/bin/python
OUT=/Users/nathan/Source/choptuik-large-d-raw/I214-mac
nice -n 10 $PY -I -W ignore fit_arc.py "$1" > $OUT/fit_arc.txt 2>&1
echo "fit exit $?" >> $OUT/exits.txt
cp arc_fit.json $OUT/arc_fit.json
