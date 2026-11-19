#!/bin/bash
# #1020 second-radius checks, rerun of the partners with the A grid moved: run1020b.sh's boxes centred each partner's zero on the box's central grid line (A +- 0.05 around 2.5986 and 2.8448), and the first run's unresolved
# cells at xi1 0.35 are the two cells that share a line 1.5e-4 (minus) and 1.2e-4 (plus) from the zero. Here the zero sits at 0.4 of the box (A0 = A - 0.04, A1 = A + 0.06), wf and everything else as in run1020b.sh.
. "$(dirname "$0")/common1020.sh"
EX=$RAW/exits_1020.txt
log() { echo "1020c $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
log "start, code $(git -C $WT rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg)"
try() { local name=$1 want=$2; shift 2; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s"; }
box3() { local tag=$1 A=$2 wf=$3 r1=$4 r1b=$5 seed=$6; try reloc3_$tag 0 bash -c "nice -n 10 timeout 2h $PY -u argcount.py --M=3 --A=$A --wf=$wf --nA=4 --nwf=4 --r1=$r1 --r1b=$r1b --seed=$seed --procs=$N --out=$RAW/m3 --tag=reloc3_$tag > $RAW/logs/m3_reloc3_$tag.log 2>&1"; }
box3 minus 2.5586,2.6586 0.205,0.245 0.35 0.3 $IN/points_M3_r0.25.jsonl
box3 plus 2.8048,2.9048 0.205,0.245 0.35 0.3 $IN/points_M3_r0.25.jsonl
try eval_reloc3 0 bash -c "$PY $RAW/reloc1020b.py --prefix reloc3 --names minus,plus > $RAW/logs/reloc3_eval.log 2>&1"
log "all steps done"
