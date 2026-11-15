#!/bin/bash
# #852: Newton's contraction in the horizon data at D 240.1244 (#837's truth_system). The controls first: --mutate
# nostep must read "does NOT contract", and the centre block (where Newton returns the move, #840) is the positive
# control. Then m_h, a_h at rel 1e-90, 1e-93, 1e-96 (seed 1), three steps, in one run sharing one unperturbed path.
# Waits for I850-mac's queue, so that one process runs at a time.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I852-mac
S240=I603-win2/chain/anm_pin3_D240.1244.npz
REF240=-4.3765436014297066e-58
cd "$(dirname "$0")" || exit 9
until [ -f $R/I850-mac/queue.done ]; do sleep 60; done
C="--threads 3 --seeds 1 --controls 0 --repeat 0 --ref $REF240"
./run.sh ctl_nostep_D240 step_spread.py $R $S240 $C --rel 1e-96 --steps 2 --mutate nostep --json $O/ctl_nostep_D240.json
./run.sh ctl_centre_D240 step_spread.py $R $S240 $C --blocks centre --rel 1e-90 --steps 2 --json $O/ctl_centre_D240.json
./run.sh steps_D240 step_spread.py $R $S240 $C --rel 1e-90,1e-93,1e-96 --steps 3 --json $O/steps_D240.json
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done
