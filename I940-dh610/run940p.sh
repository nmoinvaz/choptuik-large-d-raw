#!/bin/bash
# #940: the pinned jobs and the pinned dshift control on main 18dfeea7 (worktree choptuik-large-d-940c; the pin is taken from the file name, 18dfeea7's fix of the
# KeyError 'kfreeze' that the first pinned runs hit). First pilot3b: pin 5 at D 68.5 (T84-mac) and D 71.0 (T75), each unshifted and with --mutate dshift --dshift 1e-10,
# two streams of 2 threads at nice 10; then the 60 pinned jobs from D 71 (runs_pinned/jobs.txt) as three processes of 2 threads. Outputs pilot3b/, runs_pinned/.
WT=/home/nathan/Source/choptuik-large-d-940c
OUT=/home/nathan/Source/choptuik-large-d-raw/I940-dh610
IN=/home/nathan/scratch940/in
PY=/home/nathan/Source/choptuik-large-d-855/.venv/bin/python
log() { echo "940p $1 $(date -u '+%F %T') UTC" >> $OUT/exits_940.txt; }
cd $WT/hp || exit 9
log "start pilot3b at hp $(git rev-parse --short HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
q() { local tag=$1 st=$2; shift 2; nice -n 10 $PY -u qd_window.py $OUT/pilot3b/$tag.jsonl $st --mode pinned "$@" --states $OUT/pilot3b/states_$tag --threads 2 > $OUT/pilot3b/$tag.log 2>&1; echo "exit $?" >> $OUT/pilot3b/$tag.log; }
( q d68.5_base $IN/T84-mac/pin5_D68.5000.npz; q d68.5_dshift $IN/T84-mac/pin5_D68.5000.npz --mutate dshift --dshift 1e-10 ) &
( q d71.0_base $IN/T75/pin5_D71.0000.npz; q d71.0_dshift $IN/T75/pin5_D71.0000.npz --mutate dshift --dshift 1e-10 ) &
wait
log "pilot3b done"
log "start pinned queue, $(wc -l < $OUT/runs_pinned/jobs.txt) jobs"
xargs -P 3 -d '\n' -I{} bash -c '{}' < $OUT/runs_pinned/jobs.txt
log "pinned queue done"
cat $OUT/runs_pinned/jsonl/*.jsonl > $OUT/runs_pinned/qd_window_pinned.jsonl
log "merged $(wc -l < $OUT/runs_pinned/qd_window_pinned.jsonl) pinned records"
