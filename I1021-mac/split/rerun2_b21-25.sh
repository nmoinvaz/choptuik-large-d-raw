#!/bin/bash
# boxes 21-25 of #1021's recount again at wip/argcount-m3-bounds 998fd290 (noise cap 1e7), from the job's own cache with
# --retry, so the points the 728f59c7 run (cap 1e2) left without value are computed again; run it after that job stops
#   rerun2_b21-25.sh CODE PY RAW    CODE: a choptuik-large-d worktree at 998fd290; PY: python; RAW: the raw clone's root
set -u
CODE=$1; PY=$2; RAW=$3
IN=$RAW/I1021-mac
OUT=$RAW/I1021-dh610
C=$OUT/b21-25/points_M3_r0.17.jsonl
cd "$CODE/solver/inner_stokes" || exit 1
[ "$(git rev-parse HEAD)" = 998fd290406b768c1e0e6e0b9a0dccf0844a9d1d ] || { echo "CODE is not at 998fd290"; exit 1; }
pgrep -f 'fix_b21-25_728f59c7' > /dev/null && { echo "the 728f59c7 job still runs: stop it first"; exit 1; }
head -n 617 "$C" | cmp -s - "$IN/split/points_M3_r0.17_in.jsonl" || { echo "b21-25 cache does not begin with the input"; exit 1; }
[ -z "$(tail -c 1 "$C")" ] || { echo "b21-25 cache ends inside a line"; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "b21-25 rerun at 998fd290 start $(date -u '+%F %T'), cache $(wc -l < "$C") lines" >> "$OUT/logs/exits.txt"
nice -n 10 $PY -u argcount.py --selftest > "$OUT/logs/selftest_998fd290.log" 2>&1; s=$?
for m in nocap lowcap; do nice -n 10 $PY -u argcount.py --selftest --mutate=$m >> "$OUT/logs/selftest_998fd290.log" 2>&1; s="$s $?"; done
echo "selftest 998fd290, nocap, lowcap exits: $s" >> "$OUT/logs/exits.txt"
[ "$s" = "0 1 1" ] || exit 1
nice -n 10 timeout 24h $PY -u argcount.py --M=3 --recount="$IN/split/leaves_b21-25.jsonl" --r1=0.17 --r1b=0.2 \
    --seed="$OUT/b21-25/points_M3_r0.2.jsonl" --m3fix --retry --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 \
    --procs=3 --out="$OUT/b21-25" --tag=M3_cand_r0.17_fix_b21-25_998fd290 > "$OUT/logs/recount_b21-25_998fd290.log" 2>&1
echo "b21-25 998fd290 exit $? $(date -u '+%F %T')" >> "$OUT/logs/exits.txt"
