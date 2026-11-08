#!/bin/zsh
# row 0 disc mutations, one process at a time
R=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ab6ec531e45efaac2/solver/proof/review_39
O=/Users/nathan/Source/choptuik-large-d-raw/I39-mac
PY=/Users/nathan/venv-qd/bin/python
nice -n 10 $PY -u $R/check_6b1.py discs --inputs=$O/disc_inputs --rows=0 --discs=0,18,37 --out=$O/check_6b1_mut --mutate=sign > $O/mut_sign_row0.log 2>&1; echo "exit $? (0 only if every disc certifies)" >> $O/mut_sign_row0.log
nice -n 10 $PY -u $R/controls.py orig_discs --inputs=$O/disc_inputs --rows=0 --discs=0,18,37 --mutate=sign > $O/orig_mut_sign_row0.log 2>&1; echo "exit $? (0 only if no disc certifies)" >> $O/orig_mut_sign_row0.log
nice -n 10 $PY -u $R/check_6b1.py discs --inputs=$O/disc_inputs --rows=0 --discs=0,37 --out=$O/check_6b1_mut --r_scale=1.01 > $O/rscale_row0.log 2>&1; echo "exit $? (0 only if every disc certifies)" >> $O/rscale_row0.log
nice -n 10 $PY -u $R/controls.py orig_discs --inputs=$O/disc_inputs --rows=0 --discs=0,37 --r_scale=1.01 > $O/orig_rscale_row0.log 2>&1; echo "exit $? (0 only if every disc certifies)" >> $O/orig_rscale_row0.log
