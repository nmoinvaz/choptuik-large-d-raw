#!/bin/bash
# #1080 (macm3): the restart of x1's extended-precision M = 5 walk on feat/inner-mp 73dcf243 (the coordinator's order, copied in README.md):
# row 0 of walk_x1.jsonl (a0441d8b) stands as iteration 0; this run starts at row 0's next point (A + dA, wf + dwf, full float repr) with
# v0 = row 0's F3 (the centre's solved v). Same rule as comment 7111416293. Rows go to walk_x1b.jsonl (its `it` 0 is the walk's iteration 1).
#   python3 zero_mp.py A0 WF0 - walk_x1b.jsonl --M=5 --v0=<F3 of row 0> --procs=5 --iters=8     (cwd solver/inner_stokes of the worktree)
# then, only when the walk ends "located" (zero_mp exits 0): python3 value_mp.py pointv <A> <WF> --M=5 --v=<last v> --r1=0.2.
RAW=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3/m5
WT=/Users/nathan/Source/choptuik-large-d-1080mp3
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
EXPECT=73dcf243
NAME=x1b
EX=$RAW/exits_walk.txt
stamp() { date -u '+%F %T'; }
log() { echo "walk $NAME $* $(stamp) UTC" >> $EX; }
ROW0=$RAW/walk_x1.jsonl
read -r A0 WF0 <<< "$($PY -c 'import json, sys; r = json.loads(open(sys.argv[1]).readline()); assert r["it"] == 0; print(repr(r["A"] + r["dA"]), repr(r["wf"] + r["dwf"]))' $ROW0)"
V0=$($PY -c 'import json, sys; r = json.loads(open(sys.argv[1]).readline()); print(",".join(r["F3"]))' $ROW0)
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/logs
HEAD=$(git -C $WT rev-parse --short=8 HEAD)
DIRTY=$(git -C $WT status --porcelain --untracked-files=no | wc -l | tr -d ' ')
log "start, code $HEAD ($DIRTY tracked changes), $($PY -V 2>&1), load $(uptime | sed 's/.*load averages: //')"
if [ "$HEAD" != "$EXPECT" ] || [ "$DIRTY" != "0" ] || [ -z "$A0" ] || [ -z "$V0" ]
then
  log "STOP: the worktree is not at $EXPECT, has tracked changes, or the row 0 arguments are empty"
  exit 1
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
$PY -u $RAW/explore_mp/memlog_mp.py $$ >> $RAW/memlog_walk_x1b.log 2>&1 &
MEMPID=$!
$PY $RAW/walk_report.py selftest > $RAW/logs/selftest_walk_report_x1b.log 2>&1 || { log "STOP: walk_report.py selftest"; kill $MEMPID; exit 1; }
$PY zero_mp.py selftest > $RAW/logs/selftest_zero_mp_x1b.log 2>&1 || { log "STOP: zero_mp.py selftest"; kill $MEMPID; exit 1; }
$PY zero_mp.py selftest --mutate=sign > $RAW/logs/selftest_zero_mp_sign_x1b.log 2>&1
if [ $? = 0 ]
then
  log "STOP: zero_mp.py selftest --mutate=sign passed (it must fail)"
  kill $MEMPID
  exit 1
fi
log "selftests pass (zero_mp: lands; --mutate=sign fails)"
OUT=$RAW/walk_x1b.jsonl
log "command: nice -n 10 $PY -u zero_mp.py $A0 $WF0 - $OUT --M=5 --v0=$V0 --procs=5 --iters=8"
/usr/bin/time -l -o $RAW/logs/walk_x1b.time nice -n 10 $PY -u zero_mp.py $A0 $WF0 - $OUT --M=5 --v0=$V0 --procs=5 --iters=8 > $RAW/logs/walk_x1b.log 2>&1
RC=$?
log "zero_mp exit $RC ($(tail -1 $RAW/logs/walk_x1b.log | cut -c1-200))"
if grep -l Traceback $RAW/logs/walk_x1b.log >> $EX 2>/dev/null; then log "Traceback in the walk log"; fi
if [ -f $OUT ]
then
  $PY $RAW/walk_report.py table $OUT > $RAW/logs/walk_x1b_table.md 2>&1
fi
if [ $RC = 0 ]
then
  AE=$($PY $RAW/walk_report.py end $OUT | sed -n 1p)
  WE=$($PY $RAW/walk_report.py end $OUT | sed -n 2p)
  VE=$($PY $RAW/walk_report.py end $OUT | sed -n 3p)
  log "located; command: nice -n 10 $PY -u value_mp.py pointv $AE $WE --M=5 --v=$VE --r1=0.2"
  /usr/bin/time -l -o $RAW/logs/pointv_r0.2_x1b.time nice -n 10 $PY -u value_mp.py pointv $AE $WE --M=5 --v=$VE --r1=0.2 > $RAW/logs/pointv_r0.2_x1b.log 2>&1
  log "pointv r1 0.2 exit $?"
  $PY $RAW/walk_report.py shift $OUT x1 > $RAW/logs/walk_x1b_shift.txt 2>&1
else
  log "NOT located (zero_mp exit $RC): no pointv at r1 0.2"
fi
log "all steps done"
kill $MEMPID 2>/dev/null
