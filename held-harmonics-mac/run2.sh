#!/bin/zsh
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a28bee1f4ff612f8d/hp
PY=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/venv-hp-osolve-313/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw
OUT=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/held_harmonics
rm -f $OUT/sens_chain.json
nice -n 10 $PY -u held_fit.py sens $RAW $OUT/sens_chain.json anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz \
  anm-mac/run_trend_pin3_qd7/anm_pin3_D82.7188.npz anm-mac/run_trend_pin3_qd9/anm_pin3_D85.7473.npz \
  T110-win/chain/anm_pin3_D100.1184.npz T116-win2/chain/anm_pin3_D149.5559.npz T129-win2/chain4/anm_pin3_D200.2746.npz > $OUT/sens_chain.log 2>&1
echo "sens chain exit $?" >> $OUT/sens_chain.log
# the chain's control: one step from 73.0 on a fit whose harmonic 5 is 1% wrong; predicted bias -2.96e-9
nice -n 10 $PY -u anm_run.py $RAW $OUT/chain_wrong5 --state T81/conv_pin5_D73.0000_D73.000000.npz --kfreeze 3 --corrector qd \
  --held_fit $OUT/fit_wrong5.json --h_max 0.8108651627 --D_max 73.82 --steps 1 --threads 2 --fix1 1 --F_pred_max 1.5e-14 --allow_unraw > $OUT/chain_wrong5.log 2>&1
echo "chain control exit $?" >> $OUT/chain_wrong5.log
nice -n 10 $PY -u held_schur.py $RAW anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz --json=$OUT/schur_79.json > $OUT/schur_79.log 2>&1
echo "schur 79 exit $?" >> $OUT/schur_79.log
echo all done
