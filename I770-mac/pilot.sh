#!/bin/bash
# I770 pilot at kappa = 1: the exact modes as zeros of det M at settings A, B (and C), the conjugation symmetry, and the
# count of box B (expected 2: lambda = 1, 2) at setting A with its time.
source ~/venv-314/bin/activate
P=/Users/nathan/Source/choptuik-large-d-xf-770/solver/matter/css_inner_pert.py
PK=/Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter/css_inner_pert.py   # check with the kappa != 0 metric
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$@"; echo "== exit $?"; }
run "$PK" check 1 --out=check_k1.jsonl
run "$P" root 1 2.1 --set=A,B,C --out=roots_k1.jsonl
run "$P" root 1 1.1 --set=A,B,C --out=roots_k1.jsonl
for z in 1.3+2.1j 1.3-2.1j 0.7+6.5j 0.7-6.5j; do
  run "$P" det 1 $z --out=conj_k1.jsonl
  run "$P" det 1 $z --r0=0.1 --r1=0.25 --out=conj_k1.jsonl
done
run "$P" count 1 0.9 5 -2.9498939 2.9498939 --set=A --out=counts_k1.jsonl
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
