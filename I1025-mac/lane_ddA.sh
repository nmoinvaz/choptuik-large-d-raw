#!/bin/bash
{
# #1025 route (c) checks A and B at D 13 (dd_checkAB_criteria.log, written first). Takes the second free slot: after lane dd has started
# in the first, it waits for lane T's other lane or lane dd to end.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { local to=$1; shift; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout $to nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
until grep -q 'a lane T slot is free' $R/lane_dd.log; do sleep 60; done
until { grep -q 'T-a done' $R/lane_t_a.log && grep -q 'T-b2 done' $R/lane_t_b2.log; } || grep -q 'lane dd done' $R/lane_dd.log; do sleep 60; done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') a second slot is free"
ST=data/sol_l1kc31L1025_D13.0000.npy; L1=2.6841484641099442
O=data/ell_ddm_checks_1025.jsonl
run 7200 ell_ddm.py check $ST 13 31 $L1 --bar 1e-13 --out $O
run 7200 ell_ddm.py check $ST 13 31 $L1 --bar 1e-13 --out $O --blocks 1,6,11 --mutate=lam
run 3600 ell_ddm.py sshres $ST 13 31 $L1 --us 0.01,0.005 --bar 1e-24 --out $O
run 3600 ell_ddm.py sshres $ST 13 31 $L1 --us 0.01,0.005 --bar 1e-24 --out $O --mutate=lam
run 7200 ell_ddm.py det $ST 13 31 2.6641484641099442,2.7041484641099442 --out $O
run 7200 ell_ddm.py det $ST 13 31 2.6641484641099442,2.7041484641099442 --out $O --mutate=lam
run 14400 ell_ddm.py root $ST 13 31 2.6641484641099442 2.7041484641099442 --record $L1 --bar 1e-7 --out $O
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane ddA done"
exit
}
