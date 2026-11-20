#!/bin/bash
{
# #1025 lane S: the SVD track (svdtrack_criteria.log, written first), then lambda at k_c 47 at D 16.75 and 16.25 (plain ell_refine,
# valid below D 17; the 47 -> 55 spread beside win2b's k_c 55 values). Starts when lane (a)'s second run (python 78768) ends.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout 7200 nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve\|^  warn'; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
while kill -0 78768 2>/dev/null; do sleep 30; done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane (a) ended"
L13=2.6841484641099442
run $R/svdtrack.py data/sol_l1kc31L1025_D13.0000.npy 13 31 $L13; c1=$?
run $R/svdtrack.py data/sol_l1kc31L1025_D13.0000.npy 13 31 $L13 --mutate=shift; c2=$?
if [ $c1 -eq 0 ] && [ $c2 -eq 3 ]; then
  echo "== controls read as they must (regular; mutation not regular)"
  run $R/svdtrack.py data/sol_l1kc55Fs1025_D17.0000.npy 17 55 2.025718689014619 --extra 0.0124,0.0144,0.0164
else
  echo "== CONTROL MISREAD (exit $c1, mutation exit $c2): the D 17 track does not run"
fi
OPT="--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12"
cp data/sol_l1kc47F1025_D16.750000.npy data/sol_l1kc47Fx1025_D16.7500.npy
cp data/sol_l1kc47F1025_D16.250000.npy data/sol_l1kc47Fx1025_D16.2500.npy
run ell_refine.py l1kc47Fx1025 47 l1kc47Fq1025 47 1 16.75 2.0928 $OPT --wait 60
run ell_refine.py l1kc47Fx1025 47 l1kc47Fp1025 47 1 16.25 2.2009 $OPT --wait 60
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane S done"
exit
}
