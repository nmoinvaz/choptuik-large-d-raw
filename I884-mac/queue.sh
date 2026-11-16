#!/bin/bash
# #884: truth_system reads #874's re-stepped state in its source's system. check with held_src auto must match #852's
# step 3 as doubles; held_src state (the old behaviour) must not. Then the four #837 truths' residuals against #840's
# records, and their control (held float) must fail. Waits for I875-mac's queue: one process at a time.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I884-mac
S240=I603-win2/chain/anm_pin3_D240.1244.npz
U2=I874-mac/anm_pin3_D240.1244_u2.npz
J852=$R/I852-mac/steps_D240.json
SS="$R/I840-mac/ss_D240.json $R/I840-mac/ss_D245.json $R/I840-mac/ss_D250.json $R/I840-mac/ss_D252.json"
cd "$(dirname "$0")" || exit 9
until [ -f $R/I875-mac/queue.done ]; do sleep 60; done
./run.sh check_u2_src truth_restep.py check $R $U2 --threads 3 --held_ref $S240 --match $J852 --match_k 3 \
  --json $O/check_u2_src.json
./run.sh check_u2_state truth_restep.py check $R $U2 --threads 3 --held_src state --held_ref $S240 --match $J852 \
  --match_k 3 --json $O/check_u2_state.json
./run.sh residuals truth_restep.py residuals $R $SS --threads 3
./run.sh residuals_float truth_restep.py residuals $R $SS --threads 3 --held float
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done
