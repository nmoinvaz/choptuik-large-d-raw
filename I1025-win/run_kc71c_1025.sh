#!/bin/bash
# #1025 (win), the coordinator's two checks of the k_c 71 D 16.5 record (hc 2026-11-20 ~10:25 UTC), in order, 4 BLAS threads, BelowNormal:
# (1) signtest of that record at lam -+ 0.002 (hash a2f53a90 checked), appended to $LOGS/signtest.log
# (2) lambda search on the saved k_c 71 state from another guess, 2.1408016, new tag l1kc71Fw1025c (12 h timeout, log $LOGS/kc71c_D16.5.log); then check_1025.py on its record
#     (edge rule, ref 2.1454677; log $LOGS/check_D16.5_kc71c_1025.log) and a signtest at lam -+ 0.02 on its own state (its own checks)
set -u
: "${PY:?set PY}" "${LOGS:?set LOGS}"
cd "$(dirname "$0")/solver/matter"
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
h=$(git hash-object $LOGS/signtest.py)
case $h in a2f53a90*) ;; *) echo "== $(date -u '+%Y-%m-%d %H:%M:%S') signtest.py hash $h does not start a2f53a90, stopping" >> $LOGS/signtest.log; exit 3;; esac
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') signtest.py data/sol_l1kc71Fw1025_D16.5000.npy 16.5 71 around=data/l1kc71Fw1025.jsonl:16.5:0.002" >> $LOGS/signtest.log
timeout 7200 "$PY" -u $LOGS/signtest.py data/sol_l1kc71Fw1025_D16.5000.npy 16.5 71 around=data/l1kc71Fw1025.jsonl:16.5:0.002 >> $LOGS/signtest.log 2>&1
echo "== exit $? $(date -u '+%Y-%m-%d %H:%M:%S')" >> $LOGS/signtest.log
L=$LOGS/kc71c_D16.5.log
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') ell_refine.py l1kc71Fw1025 71 l1kc71Fw1025c 71 1 16.5 2.1408016 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60" >> $L
timeout 43200 "$PY" -u ell_refine.py l1kc71Fw1025 71 l1kc71Fw1025c 71 1 16.5 2.1408016 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 >> $L 2>&1
echo "== exit $? $(date -u '+%Y-%m-%d %H:%M:%S')" >> $L
if grep -Eq '"D": 16.5,.*"lam": [0-9]' data/l1kc71Fw1025c.jsonl 2>/dev/null; then
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') record landed: check_1025.py data/l1kc71Fw1025c.jsonl 16.5 --rule edge --ref 2.1454677" >> $LOGS/check_D16.5_kc71c_1025.log
  "$PY" ../../check_1025.py data/l1kc71Fw1025c.jsonl 16.5 --rule edge --ref 2.1454677 >> $LOGS/check_D16.5_kc71c_1025.log 2>&1
  echo "== exit $? $(date -u '+%Y-%m-%d %H:%M:%S')" >> $LOGS/check_D16.5_kc71c_1025.log
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') signtest.py data/sol_l1kc71Fw1025c_D16.5000.npy 16.5 71 around=data/l1kc71Fw1025c.jsonl:16.5:0.02" >> $LOGS/signtest.log
  timeout 7200 "$PY" -u $LOGS/signtest.py data/sol_l1kc71Fw1025c_D16.5000.npy 16.5 71 around=data/l1kc71Fw1025c.jsonl:16.5:0.02 >> $LOGS/signtest.log 2>&1
  echo "== exit $? $(date -u '+%Y-%m-%d %H:%M:%S')" >> $LOGS/signtest.log
else
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') no record in data/l1kc71Fw1025c.jsonl, no check or signtest" >> $LOGS/check_D16.5_kc71c_1025.log
fi
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') kc71c driver done" >> $LOGS/signtest.log
