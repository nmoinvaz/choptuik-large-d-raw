#!/bin/bash
# I811 queue 1: lambda at D = 4 from the stored k_c 39 state, tol 1e-13: k_c 39 and 47 on ELL.md's stated settings
# (kappa 0.7, u0 0.04, Ks 30), then k_c 47 on the row's own settings (kappa 0.5, u0 0.01, Ks 16) as the diagnostic.
source ~/venv-314/bin/activate
M=/Users/nathan/Source/choptuik-large-d-xf-811/solver/matter
cd $M
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$@"; echo "== exit $?"; }
run ell_refine.py l1_D4_kc39 39 l1kc39d4st811 39 1 4 8.41 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-13
run ell_refine.py l1_D4_kc39 39 l1kc47d4st811 47 1 4 8.41 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-13
run ell_refine.py l1_D4_kc39 39 l1kc47d4ow811 47 1 4 8.41 --kappa 0.5 --u0 0.01 --Ks 16 --tol 1e-13
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') queue done"
