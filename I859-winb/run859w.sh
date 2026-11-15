#!/bin/bash
# stage 2 of #859 (runner's launcher; the issue's walks and the width at each walk's end, for the arms given as arguments)
W=/c/Users/nathan/Source/choptuik-i859
RAW=/c/Users/nathan/Source/choptuik-large-d-raw-754
O=$RAW/I859-winb
A=$RAW/I846-winb
PY=/c/Users/nathan/Source/venv-t179/Scripts/python.exe
export OPENBLAS_NUM_THREADS=3 PYTHONUNBUFFERED=1
cd "$W/solver/matter" || exit 99
ts() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
step() { n=$1; shift; echo "$n start $(ts)" >> "$O/exits_859.txt"; "$@" > "$O/$n.log" 2>&1; rc=$?; echo "$n exit $rc $(ts)" >> "$O/exits_859.txt"; }
declare -A D=([a]=9 [b]=9 [c]=10 [e]=10)
declare -A KC=([a]=15 [b]=23 [c]=15 [e]=23)
for x in "$@"; do
  step walk_$x $PY sigdss_band.py walk $A/sigdss_sol_ref_i846${x}_D${D[$x]}.0000_eta1.0000.npy --D ${D[$x]} --eps 1 --kc ${KC[$x]} --maxjac 250 --out $O/walk_$x.npy --json $O/walk.jsonl
  step width_walk_$x $PY sigdss_band.py width $O/walk_$x.npy --D ${D[$x]} --eps 1 --kc ${KC[$x]} --json $O/width.jsonl
  echo "arm $x done $(ts)" >> "$O/exits_859.txt"
done
