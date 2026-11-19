#!/bin/bash
# #1025 lanes D and E (coordinator: D 15 to 20 at k_c 47, watching for a fold). Waits for lane C's k_c 47 states at D 13.5
# and 14, stops lane C before its pilot, then runs D: ell_leap --fold at k_c 47 from D 14 to 20 (h 0.25, |F| bar 1e-8,
# psi-constraint bar 1e-2), and E: lambda at k_c 47 on its half-integer states as they appear (ell_refine 47 -> 47).
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
t0=$(date +%s)
until [ "$(wc -l < data/l1kc47L1025.jsonl 2>/dev/null || echo 0)" -ge 2 ]; do
  sleep 30; [ $(( $(date +%s) - t0 )) -gt 10800 ] && { echo "gave up waiting for lane C"; exit 1; }
done
pkill -f "lane_c.sh"; pkill -f "ell_leap.py l1kc47L1025p"; sleep 2
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane C stopped after its k_c 47 states"
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout 43200 nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered '^{\|^==\|^stop\|^failed\|^the fold\|^reached\|^gave\|Error\|error'; echo "== exit ${PIPESTATUS[0]}"; }
run ell_leap.py l1kc47F1025 1 47 data/sol_l1kc47L1025_D13.5000.npy 13.5 data/sol_l1kc47L1025_D14.0000.npy 14 20 0.25 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold > $R/leap_kc47_fold.log 2>&1 &
sleep 60
run ell_refine.py l1kc47F1025 47 l1kc47Fr1025 47 1 14.5,15,15.5,16,16.5,17,17.5,18,18.5,19,19.5,20 2.49 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 14400 > $R/lam_kc47_fold.log 2>&1
wait
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lanes D, E done"
