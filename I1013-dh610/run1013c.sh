#!/bin/bash
# #1013 step 4 (the coordinator's order, comment of 2026-11-19 08:56 UTC; xfchecks' second M = 3 box for the upper chain of M = 1 zeros): runs only after run1013b.sh has ended with "all steps done"
# (steps 1 to 3 as ordered), never after a stop. Waits for that line (at most 30 h), then the three commands of the order: the box A 3.6-5.1, wf 0.5-1.3 (--nA=6 --nwf=8, 12 h cap), then its two
# recount rungs (xi1 0.25 and 0.17, 6 h caps), same N, out folder, seed and nice as the earlier steps.
. "$(dirname "$0")/common1013.sh"
EX=$RAW/exits_1013.txt
log() { echo "1013c $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
log "waiting for 1013b to end"
S=$(date +%s)
until grep -qE "^1013b (all steps done|stopped at)" $EX || [ $(( $(date +%s) - S )) -ge 108000 ]; do sleep 30; done
grep -q "^1013b all steps done" $EX || { log "1013b did not end with all steps done, step 4 not run"; exit 1; }
step() { local name=$1 want=$2; shift 2; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s"; [ $rc = $want ] || { log "stopped at $name"; exit 1; }; }
SEED=$RAW/m3/points_M3_r0.2.jsonl
step upper 0 bash -c "nice -n 10 timeout 12h $PY -u argcount.py --M=3 --A=3.6,5.1 --wf=0.5,1.3 --nA=6 --nwf=8 --procs=$N --out=$RAW/m3 --tag=M3_upper > $RAW/logs/m3_upper.log 2>&1"
step upper_r0.25 0 bash -c "nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_upper.jsonl --r1=0.25 --r1b=0.2 --seed=$SEED --procs=$N --out=$RAW/m3 --tag=M3_upper_r0.25 > $RAW/logs/m3_upper_r0.25.log 2>&1"
step upper_r0.17 0 bash -c "nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_upper_r0.25.jsonl --r1=0.17 --r1b=0.2 --seed=$SEED --procs=$N --out=$RAW/m3 --tag=M3_upper_r0.17 > $RAW/logs/m3_upper_r0.17.log 2>&1"
log "step 4 done"
