#!/bin/bash
# I660 queue 1: (1) the k_c 23 march from D = 9 to 10 with t31_super.log's command; (2) ell_refine at D = 10,
# k_c 23 -> 23 (lambda by the same root finder) and 23 -> 31 (Delta, lambda, psi-constraint, |dDelta/dF|).
source ~/venv-314/bin/activate
M=/Users/nathan/Source/choptuik-large-d-xf-660/solver/matter
cd $M
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$@"; echo "== exit $?"; }
run ell_march.py l1kc23hi660 1 23 data/sol_l1_kc23r_D9.0000.npy 9 10 10 --dinit 0.05 --dmax 0.1 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-10
run ell_refine.py l1kc23hi660 23 l1kc23r660 23 1 10 2.915 --kappa 0.7 --u0 0.04 --Ks 30
run ell_refine.py l1kc23hi660 23 l1kc31r660 31 1 10 2.915 --kappa 0.7 --u0 0.04 --Ks 30
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') done"
