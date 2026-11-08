#!/bin/zsh
# the original covering check on copies of the stored runs: clean and the three mutations (pauses $PAUSE meanwhile)
R=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ab6ec531e45efaac2/solver/proof/review_39
RUNS=/Users/nathan/Source/choptuik-large-d-raw/I38-macm3/lemma6b1_runs_M5_cert
O=/Users/nathan/Source/choptuik-large-d-raw/I39-mac
[ -n "$PAUSE" ] && kill -STOP $PAUSE
nice -n 10 /Users/nathan/venv-qd/bin/python $R/controls.py orig_cover --runs=$RUNS > $O/orig_cover_clean.log 2>&1; echo "exit $?" >> $O/orig_cover_clean.log
nice -n 10 /Users/nathan/venv-qd/bin/python $R/controls.py orig_cover --runs=$RUNS --mutate=drop:9,5 > $O/orig_cover_drop_9_5.log 2>&1; echo "exit $?" >> $O/orig_cover_drop_9_5.log
nice -n 10 /Users/nathan/venv-qd/bin/python $R/controls.py orig_cover --runs=$RUNS --mutate=radius:9 > $O/orig_cover_radius_9.log 2>&1; echo "exit $?" >> $O/orig_cover_radius_9.log
nice -n 10 /Users/nathan/venv-qd/bin/python $R/controls.py orig_cover --runs=$RUNS --mutate=g0 > $O/orig_cover_g0.log 2>&1; echo "exit $?" >> $O/orig_cover_g0.log
[ -n "$PAUSE" ] && kill -CONT $PAUSE
