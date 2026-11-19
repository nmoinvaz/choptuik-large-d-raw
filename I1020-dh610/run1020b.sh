#!/bin/bash
# #1020 follow-up (the coordinator's order of 2026-11-19 ~12:20 UTC): second-radius checks at xi1 0.3 and 0.35 of the new extended-box zero (2.338793, 0.096238), and of #1013's two partners
# (they have values at xi1 0.25, and the minus one at 0.3, only). Same code, workers, nice and box shape as run1020.sh step 1 (A +- 0.05, wf +- 0.02, --nA=4 --nwf=4); each count at r1, each zero located again at r1b.
. "$(dirname "$0")/common1020.sh"
EX=$RAW/exits_1020.txt
log() { echo "1020b $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
log "start, code $(git -C $WT rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
try() { local name=$1 want=$2; shift 2; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s"; }
box2() { local tag=$1 A=$2 wf=$3 r1=$4 r1b=$5 seed=$6; try reloc2_$tag 0 bash -c "nice -n 10 timeout 2h $PY -u argcount.py --M=3 --A=$A --wf=$wf --nA=4 --nwf=4 --r1=$r1 --r1b=$r1b --seed=$seed --procs=$N --out=$RAW/m3 --tag=reloc2_$tag > $RAW/logs/m3_reloc2_$tag.log 2>&1"; }
box2 newzero 2.2888,2.3888 0.076,0.116 0.3 0.35 $RAW/m3/points_M3_r0.25.jsonl
box2 minus 2.5486,2.6486 0.205,0.245 0.35 0.3 $IN/points_M3_r0.25.jsonl
box2 plus 2.7948,2.8948 0.205,0.245 0.35 0.3 $IN/points_M3_r0.25.jsonl
try eval_reloc2 0 bash -c "$PY $RAW/reloc1020b.py > $RAW/logs/reloc2_eval.log 2>&1"
log "all steps done"
