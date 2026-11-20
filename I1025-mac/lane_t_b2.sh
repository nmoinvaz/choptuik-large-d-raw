#!/bin/bash
{
# #1025 lane T-b again (lane_t_prediction.log), after the gesvd fallback (svd_fallback_check.log): lambda at k_c 63 at D 16, then signtest.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { local to=$1; shift; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout $to nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve\|^  '; echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"; }
OPT="--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60"
run 28800 ell_refine.py l1kc55Fb1025 55 l1kc63Fm1025 63 1 16 2.2426280416106374 $OPT
[ -f data/l1kc63Fm1025.jsonl ] && run 7200 $R/signtest.py data/sol_l1kc63Fm1025_D16.0000.npy 16 63 around=data/l1kc63Fm1025.jsonl:16:0.02
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') T-b2 done"
exit
}
