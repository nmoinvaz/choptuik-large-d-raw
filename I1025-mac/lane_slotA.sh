#!/bin/bash
{
# #1025 slot A after the k_c 63 scan (lane_p1d.sh): T2's feasibility checks (u0resolve_criteria.log, T2 addendum). The re-solve waits for
# their reading.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
until grep -q 'lane p1d done' $R/lane_p1d.log; do sleep 30; done
cd $M
run() { local to=$1; shift; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout $to nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -vE 'Warning|sl.solve'; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
ST=data/sol_l1kc55Fb1025_D16.0000.npy; L=2.2440428096
run 1800 ell_ddm.py sshres $ST 16 55 $L --us 0.04 --Ks 30
run 1800 ell_ddm.py sshres $ST 16 55 $L --us 0.04 --Ks 45
run 3600 ell_ddm.py check $ST 16 55 $L --blocks 12 --Ks 30 --bar 1
run 3600 ell_ddm.py check $ST 16 55 $L --blocks 12 --Ks 45 --bar 1
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane slotA (T2 feasibility) done"
exit
}
