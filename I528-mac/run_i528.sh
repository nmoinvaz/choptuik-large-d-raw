#!/bin/bash
# I528-mac: hp/reduced_cubic.py, the plant with its three mutations, then the two D 242.5146 starts (REF first).
# Run from the checkout's hp/ as: bash run_i528.sh RAW OUT [planted|ref|acc|all]
# RAW is a clone of the raw-data repository (the inputs below), OUT this folder.
# Environment: PYTHONPATH at main 3c35f0c's hpkernel build, OPENBLAS_NUM_THREADS=1, nice 10, 2 threads.
RAW=$1
OUT=$2
WHAT=${3:-all}
PY=${PY:-/Users/nathan/venv-314/bin/python3}
BASE=I461-win2/probeG03125a/anm_pin3_D242.5146.npz
ACC=I461-win2/probeG0078/dz0_pin3_D242.5225_a0.007812.npz
REF=I461-win2/probeG03125b/dz0_pin3_D242.5459_a0.031250.npz
export OPENBLAS_NUM_THREADS=1
stamp() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
if [ "$WHAT" = planted ] || [ "$WHAT" = all ]; then
  nice -n 10 "$PY" -u reduced_cubic.py planted --json="$OUT/planted.json" > "$OUT/planted.log" 2>&1
  echo "planted exit $? $(stamp)" >> "$OUT/exits.txt"
  for M in w0 Ssign Sh hF; do
    nice -n 10 "$PY" -u reduced_cubic.py planted --mutate=$M --json="$OUT/planted_mut_$M.json" > "$OUT/planted_mut_$M.log" 2>&1
    echo "planted --mutate=$M exit $? (must be 1) $(stamp)" >> "$OUT/exits.txt"
  done
fi
if [ "$WHAT" = ref ] || [ "$WHAT" = all ]; then
  echo "ref start $(stamp)" >> "$OUT/exits.txt"
  nice -n 10 "$PY" -u reduced_cubic.py run "$RAW" $REF $BASE --threads=2 --json="$OUT/ref.json" > "$OUT/ref.log" 2>&1
  echo "ref exit $? $(stamp)" >> "$OUT/exits.txt"
fi
if [ "$WHAT" = acc ] || [ "$WHAT" = all ]; then
  echo "acc start $(stamp)" >> "$OUT/exits.txt"
  nice -n 10 "$PY" -u reduced_cubic.py run "$RAW" $ACC $BASE --threads=2 --json="$OUT/acc.json" > "$OUT/acc.log" 2>&1
  echo "acc exit $? $(stamp)" >> "$OUT/exits.txt"
fi
