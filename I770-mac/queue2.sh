#!/bin/bash
# I770 queue 2: the wide box W counted 0 at settings A and B, against 2 from its tiles (A + B + S + C and their
# conjugates cover W's part with Re < 5, and det M is analytic). Diagnostics at setting A: the strip 5 < Re < 8 in two
# pieces, then C and W with four times the starting samples per edge (K = 24 against 6).
source ~/venv-314/bin/activate
P=/Users/nathan/Source/choptuik-large-d-xf-770/solver/matter/css_inner_pert.py
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$P" "$@"; echo "== exit $?"; }
OL=2.9498939; OH=3.4498939; O3=9.5996817
run count 1 5 8 -$OL $OL --set=A --out=diag_k1.jsonl
run count 1 5 8 $OL $O3 --set=A --out=diag_k1.jsonl
run count 1 0.05 5 $OH $O3 --set=A --K=24 --out=diag_k1.jsonl
run count 1 0.05 8 -$O3 $O3 --set=A --K=24 --out=diag_k1.jsonl
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
