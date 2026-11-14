#!/bin/bash
# I770 queue 5: the strip zero 7.7410972542 + 3.7686870595i (settings A and C, r1 = 0.3) at setting B (r1 = 0.25): its
# box counted at B, and the wide box W at B with K = 24 (queue 1's K = 6 count of W gave 0 at both settings).
source ~/venv-314/bin/activate
P=/Users/nathan/Source/choptuik-large-d-xf-770/solver/matter/css_inner_pert.py
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$P" "$@"; echo "== exit $?"; }
run count 1 6.5 8 2.9498939 4.61234085 --set=B --out=diag_k1.jsonl
run count 1 0.05 8 -9.5996817 9.5996817 --set=B --K=24 --out=diag_k1.jsonl
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
