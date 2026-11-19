#!/bin/bash
# one of dh610's 068913b4 jobs of #1021's recount (boxes 11-15, 16-20 or 26-31) again at wip/argcount-m3-bounds 998fd290
# (point bounds, noise cap 1e7), from the job's own cache with --retry, so its points without value are computed again
# and its valued points kept; run it only after that 068913b4 job has stopped (rerun2_b21-25.sh is the 21-25 job's)
#   rerun2_box.sh CODE PY RAW BOXES   CODE: a choptuik-large-d worktree at 998fd290; PY: python; RAW: the raw clone's
#                                     root; BOXES: 11-15, 16-20 or 26-31
set -u
CODE=$1; PY=$2; RAW=$3; B=$4
case "$B" in 11-15|16-20|26-31) ;; *) echo "BOXES must be 11-15, 16-20 or 26-31"; exit 1;; esac
IN=$RAW/I1021-mac
OUT=$RAW/I1021-dh610
C=$OUT/b$B/points_M3_r0.17.jsonl
cd "$CODE/solver/inner_stokes" || exit 1
[ "$(git rev-parse HEAD)" = 998fd290406b768c1e0e6e0b9a0dccf0844a9d1d ] || { echo "CODE is not at 998fd290"; exit 1; }
pgrep -f "fix_b$B\$" > /dev/null && { echo "the 068913b4 job of b$B still runs: stop it first"; exit 1; }
head -n 617 "$C" | cmp -s - "$IN/split/points_M3_r0.17_in.jsonl" || { echo "b$B cache does not begin with the input"; exit 1; }
[ -z "$(tail -c 1 "$C")" ] || { echo "b$B cache ends inside a line"; exit 1; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "b$B rerun at 998fd290 start $(date -u '+%F %T'), cache $(wc -l < "$C") lines" >> "$OUT/logs/exits.txt"
L=$OUT/logs/selftest_998fd290_b$B.log
nice -n 10 $PY -u argcount.py --selftest > "$L" 2>&1; s=$?
for m in nocap lowcap; do nice -n 10 $PY -u argcount.py --selftest --mutate=$m >> "$L" 2>&1; s="$s $?"; done
echo "b$B selftest 998fd290, nocap, lowcap exits: $s" >> "$OUT/logs/exits.txt"
[ "$s" = "0 1 1" ] || exit 1
nice -n 10 timeout 24h $PY -u argcount.py --M=3 --recount="$IN/split/leaves_b$B.jsonl" --r1=0.17 --r1b=0.2 \
    --seed="$OUT/b$B/points_M3_r0.2.jsonl" --m3fix --retry --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 \
    --procs=3 --out="$OUT/b$B" --tag="M3_cand_r0.17_fix_b${B}_998fd290" > "$OUT/logs/recount_b${B}_998fd290.log" 2>&1
echo "b$B 998fd290 exit $? $(date -u '+%F %T')" >> "$OUT/logs/exits.txt"
