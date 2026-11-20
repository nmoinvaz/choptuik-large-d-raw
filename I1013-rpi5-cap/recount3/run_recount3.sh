#!/bin/bash
# #1013 recount3 (coordinator, 2026-11-20): the 13 unresolved cells of the upper box recounted at xi1 0.18 at wip/argcount-m3-bounds
# 6da7da7b (the seed fix), --retry, --m3maxrhs=1e7, from step 2's 0.18 points without its 11 off-sheet records (m3/points_M3_r0.18.jsonl,
# removed_11_points.jsonl), seeds from the sheetfix's 0.17 points (m3/points_M3_r0.17.jsonl, 630 lines). Step 1's other flags, 4 procs.
#   run_recount3.sh CODE PY OUT   CODE: the worktree at 6da7da7b; OUT: this folder (recount3/)
set -u
CODE=$1; PY=$2; OUT=$3
cd "$CODE/solver/inner_stokes" || exit 1
[ "$(git rev-parse HEAD)" = 6da7da7be3f2325208f2d4f9570a5e5a8790bd78 ] || { echo "CODE is not at 6da7da7b"; exit 1; }
P="$OUT/m3/points_M3_r0.18.jsonl"; S="$OUT/m3/points_M3_r0.17.jsonl"
[ "$(wc -l < "$P")" = 58 ] || { echo "the cache must hold 58 lines"; exit 1; }
[ "$(wc -l < "$S")" = 630 ] || { echo "the seed file must hold 630 lines"; exit 1; }
[ "$(head -622 "$S" | sha256sum | cut -c1-16)" = 45856355359aabcb ] || { echo "the seed file's first 622 lines differ from the sheetfix's"; exit 1; }
[ -e "$OUT/logs/m3_recount3_r0.18.log" ] && { echo "the log exists: already run"; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
B="--m3fix --m3starts=0.2,0.25 --m3maxrhs=1e7 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry"
X="$OUT/logs/exits.txt"
{ echo "start $(date -u '+%F %T') $(uname -srm)"; $PY -c 'import sys, numpy, scipy, mpmath; print(sys.version.split()[0], numpy.__version__, scipy.__version__, mpmath.__version__)'; } >> "$X"
$PY argcount.py --selftest > "$OUT/logs/selftest.log" 2>&1; s=$?
for m in nocap starts norecount lowcap seedfix; do $PY argcount.py --selftest --mutate=$m >> "$OUT/logs/selftest.log" 2>&1; s="$s $?"; done
echo "selftest, nocap, starts, norecount, lowcap, seedfix exits: $s" >> "$X"
[ "$s" = "0 1 1 1 1 1" ] || exit 1
cd "$OUT" || exit 1
python3 sheet_precheck.py m3/points_M3_r0.17.jsonl m3/points_M3_r0.18.jsonl --quiet > logs/sheet_precheck.log 2>&1; a=$?
python3 sheet_precheck.py m3/points_M3_r0.17.jsonl m3/points_M3_r0.18.jsonl --mutate >> logs/sheet_precheck.log 2>&1; b=$?
python3 check_retry_reuse.py --selftest > logs/check_retry_reuse_selftest.log 2>&1; c=$?
echo "sheet_precheck on the cache (0 = no off-sheet point), its control (0 = reported), check_retry_reuse selftest: $a $b $c" >> "$X"
[ "$a $b $c" = "0 0 0" ] || exit 1
echo "recount start $(date -u '+%F %T') cache $(wc -l < "$P") lines sha256 $(sha256sum "$P" | cut -d' ' -f1) seed $(wc -l < "$S") lines sha256 $(sha256sum "$S" | cut -d' ' -f1)" >> "$X"
cd "$CODE/solver/inner_stokes" || exit 1
nice -n 10 timeout 12h $PY -u argcount.py --M=3 --recount="$OUT/m3/leaves_M3_upper_r0.17.jsonl" --r1=0.18 --r1b=0.17 --seed="$S" $B \
    --out="$OUT/m3" --tag=M3_recount3_r0.18 > "$OUT/logs/m3_recount3_r0.18.log" 2>&1
echo "recount at 6da7da7b exit $? $(date -u '+%F %T')" >> "$X"
