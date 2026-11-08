#!/bin/zsh
# the high-precision ray control, clean and mutated; pauses worker 1's current python meanwhile
R=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ab6ec531e45efaac2/solver/proof/review_39
O=/Users/nathan/Source/choptuik-large-d-raw/I39-mac
RAY=/Users/nathan/Source/choptuik-large-d-raw/I38-macm3/lemma6b1_runs_M5_cert/ray.json
P=$(pgrep -f "review_39/(dump_inputs|check_6b1).py.*--rows=$PROW( |$)" | head -1)
echo "pausing $P"
[ -n "$P" ] && kill -STOP $P
nice -n 10 /Users/nathan/venv-qd/bin/python -u $R/ray_hp.py --ray=$RAY > $O/ray_hp.log 2>&1
echo "exit $?" >> $O/ray_hp.log
nice -n 10 /Users/nathan/venv-qd/bin/python -u $R/ray_hp.py --ray=$RAY --to=3 --mutate=w > $O/ray_hp_mut_w.log 2>&1
echo "exit $?" >> $O/ray_hp_mut_w.log
[ -n "$P" ] && kill -CONT $P
tail -4 $O/ray_hp.log; tail -3 $O/ray_hp_mut_w.log
