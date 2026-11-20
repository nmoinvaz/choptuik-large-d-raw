#!/bin/bash
# #1013 upper box, rerun of step 1 after the 12 h cap cut it (coordinator, 2026-11-20): the same commit and flags as
# run_rpi5_upper.sh, with its own points file (m3/points_M3_r0.17.jsonl) as the cache, under a new 12 h cap; then step 2
# (the 0.18 recount) exactly as run_rpi5_upper.sh does.
#   run_rpi5_upper_rerun.sh CODE PY OUT   CODE: the worktree at 998fd290; OUT: the existing I1013-rpi5-cap folder
set -u
CODE=$1; PY=$2; OUT=$3
cd "$CODE/solver/inner_stokes" || exit 1
[ "$(git rev-parse HEAD)" = 998fd290406b768c1e0e6e0b9a0dccf0844a9d1d ] || { echo "CODE is not at 998fd290"; exit 1; }
P="$OUT/m3/points_M3_r0.17.jsonl"
[ -s "$P" ] || { echo "no points file $P"; exit 1; }
[ -e "$OUT/m3/leaves_M3_upper_r0.17.jsonl" ] && { echo "step 1 finished (leaves file exists): no rerun"; exit 1; }
[ -e "$OUT/logs/m3_upper_r0.17_rerun.log" ] && { echo "the rerun log exists: a rerun was started"; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
B="--m3fix --m3starts=0.2,0.25 --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4"
X="$OUT/logs/exits.txt"
n0=$(wc -l < "$P"); h0=$(sha256sum "$P" | cut -d' ' -f1)
echo "rerun of step 1 start $(date -u '+%F %T') cache $n0 lines sha256 $h0" >> "$X"
nice -n 10 timeout 12h $PY -u argcount.py --M=3 --A=3.6,4.35 --wf=0.5,1.3 --nA=3 --nwf=8 --r1=0.17 --r1b=0.18 $B \
    --out="$OUT/m3" --tag=M3_upper_r0.17 > "$OUT/logs/m3_upper_r0.17_rerun.log" 2>&1; e=$?
echo "step 1 rerun (count at 0.17) exit $e $(date -u '+%F %T')" >> "$X"
[ $e = 0 ] || exit 1
nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount="$OUT/m3/leaves_M3_upper_r0.17.jsonl" --r1=0.18 --r1b=0.17 \
    --seed="$OUT/m3/points_M3_r0.17.jsonl" $B --out="$OUT/m3" --tag=M3_upper_r0.18 > "$OUT/logs/m3_upper_r0.18.log" 2>&1
echo "step 2 (recount at 0.18) exit $? $(date -u '+%F %T')" >> "$X"
