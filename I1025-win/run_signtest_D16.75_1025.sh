#!/bin/bash
# #1025 (win): when the k_c 63 record at D 16.75 lands (data/l1kc63Fv1025.jsonl), the coordinator's record check (n_signchanges 1, 2% test against the k_c 47 value 2.1096347;
# log $LOGS/check_D16.75_1025.log), then xfkappa's signtest (hash a2f53a90 checked) at lam -+ 0.02 on the k_c 63 state at D 16.75, 4 BLAS threads, timeout 7200, appended to $LOGS/signtest.log.
set -u
: "${PY:?set PY}" "${LOGS:?set LOGS}"
cd "$(dirname "$0")/solver/matter"
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
h=$(git hash-object $LOGS/signtest.py)
case $h in a2f53a90*) ;; *) echo "== $(date -u '+%Y-%m-%d %H:%M:%S') signtest.py hash $h does not start a2f53a90, stopping" >> $LOGS/signtest.log; exit 3;; esac
until grep -Eq '"D": 16.75,.*"lam": [0-9]' data/l1kc63Fv1025.jsonl 2>/dev/null; do
  if grep -Eq '^== exit' $LOGS/kc63_D16.75.log 2>/dev/null; then echo "== $(date -u '+%Y-%m-%d %H:%M:%S') kc63_D16.75.log ended without a record, no signtest" >> $LOGS/signtest.log; exit 4; fi
  sleep 60
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') record landed: check_1025.py data/l1kc63Fv1025.jsonl 16.75 --rule pct --ref 2.1096347" >> $LOGS/check_D16.75_1025.log
"$PY" ../../check_1025.py data/l1kc63Fv1025.jsonl 16.75 --rule pct --ref 2.1096347 >> $LOGS/check_D16.75_1025.log 2>&1
echo "== exit $? $(date -u '+%Y-%m-%d %H:%M:%S')" >> $LOGS/check_D16.75_1025.log
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') signtest.py data/sol_l1kc63Fv1025_D16.7500.npy 16.75 63 around=data/l1kc63Fv1025.jsonl:16.75:0.02" >> $LOGS/signtest.log
timeout 7200 "$PY" -u $LOGS/signtest.py data/sol_l1kc63Fv1025_D16.7500.npy 16.75 63 around=data/l1kc63Fv1025.jsonl:16.75:0.02 >> $LOGS/signtest.log 2>&1
echo "== exit $? $(date -u '+%Y-%m-%d %H:%M:%S')" >> $LOGS/signtest.log
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') D 16.75 signtest done" >> $LOGS/signtest.log
