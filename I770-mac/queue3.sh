#!/bin/bash
# I770 queue 3: the zero in the strip 5 < Re < 8, 2.95 < Im < 3 omega (queue 2: winding 1 at setting A), located by
# `locate` and refined at settings B and C; first its control, a zero planted at 2.3 + 6.1i in a box free of zeros.
source ~/venv-314/bin/activate
P=/Users/nathan/Source/choptuik-large-d-xf-770/solver/matter/css_inner_pert.py
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$P" "$@"; echo "== exit $?"; }
run locate 1 2 3 5.5 6.5 --set=A,B --plant=2.3+6.1j --out=locate_k1.jsonl
run locate 1 5 8 2.9498939 9.5996817 --set=A,B,C --w=1 --out=locate_k1.jsonl
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
