#!/bin/bash
# I95-mac: the crate at D = 60 (queue3.sh), then complex_imag.py's checks again with the tolerance test (rtol 1e-9 and
# 1e-13 against 1e-11) and the Cauchy-Riemann step h = 1e-3
R=/Users/nathan/Source/choptuik-large-d-raw/I95-mac
bash $R/imag/queue3.sh
PY=/Users/nathan/Source/venv-anm/bin/python
S=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5ed9e8693e16e014/solver/matter/complex_imag.py
ST=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5ed9e8693e16e014/hp/data/states
C=$R/imag/checks2.jsonl
run() { echo "== $(date -u '+%H:%M:%S') $*"; nice -n 10 $PY $S "$@"; echo "exit $?"; }
run check $ST/up2_D20.0437.npz --out=$C
run check $ST/up_D10.0000.npz --out=$C
run check $R/states/lowDn_D4.0000_M48.npz --out=$C
