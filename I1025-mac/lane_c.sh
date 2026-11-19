#!/bin/bash
# #1025 lane C: (1) lambda at k_c 31 on the secant states D 13, 14 (k_c 31 -> 39 change of lambda there); (2) D 13.5, 14 at
# k_c 47 from the k_c 39 states; (3) the k_c 47 secant pilot from D 14 to 15, steps 0.25, psi-constraint bar 1e-2
cd /Users/nathan/Source/choptuik-1025/solver/matter
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout 10800 nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v "Warning\|slogdet\|qx = \|pc = "; echo "== exit ${PIPESTATUS[0]}"; }
run ell_refine.py l1kc31L1025 31 l1kc31Lr1025 31 1 13,14 2.68 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12
run ell_refine.py l1kc39L1025 39 l1kc47L1025 47 1 13.5,14 2.63 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12
run ell_leap.py l1kc47L1025p 1 47 data/sol_l1kc47L1025_D13.5000.npy 13.5 data/sol_l1kc47L1025_D14.0000.npy 14 15 0.25 --tol 1e-12 --cmax 1e-2
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane C done"
