#!/bin/bash
# #1025 (win), the coordinator's job (hc 2026-11-20 ~09:07 UTC): k_c 63 lambda at D 16.75 from win2b's k_c 55 state (its lambda there failed its checks, the state solve does not use lambda).
# State and record by git show from origin/main of the push worktree (no checkout), git hash-object logged; 4 BLAS threads, 12 h timeout. Guess = the k_c 47 value 2.1096347.
set -u
: "${PY:?set PY}" "${LOGS:?set LOGS}" "${RAW:?set RAW}"
cd "$(dirname "$0")/solver/matter"
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
L=$LOGS/kc63_D16.75.log
git -C $RAW fetch -q origin
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') origin/main $(git -C $RAW rev-parse origin/main)" >> $L
for f in sol_l1kc55Fv1025_D16.7500.npy l1kc55Fv1025.jsonl; do
  if [ -e data/$f ]; then echo "== data/$f exists, stopping" >> $L; exit 3; fi
  git -C $RAW show origin/main:I1025-win2b/out/$f > data/$f
  echo "== git hash-object data/$f $(git hash-object data/$f)  (git's blob id of I1025-win2b/out/$f at origin/main: $(git -C $RAW rev-parse origin/main:I1025-win2b/out/$f)), $(wc -c < data/$f) bytes" >> $L
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') ell_refine.py l1kc55Fv1025 55 l1kc63Fv1025 63 1 16.75 2.1096347 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60" >> $L
timeout 43200 "$PY" -u ell_refine.py l1kc55Fv1025 55 l1kc63Fv1025 63 1 16.75 2.1096347 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 >> $L 2>&1
echo "== exit $? $(date -u '+%Y-%m-%d %H:%M:%S')" >> $L
