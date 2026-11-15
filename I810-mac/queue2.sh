#!/bin/bash
# I810 queue 2 (the extension to D = 4 and 5; each row's own settings kappa 0.5, u0 0.01, Ks 16; tol 1e-13):
# D = 5: k_c 23 -> 23, 31, 39 from the row's state; D = 4: lambda at k_c 23, 31, 39 from the stored states at each k_c.
source ~/venv-314/bin/activate
M=/Users/nathan/Source/choptuik-large-d-xf-810/solver/matter
cd $M
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; nice -n 10 python "$@"; echo "== exit $?"; }
for kc in 23 31 39; do
  run ell_refine.py l1_kc23r 23 l1kc${kc}d5s810 $kc 1 5 4.64 --kappa 0.5 --u0 0.01 --Ks 16 --tol 1e-13
done
for kc in 23 31 39; do
  run ell_refine.py l1_D4_kc$kc $kc l1kc${kc}d4s810 $kc 1 4 8.41 --kappa 0.5 --u0 0.01 --Ks 16 --tol 1e-13
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') queue done"
