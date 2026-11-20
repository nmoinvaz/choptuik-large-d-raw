#!/bin/bash
# #1025 (win): the coordinator's signtests (xfkappa's I1025-mac/signtest.py, hash a2f53a90 checked) of the two k_c 63 records, one at a time, each when its record is in:
# D 17.5 (data/l1kc63Fw1025.jsonl) and D 16.5 (data/l1kc63Fw1025b.jsonl). 4 BLAS threads, timeout 7200 each, output appended to $LOGS/signtest.log.
set -u
: "${PY:?set PY}" "${LOGS:?set LOGS}"
cd "$(dirname "$0")/solver/matter"
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
h=$(git hash-object $LOGS/signtest.py)
case $h in a2f53a90*) ;; *) echo "== $(date -u '+%Y-%m-%d %H:%M:%S') signtest.py hash $h does not start a2f53a90, stopping" >> $LOGS/signtest.log; exit 3;; esac
have() { grep -Eq "\"D\": $2,.*\"lam\": [0-9]" "$1" 2>/dev/null; }
run() {  # state D rec
  echo "== $(date -u '+%Y-%m-%d %H:%M:%S') signtest.py $1 $2 63 around=$3:$2:0.02" >> $LOGS/signtest.log
  timeout 7200 "$PY" -u $LOGS/signtest.py $1 $2 63 around=$3:$2:0.02 >> $LOGS/signtest.log 2>&1
  echo "== exit $? $(date -u '+%Y-%m-%d %H:%M:%S')" >> $LOGS/signtest.log; }
d175=0; d165=0
while [ $d175 = 0 ] || [ $d165 = 0 ]; do
  if [ $d175 = 0 ] && have data/l1kc63Fw1025.jsonl 17.5; then run data/sol_l1kc63Fw1025_D17.5000.npy 17.5 data/l1kc63Fw1025.jsonl; d175=1; continue; fi
  if [ $d165 = 0 ] && have data/l1kc63Fw1025b.jsonl 16.5; then run data/sol_l1kc63Fw1025b_D16.5000.npy 16.5 data/l1kc63Fw1025b.jsonl; d165=1; continue; fi
  sleep 60
done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') both signtests done" >> $LOGS/signtest.log
