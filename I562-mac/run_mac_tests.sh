#!/usr/bin/env bash
# #562 code-path tests on the Mac: a planted trace in the linear regime (eps 1e-25, h_max 1: one rung, the endpoint
# polish and the planted check), then the same with --mutate tsign, whose planted check must fail.
PY=/Users/nathan/venv-314/bin/python
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i562
R=$RAW/I562-mac
S=I562-win2/renode_0975_D242.3642.npz
cd /Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a671334124392504b/hp || exit 9
log() { echo "$1 $(date -u '+%Y-%m-%d %H:%M:%S UTC') $(git rev-parse --short HEAD)" >> $R/exits.txt; }
log "test_lin start"
nice -n 10 $PY -u held_homotopy.py $RAW $S $R/test_lin --mode planted --eps 1e-25 --h_max 1 --threads 4 --ladder 0:46:4 > $R/test_lin.log 2>&1
log "test_lin exit $? (must be 0)"
log "test_lin_tsign start"
nice -n 10 $PY -u held_homotopy.py $RAW $S $R/test_lin_tsign --mode planted --eps 1e-25 --h_max 1 --threads 4 --ladder 0:46:4 --mutate tsign > $R/test_lin_tsign.log 2>&1
log "test_lin_tsign exit $? (must not be 0)"
