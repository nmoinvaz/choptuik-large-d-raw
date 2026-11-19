#!/bin/bash
# #1020 (dh610): step 1 relocates #1013's two M = 3 partners at xi1 0.3 (second radius 0.17) by small boxes, with the known zero as control; step 2 counts the extended box A 1.9-3.0, wf 0.03-0.2
# with #1013's step-2 settings (xi1 0.2, --nA=8 --nwf=9, second radius 0.17) and its two recount rungs (xi1 0.25, 0.17). Same code (cl-995 fc7dee4d), workers and nice as run1013b.sh.
# Step 1's boxes and its verdict never stop step 2; step 2 and its rungs stop the run when one fails.
. "$(dirname "$0")/common1020.sh"
EX=$RAW/exits_1020.txt
log() { echo "1020 $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/m3 $RAW/logs
log "start, code $(git -C $WT rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
try() { local name=$1 want=$2; shift 2; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s"; }
step() { local name=$1 want=$2; shift 2; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s"; [ $rc = $want ] || { log "stopped at $name"; exit 1; }; }
# step 1: the control (the known zero), then the two partners, each A +- 0.05 around the xi1 0.25 place, wf as given; xi1 0.3, second radius 0.17, F_3 seeded from #1013's xi1 0.25 points
box1() { local tag=$1 A=$2 wf=$3; try reloc_$tag 0 bash -c "nice -n 10 timeout 2h $PY -u argcount.py --M=3 --A=$A --wf=$wf --nA=4 --nwf=4 --r1=0.3 --r1b=0.17 --seed=$IN/points_M3_r0.25.jsonl --procs=$N --out=$RAW/m3 --tag=reloc_$tag > $RAW/logs/m3_reloc_$tag.log 2>&1"; }
box1 control 2.6765,2.7765 0.9956,1.0356
box1 minus 2.5486,2.6486 0.205,0.245
box1 plus 2.7948,2.8948 0.205,0.245
try eval_reloc 0 bash -c "$PY $RAW/reloc1020.py > $RAW/logs/reloc_eval.log 2>&1"
# step 2
SEEDX=$IN/points_M3_r0.2.jsonl
step ext 0 bash -c "nice -n 10 timeout 12h $PY -u argcount.py --M=3 --A=1.9,3.0 --wf=0.03,0.2 --nA=8 --nwf=9 --seed=$SEEDX --procs=$N --out=$RAW/m3 --tag=M3_ext > $RAW/logs/m3_ext.log 2>&1"
SEED=$RAW/m3/points_M3_r0.2.jsonl
step ext_r0.25 0 bash -c "nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_ext.jsonl --r1=0.25 --r1b=0.2 --seed=$SEED --procs=$N --out=$RAW/m3 --tag=M3_ext_r0.25 > $RAW/logs/m3_ext_r0.25.log 2>&1"
step ext_r0.17 0 bash -c "nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_ext_r0.25.jsonl --r1=0.17 --r1b=0.2 --seed=$SEED --procs=$N --out=$RAW/m3 --tag=M3_ext_r0.17 > $RAW/logs/m3_ext_r0.17.log 2>&1"
log "all steps done"
