#!/bin/bash
{
# #1025 route (c) milestone 4 (dd_signtest_D17.5_criteria.log, written first).
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { local to=$1; shift; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout $to nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
ST=data/sol_l1kc55Fs1025_D17.5000.npy; O=data/ell_ddm_D17.5_1025.jsonl
run 36000 ell_ddm.py det $ST 17.5 55 1.935,1.945,1.9505,1.9515,1.955,1.965 --noise 1e-24,1e-20,1e-16 --out $O
run 21600 ell_ddm.py det $ST 17.5 55 1.9505,1.9515,1.955 --out $O --mutate=hionly
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane dd17 done"
exit
}
