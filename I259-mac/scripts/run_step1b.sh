#!/bin/bash
# #259 step 1b: acc 0, 2, 3 at D 55 M 64, then its M 48 control (one process at a time)
PY=/Users/nathan/venv-314/bin/python
WT=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ad7c3fd5979c081c9
ST=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/states/I252-mac/states
cd /Users/nathan/Source/choptuik-large-d-raw/I259-mac
nice -n 10 caffeinate -i $PY scripts/series_acc_probe.py $WT/hp $ST/modecount_state_D55.0351_M64_kf23.npz 23 2.04768412771239 probe/series_acc023_D55_M64.json --accs=0,2,3 > probe/series_acc023_D55_M64.log 2>&1
echo "1b D55 M64 exit $?" >> probe/exits.txt
nice -n 10 caffeinate -i $PY scripts/series_acc_probe.py $WT/hp $ST/modecount_state_D55.0351_M48_kf23_from_I232.npz 23 2.04768412771239 probe/series_acc023_D55_M48.json --accs=0,2,3 > probe/series_acc023_D55_M48.log 2>&1
echo "1b D55 M48 exit $?" >> probe/exits.txt
