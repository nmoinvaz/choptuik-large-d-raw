#!/bin/bash
# #1025 refine lane B: the k_c 31 secant states at D 12.5-14 re-solved at k_c 39 (Delta, constraint and lambda), tol 1e-12
cd /Users/nathan/Source/choptuik-1025/solver/matter
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout 7200 nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v "Warning\|slogdet"; echo "== exit ${PIPESTATUS[0]}"; }
run ell_refine.py l1kc31L1025 31 l1kc39L1025 39 1 12.5,13,13.5,14 2.75 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane B done"
