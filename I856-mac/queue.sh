#!/bin/bash
# #856: the Delta block at D 252.6135 at rel 1e-68 and 1e-69 (seed 1, the same signs as #850), the power reading over
# 1e-67 (#850's run) .. 1e-69 and its controls, then qcheck.py. Waits for I852-mac's queue: one process at a time.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I856-mac
PY=/Users/nathan/venv-314/bin/python3
S252=I603-win2/chain/anm_pin3_D252.6135.npz
REF252=5.2645963792835124e-82
cd "$(dirname "$0")" || exit 9
chk() { n=$1; shift; { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $*"; "$PY" "$@"; echo "exit $?"; } > "$O/$n.log" 2>&1; }
until [ -f $R/I852-mac/queue.done ]; do sleep 60; done
C="--threads 3 --seeds 1 --controls 0 --repeat 0"
for k in 68 69; do
  ./run.sh dl_D252_r$k step_spread.py $R $S252 $C --blocks Delta --rel 1e-$k --ref $REF252 --json $O/dl_D252_r$k.json
done
P3="$R/I850-mac/dl_D252_r67.json $O/dl_D252_r68.json $O/dl_D252_r69.json"
./run.sh power step_spread.py power $P3 --json $O/power.json
./run.sh power_start step_spread.py power $P3 --mutate start
chk qcheck_selftest qcheck.py --selftest
chk qcheck_ctl850 qcheck.py $R/I850-mac/power.json
chk qcheck qcheck.py $O/power.json
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done
