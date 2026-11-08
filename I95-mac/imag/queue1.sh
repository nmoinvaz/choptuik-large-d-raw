#!/bin/bash
# I95-mac imaginary-sector counts, run 1 (complex_imag.py, worktree branch wip/i95); one process, nice 10
PY=/Users/nathan/Source/venv-anm/bin/python
S=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5ed9e8693e16e014/solver/matter/complex_imag.py
ST=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5ed9e8693e16e014/hp/data/states
R=/Users/nathan/Source/choptuik-large-d-raw/I95-mac
O=$R/imag/counts.jsonl
run() { echo "== $(date -u '+%H:%M:%S') $*"; nice -n 10 $PY $S "$@"; echo "exit $?"; }
run count $ST/up2_D20.0437.npz B0 U0 FULL --out=$O --evlog=$R/imag/evals_D20.jsonl
run count $ST/up2_D20.0437.npz B0 FULL --plant=3.1+1.0j --out=$O --evlog=$R/imag/evals_D20.jsonl
run count $ST/up2_D20.0437.npz B0 --mutate=coupling --out=$O --evlog=$R/imag/evals_D20.jsonl
run count $ST/up2_D20.0437.npz B0 --mutate=noG --out=$O --evlog=$R/imag/evals_D20.jsonl
run count $ST/up13_D60.0020.npz B0 U0 FULL --kf=13 --out=$O --evlog=$R/imag/evals_D60_kf13.jsonl
run count $ST/up13_D60.0020.npz B0 FULL --kf=13 --plant=3.1+1.0j --out=$O --evlog=$R/imag/evals_D60_kf13.jsonl
run count $ST/up13_D60.0020.npz B0 --kf=13 --mutate=coupling --out=$O --evlog=$R/imag/evals_D60_kf13.jsonl
run count $ST/up_D10.0000.npz B0 U0 FULL --out=$O --evlog=$R/imag/evals_D10.jsonl
run count $R/states/lowDn_D4.0000_M48.npz B0 U0 FULL --out=$O --evlog=$R/imag/evals_D4_M48.jsonl
run count $R/states/lowDn_D4.0000_M48.npz U0 --plant=0.05+1.5j --out=$O --evlog=$R/imag/evals_D4_M48.jsonl
