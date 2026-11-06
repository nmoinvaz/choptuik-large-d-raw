#!/bin/bash
# check (d): one --corrector od step from T129-win2/chain2/anm_pin3_D193.7746.npz with the chain's options, then a restart
# from the saved eight-part state (--steps 0: the base polish only). The restart reads the state through RAW, so the
# first run's output folder is given to it as a path relative to a RAW that holds it: the scratch folder itself.
A=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/octo_agent
PY=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/venv-hp-osolve-313/bin/python
R=/Users/nathan/Source/choptuik-large-d-raw
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp
if [ "$1" != restart ]; then
  $PY -u anm_run.py $R $A/d_step --state T129-win2/chain2/anm_pin3_D193.7746.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 \
    --steps 1 --D_max 1000 --threads 3 --corrector od --tol_od 1e-40 --qd_it 12 --trend T75 --jet_o 1 --reseed 2 --reseed_q 1 \
    --save_pred 1 --allow_unraw > $A/d_step.log 2>&1
  echo "d_step exit $?" >> $A/checks_status.log
fi
S=$(ls $A/d_step/anm_pin3_D*.npz 2>/dev/null | head -1)
if [ -n "$S" ]; then
  # the trend folder is read through RAW too: link it beside the saved state
  ln -sfn $R/T75 $A/T75
  $PY -u anm_run.py $A $A/d_restart --state d_step/$(basename $S) --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 --steps 0 \
    --D_max 1000 --threads 3 --corrector od --tol_od 1e-40 --qd_it 12 --trend T75 --jet_o 1 --reseed 2 --reseed_q 1 \
    --allow_unraw > $A/d_restart.log 2>&1
  echo "d_restart exit $?" >> $A/checks_status.log
fi
