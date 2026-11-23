#!/bin/bash
# #1080 EXPLORATORY-then-READING (the coordinator's rule of comment 7111416293, copied in README.md): the extended-precision M = 5 walk of one excited zero.
#   python3 zero_mp.py A0 WF0 - OUT --M=5 --v0=<the four solved harmonics of the start> --procs=5 --iters=8     (cwd solver/inner_stokes of the worktree, a0441d8b)
# then, only when the walk ends "located" (zero_mp exits 0): python3 value_mp.py pointv <A> <WF> --M=5 --v=<last v> --r1=0.2.
# usage: run_walk_mp.sh NAME     (x1: A0 3.446218246366727, WF0 0.347606965217407, v0 = x1fm's solved v of explore_mp/logs/pointv_x1fm.log)
RAW=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3/m5
WT=/Users/nathan/Source/choptuik-large-d-1080mp2
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
EXPECT=a0441d8b
NAME=$1
EX=$RAW/exits_walk.txt
stamp() { date -u '+%F %T'; }
log() { echo "walk $NAME $* $(stamp) UTC" >> $EX; }
case $NAME in
  x1) A0=3.446218246366727; WF0=0.347606965217407; V0=$($PY -c 'import json, sys; r = json.loads([l for l in open(sys.argv[1]) if l.startswith("{")][-1]); print(",".join(r["v"]))' $RAW/explore_mp/logs/pointv_x1fm.log) ;;
  *) echo "walk $NAME $(stamp) UTC STOP: unknown name $NAME" >> $EX; exit 1 ;;
esac
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/logs
HEAD=$(git -C $WT rev-parse --short=8 HEAD)
DIRTY=$(git -C $WT status --porcelain --untracked-files=no | wc -l | tr -d ' ')
log "start, code $HEAD ($DIRTY tracked changes), $($PY -V 2>&1), load $(uptime | sed 's/.*load averages: //')"
if [ "$HEAD" != "$EXPECT" ] || [ "$DIRTY" != "0" ]
then
  log "STOP: the worktree is not at $EXPECT or has tracked changes"
  exit 1
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
$PY -u $RAW/explore_mp/memlog_mp.py $$ >> $RAW/memlog_walk.log 2>&1 &
MEMPID=$!
$PY $RAW/walk_report.py selftest > $RAW/logs/selftest_walk_report.log 2>&1 || { log "STOP: walk_report.py selftest"; kill $MEMPID; exit 1; }
$PY zero_mp.py selftest > $RAW/logs/selftest_zero_mp.log 2>&1 || { log "STOP: zero_mp.py selftest"; kill $MEMPID; exit 1; }
$PY zero_mp.py selftest --mutate=sign > $RAW/logs/selftest_zero_mp_sign.log 2>&1
if [ $? = 0 ]
then
  log "STOP: zero_mp.py selftest --mutate=sign passed (it must fail)"
  kill $MEMPID
  exit 1
fi
log "selftests pass (zero_mp: lands; --mutate=sign fails)"
OUT=$RAW/walk_$NAME.jsonl
log "command: nice -n 10 $PY -u zero_mp.py $A0 $WF0 - $OUT --M=5 --v0=$V0 --procs=5 --iters=8"
/usr/bin/time -l -o $RAW/logs/walk_$NAME.time nice -n 10 $PY -u zero_mp.py $A0 $WF0 - $OUT --M=5 --v0=$V0 --procs=5 --iters=8 > $RAW/logs/walk_$NAME.log 2>&1
RC=$?
log "zero_mp exit $RC ($(tail -1 $RAW/logs/walk_$NAME.log | cut -c1-200))"
if grep -l Traceback $RAW/logs/walk_$NAME.log >> $EX 2>/dev/null; then log "Traceback in the walk log"; fi
if [ -f $OUT ]
then
  $PY $RAW/walk_report.py table $OUT > $RAW/logs/walk_${NAME}_table.md 2>&1
fi
if [ $RC = 0 ]
then
  AE=$($PY $RAW/walk_report.py end $OUT | sed -n 1p)
  WE=$($PY $RAW/walk_report.py end $OUT | sed -n 2p)
  VE=$($PY $RAW/walk_report.py end $OUT | sed -n 3p)
  log "located; command: nice -n 10 $PY -u value_mp.py pointv $AE $WE --M=5 --v=$VE --r1=0.2"
  /usr/bin/time -l -o $RAW/logs/pointv_r0.2_$NAME.time nice -n 10 $PY -u value_mp.py pointv $AE $WE --M=5 --v=$VE --r1=0.2 > $RAW/logs/pointv_r0.2_$NAME.log 2>&1
  log "pointv r1 0.2 exit $?"
  $PY $RAW/walk_report.py shift $OUT $NAME > $RAW/logs/walk_${NAME}_shift.txt 2>&1
else
  log "NOT located (zero_mp exit $RC): no pointv at r1 0.2"
fi
log "all steps done"
kill $MEMPID 2>/dev/null
