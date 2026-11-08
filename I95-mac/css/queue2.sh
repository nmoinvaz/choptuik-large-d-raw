#!/bin/bash
# I95-mac CSS (kappa = 0) box counts, run 2 (complex_css.py boxes / root, worktree branch wip/i95); one process, nice 10
PY=/Users/nathan/venv-qd/bin/python
S=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a5ed9e8693e16e014/solver/matter/complex_css.py
R=/Users/nathan/Source/choptuik-large-d-raw/I95-mac/css
O=$R/boxes_k0.jsonl
run() { echo "== $(date -u '+%H:%M:%S') $*"; nice -n 10 $PY $S "$@"; echo "exit $?"; }
# controls first, at D = 4: a zero planted in C; the metric perturbation not fed back (C and B must change)
run boxes 4 0.25866983+3.50224880j --R=0.85 --names=C --plant=1.0+3.0j --out=$O
run boxes 4 0.25866983+3.50224880j --R=0.85 --names=B,C --mutate=nometric --out=$O
run boxes 4 0.25866983+3.50224880j --out=$O
run boxes 5 0.31462468+3.78948723j --out=$O
run boxes 6 0.35163567+4.09794310j --out=$O
run boxes 8 0.39769776+4.60913768j --out=$O
run boxes 10 0.42514173+4.99931817j --out=$O
run boxes 20 0.47996049+6.06909284j --out=$O
run boxes 40 0.50779164+6.84526018j --out=$O
run root 20 2.0973 --out=$R/roots_k0.jsonl
run root 40 2.0565 --out=$R/roots_k0.jsonl
run boxes 80 0.52199898+7.33689470j --out=$O
run root 80 2.0312 --out=$R/roots_k0.jsonl
