#!/bin/bash
# #940: the kt control (the coordinator's, main 68f5c439): `qd_window.py --mode pinned --mutate kt` (Taylor order kt - 4, --dkt 4 by default) on pin 5 at
# D 68.5 (T84-mac) and D 71.0 (T75), 2 threads each at nice 10, from the worktree choptuik-large-d-940d. The unmutated pinned runs to compare with are pilot3b/d68.5_base and d71.0_base.
WT=/home/nathan/Source/choptuik-large-d-940d
OUT=/home/nathan/Source/choptuik-large-d-raw/I940-dh610/pilot4
IN=/home/nathan/scratch940/in
PY=/home/nathan/Source/choptuik-large-d-855/.venv/bin/python
cd $WT/hp || exit 9
echo "# $(date -u '+%F %T') UTC hp $(git rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)" > $OUT/pilot4.log
q() { local tag=$1 st=$2; shift 2; nice -n 10 $PY -u qd_window.py $OUT/$tag.jsonl $st --mode pinned "$@" --states $OUT/states_$tag --threads 2 > $OUT/$tag.log 2>&1; echo "exit $?" >> $OUT/$tag.log; }
q d68.5_kt $IN/T84-mac/pin5_D68.5000.npz --mutate kt &
q d71.0_kt $IN/T75/pin5_D71.0000.npz --mutate kt &
wait
echo "# $(date -u '+%F %T') UTC pilot4 done" >> $OUT/pilot4.log
