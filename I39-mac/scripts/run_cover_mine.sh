#!/bin/zsh
# the per-row summary and the review's covering check, clean and mutated
R=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ab6ec531e45efaac2/solver/proof/review_39
O=/Users/nathan/Source/choptuik-large-d-raw/I39-mac
RUNS=/Users/nathan/Source/choptuik-large-d-raw/I38-macm3/lemma6b1_runs_M5_cert
PY=/Users/nathan/venv-qd/bin/python
PHAT=2.7185791892117424129838364801284328088346127237383,0.99922840320656778341382852244561290493008493287400,0.14920357491144750568385993252030607895883448797542,0.014719052490251352880370993221847567330326070847323,0.0084053469057616610717371606774095980018242241353148,0.0014703451815915780267358143174281560008811122540642
nice -n 10 $PY $R/check_6b1.py summary --mine=$O/check_6b1 --inputs=$O/disc_inputs --runs=$RUNS > $O/summary_6b1.md 2>&1; echo "exit $?" >> $O/summary_6b1.md
nice -n 10 $PY $R/check_6b1.py cover --runs=$RUNS --mine=$O/check_6b1 --x=$PHAT --json=$O/cover_6b1.json > $O/cover_6b1.log 2>&1; echo "exit $?" >> $O/cover_6b1.log
nice -n 10 $PY $R/check_6b1.py cover --runs=$RUNS --mine=$O/check_6b1 --x=$PHAT --mutate=drop:9,5 > $O/cover_6b1_mut_drop_9_5.log 2>&1; echo "exit $?" >> $O/cover_6b1_mut_drop_9_5.log
nice -n 10 $PY $R/check_6b1.py cover --runs=$RUNS --mine=$O/check_6b1 --x=$PHAT --mutate=radius:9 > $O/cover_6b1_mut_radius_9.log 2>&1; echo "exit $?" >> $O/cover_6b1_mut_radius_9.log
nice -n 10 $PY $R/check_6b1.py cover --runs=$RUNS --mine=$O/check_6b1 --x=$PHAT --mutate=g0 > $O/cover_6b1_mut_g0.log 2>&1; echo "exit $?" >> $O/cover_6b1_mut_g0.log
