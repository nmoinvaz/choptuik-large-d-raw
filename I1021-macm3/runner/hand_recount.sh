#!/bin/bash
# #1076 macm3b: pass 1's recount by hand (the coordinator's order, hc 2026-11-23 about 04:40 UTC): the driver's argcount line (run_fu022mp.sh, cc3c58e0's raw pin 0f3e5ef9) argument for argument,
# with capped_run.py (the driver's 16 h cap, 57600 s) in place of `timeout 16h` (macOS has none), the venv python for both, from the code worktree's inner_stokes directory,
# 1 thread per BLAS, nice 10, own session under caffeinate -is (launch_1070.py). The driver's recount_pass1.log and exits.txt stay as they are; this script writes logs/recount_pass1_hand.log and logs/hand_steps.txt.
{
RAW=/Users/nathan/Source/choptuik-large-d-raw-749p
OUT=$RAW/I1021-macm3/fu022mp
IS=/Users/nathan/Source/choptuik-inner-mp/solver/inner_stokes
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
CAP=/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_d195/capped_run.py
CELLS=$RAW/I1021-mac/rpi5_fu021/in/cells_unresolved11.jsonl
SEED=$OUT/m3/points_M3_r0.2.jsonl
H=$OUT/logs/hand_steps.txt
TAG=M3_fu022mp_pass1_r0.17
stamp() { date -u '+%F %T'; }
B="--m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry"
[ "$(git -C /Users/nathan/Source/choptuik-inner-mp rev-parse HEAD)" = "$(cat $RAW/I1021-mac/fu022mp/CODE_COMMIT)" ] || { echo "$(stamp) STOP: the code worktree is not at CODE_COMMIT" >> $H; exit 1; }
[ -z "$(git -C /Users/nathan/Source/choptuik-inner-mp status --porcelain -- solver)" ] || { echo "$(stamp) STOP: the code worktree has local changes in solver" >> $H; exit 1; }
CMD="cd $IS && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 $PY $CAP 57600 $PY -u argcount.py --M=3 --recount=$CELLS --r1=0.17 --r1b=0.2 --seed=$SEED $B --out=$OUT/m3 --tag=$TAG > $OUT/logs/recount_pass1_hand.log 2>&1"
{ echo "hand step 1 of the order (the driver's recount exit 127, timeout missing on macOS): the recount of pass 1 by hand"
  echo "command: $CMD"
  echo "capped_run.py blob $(git hash-object --no-filters $CAP | cut -c1-8) (at $CAP); code $(git -C /Users/nathan/Source/choptuik-inner-mp rev-parse HEAD); cells blob $(git hash-object --no-filters $CELLS | cut -c1-8); seed blob $(git hash-object --no-filters $SEED | cut -c1-8); cache lines $(wc -l < $OUT/m3/points_M3_r0.17.jsonl)"
  echo "start $(stamp)"; } >> $H
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
(cd $IS && nice -n 10 $PY $CAP 57600 $PY -u argcount.py --M=3 --recount=$CELLS --r1=0.17 --r1b=0.2 --seed=$SEED $B --out=$OUT/m3 --tag=$TAG > $OUT/logs/recount_pass1_hand.log 2>&1)
s=$?
echo "end $(stamp) exit $s (0 wanted; 124 is the cap)" >> $H
K=$OUT/m3/count_${TAG}.json
if [ -f $K ]; then
  u=$($PY -c 'import json, sys; print(len(json.load(open(sys.argv[1]))["unresolved"]))' "$K" 2>&1)
  echo "unresolved leaves (len of the unresolved list in $K): $u" >> $H
else
  echo "no $K" >> $H
fi
echo "hand steps done $(stamp)" >> $H
exit 0
}
