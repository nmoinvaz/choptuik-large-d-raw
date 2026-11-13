#!/bin/bash
# I698-mac: hp/reduced_cubic.py curve, the plant with its two controls, then REF (the pilot) and the class A start.
# Run from the checkout's hp/ as: bash run_i698.sh RAW OUT [planted|ref|classA|all]
# RAW is a clone of the raw-data repository (the inputs below), OUT this folder.
# Environment: PYTHONPATH at main 3c35f0c's hpkernel build, OPENBLAS_NUM_THREADS=1, nice 10, 2 threads.
RAW=$1
OUT=$2
WHAT=${3:-all}
PY=${PY:-/Users/nathan/venv-314/bin/python3}
B5146=I461-win2/probeG03125a/anm_pin3_D242.5146.npz
REF=I461-win2/probeG03125b/dz0_pin3_D242.5459_a0.031250.npz
B248=I603-win2/chain/anm_pin3_D248.6298.npz
CLA=I677-mac/classA/dz0_pin3_D249.3927_a0.762939.npz
export OPENBLAS_NUM_THREADS=1
stamp() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
rev=$(git rev-parse --short=8 HEAD)
one() {   # name, then the arguments of reduced_cubic.py
  local name=$1
  shift
  echo "$name start $(stamp) $rev" >> "$OUT/exits.txt"
  nice -n 10 "$PY" -u reduced_cubic.py "$@" --json="$OUT/$name.json" > "$OUT/$name.log" 2>&1
  echo "$name exit $? $(stamp)" >> "$OUT/exits.txt"
}
case $WHAT in planted|all)
  one curve_planted curve planted
  one curve_planted_mut_w0 curve planted --mutate=w0
  one curve_planted_mut_chord curve planted --mutate=chord ;;
esac
case $WHAT in ref|all) one curve_ref curve "$RAW" $REF $B5146 --threads=2 --ref677="$RAW/I677-mac/ray_ref.json" \
  --ref694="$RAW/I694-mac/rows_ref.json" ;; esac
case $WHAT in classA|all) one curve_classA curve "$RAW" $CLA $B248 --threads=2 \
  --ref677="$RAW/I677-mac/ray_classA.json" --ref694="$RAW/I694-mac/rows_classA.json" ;; esac
