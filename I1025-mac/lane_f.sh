#!/bin/bash
# #1025 lanes F-H (coordinator: k_c 47 to about D 17.5, then k_c 55).
# F: ell_leap --fold at k_c 47 from D 17 to 17.5, h 0.125. The first k_c 47 run (leap_kc47_fold.log) halved h to 1/64 on
#    rounding-floor singular values; ell_leap now watches the smallest regular singular value and |J^+ dF/dn|.
#    Then lane E's lambda at D 17.5, after which lane E is stopped (it would wait 4 h for a D 18 state).
# G: k_c 55 starts at D 17 and 17.5 (ell_refine 47 -> 55), then ell_leap --fold at k_c 55 from D 17.5 to 20.
# H: k_c 55 at D 14.5-16.5 (the k_c bar against 47), then lambda on the k_c 55 leap's half-integer states (D 18-20).
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout 43200 nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered '^{\|^==\|^stop\|^failed\|^fold watch\|^reached\|^gave\|Error\|error'; echo "== exit ${PIPESTATUS[0]}"; }
OPT="--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12"
run ell_leap.py l1kc47F1025 1 47 data/sol_l1kc47F1025_D16.875000.npy 16.875 data/sol_l1kc47F1025_D17.000000.npy 17 17.5 0.125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold > $R/leap_kc47_fold2.log 2>&1
t0=$(date +%s)
until grep -q '"D": 17.5,' $R/lam_kc47_fold.log; do sleep 60; [ $(( $(date +%s) - t0 )) -gt 5400 ] && break; done
pkill -f "ell_refine.py l1kc47F1025 47 l1kc47Fr1025"; sleep 2
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane E stopped"
L17=$(grep '^{' $R/lam_kc47_fold.log | jq -r 'select(.D == 17) | .lam')
( run ell_refine.py l1kc47F1025 47 l1kc55Fs1025 55 1 17,17.5 $L17 $OPT --wait 600 > $R/refine_kc55_start.log 2>&1
  run ell_leap.py l1kc55F1025 1 55 data/sol_l1kc55Fs1025_D17.0000.npy 17 data/sol_l1kc55Fs1025_D17.5000.npy 17.5 20 0.125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold > $R/leap_kc55_fold.log 2>&1 ) &
run ell_refine.py l1kc47F1025 47 l1kc55Fb1025 55 1 14.5,15,15.5,16,16.5 2.49 $OPT --wait 600 > $R/refine_kc55_bar.log 2>&1
t0=$(date +%s)
until [ "$(jq -s '[.[] | select(.lam)] | length' data/l1kc55Fs1025.jsonl 2>/dev/null || echo 0)" -ge 2 ]; do
  sleep 60; [ $(( $(date +%s) - t0 )) -gt 5400 ] && { echo "gave up waiting for the k_c 55 starts"; wait; exit 1; }
done
G18=$(jq -s '[.[] | select(.lam)] | 2 * .[-1].lam - .[-2].lam' data/l1kc55Fs1025.jsonl)
run ell_refine.py l1kc55F1025 55 l1kc55Fr1025 55 1 18,18.5,19,19.5,20 $G18 $OPT --wait 5400 > $R/lam_kc55_fold.log 2>&1
wait
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lanes F-H done"
