#!/bin/bash
# #940 (an addition: the kt control at kt - 4 moved Delta by -1.99e-29 and -2.58e-29, below the 1e-26 bar): the same pinned control at D 71.0 (T75, pin 5) with --dkt 2, 8 and 12,
# three processes of 2 threads at nice 10, main 68f5c439.
WT=/home/nathan/Source/choptuik-large-d-940d
OUT=/home/nathan/Source/choptuik-large-d-raw/I940-dh610/pilot4
IN=/home/nathan/scratch940/in
PY=/home/nathan/Source/choptuik-large-d-855/.venv/bin/python
cd $WT/hp || exit 9
for k in 2 8 12; do
  ( nice -n 10 $PY -u qd_window.py $OUT/d71.0_kt$k.jsonl $IN/T75/pin5_D71.0000.npz --mode pinned --mutate kt --dkt $k --states $OUT/states_d71.0_kt$k --threads 2 > $OUT/d71.0_kt$k.log 2>&1; echo "exit $?" >> $OUT/d71.0_kt$k.log ) &
done
wait
echo "# $(date -u '+%F %T') UTC pilot4b done" >> $OUT/pilot4.log
