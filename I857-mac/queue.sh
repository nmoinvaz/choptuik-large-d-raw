#!/bin/bash
# #857: the Delta block at D 240.1244 at rel 1e-83, 1e-84, 1e-85 (seed 1, the issue's commands) and seed 3 (the
# opposite Delta sign) at 1e-85 for the noise floor, from two starts: the stored truth as written (truth/) and #874's
# re-converged state (u2/). Then the power readings and their controls, and linear.py on each. Waits for I874-mac's
# queue: one process at a time.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I857-mac
PY=/Users/nathan/venv-314/bin/python3
S240=I603-win2/chain/anm_pin3_D240.1244.npz
U2=I874-mac/anm_pin3_D240.1244_u2.npz
REF240=-4.3765436014297066e-58
cd "$(dirname "$0")" || exit 9
chk() { n=$1; shift; { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $*"; "$PY" "$@"; echo "exit $?"; } > "$O/$n.log" 2>&1; }
until [ -f $R/I874-mac/queue.done ]; do sleep 60; done
REFU2=$(jq -r '.step.dDelta_str // empty' $R/I874-mac/check_u2.json 2>/dev/null)
starts="truth:$S240:$REF240"
if [ -n "$REFU2" ]; then starts="$starts u2:$U2:$REFU2"; else echo "no check_u2.json: the u2 runs are skipped" >> queue.log; fi
for st in $starts; do
  t=${st%%:*}; rest=${st#*:}; S=${rest%%:*}; REF=${rest#*:}
  for k in 83 84 85; do
    ./run.sh ${t}_dl_D240_r$k step_spread.py $R $S --threads 3 --seeds 1 --controls 0 --repeat 0 --blocks Delta \
      --rel 1e-$k --ref $REF --json $O/$t/dl_D240_r$k.json
  done
  ./run.sh ${t}_dl_D240_r85_s3 step_spread.py $R $S --threads 3 --seeds 3 --controls 0 --repeat 0 --blocks Delta \
    --rel 1e-85 --ref $REF --json $O/$t/dl_D240_r85_s3.json
  P3="$O/$t/dl_D240_r83.json $O/$t/dl_D240_r84.json $O/$t/dl_D240_r85.json"
  ./run.sh ${t}_power step_spread.py power $P3 --json $O/$t/power.json
  ./run.sh ${t}_power_s3 step_spread.py power $P3 $O/$t/dl_D240_r85_s3.json --json $O/$t/power_s3.json
  ./run.sh ${t}_power_start step_spread.py power $P3 --mutate start
  chk ${t}_linear_samesign linear.py $O/$t --noise $O/$t/power_s3.json --mutate samesign
  chk ${t}_linear linear.py $O/$t --noise $O/$t/power_s3.json
done
chk linear_selftest linear.py --selftest
chk linear_ctl850 linear.py $R/I850-mac
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done
