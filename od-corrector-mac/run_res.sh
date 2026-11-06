#!/bin/bash
# step 0a at two plan tolerances
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp
PY=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/venv-hp-osolve-313/bin/python
A=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/octo_agent
for T in 1e-32 1e-40 1e-48; do
  $PY -u $A/step0_res.py /Users/nathan/Source/choptuik-large-d-raw $T T129-win2/chain/anm_pin3_D180.5246.npz \
    T129-win2/chain/anm_pin3_D185.5246.npz T129-win2/chain/anm_pin3_D188.0246.npz T129-win2/chain2/anm_pin3_D193.7746.npz
done
