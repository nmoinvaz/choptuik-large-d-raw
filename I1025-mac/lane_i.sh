#!/bin/bash
# #1025 lane I (coordinator: continue k_c 55 to D 20; report the two or three eigenvalues nearest lambda_1 at each D).
# Replaces lane H's lambda lane (made a no-op by data/l1kc55Fr1025_skip.txt). After lane H's k_c 55 bar re-solves:
#   ell_eigs at k_c 47 D 17.5 and k_c 55 D 17.5 (with the state checks), then for D 18, 18.5, .., 20: lambda at k_c 55
#   (ell_refine on the k_c 55 leap's state, tag l1kc55Fs1025 so its D 17, 17.5 points seed the guess) and ell_eigs on
#   the refined state; then ell_eigs at k_c 55 D 17. Stops when a leap state does not appear within 2 h.
# ell_eigs: Beyn circle around lambda_1 with the gauge mode inside (--r 0), N 24, p 12, no real-axis scan, complex
# eigenvalues at Beyn's values (half_diff as their error), real ones polished.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout 14400 nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'LinAlgWarning\|sl.solve\|^  '; echo "== exit ${PIPESTATUS[0]}"; }
EIG="--r 0 --N 24 --p 12 --dlam 0 --no_polish_complex --out data/ell_eigs_1025.jsonl"
OPT="--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12"
t0=$(date +%s)
until grep -q '== exit' $R/refine_kc55_bar.log 2>/dev/null; do
  sleep 60; [ $(( $(date +%s) - t0 )) -gt 14400 ] && { echo "gave up waiting for lane H's bar re-solves"; exit 1; }
done
sleep 90
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane H's bar re-solves done"
lam() { jq -r "select(.D == $2 and .lam != null) | .lam" data/$1.jsonl | tail -1; }
run ell_eigs.py data/sol_l1kc47Fr1025_D17.5000.npy 17.5 47 $(lam l1kc47Fr1025 17.5) $EIG --check
run ell_eigs.py data/sol_l1kc55Fs1025_D17.5000.npy 17.5 55 $(lam l1kc55Fs1025 17.5) $EIG --check
for D in 18 18.5 19 19.5 20; do
  run ell_refine.py l1kc55F1025 55 l1kc55Fs1025 55 1 $D 1.8 $OPT --wait 7200
  L=$(lam l1kc55Fs1025 $D)
  F=data/sol_l1kc55Fs1025_D$(printf '%.4f' $D).npy
  [ -n "$L" ] && [ -f $F ] || { echo "== no k_c 55 state or lambda at D $D: stop"; break; }
  run ell_eigs.py $F $D 55 $L $EIG
done
run ell_eigs.py data/sol_l1kc55Fs1025_D17.0000.npy 17 55 $(lam l1kc55Fs1025 17) $EIG
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane I done"
