#!/bin/bash
# #874: u_2, two plain Newton steps from #837's truth at D 240.1244, stored in eight parts in this folder, then read
# back and checked; the control reads the old truth through the same path and must fail both bounds (and the match).
# Waits for I856-mac's queue: one process at a time.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I874-mac
S240=I603-win2/chain/anm_pin3_D240.1244.npz
U2=I874-mac/anm_pin3_D240.1244_u2.npz
J852=$R/I852-mac/steps_D240.json
cd "$(dirname "$0")" || exit 9
until [ -f $R/I856-mac/queue.done ]; do sleep 60; done
./run.sh store_u2 truth_restep.py store $R $S240 $U2 --steps 2 --threads 3 --match $J852
./run.sh check_u2 truth_restep.py check $R $U2 --threads 3 --held_ref $S240 --match $J852 --match_k 3 --json $O/check_u2.json
./run.sh check_truth truth_restep.py check $R $S240 --threads 3 --match $J852 --match_k 3 --json $O/check_truth.json
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done
