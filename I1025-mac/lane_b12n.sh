#!/bin/bash
{
# #1025 route (c): A2 at D 17.5 and the block-12 noise scan (dd_b12_noise_criteria.log).
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { local to=$1; shift; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout $to nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
ST=data/sol_l1kc55Fs1025_D17.5000.npy; O=data/ell_ddm_checks_1025.jsonl
run 3600 ell_ddm.py sshres $ST 17.5 55 1.93 --us 0.01,0.005 --bar 1e-24 --out $O
run 3600 ell_ddm.py sshres $ST 17.5 55 1.93 --us 0.01,0.005 --bar 1e-24 --out $O --mutate=lam
run 3600 ell_ddm.py sshres $ST 17.5 55 1.93 --us 0.04 --bar 1e-24
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') dd_b12_noise.py 1.92,1.935,1.9505,1.955"
RAYON_NUM_THREADS=4 timeout 7200 nice -n 10 /Users/nathan/venv-1025dd/bin/python -u $R/dd_b12_noise.py 1.92,1.935,1.9505,1.955 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'
echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane b12n done"
exit
}
