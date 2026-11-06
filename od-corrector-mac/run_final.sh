#!/bin/bash
# after (e) after: (e) before (the pre-change code, its data file restored), then the planted-start probes with logs
A=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/octo_agent
PY=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/venv-hp-osolve-313/bin/python
until grep -q "e_after exit" $A/checks_status.log; do sleep 20; done
bash $A/run_checks.sh e_before
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp
$PY -u $A/probe_a.py 1e-12 > $A/probe_a_last.log 2>&1
EXCL_LAST=1 $PY -u $A/probe_a.py 1e-12 > $A/probe_a.log 2>&1
echo "probes exit $?" >> $A/checks_status.log
