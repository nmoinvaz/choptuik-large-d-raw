#!/bin/bash
# #1025 macm3 kc87_leg_lambda (t5's standing order, hc 24 Nov: take every k_c 87 leg state from D 21.125 on, 4 processes): one point from the raw commit to the pushed result.
# usage: bash pipeline87.sh D PREV_D PREV_ROOT [SLOPE, default -0.28]   (run detached under caffeinate -is nice -n 10 by launch_1070.py)
# steps: newpoint87.py selftest (0) and the setup (point.env, README section with the prediction, written before any run); prepare87.sh (pins by blob); push (README first); point87.sh accept;
# if ACCEPTED point87.sh scan; push. Log: <D>/pipeline.log. No hc from here.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
D=$1; PD=$2; PR=$3; SL=${4:--0.28}      # SL: the slope of t5's rule per unit D (-0.28 from the first order; -0.32 from D 21.21875)
DN=$(python3 -c "print(repr(float('$D')))")${DNSUFFIX}      # DNSUFFIX: the folder suffix of a control scan of the same D (21.375_ctl)
mkdir -p $L/$DN
LOG=$L/$DN/pipeline.log
say() { echo "$(date -u '+%F %T') UTC $*" >> $LOG; }
# one scan at a time (the chain's and the control's): a mkdir lock; its owner's pid is in a file beside it (so that rmdir can release it); a stale lock (owner gone) is moved aside, not deleted
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
say "pipeline start: D $DN, previous root $PR at D $PD, slope $SL${SL2:+, scored beside: slope $SL2}"
python3 $L/newpoint87.py selftest > $L/$DN/selftest_newpoint87.txt 2>&1 || { say "STOP: newpoint87 selftest failed"; exit 1; }
python3 $L/newpoint87.py selftest --mutate=round > $L/$DN/selftest_newpoint87_mutate_round.txt 2>&1 && { say "STOP: newpoint87 selftest --mutate=round passed (it must fail)"; exit 1; }
python3 $L/newpoint87.py selftest --mutate=g > $L/$DN/selftest_newpoint87_mutate_g.txt 2>&1 && { say "STOP: newpoint87 selftest --mutate=g passed (it must fail)"; exit 1; }
python3 $L/newpoint87.py selftest --mutate=slope > $L/$DN/selftest_newpoint87_mutate_slope.txt 2>&1 && { say "STOP: newpoint87 selftest --mutate=slope passed (it must fail)"; exit 1; }
SL3=${SL3:-$(python3 $L/chain_next.py slope3 $D 2>/dev/null)}      # the below-only slope, only when the primary SL is the interpolation between bracketing roots (t5, phase 2)
python3 $L/newpoint87.py $D $PD $PR --slope=$SL ${SL2:+--slope2=$SL2} ${SL3:+--slope3=$SL3} >> $LOG 2>&1 || { say "STOP: newpoint87 failed"; exit 1; }
bash $L/prepare87.sh $DN >> $LOG 2>&1 || { say "STOP: prepare87 failed (a pin mismatch)"; exit 1; }
bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN README first (rule prediction, grid, pins)" >> $LOG 2>&1; say "README pushed ($?)"
bash $L/point87.sh $DN accept >> $LOG 2>&1
say "accept: $(cat $L/$DN/VERDICT.txt)"
grep -q '^ACCEPTED' $L/$DN/VERDICT.txt || { bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN REFUSED by the source check" >> $LOG 2>&1; say "STOP: refused"; exit 1; }
bash $L/point87.sh $DN scan >> $LOG 2>&1; say "scan exit $?"
bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN scan done" >> $LOG 2>&1; say "results pushed ($?)"
