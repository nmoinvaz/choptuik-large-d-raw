#!/bin/bash
# #1076 macm3b: pass 2 by hand (the coordinator's order, hc 2026-11-23 about 05:20 UTC), as the driver's pass 2 would run (run_fu022mp.sh at raw 0f3e5ef9):
# 1 select (stop if the stderr differs from the expected line), 2 value (value_mp.py batch, 6 processes), 3 recount (only if the value step exits 0 and valued at least 1 point; the pass-1 command with
# --tag=M3_fu022mp_pass2_r0.17 under capped_run.py 57600), 4 prefix_keys fu021 -> fu022mp. Everything is recorded in logs/hand_steps.txt. Own session under caffeinate -is (launch_1070.py).
{
R=/Users/nathan/Source/choptuik-large-d-raw-749p
OUT=$R/I1021-macm3/fu022mp
CODE=/Users/nathan/Source/choptuik-inner-mp
IS=$CODE/solver/inner_stokes
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
CAP=/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_d195/capped_run.py
S21=$R/I1021-mac/rpi5_fu021; F21=$R/I1021-rpi5/fu021/m3
CELLS=$S21/in/cells_unresolved11.jsonl; SEED=$OUT/m3/points_M3_r0.2.jsonl
C=$OUT/m3/points_M3_r0.17.jsonl; L1=$OUT/m3/leaves_M3_fu022mp_pass1_r0.17.jsonl; R1=$OUT/rows_pass1.jsonl
H=$OUT/logs/hand_steps.txt
stamp() { date -u '+%F %T'; }
[ "$(git -C $CODE rev-parse HEAD)" = "$(cat $R/I1021-mac/fu022mp/CODE_COMMIT)" ] && [ -z "$(git -C $CODE status --porcelain -- solver)" ] || { echo "$(stamp) STOP: the code worktree is not at CODE_COMMIT or has local changes in solver" >> $H; exit 1; }
echo "" >> $H
echo "hand pass 2 (the coordinator's order after the pass 1 recount): select, value, recount, prefix_keys; start $(stamp)" >> $H
# 1 select
echo "select command: cd $S21 && PTS=\$($PY select_points.py $CODE $C $L1 $R1 2> $OUT/logs/select_pass2.log)" >> $H
PTS=$(cd $S21 && $PY select_points.py $CODE $C $L1 $R1 2> $OUT/logs/select_pass2.log); sel=$?
echo "pass 2 select exit $sel $(stamp): $(cat $OUT/logs/select_pass2.log)" >> $H
EXP="12 points without value in 17 unresolved leaves; 1 already run; 11 to run"
[ "$(cat $OUT/logs/select_pass2.log)" = "$EXP" ] || { echo "$(stamp) STOP: the select line differs from the expected '$EXP'" >> $H; exit 1; }
[ -n "$PTS" ] || { echo "$(stamp) STOP: select printed no points" >> $H; exit 1; }
echo "pass 2 points: $PTS" >> $H
# 2 value
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "pass 2 value command: cd $IS && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 $PY -u value_mp.py batch $C $OUT/rows_pass2.jsonl --points=\"\$PTS\" --procs=6 > $OUT/logs/value_pass2.log 2>&1" >> $H
echo "pass 2 value start $(stamp) cache $(wc -l < $C) lines" >> $H
(cd $IS && nice -n 10 $PY -u value_mp.py batch $C $OUT/rows_pass2.jsonl --points="$PTS" --procs=6 > $OUT/logs/value_pass2.log 2>&1); v=$?
echo "pass 2 value exit $v $(stamp): $(tail -1 $OUT/logs/value_pass2.log)" >> $H
rec=0
if [ $v != 0 ]; then echo "pass 2 value step failed: no recount" >> $H
elif grep -q '^valued 0 of' $OUT/logs/value_pass2.log; then echo "pass 2 valued no point: no recount" >> $H
else rec=1; fi
# 3 recount
if [ $rec = 1 ]; then
  TAG=M3_fu022mp_pass2_r0.17; B="--m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry"
  echo "pass 2 recount command: cd $IS && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 $PY $CAP 57600 $PY -u argcount.py --M=3 --recount=$CELLS --r1=0.17 --r1b=0.2 --seed=$SEED $B --out=$OUT/m3 --tag=$TAG > $OUT/logs/recount_pass2_hand.log 2>&1" >> $H
  echo "pass 2 recount start $(stamp) cache $(wc -l < $C) lines" >> $H
  (cd $IS && nice -n 10 $PY $CAP 57600 $PY -u argcount.py --M=3 --recount=$CELLS --r1=0.17 --r1b=0.2 --seed=$SEED $B --out=$OUT/m3 --tag=$TAG > $OUT/logs/recount_pass2_hand.log 2>&1); s=$?
  echo "pass 2 recount exit $s $(stamp) (0 wanted; 124 is the cap)" >> $H
  K=$OUT/m3/count_${TAG}.json
  if [ $s = 0 ] && [ -f $K ]; then echo "pass 2 unresolved leaves (len of the unresolved list in $K): $($PY -c 'import json, sys; print(len(json.load(open(sys.argv[1]))["unresolved"]))' "$K" 2>&1)" >> $H
  else echo "pass 2 recount: no count (exit $s)" >> $H; fi
fi
# 4 prefix_keys, as the driver's last step
$PY $S21/prefix_keys.py $F21/points_M3_r0.17.jsonl $C > $OUT/logs/prefix_keys_pass2.log 2>&1
echo "prefix_keys fu021 -> fu022mp (pass 2) exit $? (0) $(stamp)" >> $H
echo "hand pass 2 done $(stamp)" >> $H
exit 0
}
