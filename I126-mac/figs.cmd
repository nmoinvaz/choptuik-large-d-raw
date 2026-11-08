#!/bin/zsh
# Figs. 4-5 measures: exact, Eq. (16) and D = infinity profiles; NLO, NNLO printed, corrected; the centre x = 0
W=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-aad2528b106a4fd00
R=/Users/nathan/Source/choptuik-large-d-raw/I126-mac
PY=/Users/nathan/venv-qd/bin/python
P=$W/solver/inner_pert/nnlo_vs_solution.py
nice -n 10 $PY $P figs $R/fields/fields_D*.npz --json=$R/figs.json > $R/figs.log 2>&1; echo "figs (NLO, centre) $?" >> $R/exits.txt
