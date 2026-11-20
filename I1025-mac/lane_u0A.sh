#!/bin/bash
{
# #1025: the u0 test (u0test_criteria.log), lane A.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
run() { local py=$1 to=$2; shift 2; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') u0test.py $*"; RAYON_NUM_THREADS=4 timeout $to nice -n 10 $py -u $R/u0test.py "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
P=/Users/nathan/venv-314/bin/python; Q=/Users/nathan/venv-1025dd/bin/python; O=$R/out
run $P 3600 $O/sol_l1kc55Fb1025_D16.0000.npy 16 55 2.2426280416106374 0.04 f64
run $P 3600 $O/sol_l1kc55Fb1025_D16.0000.npy 16 55 2.2426280416106374 0.02 f64 --signs
run $P 3600 $O/sol_l1kc55Fb1025_D16.0000.npy 16 55 2.2426280416106374 0.03 f64
run $P 3600 $O/sol_l1kc63Fm1025_D16.0000.npy 16 63 2.2459627535552045 0.03 f64
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane u0A done"
exit
}
