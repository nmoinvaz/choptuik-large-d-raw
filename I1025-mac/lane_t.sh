#!/bin/bash
{
# #1025 lane T (lane_t_prediction.log, written first): T-a lambda at k_c 71 at D 17; T-b lambda at k_c 63 at D 16; each with its signtest.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { local to=$1; shift; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout $to nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve\|^  '; echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"; }
OPT="--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60"
( run 43200 ell_refine.py l1kc63Fw1025 63 l1kc71Fm1025 71 1 17 2.026546497375959 $OPT
  run 7200 $R/signtest.py data/sol_l1kc71Fm1025_D17.0000.npy 17 71 around=data/l1kc71Fm1025.jsonl:17:0.02
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') T-a done" ) > $R/lane_t_a.log 2>&1 &
( run 28800 ell_refine.py l1kc55Fb1025 55 l1kc63Fm1025 63 1 16 2.2426280416106374 $OPT
  run 7200 $R/signtest.py data/sol_l1kc63Fm1025_D16.0000.npy 16 63 around=data/l1kc63Fm1025.jsonl:16:0.02
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') T-b done" ) > $R/lane_t_b.log 2>&1 &
wait
exit
}
