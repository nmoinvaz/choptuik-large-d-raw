#!/bin/bash
# I660 queue 2 (diagnostics, after the bar failed): the k_c 31 solve stopped at |F| 4.4e-12, where |dDelta/dF| |F| =
# 6.2e-6 exceeds the k_c 23 -> 31 change of Delta (2.5e-6), so the comparison could not separate truncation from the
# residual. Re-solve k_c 23, 31 and 39 at D = 10 from the same k_c 23 state with tol 1e-13.
source ~/venv-314/bin/activate
M=/Users/nathan/Source/choptuik-large-d-xf-660/solver/matter
cd $M
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$@"; echo "== exit $?"; }
for kc in 23 31 39; do
  run ell_refine.py l1kc23hi660 23 l1kc${kc}t660 $kc 1 10 2.915 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-13
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') queue done"
