#!/bin/bash
# #259: production mode_det, the main checkout's build against this worktree's (D 55 M 48), one process at a time
PY=/Users/nathan/venv-314/bin/python
WT=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ad7c3fd5979c081c9
ST=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/states/I252-mac/states
S=$ST/modecount_state_D55.0351_M48_kf23_from_I232.npz
cd /Users/nathan/Source/choptuik-large-d-raw/I259-mac
nice -n 10 caffeinate -i $PY scripts/prod_identity.py $WT/hp $S 23 2.04768412771239 /Users/nathan/Source/choptuik-large-d/hp/modecount_cx/build checks/identity_main.json > checks/identity_main.log 2>&1
echo "identity main exit $?" >> checks/exits.txt
nice -n 10 caffeinate -i $PY scripts/prod_identity.py $WT/hp $S 23 2.04768412771239 $WT/hp/modecount_cx/build checks/identity_wt.json > checks/identity_wt.log 2>&1
echo "identity worktree exit $?" >> checks/exits.txt
