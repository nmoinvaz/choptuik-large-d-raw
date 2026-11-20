#!/bin/bash
# #1025 (win), the coordinator's two jobs for the free cores, in order, 4 BLAS threads each, BelowNormal (hc 2026-11-20 ~07:20 UTC):
# (1) signtest of the k_c 63 D 17 record (xfkappa's I1025-mac/signtest.py, hash a2f53a90 checked), timeout 7200, appended to $LOGS/signtest.log
# (2) k_c 71 lambda at D 16.5 from the k_c 63 D 16.5 state, 12 h timeout, log $LOGS/kc71_D16.5.log (records in data/l1kc71Fw1025.jsonl)
set -u
: "${PY:?set PY}" "${LOGS:?set LOGS}"
cd "$(dirname "$0")/solver/matter"
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
h=$(git hash-object $LOGS/signtest.py)
case $h in a2f53a90*) ;; *) echo "== $(date -u '+%Y-%m-%d %H:%M:%S') signtest.py hash $h does not start a2f53a90, stopping" >> $LOGS/signtest.log; exit 3;; esac
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') signtest.py data/sol_l1kc63Fw1025_D17.0000.npy 17 63 around=data/l1kc63Fw1025.jsonl:17:0.02" >> $LOGS/signtest.log
timeout 7200 "$PY" -u $LOGS/signtest.py data/sol_l1kc63Fw1025_D17.0000.npy 17 63 around=data/l1kc63Fw1025.jsonl:17:0.02 >> $LOGS/signtest.log 2>&1
echo "== exit $? $(date -u '+%Y-%m-%d %H:%M:%S')" >> $LOGS/signtest.log
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') ell_refine.py l1kc63Fw1025b 63 l1kc71Fw1025 71 1 16.5 2.1454677 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60" >> $LOGS/kc71_D16.5.log
timeout 43200 "$PY" -u ell_refine.py l1kc63Fw1025b 63 l1kc71Fw1025 71 1 16.5 2.1454677 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 >> $LOGS/kc71_D16.5.log 2>&1
echo "== exit $? $(date -u '+%Y-%m-%d %H:%M:%S')" >> $LOGS/kc71_D16.5.log
