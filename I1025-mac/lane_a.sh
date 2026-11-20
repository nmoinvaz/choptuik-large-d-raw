#!/bin/bash
# #1025 test (a): the lift's root shift against the reference's distance (lift_offset_prediction.log, written first).
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout 7200 nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve\|^  '; echo "== exit ${PIPESTATUS[0]} $(date -u '+%Y-%m-%d %H:%M:%S')"; }
L=2.025718689014619
run ell_lam.py data/sol_l1kc55Fs1025_D17.0000.npy 17 55 $L --refs 2.015718689014619,2.035718689014619 --record $L --all_roots --out data/ell_lam_offset_1025.jsonl
run ell_lam.py data/sol_l1kc55Fs1025_D17.0000.npy 17 55 $L --refs 2.024718689014619,2.026718689014619 --record $L --all_roots --out data/ell_lam_offset_1025.jsonl
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane (a) done"
