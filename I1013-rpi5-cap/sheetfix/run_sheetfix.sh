#!/bin/bash
# #1013 sheetfix (coordinator, 2026-11-20): the 2 cells of the upper box's step 1 that failed xfchecks' sheet check, recounted at
# xi1 0.17 at wip/argcount-m3-bounds 6da7da7b (the seed fix) from step 1's points file minus the 5 contaminated records
# (m3/points_M3_r0.17.jsonl here, removed_5_points.jsonl), same flags as run_rpi5_upper.sh except --procs=2 (two idle cores).
#   run_sheetfix.sh CODE PY OUT   CODE: the worktree at 6da7da7b; OUT: this folder (sheetfix/)
set -u
CODE=$1; PY=$2; OUT=$3
cd "$CODE/solver/inner_stokes" || exit 1
[ "$(git rev-parse HEAD)" = 6da7da7be3f2325208f2d4f9570a5e5a8790bd78 ] || { echo "CODE is not at 6da7da7b"; exit 1; }
P="$OUT/m3/points_M3_r0.17.jsonl"
[ "$(wc -l < "$P")" = 622 ] || { echo "the cache must hold 622 lines"; exit 1; }
[ -e "$OUT/logs/m3_sheetfix_r0.17.log" ] && { echo "the log exists: already run"; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
B="--m3fix --m3starts=0.2,0.25 --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=2"
X="$OUT/logs/exits.txt"
{ echo "start $(date -u '+%F %T') $(uname -srm)"; $PY -c 'import sys, numpy, scipy, mpmath; print(sys.version.split()[0], numpy.__version__, scipy.__version__, mpmath.__version__)'; } >> "$X"
$PY argcount.py --selftest > "$OUT/logs/selftest.log" 2>&1; s=$?
for m in nocap starts norecount lowcap seedfix; do $PY argcount.py --selftest --mutate=$m >> "$OUT/logs/selftest.log" 2>&1; s="$s $?"; done
echo "selftest, nocap, starts, norecount, lowcap, seedfix exits: $s" >> "$X"
[ "$s" = "0 1 1 1 1 1" ] || exit 1
echo "recount start $(date -u '+%F %T') cache $(wc -l < "$P") lines sha256 $(sha256sum "$P" | cut -d' ' -f1)" >> "$X"
nice -n 10 timeout 12h $PY -u argcount.py --M=3 --recount="$OUT/m3/leaves_2cells.jsonl" --r1=0.17 --r1b=0.18 $B \
    --out="$OUT/m3" --tag=M3_sheetfix_r0.17 > "$OUT/logs/m3_sheetfix_r0.17.log" 2>&1
echo "recount at 6da7da7b exit $? $(date -u '+%F %T')" >> "$X"
