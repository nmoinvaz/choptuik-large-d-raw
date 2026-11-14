#!/bin/bash
# I376 queue 3: the conjugation symmetry of det M at D = infinity (kappa = 0): det M at lambda and conj(lambda), and the
# secant from conj(lambda_osc)
source ~/venv-314/bin/activate
P=/Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter/css_inner_pert.py
cd "$(dirname "$0")"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$P" "$@"; echo "== exit $?"; }
for l in 1.3+2.1j 1.3-2.1j 0.7+6.5j 0.7-6.5j; do run det 0 $l --out=conj_k0.jsonl; done
run root 0 0.536-7.93j --set=A,B --out=conj_k0.jsonl
echo "== done $(date -u '+%Y-%m-%d %H:%M:%S')"
