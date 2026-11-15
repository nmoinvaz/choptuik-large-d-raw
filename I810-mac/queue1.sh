#!/bin/bash
# I810 queue 1: ell_refine from the table's k_c 23 states at D = 7, 8, 9 (kappa 0.7, u0 0.04, Ks 30, tol 1e-13):
# k_c 23 -> 23, 23 -> 31, 23 -> 39, each with Delta, lambda, |F|, |dDelta/dF| and the psi-constraint.
source ~/venv-314/bin/activate
M=/Users/nathan/Source/choptuik-large-d-xf-810/solver/matter
cd $M
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$@"; echo "== exit $?"; }
for kc in 23 31 39; do
  run ell_refine.py l1_kc23r 23 l1kc${kc}s810 $kc 1 7,8,9 3.381 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-13
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') queue done"
