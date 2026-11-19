#!/bin/bash
# #1025 refine lane A: D 10.5-12, k_c 31 from the k_c 23 march, then 39 from 31, then 47 from 39 (tol 1e-13)
cd /Users/nathan/Source/choptuik-1025/solver/matter
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout 7200 nice -n 10 /Users/nathan/venv-314/bin/python "$@" 2>&1 | grep -v "Warning\|slogdet"; echo "== exit ${PIPESTATUS[0]}"; }
DS=10.5,11,11.5,12
run ell_refine.py l1kc23m1025 23 l1kc31r1025 31 1 $DS 2.85 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-13
run ell_refine.py l1kc31r1025 31 l1kc39r1025 39 1 $DS 2.85 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-13
run ell_refine.py l1kc39r1025 39 l1kc47r1025 47 1 $DS 2.85 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-13
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane A done"
