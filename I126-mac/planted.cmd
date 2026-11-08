#!/bin/zsh
# C5, planted truth on every state's beta~ (run before the real comparison); exits in exits.txt
W=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-aad2528b106a4fd00
R=/Users/nathan/Source/choptuik-large-d-raw/I126-mac
PY=/Users/nathan/venv-qd/bin/python
P=$W/solver/inner_pert/nnlo_vs_solution.py
nice -n 10 $PY $P planted $R/fields/fields_D*.npz --json=$R/planted.json > $R/planted.log 2>&1; echo "planted $?" >> $R/exits.txt
nice -n 10 $PY $P planted $R/fields/fields_D*.npz --plant_pi=3 --json=$R/planted_pi3.json > $R/planted_pi3.log 2>&1; echo "planted --plant_pi=3 $?" >> $R/exits.txt
nice -n 10 $PY $P planted $R/fields/fields_D*.npz --mutate=pi3x1.01 --json=$R/planted_mut.json > $R/planted_mut.log 2>&1; echo "planted --mutate=pi3x1.01 $?" >> $R/exits.txt
