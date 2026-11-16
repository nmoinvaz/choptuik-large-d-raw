#!/bin/bash
# #899: re-converge the stored truth at D 252.6135 (truth_restep.py store, two steps, held values from the truth, #884)
# and check it; then the Delta block at rel 1e-93, 1e-94 (seed 1) and 1e-95 (seeds 1 and 3) from the re-converged
# state (u2/) and the stored truth (truth/), power and its control, and oddeven.py. Waits for I900-mac's queue: one
# process at a time.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I899-mac
PY=/Users/nathan/venv-314/bin/python3
S252=I603-win2/chain/anm_pin3_D252.6135.npz
U2=I899-mac/anm_pin3_D252.6135_u2.npz
REF252=5.2645963792835124e-82
cd "$(dirname "$0")" || exit 9
chk() { n=$1; shift; { echo "== $n $(date -u '+%Y-%m-%d %H:%M:%S') UTC, $*"; "$PY" "$@"; echo "exit $?"; } > "$O/$n.log" 2>&1; }
until [ -f $R/I900-mac/queue.done ]; do sleep 60; done
./run.sh store_u2 truth_restep.py store $R $S252 $U2 --threads 3 --steps 2
./run.sh check_u2 truth_restep.py check $R $U2 --threads 3 --held_ref $S252 --json $O/check_u2.json
REFU2=$(jq -r '.step.dDelta_str // empty' $O/check_u2.json 2>/dev/null)
starts="truth:$S252:$REF252"
if [ -n "$REFU2" ]; then starts="u2:$U2:$REFU2 $starts"; else echo "no check_u2.json: the u2 runs are skipped" >> queue.log; fi
for st in $starts; do
  t=${st%%:*}; rest=${st#*:}; S=${rest%%:*}; REF=${rest#*:}
  for k in 93 94 95; do
    seeds=1
    [ $k = 95 ] && seeds=1,3
    ./run.sh ${t}_dl_D252_r$k step_spread.py $R $S --threads 3 --seeds $seeds --controls 0 --repeat 0 --blocks Delta \
      --rel 1e-$k --ref $REF --json $O/$t/dl_D252_r$k.json
  done
  P3="$O/$t/dl_D252_r93.json $O/$t/dl_D252_r94.json $O/$t/dl_D252_r95.json"
  ./run.sh ${t}_power step_spread.py power $P3 --json $O/$t/power.json
  ./run.sh ${t}_power_start step_spread.py power $P3 --mutate start
  chk ${t}_oddeven_samesign oddeven.py $O/$t --mutate samesign
  chk ${t}_oddeven oddeven.py $O/$t
done
chk oddeven_selftest oddeven.py --selftest
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done
