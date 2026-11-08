#!/bin/bash
# I95-mac imaginary-sector counts, run 1b (after run 1 was stopped at D = 60, where det M in double precision is
# rounding noise even with the cut kf = 13; evals_D60_kf13.jsonl shows ln|det| jumping by 1-3 between neighbours)
PY=/Users/nathan/Source/venv-anm/bin/python
S=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5ed9e8693e16e014/solver/matter/complex_imag.py
ST=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5ed9e8693e16e014/hp/data/states
R=/Users/nathan/Source/choptuik-large-d-raw/I95-mac
O=$R/imag/counts.jsonl
C=$R/imag/checks.jsonl
run() { echo "== $(date -u '+%H:%M:%S') $*"; nice -n 10 $PY $S "$@"; echo "exit $?"; }
run check $ST/up2_D20.0437.npz --out=$C
run check $ST/up_D10.0000.npz --out=$C
run check $R/states/lowDn_D4.0000_M48.npz --out=$C
run check $ST/up13_D60.0020.npz --out=$C
run count $ST/up_D10.0000.npz B0 U0 FULL --out=$O --evlog=$R/imag/evals_D10.jsonl
run count $ST/up_D10.0000.npz B0 --mutate=coupling --out=$O --evlog=$R/imag/evals_D10.jsonl
run count $R/states/lowDn_D4.0000_M48.npz B0 U0 FULL --out=$O --evlog=$R/imag/evals_D4_M48.jsonl
run count $R/states/lowDn_D4.0000_M48.npz U0 --plant=0.05+1.5j --out=$O --evlog=$R/imag/evals_D4_M48.jsonl
run count $R/states/lowDn_D4.0000_M48.npz B0 --mutate=noG --out=$O --evlog=$R/imag/evals_D4_M48.jsonl
run root $R/states/lowDn_D4.0000_M48.npz -0.36 --out=$R/imag/roots.jsonl
run root $ST/up2_D20.0437.npz 0.03+0.02j --out=$R/imag/roots.jsonl
