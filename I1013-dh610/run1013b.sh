#!/bin/bash
# #1013, second driver (the coordinator's order (b), hc 2026-11-19): recount the pilot's 4 unresolved cells at xi1 0.25 (r1b 0.2), then the ones still unresolved at xi1 0.17; if every cell resolves
# (adding no zero, or a zero that is reported with its sign), run step 2 and its two recount rungs as in run1013.sh; if a rim cell stays unresolved at every radius, stop (it sits at wf 1.11-1.21,
# outside step 2's box wf 0.2-1.1) and report. Same flags, workers and nice as run1013.sh.
. "$(dirname "$0")/common1013.sh"
EX=$RAW/exits_1013.txt
log() { echo "1013b $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
log "start, code $(git -C $WT rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
step() { local name=$1 want=$2; shift 2; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s"; [ $rc = $want ] || { log "stopped at $name"; exit 1; }; }
SEED=$RAW/m3/points_M3_r0.2.jsonl
step recount_pilot_r0.25 0 bash -c "nice -n 10 timeout 2h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_pilot_known.jsonl --r1=0.25 --r1b=0.2 --seed=$SEED --procs=$N --out=$RAW/m3 --tag=pilot_r0.25 > $RAW/logs/m3_pilot_r0.25.log 2>&1"
if ! python3 $RAW/eval1013.py $RAW/m3/count_pilot_known.json $RAW/m3/count_pilot_r0.25.json > $RAW/logs/eval_pilot_r0.25.log 2>&1; then
  log "cells remain after xi1 0.25, recount at 0.17"
  step recount_pilot_r0.17 0 bash -c "nice -n 10 timeout 2h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_pilot_r0.25.jsonl --r1=0.17 --r1b=0.2 --seed=$SEED --procs=$N --out=$RAW/m3 --tag=pilot_r0.17 > $RAW/logs/m3_pilot_r0.17.log 2>&1"
  step eval_pilot 0 bash -c "python3 $RAW/eval1013.py $RAW/m3/count_pilot_known.json $RAW/m3/count_pilot_r0.25.json $RAW/m3/count_pilot_r0.17.json > $RAW/logs/eval_pilot_r0.17.log 2>&1"
else
  log "all pilot cells resolved at xi1 0.25"
fi
step cand 0 bash -c "nice -n 10 timeout 12h $PY -u argcount.py --M=3 --A=1.9,3.9 --wf=0.2,1.1 --nA=8 --nwf=9 --procs=$N --out=$RAW/m3 --tag=M3_cand > $RAW/logs/m3_cand.log 2>&1"
step recount_r0.25 0 bash -c "nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_cand.jsonl --r1=0.25 --r1b=0.2 --seed=$SEED --procs=$N --out=$RAW/m3 --tag=M3_cand_r0.25 > $RAW/logs/m3_cand_r0.25.log 2>&1"
step recount_r0.17 0 bash -c "nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_cand_r0.25.jsonl --r1=0.17 --r1b=0.2 --seed=$SEED --procs=$N --out=$RAW/m3 --tag=M3_cand_r0.17 > $RAW/logs/m3_cand_r0.17.log 2>&1"
log "all steps done"
