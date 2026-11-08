#!/bin/zsh
# C4 did not fire at Pi_3 x 1.01; how large a scale the exponent test resolves (reported, not a criterion), and the
# planted test with a plant as large as the real residual (plant_scale 1000), where the 1.01 control should then also
# stay silent if the cause is the size of the real eps^(7/2) term
W=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-aad2528b106a4fd00
R=/Users/nathan/Source/choptuik-large-d-raw/I126-mac
PY=/Users/nathan/venv-qd/bin/python
P=$W/solver/inner_pert/nnlo_vs_solution.py
for s in 1.02 1.05 1.1 1.2 1.5; do
  nice -n 10 $PY $P compare $R/fields/fields_D*.npz --mutate=pi3x$s --json=$R/compare_mut$s.json > $R/compare_mut$s.log 2>&1; echo "compare --mutate=pi3x$s $?" >> $R/exits.txt
done
nice -n 10 $PY $P planted $R/fields/fields_D*.npz --plant_scale=1000 --mutate=pi3x1.01 --json=$R/planted_big_mut.json > $R/planted_big_mut.log 2>&1; echo "planted --plant_scale=1000 --mutate=pi3x1.01 $?" >> $R/exits.txt
nice -n 10 $PY $P compare $R/fields/fields_D*.npz --dmax=140 --json=$R/compare_dmax140.json > $R/compare_dmax140.log 2>&1; echo "compare --dmax=140 $?" >> $R/exits.txt
nice -n 10 $PY $P compare $R/fields/fields_D*.npz --dmin=73 --json=$R/compare_dmin73.json > $R/compare_dmin73.log 2>&1; echo "compare --dmin=73 $?" >> $R/exits.txt
nice -n 10 $PY $P figs $R/fields/fields_D*.npz --json=$R/figs.json > $R/figs.log 2>&1; echo "figs (with NLO) $?" >> $R/exits.txt
