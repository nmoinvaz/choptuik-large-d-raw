#!/bin/bash
# check (e): one --corrector qd step from 180.5246 with the chain's options (N 8, h_max 0.0625 to keep it short), by
# the code before the change (before/hp, fc636e7) or after it (the worktree). $1 = before | after
A=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/octo_agent
PY=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/venv-hp-osolve-313/bin/python
R=/Users/nathan/Source/choptuik-large-d-raw
if [ "$1" = before ]; then cd $A/before/hp; else cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp; fi
rm -rf $A/e_$1
$PY -u anm_run.py $R $A/e_$1 --state T129-win2/chain/anm_pin3_D180.5246.npz --kfreeze 3 --N 8 --eps 1e-14 --h_max 0.0625 \
  --steps 1 --D_max 1000 --threads 3 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_o 1 --reseed 2 --reseed_q 1 \
  --allow_unraw
