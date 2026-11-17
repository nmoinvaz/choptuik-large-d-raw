#!/bin/bash
# #940: the pinned-mode dshift control (the coordinator's choice after the full mode's did not converge): qd_window.py at main 92019bc7 --mode pinned,
# pin 5 at D 68.5 (T84-mac) and at D 71.0 (T75), each unshifted (the baseline) and with --mutate dshift --dshift 1e-10, as two streams of 2 threads at nice 10.
WT=/home/nathan/Source/choptuik-large-d-940b
OUT=/home/nathan/Source/choptuik-large-d-raw/I940-dh610/pilot3
IN=/home/nathan/scratch940/in
PY=/home/nathan/Source/choptuik-large-d-855/.venv/bin/python
cd $WT/hp || exit 9
echo "# $(date -u '+%F %T') UTC hp $(git rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > $OUT/pilot3.log
q() { local tag=$1 st=$2; shift 2; nice -n 10 $PY -u qd_window.py $OUT/$tag.jsonl $st --mode pinned "$@" --states $OUT/states_$tag --threads 2 > $OUT/$tag.log 2>&1; echo "exit $?" >> $OUT/$tag.log; }
( q d68.5_base $IN/T84-mac/pin5_D68.5000.npz; q d68.5_dshift $IN/T84-mac/pin5_D68.5000.npz --mutate dshift --dshift 1e-10 ) &
( q d71.0_base $IN/T75/pin5_D71.0000.npz; q d71.0_dshift $IN/T75/pin5_D71.0000.npz --mutate dshift --dshift 1e-10 ) &
wait
echo "# $(date -u '+%F %T') UTC pilot3 done" >> $OUT/pilot3.log
