#!/bin/bash
# #830's queue, one job at a time: the repeat check's control, then step_spread at #603's three states, then sum.
D=$(cd "$(dirname "$0")" && pwd)
RAW=$(dirname "$D")
bash "$D/run.sh" repeat_control step_spread.py "$RAW" I603-win2/chain/anm_pin3_D240.1244.npz --threads 3 --seeds "" \
    --controls 0 --repeat 1 --mutate repeat --json "$D/repeat_control.json"
for x in 240.1244 245.6366 250.1676; do
  bash "$D/run.sh" "spread_D$x" step_spread.py "$RAW" "I603-win2/chain/anm_pin3_D$x.npz" --threads 3 --rel 1e-65 \
      --seeds 1,2,3,4 --repeat 1 --json "$D/spread_D$x.json"
done
bash "$D/run.sh" sum step_spread.py sum "$D/table805.json" "$RAW/I827-mac/spread.json" "$D/spread_D240.1244.json" \
    "$D/spread_D245.6366.json" "$D/spread_D250.1676.json" --json "$D/sum.json"
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC: queue done" >> "$D/queue.log"
