#!/bin/bash
# #839's queue, one job at a time: arm A (#713's flags) and arm B (+ --full_drop 1e-2), seed 1, then seed 2
D=$(cd "$(dirname "$0")" && pwd)
RAW=$(dirname "$D")
S=I603-win2/chain/anm_pin3_D252.6135.npz
DT=1.68453445011892229445312904531756908899422197089059690341775    # the truth's Delta, all eight parts
for seed in 1 2; do
  bash "$D/run.sh" "A_s$seed" octo_corrector.py planted "$RAW" $S --threads 3 --switch 0 --reseed_o 3 \
      --reseed_start pred --qd 0 --seed $seed --Delta_ref $DT --out "$D/A_s$seed"
  bash "$D/run.sh" "B_s$seed" octo_corrector.py planted "$RAW" $S --threads 3 --switch 0 --reseed_o 3 \
      --reseed_start pred --qd 0 --seed $seed --full_drop 1e-2 --Delta_ref $DT --out "$D/B_s$seed"
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC: seed $seed done" >> "$D/queue.log"
done
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC: queue done" >> "$D/queue.log"
