#!/bin/bash
# #840 diagnostic (posted before it ran): the power of D 240.1244's horizon response in the perturbation's size. Seed 1's
# signs at rel 1e-66 and 1e-67, the same signs as ss_D240's seed 1 at 1e-65, so the move scales by exactly 0.1 per run.
# Waits for queue.sh's end, so that one process runs at a time.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
cd "$(dirname "$0")" || exit 9
until [ -f queue.done ]; do sleep 60; done
for k in 66 67; do
  ./run.sh pw_D240_r$k step_spread.py $R I603-win2/chain/anm_pin3_D240.1244.npz --threads 3 --repeat 0 --controls 0 \
    --seeds 1 --rel 1e-$k --ref -4.3765436014297066e-58 --json $R/I840-mac/pw_D240_r$k.json
done
echo "queue2 done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue2.done
