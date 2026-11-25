#!/bin/bash
# #1025 macm3 kc87_leg_lambda (t5's order, hc 25 Nov ~12:10 UTC, after part c2's guard stop at D 23.0): one scan of a late leg point from the raw commit to the pushed result; pipeline87.sh with newpoint_post23.py in place of newpoint87.py.
# usage: bash pipeline87_post23.sh D [newpoint_post23.py options: --window=LO:HI:STEP --rep=X | --auto]   (run detached by launch_1070.py under caffeinate -is nice -n 15, by post23_scans.sh)
# steps: the scan lock; newpoint_post23.py selftest (0) and its mutations (1 each); newpoint_post23.py (point.env and the README section with the predictions, written before any run); prepare87.sh (pins by blob); push (README first);
# point87.sh accept; if ACCEPTED point87.sh scan; push. Log: <D>/pipeline.log. No hc from here (the chain's record loop reports the root).
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
D=$1; shift
DN=$(python3 -c "print(repr(float('$D')))")
mkdir -p $L/$DN
LOG=$L/$DN/pipeline.log
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
say "pipeline start: D $DN ($*)"
python3 $L/newpoint_post23.py selftest > $L/$DN/selftest_newpoint_post23.txt 2>&1 || { say "STOP: newpoint_post23 selftest failed"; exit 1; }
for m in rule round; do
  python3 $L/newpoint_post23.py selftest --mutate=$m > $L/$DN/selftest_newpoint_post23_mutate_$m.txt 2>&1 && { say "STOP: newpoint_post23 selftest --mutate=$m passed (it must fail)"; exit 1; }
done
git -C $HOME/Source/choptuik-large-d-raw-1076p fetch -q
python3 $L/newpoint_post23.py $D "$@" >> $LOG 2>&1 || { say "STOP: newpoint_post23 failed"; exit 1; }
bash $L/prepare87.sh $DN >> $LOG 2>&1 || { say "STOP: prepare87 failed (a pin mismatch)"; exit 1; }
bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN README first (predictions, grid, pins)" >> $LOG 2>&1; say "README pushed ($?)"
bash $L/point87.sh $DN accept >> $LOG 2>&1
say "accept: $(cat $L/$DN/VERDICT.txt)"
grep -q '^ACCEPTED' $L/$DN/VERDICT.txt || { bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN REFUSED by the source check" >> $LOG 2>&1; say "STOP: refused"; exit 1; }
bash $L/point87.sh $DN scan >> $LOG 2>&1; say "scan exit $?"
bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN scan done" >> $LOG 2>&1; say "results pushed ($?)"
