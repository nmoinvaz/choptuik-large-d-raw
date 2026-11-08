#!/bin/bash
# I95-mac: the cheap controls and fits, logged with their exit codes (controls.log)
M=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5ed9e8693e16e014/solver/matter
R=/Users/nathan/Source/choptuik-large-d-raw/I95-mac
run() { echo "== $(date -u '+%H:%M:%S') $*"; nice -n 10 "$@"; echo "exit $?"; }
run /Users/nathan/venv-qd/bin/python $M/complex_imag_eqs.py --mutate
run /Users/nathan/venv-qd/bin/python $M/complex_css.py selftest
run /Users/nathan/Source/venv-anm/bin/python $M/complex_imag.py selftest
run /Users/nathan/venv-qd/bin/python $M/complex_osc_fit.py $R
run python3 $M/complex_table.py $R
