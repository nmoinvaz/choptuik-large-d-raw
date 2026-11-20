#!/bin/bash
# #1025 lane J (coordinator 2026-11-20 03:00-03:25 UTC). Lane I2 was stopped at 03:20 UTC after its D 18 refine began:
# its eigenvalue scans are invalid (eigs_control.log, eigs_planted_ill_before.log). Two sub-lanes, one process each:
#   J-a: lambda at k_c 55 on the k_c 55 leap's states at D 18.5, 19, 19.5 (tag l1kc55Fs1025, as lane I2), after lane I2's
#        D 18 refine (python pid 79132) ends; a D whose state is missing once the leap has ended stops it.
#   J-b: after the k_c 55 leap ends: lambda at k_c 63 at D 16.5 from the k_c 55 bar state (the direct test,
#        kink_criteria.log), then at k_c 55 at D 16.75 and 16.25 from the k_c 47 leap's states, then at k_c 47 there.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout 14400 nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'LinAlgWarning\|sl.solve\|^  '; echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"; }
OPT="--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12"
leap_done() { grep -q '^== exit' $R/leap_kc55_fold.log; }
( while kill -0 79132 2>/dev/null; do sleep 60; done
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane I2's D 18 refine ended"
  for D in 18.5 19 19.5; do
    F=data/sol_l1kc55F1025_D$(printf '%.4f' $D).npy
    until [ -f $F ] || leap_done; do sleep 60; done
    [ -f $F ] || { echo "== no k_c 55 leap state at D $D and the leap has ended: J-a stops"; break; }
    run ell_refine.py l1kc55F1025 55 l1kc55Fs1025 55 1 $D 1.8 $OPT --wait 600
  done
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') J-a done" ) > $R/lane_j_a.log 2>&1 &
( until leap_done; do sleep 60; done
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') the k_c 55 leap ended"
  cp data/sol_l1kc47F1025_D16.750000.npy data/sol_l1kc47Fx1025_D16.7500.npy
  cp data/sol_l1kc47F1025_D16.250000.npy data/sol_l1kc47Fx1025_D16.2500.npy
  run ell_refine.py l1kc55Fb1025 55 l1kc63Fb1025 63 1 16.5 2.159124821824751 $OPT --wait 60
  run ell_refine.py l1kc47Fx1025 47 l1kc55Fq1025 55 1 16.75 2.0928 $OPT --wait 60
  run ell_refine.py l1kc47Fx1025 47 l1kc55Fp1025 55 1 16.25 2.2009 $OPT --wait 60
  run ell_refine.py l1kc47Fx1025 47 l1kc47Fq1025 47 1 16.75 2.0928 $OPT --wait 60
  run ell_refine.py l1kc47Fx1025 47 l1kc47Fp1025 47 1 16.25 2.2009 $OPT --wait 60
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') J-b done" ) > $R/lane_j_b.log 2>&1 &
wait
