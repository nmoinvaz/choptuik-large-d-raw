#!/bin/bash
# boxes 21-25 of #1021's recount again at wip/argcount-m3-bounds 728f59c7 (point bounds, noise cap), from the job's own
# cache after its stop; the other three dh610 jobs stay on 068913b4
#   rerun_b21-25.sh CODE PY RAW    CODE: a choptuik-large-d worktree at 728f59c7; PY: python; RAW: the raw clone's root
set -u
CODE=$1; PY=$2; RAW=$3
IN=$RAW/I1021-mac
OUT=$RAW/I1021-dh610
cd "$CODE/solver/inner_stokes" || exit 1
[ "$(git rev-parse HEAD)" = 728f59c70b14ac3103658fcfc746e5d968a8a0de ] || { echo "CODE is not at 728f59c7"; exit 1; }
n=$(wc -l < "$OUT/b21-25/points_M3_r0.17.jsonl")
head -n 617 "$OUT/b21-25/points_M3_r0.17.jsonl" | cmp -s - "$IN/split/points_M3_r0.17_in.jsonl" || { echo "b21-25 cache does not begin with the input"; exit 1; }
[ -z "$(tail -c 1 "$OUT/b21-25/points_M3_r0.17.jsonl")" ] || { echo "b21-25 cache ends inside a line"; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "b21-25 rerun at 728f59c7 start $(date -u '+%F %T'), cache $n lines" >> "$OUT/logs/exits.txt"
nice -n 10 $PY -u argcount.py --selftest > "$OUT/logs/selftest_728f59c7.log" 2>&1; s=$?
nice -n 10 $PY -u argcount.py --selftest --mutate=nocap >> "$OUT/logs/selftest_728f59c7.log" 2>&1; m=$?
echo "selftest 728f59c7 exit $s, --mutate=nocap exit $m" >> "$OUT/logs/exits.txt"
[ $s = 0 ] && [ $m = 1 ] || exit 1
nice -n 10 timeout 24h $PY -u argcount.py --M=3 --recount="$IN/split/leaves_b21-25.jsonl" --r1=0.17 --r1b=0.2 \
    --seed="$OUT/b21-25/points_M3_r0.2.jsonl" --m3fix --retry --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=100 \
    --procs=3 --out="$OUT/b21-25" --tag=M3_cand_r0.17_fix_b21-25_728f59c7 > "$OUT/logs/recount_b21-25_728f59c7.log" 2>&1
echo "b21-25 728f59c7 exit $? $(date -u '+%F %T')" >> "$OUT/logs/exits.txt"
