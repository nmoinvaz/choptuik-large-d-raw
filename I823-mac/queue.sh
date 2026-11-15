#!/bin/bash
# #823's queue, one job at a time: the plant and its w0 control, the stored system's dz0 control, then the real
# curve only if the plant passed, w0 failed and dz0 failed at its own check. Each job writes I823-mac/NAME.log.
D=$(cd "$(dirname "$0")" && pwd)
RAW=$(dirname "$D")
BASE=I603-win2/chain/anm_pin3_D252.6135.npz
bash "$D/run.sh" curve_planted reduced_cubic.py curve planted --json="$D/curve_planted.json"
bash "$D/run.sh" curve_planted_w0 reduced_cubic.py curve planted --mutate=w0 --json="$D/curve_planted_w0.json"
bash "$D/run.sh" curve_dz0mut reduced_cubic.py curve "$RAW" I823-mac/dz0_truth.npz $BASE --threads=3 --mutate=dz0 \
    --json="$D/curve_dz0mut.json"
p=$(grep -c "^exit 0" "$D/curve_planted.log"); w=$(grep -c "^exit 1" "$D/curve_planted_w0.log")
m=$(grep -c "the stored first step is not the stored system's Newton step" "$D/curve_dz0mut.log")
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC: plant exit 0 $p, w0 exit 1 $w, dz0 control's FAIL line $m" >> "$D/queue.log"
if [ "$p" = 1 ] && [ "$w" = 1 ] && [ "$m" = 1 ]; then
  echo "the gate holds: the real curve starts" >> "$D/queue.log"
  bash "$D/run.sh" curve_truth reduced_cubic.py curve "$RAW" I823-mac/dz0_truth.npz $BASE --threads=3 --curve_t=a \
      --json="$D/curve_truth.json"
else
  echo "the gate does not hold: the real curve is not run" >> "$D/queue.log"
fi
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC: queue done" >> "$D/queue.log"
