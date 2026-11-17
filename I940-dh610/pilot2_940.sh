#!/bin/bash
# #940: the dshift control again at main 92019bc7 (--dshift 1e-10), pin 5 at D 68.5, --mode full, 2 threads, nice 10, from a second worktree
# (choptuik-large-d-940b) so that the running queue keeps its own code.
WT=/home/nathan/Source/choptuik-large-d-940b
OUT=/home/nathan/Source/choptuik-large-d-raw/I940-dh610/pilot2
IN=/home/nathan/scratch940/in
PY=/home/nathan/Source/choptuik-large-d-855/.venv/bin/python
cd $WT/hp || exit 9
echo "# $(date -u '+%F %T') UTC hp $(git rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > $OUT/dshift.log
nice -n 10 $PY -u qd_window.py $OUT/dshift.jsonl $IN/T84-mac/pin5_D68.5000.npz --mode full --mutate dshift --dshift 1e-10 --states $OUT/states_dshift --threads 2 >> $OUT/dshift.log 2>&1
echo "exit $?" >> $OUT/dshift.log
