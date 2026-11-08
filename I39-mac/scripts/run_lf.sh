#!/bin/zsh
# the double-precision control of the disc inputs, clean and mutated; pauses worker 1's current python meanwhile
R=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ab6ec531e45efaac2/solver/proof/review_39
O=/Users/nathan/Source/choptuik-large-d-raw/I39-mac
RAY=/Users/nathan/Source/choptuik-large-d-raw/I38-macm3/lemma6b1_runs_M5_cert/ray.json
P=$(pgrep -f "review_39/(dump_inputs|check_6b1).py.*--rows=$PROW( |$)" | head -1)
echo "pausing $P"
[ -n "$P" ] && kill -STOP $P
nice -n 10 /Users/nathan/venv-qd/bin/python $R/lohner_float.py --ray=$RAY --inputs=$O/disc_inputs --rows=$LROWS > $O/lohner_float$TAG.log 2>&1
echo "exit $?" >> $O/lohner_float$TAG.log
nice -n 10 /Users/nathan/venv-qd/bin/python $R/lohner_float.py --ray=$RAY --inputs=$O/disc_inputs --rows=$LROWS --mutate=w > $O/lohner_float_mut_w$TAG.log 2>&1
echo "exit $?" >> $O/lohner_float_mut_w$TAG.log
[ -n "$P" ] && kill -CONT $P
tail -3 $O/lohner_float$TAG.log; tail -3 $O/lohner_float_mut_w$TAG.log
