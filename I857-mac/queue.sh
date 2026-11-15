#!/bin/bash
# #857: the Delta block at D 240.1244 at rel 1e-83, 1e-84, 1e-85 (seed 1, the issue's commands), then seed 3 (the
# opposite Delta sign) at 1e-85 for the noise floor, the power readings and their controls, then linear.py. Waits for
# I856-mac's queue: one process at a time.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I857-mac
PY=/Users/nathan/venv-314/bin/python3
S240=I603-win2/chain/anm_pin3_D240.1244.npz
REF240=-4.3765436014297066e-58
cd "$(dirname "$0")" || exit 9
chk() { n=$1; shift; { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $*"; "$PY" "$@"; echo "exit $?"; } > "$O/$n.log" 2>&1; }
until [ -f $R/I856-mac/queue.done ]; do sleep 60; done
C="--threads 3 --seeds 1 --controls 0 --repeat 0"
for k in 83 84 85; do
  ./run.sh dl_D240_r$k step_spread.py $R $S240 $C --blocks Delta --rel 1e-$k --ref $REF240 --json $O/dl_D240_r$k.json
done
C3="--threads 3 --seeds 3 --controls 0 --repeat 0"
./run.sh dl_D240_r85_s3 step_spread.py $R $S240 $C3 --blocks Delta --rel 1e-85 --ref $REF240 --json $O/dl_D240_r85_s3.json
P3="$O/dl_D240_r83.json $O/dl_D240_r84.json $O/dl_D240_r85.json"
./run.sh power step_spread.py power $P3 --json $O/power.json
./run.sh power_s3 step_spread.py power $P3 $O/dl_D240_r85_s3.json --json $O/power_s3.json
./run.sh power_start step_spread.py power $P3 --mutate start
chk linear_selftest linear.py --selftest
chk linear_ctl850 linear.py $R/I850-mac
chk linear_samesign linear.py $O --noise $O/power_s3.json --mutate samesign
chk linear linear.py $O --noise $O/power_s3.json
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done
