#!/bin/bash
# #1025 macm3 kc87_leg_lambda (t5's standing order, hc 24 Nov: take every k_c 87 leg state from D 21.125 on, 4 processes): one point from the raw commit to the pushed result.
# usage: bash pipeline87.sh D PREV_D PREV_ROOT   (run detached under caffeinate -is nice -n 10 by launch_1070.py)
# steps: newpoint87.py selftest (0) and the setup (point.env, README section with the prediction, written before any run); prepare87.sh (pins by blob); push (README first); point87.sh accept;
# if ACCEPTED point87.sh scan; push. Log: <D>/pipeline.log. No hc from here.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
D=$1; PD=$2; PR=$3
DN=$(python3 -c "print(repr(float('$D')))")
mkdir -p $L/$DN
LOG=$L/$DN/pipeline.log
say() { echo "$(date -u '+%F %T') UTC $*" >> $LOG; }
say "pipeline start: D $DN, previous root $PR at D $PD"
python3 $L/newpoint87.py selftest > $L/$DN/selftest_newpoint87.txt 2>&1 || { say "STOP: newpoint87 selftest failed"; exit 1; }
python3 $L/newpoint87.py selftest --mutate=round > $L/$DN/selftest_newpoint87_mutate_round.txt 2>&1 && { say "STOP: newpoint87 selftest --mutate=round passed (it must fail)"; exit 1; }
python3 $L/newpoint87.py selftest --mutate=g > $L/$DN/selftest_newpoint87_mutate_g.txt 2>&1 && { say "STOP: newpoint87 selftest --mutate=g passed (it must fail)"; exit 1; }
python3 $L/newpoint87.py $D $PD $PR >> $LOG 2>&1 || { say "STOP: newpoint87 failed"; exit 1; }
bash $L/prepare87.sh $DN >> $LOG 2>&1 || { say "STOP: prepare87 failed (a pin mismatch)"; exit 1; }
bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN README first (rule prediction, grid, pins)" >> $LOG 2>&1; say "README pushed ($?)"
bash $L/point87.sh $DN accept >> $LOG 2>&1
say "accept: $(cat $L/$DN/VERDICT.txt)"
grep -q '^ACCEPTED' $L/$DN/VERDICT.txt || { bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN REFUSED by the source check" >> $LOG 2>&1; say "STOP: refused"; exit 1; }
bash $L/point87.sh $DN scan >> $LOG 2>&1; say "scan exit $?"
bash $L/push87.sh "I1025-macm3/kc87_leg_lambda: D $DN scan done" >> $LOG 2>&1; say "results pushed ($?)"
