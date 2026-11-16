#!/bin/bash
# #918: mode_check.py on one state behind the gate. Usage: run_check.sh <state file name> <name> [mode_check.py arguments]
J=$(cd "$(dirname "$0")" && pwd)
ST=$1; NAME=$2; shift 2
export PYTHONPATH=$J/site VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
bash "$J/gate.sh" ${GATE:-100000} "$J/out/gate.log" nice -n 10 python3 matter/sigma_ms/mode_check.py \
    "$J/states/$ST" --threads 2 --out "$J/out/check_$NAME.json" "$@" > "$J/out/check_$NAME.txt" 2>&1
rc=$?
echo "$(date -u '+%F %T') UTC check_$NAME exit $rc" >> "$J/out/gate.log"
exit $rc
