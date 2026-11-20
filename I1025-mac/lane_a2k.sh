#!/bin/bash
{
# #1025: the u0 0.04 truncation against k_c at fixed D (a2_u0_scan_criteria.log, addendum).
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { local to=$1; shift; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout $to nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
run 600 ell_ddm.py sshres data/sol_l1kc47L1025_D13.5000.npy 13.5 47 2.6288 --us 0.04
run 600 ell_ddm.py sshres data/sol_l1kc47Fr1025_D16.0000.npy 16 47 2.2471293 --us 0.04
run 600 ell_ddm.py sshres data/sol_l1kc63Fm1025_D16.0000.npy 16 63 2.2459628 --us 0.04
run 600 ell_ddm.py sshres data/sol_l1kc63Fw1025_D17.0000.npy 17 63 2.0265465 --us 0.04
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane a2k done"
exit
}
