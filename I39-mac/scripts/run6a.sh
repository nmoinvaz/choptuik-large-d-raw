#!/bin/zsh
# usage: run6a.sh <args for check_6a.py>; pauses the review's disc check (pid in $PAUSE) while it runs
R=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-ab6ec531e45efaac2/solver/proof/review_39
[ -n "$PAUSE" ] && kill -STOP $PAUSE
nice -n 10 /Users/nathan/venv-qd/bin/python $R/check_6a.py "$@"
rc=$?
[ -n "$PAUSE" ] && kill -CONT $PAUSE
echo "exit $rc"
