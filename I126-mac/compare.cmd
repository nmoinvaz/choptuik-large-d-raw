#!/bin/zsh
# C1-C4, C6 on the solutions; Figs. 4-5 measures with the exact, Eq. (16) and D = infinity profiles
W=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-aad2528b106a4fd00
R=/Users/nathan/Source/choptuik-large-d-raw/I126-mac
PY=/Users/nathan/venv-qd/bin/python
P=$W/solver/inner_pert/nnlo_vs_solution.py
nice -n 10 $PY $P compare $R/fields/fields_D*.npz --spread=$R/fields_t140_d6,$R/fields_t140_d10 --json=$R/compare.json > $R/compare.log 2>&1; echo "compare $?" >> $R/exits.txt
nice -n 10 $PY $P compare $R/fields/fields_D*.npz --mutate=pi3x1.01 --json=$R/compare_mut.json > $R/compare_mut.log 2>&1; echo "compare --mutate=pi3x1.01 $?" >> $R/exits.txt
nice -n 10 $PY $P figs $R/fields/fields_D*.npz --json=$R/figs.json > $R/figs.log 2>&1; echo "figs $?" >> $R/exits.txt
