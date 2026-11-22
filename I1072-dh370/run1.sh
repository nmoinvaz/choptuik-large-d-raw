#!/bin/bash
# #1072 step 1 (unit i1072b): the mapped states at D 3.15, then the identity and gp-control selftest of lowD_gamma on the uniform state and one mapped M' 128 state.
# Cap 21600 s on the solve. Writes step1.txt and, at the end, STEP1_DONE.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1072-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
WT=/home/nathan/Source/choptuik-large-d-1072
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
SRC=$RAWIN/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
cd $WT/hp || exit 9
stamp() { date -u '+%F %T'; }
echo "$(stamp) UTC step 1 starts; worktree $(git -C $WT rev-parse --short=8 HEAD); load $(cut -d' ' -f1-3 /proc/loadavg)" > $OUT/step1.txt
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 46a8dac5 ] || { echo "$(stamp) UTC STOP: worktree not at 46a8dac5" >> $OUT/step1.txt; exit 1; }
[ "$(git hash-object --no-filters $SRC | cut -c1-8)" = df2ab378 ] || { echo "$(stamp) UTC STOP: input state is not blob df2ab378" >> $OUT/step1.txt; exit 1; }
mkdir -p $OUT/states
CMD="nice -n 10 timeout 21600 $PY -u tau_map_gain.py solve $SRC --pairs 0.5:96,0.5:128,0.4:96,0.4:128 --states $OUT/states --out $OUT/solve_D3.15.jsonl --threads 6"
echo "$(stamp) UTC cmd (cwd $WT/hp): $CMD" >> $OUT/step1.txt
t0=$(date +%s)
( $CMD > $OUT/solve_D3.15.log 2>&1 ); rc=$?
echo "$(stamp) UTC solve exit $rc, wall $(( $(date +%s) - t0 )) s" >> $OUT/step1.txt
echo "SOLVE EXIT $rc $(stamp) UTC" > $OUT/STEP1_DONE.txt
exit 0
}
