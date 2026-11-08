#!/bin/bash
# I95-mac: the D = 60 imaginary-sector count with the double-double crate (hp/modecount_test.py, hp/modecount_cx built
# 2026-10-26 in the main checkout; notes/GHOST_ADMIXTURE.md), where complex_imag.py's double precision fails
PY=/Users/nathan/Source/venv-anm/bin/python
W=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5ed9e8693e16e014
R=/Users/nathan/Source/choptuik-large-d-raw/I95-mac/imag/crate
mkdir -p $R
export PYTHONPATH=/Users/nathan/Source/choptuik-large-d/hp/modecount_cx/build
run() { echo "== $(date -u '+%H:%M:%S') $*"; nice -n 10 $PY "$@"; echo "exit $?"; }
run $W/hp/modecount_test.py $W/hp/data/states/up13_D60.0020.npz --boxes=B0,full --data=$R --tag=D60.0020_M32
run $W/hp/modecount_test.py $W/hp/data/states/up13_D60.0020.npz --boxes=B0,full --data=$R --tag=D60.0020_M32 --plant=3.1+1.0j
