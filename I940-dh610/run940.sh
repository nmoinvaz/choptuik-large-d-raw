#!/bin/bash
# #940 on dh610: the window's solves of hp/qd_window.py as four processes of 2 threads at nice 10 (xargs -P 4 over runs/jobs.txt): below D 71
# --mode full on both states of each D (78), from D 71 --mode pinned on both (60), pin 5 below 71 again at --plan_tol 1e-34 (39),
# and from D 71 --mode full on both (60). Each job writes its own jsonl (runs/jsonl) and log (runs/logs); the states go to runs/states
# (runs/states_plan1e-34 for the finer plan). When the queue is empty the jsonl files are merged into runs/qd_window.jsonl.
OUT=/home/nathan/Source/choptuik-large-d-raw/I940-dh610
log() { echo "940 $1 $(date -u '+%F %T') UTC" >> $OUT/exits_940.txt; }
log "start window, $(wc -l < $OUT/runs/jobs.txt) jobs, load $(cut -d' ' -f1-3 /proc/loadavg)"
xargs -P 4 -d '\n' -I{} bash -c '{}' < $OUT/runs/jobs.txt
log "queue done"
cat $OUT/runs/jsonl/*.jsonl > $OUT/runs/qd_window.jsonl
log "merged $(wc -l < $OUT/runs/qd_window.jsonl) records into runs/qd_window.jsonl"
