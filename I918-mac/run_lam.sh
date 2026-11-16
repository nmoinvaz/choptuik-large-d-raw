#!/bin/bash
# #918: mode_lam.py on states, each behind the load gate when GATE is set (--gate; the gate of 31 was dropped on 2026-11-16 16:50 UTC, #918). Usage: run_lam.sh <name> <guess> <extra args or ""> <state file name> ...
J=$(cd "$(dirname "$0")" && pwd)
NAME=$1; GUESS=$2; EXTRA=$3; shift 3
ST=()
for s in "$@"; do ST+=("$J/states/$s"); done
export PYTHONPATH=$J/site VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
nice -n 10 python3 matter/sigma_ms/mode_lam.py "${ST[@]}" --out "$J/out" --guess "$GUESS" \
    --threads 2 --gate ${GATE:-0} $EXTRA > "$J/out/lam_$NAME.txt" 2>&1
rc=$?
echo "$(date -u '+%F %T') UTC lam_$NAME exit $rc" >> "$J/out/gate.log"
exit $rc
