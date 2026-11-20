#!/bin/bash
{
# #1025 P1-prime (u0resolve_criteria.log): re-solve at u0 0.02, then the u0-aware signtest. Usage: lane_u0r.sh 55|63
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { local to=$1; shift; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout $to nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
if [ "$1" = 55 ]; then SRC=l1kc55Fb1025; TAG=l1kc55Fh1025; G=2.2426280416106374; else SRC=l1kc63Fm1025; TAG=l1kc63Fh1025; G=2.2459627535552045; fi
run 14400 ell_refine.py $SRC $1 $TAG $1 1 16 $G --kappa 0.7 --u0 0.02 --Ks 30 --tol 1e-12 --wait 60
cat data/$TAG.jsonl
run 3600 $R/signtest.py data/sol_${TAG}_D16.0000.npy 16 $1 around=data/$TAG.jsonl:16:0.02 --u0=0.02 --Ks=30
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane u0r $1 done"
exit
}
