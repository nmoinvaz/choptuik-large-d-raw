#!/bin/bash
# #837's second queue: step_spread's and proj_shift's truth_system against planted's step at 252.6135
D=$(cd "$(dirname "$0")" && pwd)
RAW=$(dirname "$D")
bash "$D/run.sh" ss_D252 step_spread.py "$RAW" I603-win2/chain/anm_pin3_D252.6135.npz --threads 3 --seeds "" \
    --controls 0 --repeat 1 --ref 5.2645963792835124e-82 --json "$D/ss_D252.json"
bash "$D/run.sh" ps_D252 proj_shift.py "$RAW" I603-win2/chain/anm_pin3_D252.6135.npz --threads 3 --switch 0 \
    --reseed_o 3 --reseed_start pred --ref_plain 5.2645963792835124e-82 --json "$D/ps_D252.json"
echo "$(date -u '+%Y-%m-%d %H:%M:%S') UTC: queue2 done" >> "$D/queue.log"
