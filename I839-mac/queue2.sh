#!/bin/bash
# #839's queue from 2026-11-15 16:07 UTC (the coordinator's reply; queue.sh was stopped after its A_s1 began): A_s1
# runs out its 12 steps, then A_s2. A B arm (+ --full_drop 1e-2) runs only when its A run had a lam-1 trial within
# 1e-2 of |F| (b_needed.py), since otherwise B repeats A bit for bit. One job at a time.
D=$(cd "$(dirname "$0")" && pwd)
RAW=$(dirname "$D")
S=I603-win2/chain/anm_pin3_D252.6135.npz
DT=1.68453445011892229445312904531756908899422197089059690341775    # the truth's Delta, all eight parts
PY=/Users/nathan/venv-314/bin/python3
stamp() { echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC: $*" >> "$D/queue.log"; }
stamp "queue2 started, waiting for A_s1"
until grep -q "^exit " "$D/A_s1.log"; do sleep 60; done
stamp "A_s1 done"
bash "$D/run.sh" A_s2 octo_corrector.py planted "$RAW" $S --threads 3 --switch 0 --reseed_o 3 \
    --reseed_start pred --qd 0 --seed 2 --Delta_ref $DT --out "$D/A_s2"
stamp "A_s2 done"
for seed in 1 2; do
  if "$PY" "$D/b_needed.py" "$D/A_s$seed.log" >> "$D/queue.log"; then
    bash "$D/run.sh" "B_s$seed" octo_corrector.py planted "$RAW" $S --threads 3 --switch 0 --reseed_o 3 \
        --reseed_start pred --qd 0 --seed $seed --full_drop 1e-2 --Delta_ref $DT --out "$D/B_s$seed"
    stamp "B_s$seed done"
  else
    stamp "B_s$seed not run"
  fi
done
stamp "queue done"
