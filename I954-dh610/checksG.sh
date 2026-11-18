#!/bin/bash
# #954 isolation of B's checkq mismatch (B_checkq exit 1 at PRED, the ks 240 D 229.5165 prediction): the same line on build A, 1 thread (the budget is in use by checksC), nice 10.
. "$(dirname "$0")/common954.sh"
WT=/home/nathan/Source/choptuik-large-d-954a
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH="$WT/hp"
{ echo "# $(stamp) UTC build A, hp $(git -C $WT rev-parse --short HEAD)"; echo "# cmd: python reseed.py checkq $R/$PRED --threads 1"; } > $OUT/A_checkq.log
s=$(date +%s); nice -n 10 python reseed.py checkq $R/$PRED --threads 1 >> $OUT/A_checkq.log 2>&1; rc=$?
echo "exit $rc" >> $OUT/A_checkq.log
echo "A_checkq: exit $rc, $(( $(date +%s) - s )) s (B: exit 1, 76 s at 8 threads)" >> $OUT/summary_A.txt
