#!/bin/bash
# #875: #852's m_h, a_h move at rel 1e-90, 1e-93, 1e-96 (seed 1), two steps, from #874's re-converged state, then
# gain.py with its selftest and its control (#852's run from the stored truth must FAIL). Waits for I857-mac's queue:
# one process at a time.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I875-mac
PY=/Users/nathan/venv-314/bin/python3
U2=I874-mac/anm_pin3_D240.1244_u2.npz
cd "$(dirname "$0")" || exit 9
chk() { n=$1; shift; { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $*"; "$PY" "$@"; echo "exit $?"; } > "$O/$n.log" 2>&1; }
until [ -f $R/I857-mac/queue.done ]; do sleep 60; done
REFU2=$(jq -r '.step.dDelta_str // empty' $R/I874-mac/check_u2.json 2>/dev/null)
if [ -n "$REFU2" ]; then
  ./run.sh steps_u2 step_spread.py $R $U2 --threads 3 --seeds 1 --controls 0 --repeat 0 --ref $REFU2 \
    --rel 1e-90,1e-93,1e-96 --steps 2 --json $O/steps_u2.json
  chk gain gain.py $O/steps_u2.json
else
  echo "no check_u2.json: steps_u2 skipped" >> queue.log
fi
chk gain_selftest gain.py --selftest
chk gain_ctl852 gain.py $R/I852-mac/steps_D240.json
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done
