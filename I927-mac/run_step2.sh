#!/usr/bin/env bash
# #927: the second pilot step's reference and the step. The first reference run stopped on its --hours rule after
# D 3.695 (ref48/leg.log), so lowD_highM.py runs again from its converged 3.695 pair to 3.69 (ref48b/), and then the
# pilot's step 2 goes from step 1's corrected state at 3.695 to 3.69 against it. Waits for run_pilot_chain.sh.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/afb99455-a815-419f-becf-38b07aee7d3a/scratchpad/raw927/I927-mac
PY=/Users/nathan/venv-314/bin/python
while pgrep -f run_pilot_chain.sh > /dev/null; do sleep 15; done
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a611e0854f7930044/hp || exit 9
mkdir -p $R/ref48b
echo "ref48b start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/ref48b/exits.txt
nice -n 10 $PY -u lowD_highM.py --start_w $R/ref48/states/lowD927_D3.6950_M48.npz \
    --start_n $R/ref48/states/lowD927_D3.6950_M64.npz --Ms 48,64 --dD 0.005 --D_end 3.6876 --diff_max 1 --hours 1 \
    --point_hours 3 --tag lowD927 --threads 4 --out $R/ref48b/leg.jsonl --points $R/ref48b/points.jsonl \
    --states $R/ref48b/states >> $R/ref48b/leg.log 2>&1
echo "ref48b exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/ref48b/exits.txt
sed -i '' 's#REF2=$R/ref48/states/lowD927_D3.6900_M48.npz#REF2=$R/ref48b/states/lowD927_D3.6900_M48.npz#' $R/run_pilot.sh
if [ -f $R/ref48b/states/lowD927_D3.6900_M48.npz ]; then bash $R/run_pilot.sh step2; fi
echo "step2 chain done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/chain_exits.txt
