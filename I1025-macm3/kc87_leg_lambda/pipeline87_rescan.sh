#!/bin/bash
# #1025 macm3 kc87_leg_lambda: a rescan of one state on another lambda grid (t5, hc 25 Nov: D 22.125 on 0.487 to 0.497 by 0.0025 plus the repeat). The folder's point.env and README section are written by hand before this runs;
# this is pipeline87.sh from the lock on, without newpoint87.py: the scan lock, prepare87.sh (pins by blob), push (README first), point87.sh accept, scan, push.   usage: bash pipeline87_rescan.sh FOLDER   (e.g. 22.125_rescan)
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
DN=$1; mkdir -p $L/$DN; LOG=$L/$DN/pipeline.log
say() { echo "$(date -u '+%F %T') UTC $*" >> $LOG; }
LOCK=$L/.scan.lock
n=0
until mkdir $LOCK 2>/dev/null; do
  p=$(cat $LOCK.pid 2>/dev/null)
  if [ -n "$p" ] && ! kill -0 $p 2>/dev/null; then mv $LOCK $LOCK.stale.$(date +%s); mv $LOCK.pid $LOCK.pid.stale.$(date +%s); say "a stale scan lock of pid $p moved aside"; continue; fi
  n=$((n+1)); [ $n -gt 2700 ] && { say "STOP: the scan lock stayed busy for 15 h"; exit 1; }
  sleep 20
done
echo $$ > $LOCK.pid
trap 'rmdir $LOCK 2>/dev/null; mv $LOCK.pid $LOCK.pid.done 2>/dev/null' EXIT
say "rescan pipeline start: $DN ($(grep '^LAMP' $L/$DN/point.env))"
bash $L/prepare87.sh $DN >> $LOG 2>&1 || { say "STOP: prepare87 failed (a pin mismatch)"; exit 1; }
bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN README first (grid, pins, order)" >> $LOG 2>&1; say "README pushed ($?)"
bash $L/point87.sh $DN accept >> $LOG 2>&1
say "accept: $(cat $L/$DN/VERDICT.txt)"
grep -q '^ACCEPTED' $L/$DN/VERDICT.txt || { bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN REFUSED by the source check" >> $LOG 2>&1; say "STOP: refused"; exit 1; }
bash $L/point87.sh $DN scan >> $LOG 2>&1; say "scan exit $?"
bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN scan done" >> $LOG 2>&1; say "results pushed ($?)"
