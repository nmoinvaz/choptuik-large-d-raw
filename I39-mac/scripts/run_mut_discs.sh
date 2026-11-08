#!/bin/zsh
# disc mutations on the given rows, in the review and in the original (pauses $PAUSE meanwhile). usage: ROWS=17 run_mut_discs.sh
R=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ab6ec531e45efaac2/solver/proof/review_39
O=/Users/nathan/Source/choptuik-large-d-raw/I39-mac
IN=$O/disc_inputs
PY=/Users/nathan/venv-qd/bin/python
[ -n "$PAUSE" ] && kill -STOP $PAUSE
for j in ${(s:,:)ROWS}; do
  nice -n 10 $PY -u $R/check_6b1.py discs --inputs=$IN --rows=$j --out=$O/check_6b1_mut --mutate=sign > $O/mut_sign_row$j.log 2>&1; echo "exit $? (0 only if every disc certifies)" >> $O/mut_sign_row$j.log
  nice -n 10 $PY -u $R/controls.py orig_discs --inputs=$IN --rows=$j --mutate=sign > $O/orig_mut_sign_row$j.log 2>&1; echo "exit $? (0 only if no disc certifies)" >> $O/orig_mut_sign_row$j.log
  nice -n 10 $PY -u $R/check_6b1.py discs --inputs=$IN --rows=$j --out=$O/check_6b1_mut --r_scale=1.01 > $O/rscale_row$j.log 2>&1; echo "exit $? (0 only if every disc certifies)" >> $O/rscale_row$j.log
  nice -n 10 $PY -u $R/controls.py orig_discs --inputs=$IN --rows=$j --r_scale=1.01 > $O/orig_rscale_row$j.log 2>&1; echo "exit $? (0 only if every disc certifies)" >> $O/orig_rscale_row$j.log
done
[ -n "$PAUSE" ] && kill -CONT $PAUSE
