#!/bin/bash
# #1080 EXPLORATORY (the coordinator's order): the M = 5 inner solve in extended precision at the two excited zeros, one value each, no walk.
#   python3 value_mp.py pointv A WF --M=5 --v=B3,C3,B5,C5      (cwd solver/inner_stokes of the worktree, feat/inner-mp 176daf53; defaults r1 0.17, dps 34/42)
# Three runs side by side, one process each, nice 10, under caffeinate -is (../launch.py): x1 and x2 from (B3, C3, 0, 0) of their box centres, and x1 from the four
# harmonics of the floor_max start at xi1 0.2. The arguments come from mp_args.py. Exits go to exits_mp.txt.
RAW=/Users/nathan/Source/choptuik-large-d-raw-903/I1079-macm3/m5/explore_mp
WT=/Users/nathan/Source/choptuik-large-d-1080mp
PY=/Users/nathan/Source/venv-macm3-1058b/bin/python
EXPECT=176daf53
EX=$RAW/exits_mp.txt
stamp() { date -u '+%F %T'; }
log() { echo "mp $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/logs
HEAD=$(git -C $WT rev-parse --short=8 HEAD)
DIRTY=$(git -C $WT status --porcelain --untracked-files=no | wc -l | tr -d ' ')
log "start, code $HEAD ($DIRTY tracked changes), $($PY -V 2>&1), mpmath $($PY -c 'import mpmath, mpmath.libmp as l; print(mpmath.__version__, l.BACKEND)'), load $(uptime | sed 's/.*load averages: //')"
if [ "$HEAD" != "$EXPECT" ] || [ "$DIRTY" != "0" ]
then
  log "STOP: the worktree is not at $EXPECT or has tracked changes"
  exit 1
fi
$PY $RAW/report_mp.py selftest > $RAW/logs/selftest_mp.log 2>&1 || { log "STOP: report_mp.py selftest"; exit 1; }
$PY -u $RAW/memlog_mp.py $$ >> $RAW/memlog_mp.log 2>&1 &
MEMPID=$!

job() {
  local name=$1
  local A=$($PY $RAW/mp_args.py $name | sed -n 1p)
  local WF=$($PY $RAW/mp_args.py $name | sed -n 2p)
  local V=$($PY $RAW/mp_args.py $name | sed -n 3p)
  local out=$RAW/logs/pointv_$name.log
  echo "# cd $WT/solver/inner_stokes && nice -n 10 $PY -u value_mp.py pointv $A $WF --M=5 --v=$V" > $out
  log "command $name: nice -n 10 $PY -u value_mp.py pointv $A $WF --M=5 --v=$V"
  /usr/bin/time -l -o $RAW/logs/pointv_$name.time nice -n 10 $PY -u value_mp.py pointv $A $WF --M=5 --v=$V >> $out 2>&1
}

job x1 &
p1=$!
job x2 &
p2=$!
job x1fm &
p3=$!
wait $p1; log "x1 exit $?"
wait $p2; log "x2 exit $?"
wait $p3; log "x1fm exit $?"
if grep -l Traceback $RAW/logs/pointv_*.log >> $EX 2>/dev/null; then log "Traceback in a log (files listed above)"; fi
$PY $RAW/report_mp.py report > $RAW/logs/report.txt 2>&1
log "report exit $?"
log "all steps done"
kill $MEMPID 2>/dev/null
