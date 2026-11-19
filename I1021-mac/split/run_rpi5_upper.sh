#!/bin/bash
# #1013 step 4, rpi5's upper box cut to A <= 4.5, at wip/argcount-m3-bounds 998fd290 (noise cap 1e7): the count at
# xi1 0.17 with the 0.2 start first, then one recount rung at 0.18. Above A 4.5 real noise_3 passes 1e7 before xi1 0.17
# (A 5.11, #1021), so A 3.6-4.35 here: grid points A 3.6123-4.3623 (step 0.25), w/w_inf 0.5065-1.3065 (step 0.1)
#   run_rpi5_upper.sh CODE PY OUT   CODE: a choptuik-large-d worktree at 998fd290; OUT: a new raw folder (I1013-rpi5 stays)
set -u
CODE=$1; PY=$2; OUT=$3
cd "$CODE/solver/inner_stokes" || exit 1
[ "$(git rev-parse HEAD)" = 998fd290406b768c1e0e6e0b9a0dccf0844a9d1d ] || { echo "CODE is not at 998fd290"; exit 1; }
[ -e "$OUT/m3" ] && { echo "$OUT/m3 exists: use a fresh folder"; exit 1; }
mkdir -p "$OUT/m3" "$OUT/logs"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
B="--m3fix --m3starts=0.2,0.25 --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4"
X="$OUT/logs/exits.txt"
{ echo "start $(date -u '+%F %T') $(uname -srm)"; $PY -c 'import sys, numpy, scipy, mpmath; print(sys.version.split()[0], numpy.__version__, scipy.__version__, mpmath.__version__)'; } >> "$X"
$PY argcount.py --selftest > "$OUT/logs/selftest.log" 2>&1; s=$?
for m in nocap starts norecount lowcap; do $PY argcount.py --selftest --mutate=$m >> "$OUT/logs/selftest.log" 2>&1; s="$s $?"; done
echo "selftest, nocap, starts, norecount, lowcap exits: $s" >> "$X"
[ "$s" = "0 1 1 1 1" ] || exit 1
nice -n 10 timeout 12h $PY -u argcount.py --M=3 --A=3.6,4.35 --wf=0.5,1.3 --nA=3 --nwf=8 --r1=0.17 --r1b=0.18 $B \
    --out="$OUT/m3" --tag=M3_upper_r0.17 > "$OUT/logs/m3_upper_r0.17.log" 2>&1; e=$?
echo "step 1 (count at 0.17) exit $e $(date -u '+%F %T')" >> "$X"
[ $e = 0 ] || exit 1
nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount="$OUT/m3/leaves_M3_upper_r0.17.jsonl" --r1=0.18 --r1b=0.17 \
    --seed="$OUT/m3/points_M3_r0.17.jsonl" $B --out="$OUT/m3" --tag=M3_upper_r0.18 > "$OUT/logs/m3_upper_r0.18.log" 2>&1
echo "step 2 (recount at 0.18) exit $? $(date -u '+%F %T')" >> "$X"
