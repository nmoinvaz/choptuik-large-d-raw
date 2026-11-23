#!/bin/bash
# #1076 macm3b: pass 3 by hand (the coordinator's order, hc 2026-11-23 about 07:00 UTC), the four steps of pass 2 with these changes:
# 0 code at 6b5a7f79 (value_mp.py chord steps; checked below), 1 select with both earlier rows files and the pass 2 leaves (stop if the select line is not "N points without value ...; M to run" with 12 <= M <= 17),
# 2 value (value_mp.py batch, 6 processes, rows_pass3.jsonl), 3 recount (only if the value step exits 0 and valued at least 1 point; the pass-1 command with --tag=M3_fu022mp_pass3_r0.17
# under capped_run.py 57600), 4 prefix_keys fu021 -> fu022mp. Everything is recorded in logs/hand_steps.txt. Own session under caffeinate -is (launch_1070.py).
{
R=/Users/nathan/Source/choptuik-large-d-raw-749p
OUT=$R/I1021-macm3/fu022mp
CODE=/Users/nathan/Source/choptuik-inner-mp
CODE3=6b5a7f79245128e53c7e8a93602d6aac2a80cff5
IS=$CODE/solver/inner_stokes
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
CAP=/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_d195/capped_run.py
S21=$R/I1021-mac/rpi5_fu021; F21=$R/I1021-rpi5/fu021/m3
CELLS=$S21/in/cells_unresolved11.jsonl; SEED=$OUT/m3/points_M3_r0.2.jsonl
C=$OUT/m3/points_M3_r0.17.jsonl; L2=$OUT/m3/leaves_M3_fu022mp_pass2_r0.17.jsonl; R1=$OUT/rows_pass1.jsonl; R2=$OUT/rows_pass2.jsonl
H=$OUT/logs/hand_steps.txt
stamp() { date -u '+%F %T'; }
[ "$(git -C $CODE rev-parse HEAD)" = "$CODE3" ] && [ -z "$(git -C $CODE status --porcelain -- solver)" ] || { echo "$(stamp) STOP: the code worktree is not at $CODE3 or has local changes in solver" >> $H; exit 1; }
echo "" >> $H
echo "hand pass 3 (the coordinator's order after pass 2): code check, select, value, recount, prefix_keys; start $(stamp)" >> $H
echo "step 0 (run by hand before this script): git -C $CODE fetch origin feat/inner-mp && git -C $CODE checkout --detach 6b5a7f79; HEAD $(git -C $CODE rev-parse HEAD); git status --porcelain -- solver: [$(git -C $CODE status --porcelain -- solver)] (empty); git diff --stat cc3c58e0..HEAD: $(git -C $CODE diff --stat cc3c58e0ce4de673e77e36f6ed420a00a28cc657 HEAD | tail -2 | tr '\n' ' ')" >> $H
# 1 select
echo "select command: cd $S21 && PTS=\$($PY select_points.py $CODE $C $L2 $R1 $R2 2> $OUT/logs/select_pass3.log)" >> $H
PTS=$(cd $S21 && $PY select_points.py $CODE $C $L2 $R1 $R2 2> $OUT/logs/select_pass3.log); sel=$?
echo "pass 3 select exit $sel $(stamp): $(cat $OUT/logs/select_pass3.log)" >> $H
[ $sel = 0 ] || { echo "$(stamp) STOP: select exit $sel" >> $H; exit 1; }
N=$(sed -n 's/.*; \([0-9][0-9]*\) to run$/\1/p' $OUT/logs/select_pass3.log)
if [ -z "$N" ] || [ "$N" -lt 12 ] || [ "$N" -gt 17 ]; then echo "$(stamp) STOP: the select line has $N points to run, outside the expected 12 to 17" >> $H; exit 1; fi
[ -n "$PTS" ] || { echo "$(stamp) STOP: select printed no points" >> $H; exit 1; }
echo "pass 3 points: $PTS" >> $H
# 2 value
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "pass 3 value command: cd $IS && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 $PY -u value_mp.py batch $C $OUT/rows_pass3.jsonl --points=\"\$PTS\" --procs=6 > $OUT/logs/value_pass3.log 2>&1" >> $H
echo "pass 3 value start $(stamp) cache $(wc -l < $C) lines" >> $H
(cd $IS && nice -n 10 $PY -u value_mp.py batch $C $OUT/rows_pass3.jsonl --points="$PTS" --procs=6 > $OUT/logs/value_pass3.log 2>&1); v=$?
echo "pass 3 value exit $v $(stamp): $(tail -1 $OUT/logs/value_pass3.log)" >> $H
rec=0
if [ $v != 0 ]; then echo "pass 3 value step failed: no recount" >> $H
elif grep -q '^valued 0 of' $OUT/logs/value_pass3.log; then echo "pass 3 valued no point: no recount" >> $H
else rec=1; fi
# 3 recount
if [ $rec = 1 ]; then
  TAG=M3_fu022mp_pass3_r0.17; B="--m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry"
  echo "pass 3 recount command: cd $IS && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 $PY $CAP 57600 $PY -u argcount.py --M=3 --recount=$CELLS --r1=0.17 --r1b=0.2 --seed=$SEED $B --out=$OUT/m3 --tag=$TAG > $OUT/logs/recount_pass3_hand.log 2>&1" >> $H
  echo "pass 3 recount start $(stamp) cache $(wc -l < $C) lines" >> $H
  (cd $IS && nice -n 10 $PY $CAP 57600 $PY -u argcount.py --M=3 --recount=$CELLS --r1=0.17 --r1b=0.2 --seed=$SEED $B --out=$OUT/m3 --tag=$TAG > $OUT/logs/recount_pass3_hand.log 2>&1); s=$?
  echo "pass 3 recount exit $s $(stamp) (0 wanted; 124 is the cap)" >> $H
  K=$OUT/m3/count_${TAG}.json
  if [ $s = 0 ] && [ -f $K ]; then echo "pass 3 unresolved leaves (len of the unresolved list in $K): $($PY -c 'import json, sys; print(len(json.load(open(sys.argv[1]))["unresolved"]))' "$K" 2>&1)" >> $H
  else echo "pass 3 recount: no count (exit $s)" >> $H; fi
fi
# 4 prefix_keys, as the driver's last step
$PY $S21/prefix_keys.py $F21/points_M3_r0.17.jsonl $C > $OUT/logs/prefix_keys_pass3.log 2>&1
echo "prefix_keys fu021 -> fu022mp (pass 3) exit $? (0) $(stamp)" >> $H
echo "hand pass 3 done $(stamp)" >> $H
exit 0
}
