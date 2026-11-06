#!/bin/bash
# step 0b and 0c
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp
PY=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/venv-hp-osolve-313/bin/python
A=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/octo_agent
R=/Users/nathan/Source/choptuik-large-d-raw
echo "== step 0b: one step at 188.0246, plan 1e-32"
$PY -u $A/step0_step.py $R 1e-32 T129-win2/chain/anm_pin3_D188.0246.npz --qd_refine4 1 --octo 1 --out $A/step0_D188_steps.npz
echo "== step 0c: newton_qd floors at plan 1e-40 and 1e-48"
$PY -u $A/step0_floor.py $R 1e-40 T129-win2/chain/anm_pin3_D185.5246.npz T129-win2/chain/anm_pin3_D188.0246.npz T129-win2/chain2/anm_pin3_D193.7746.npz
$PY -u $A/step0_floor.py $R 1e-48 T129-win2/chain/anm_pin3_D185.5246.npz T129-win2/chain2/anm_pin3_D193.7746.npz
echo "== step 0c: newton_qd floors at plan 1e-32 (the baseline)"
$PY -u $A/step0_floor.py $R 1e-32 T129-win2/chain/anm_pin3_D185.5246.npz T129-win2/chain2/anm_pin3_D193.7746.npz
