#!/bin/zsh
# kernel work after the chain: sensitivities, then the Schur analysis with its control and plant
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a28bee1f4ff612f8d/hp
PY=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/venv-hp-osolve-313/bin/python
RAW=/Users/nathan/Source/choptuik-large-d-raw
OUT=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/held_harmonics
nice -n 10 $PY -u held_fit.py sens $RAW $OUT/sens_chain.json anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz \
  anm-mac/run_trend_pin3_qd7/anm_pin3_D82.7188.npz anm-mac/run_trend_pin3_qd9/anm_pin3_D85.7473.npz \
  T110-win/chain/anm_pin3_D100.1184.npz T116-win2/chain/anm_pin3_D149.5559.npz T129-win2/chain4/anm_pin3_D200.2746.npz > $OUT/sens_chain.log 2>&1
echo "sens chain exit $?" >> $OUT/sens_chain.log
nice -n 10 $PY -u held_schur.py $RAW anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz --json=$OUT/schur_79.json > $OUT/schur_79.log 2>&1
echo "schur 79 exit $?" >> $OUT/schur_79.log
nice -n 10 $PY -u held_fit.py sens $RAW $OUT/sens_qd.json T84-mac/pin5_D68.5000_full.npz T84-mac/pin7_D71.0000_full.npz \
  T81/conv_pin5_D73.0000_D73.000000.npz > $OUT/sens_qd.log 2>&1
echo "sens qd exit $?" >> $OUT/sens_qd.log
nice -n 10 $PY -u held_schur.py $RAW anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz --mutate=pinned_rows > $OUT/schur_79_control.log 2>&1
echo "schur control exit $?" >> $OUT/schur_79_control.log
nice -n 10 $PY -u held_schur.py $RAW T81/conv_pin5_D73.0000_D73.000000.npz --plant=5a:1e-8,13a:1e-6 > $OUT/schur_73_plant.log 2>&1
echo "schur plant exit $?" >> $OUT/schur_73_plant.log
echo all done
