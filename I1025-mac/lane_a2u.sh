#!/bin/bash
{
# #1025: the horizon series' truncation at u0 0.04 against D (a2_u0_scan_criteria.log).
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { local to=$1; shift; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout $to nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
run 600 ell_ddm.py sshres data/sol_l1kc31L1025_D13.0000.npy 13 31 2.6841484641 --us 0.04
for p in "14.5 2.4964" "15 2.4210058" "15.5 2.3387882" "16 2.2459628" "16.5 2.1454677"; do set -- $p
  run 600 ell_ddm.py sshres data/sol_l1kc55Fb1025_D$(printf '%.4f' $1).npy $1 55 $2 --us 0.04; done
run 600 ell_ddm.py sshres data/sol_l1kc55Fs1025_D17.0000.npy 17 55 2.0257 --us 0.04
run 600 ell_ddm.py sshres data/sol_l1kc55Fs1025_D18.0000.npy 18 55 1.85 --us 0.04
run 600 ell_ddm.py sshres data/sol_l1kc55F1025_D19.000000.npy 19 55 1.70 --us 0.04
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane a2u done"
exit
}
