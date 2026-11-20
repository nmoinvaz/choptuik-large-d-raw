#!/bin/bash
# #1025 lane K: lambda_1 with M's rounding floor lifted (ell_lam.py), against lift_criteria.log (written first).
#   K-a, now: C1 at k_c 55 D 17; C2 at k_c 55 D 17.5 and D 18 (with scans).
#   K-b, after the k_c 55 leap ends: C1 at k_c 55 D 16.5 and k_c 63 D 17 (winb's state, raw I1025-win/out); then lane J-b's
#        items with the lift: k_c 55 states at D 16.75, 16.25 from the k_c 47 leap's (ell_refine --no-gamma), and lambda_1
#        at k_c 55 and 47 there.
# Refs: guess -/+ 0.1. One process per sub-lane, nice 10, each under a 4 h timeout.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout 14400 nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve\|^  '; echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"; }
lam() { run ell_lam.py "$1" "$2" "$3" "$4" --refs $(python3 -c "print(f'{$4 - 0.1!r},{$4 + 0.1!r}')") "${@:5}"; }
OPT="--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12"
leap_done() { grep -q '^== exit' $R/leap_kc55_fold.log; }
( lam data/sol_l1kc55Fs1025_D17.0000.npy 17 55 2.025718689014619 --record 2.025718689014619
  lam data/sol_l1kc55Fs1025_D17.5000.npy 17.5 55 1.92 --record 1.9522284485089008 --scan 1.70:2.15:0.05
  lam data/sol_l1kc55Fs1025_D18.0000.npy 18 55 1.80 --record 1.7661884817808553 --scan 1.55:2.10:0.05
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') K-a done" ) > $R/lane_k_a.log 2>&1 &
( until leap_done; do sleep 60; done
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') the k_c 55 leap ended"
  lam data/sol_l1kc55Fb1025_D16.5000.npy 16.5 55 2.159124821824751 --record 2.159124821824751
  lam data/sol_l1kc63Fw1025_D17.0000.npy 17 63 2.026546497375959 --record 2.026546497375959
  cp data/sol_l1kc47F1025_D16.750000.npy data/sol_l1kc47Fx1025_D16.7500.npy
  cp data/sol_l1kc47F1025_D16.250000.npy data/sol_l1kc47Fx1025_D16.2500.npy
  run ell_refine.py l1kc47Fx1025 47 l1kc55Fq1025 55 1 16.75 2.0928 $OPT --wait 60 --no-gamma
  run ell_refine.py l1kc47Fx1025 47 l1kc55Fp1025 55 1 16.25 2.2009 $OPT --wait 60 --no-gamma
  lam data/sol_l1kc55Fq1025_D16.7500.npy 16.75 55 2.0928
  lam data/sol_l1kc55Fp1025_D16.2500.npy 16.25 55 2.2009
  lam data/sol_l1kc47Fx1025_D16.7500.npy 16.75 47 2.0928
  lam data/sol_l1kc47Fx1025_D16.2500.npy 16.25 47 2.2009
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') K-b done" ) > $R/lane_k_b.log 2>&1 &
wait
