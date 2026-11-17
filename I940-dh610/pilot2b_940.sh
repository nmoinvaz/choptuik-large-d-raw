#!/bin/bash
# #940 (an addition to the control's one rerun, which did not converge at 1e-10): the same control at --dshift 1e-12 and 1e-14, two processes of
# 2 threads at nice 10, to find a shift that stays inside the full system's basin.
WT=/home/nathan/Source/choptuik-large-d-940b
OUT=/home/nathan/Source/choptuik-large-d-raw/I940-dh610/pilot2
IN=/home/nathan/scratch940/in
PY=/home/nathan/Source/choptuik-large-d-855/.venv/bin/python
cd $WT/hp || exit 9
for s in 1e-12 1e-14; do
  ( nice -n 10 $PY -u qd_window.py $OUT/dshift_$s.jsonl $IN/T84-mac/pin5_D68.5000.npz --mode full --mutate dshift --dshift $s --states $OUT/states_dshift_$s --threads 2 > $OUT/dshift_$s.log 2>&1; echo "exit $?" >> $OUT/dshift_$s.log ) &
done
wait
