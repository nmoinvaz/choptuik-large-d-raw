#!/bin/bash
# #259 step 1c: acc 0, 4 (quad-double horizon tangent solves) at D 55 M 64
PY=/Users/nathan/venv-314/bin/python
WT=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ad7c3fd5979c081c9
ST=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/states/I252-mac/states
cd /Users/nathan/Source/choptuik-large-d-raw/I259-mac
nice -n 10 caffeinate -i $PY scripts/series_acc_probe.py $WT/hp $ST/modecount_state_D55.0351_M64_kf23.npz 23 2.04768412771239 probe/series_acc4_D55_M64.json --accs=0,4 > probe/series_acc4_D55_M64.log 2>&1
echo "1c D55 M64 exit $?" >> probe/exits.txt
