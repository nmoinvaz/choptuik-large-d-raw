#!/bin/bash
# #900: from z_s = u2 + s (truth - u2) (blend_s<s>.log, made before the queue), seeds 1 and 3 at rel 1e-85 on the Delta
# block, s = 1 (planted: the truth, with --ref) first, then 1/2 and 1/4; power per s, then cross.py, its selftest and
# its control. Waits for I884-mac's queue: one process at a time.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I900-mac
PY=/Users/nathan/venv-314/bin/python3
REF240=-4.3765436014297066e-58
cd "$(dirname "$0")" || exit 9
chk() { n=$1; shift; { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $*"; "$PY" "$@"; echo "exit $?"; } > "$O/$n.log" 2>&1; }
until [ -f $R/I884-mac/queue.done ]; do sleep 60; done
for s in 1 0.5 0.25; do
  ref=""
  [ $s = 1 ] && ref="--ref $REF240"
  ./run.sh dl_D240_s$s step_spread.py $R I900-mac/anm_pin3_D240.1244_s$s.npz --threads 3 --seeds 1,3 --controls 0 \
    --repeat 0 --blocks Delta --rel 1e-85 $ref --json $O/dl_D240_s$s.json
  ./run.sh power_s$s step_spread.py power $O/dl_D240_s$s.json --json $O/p_s$s.json
done
chk cross_selftest cross.py --selftest
chk cross_swap cross.py $O $R/I857-mac --mutate swap
chk cross cross.py $O $R/I857-mac
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done
