#!/bin/bash
# I677-mac: hp/reduced_cubic.py ray, the plant with its two controls, then the four starts (REF first, as the pilot).
# Run from the checkout's hp/ as: bash run_i677.sh RAW OUT [planted|ref|acc|d232|classA|all]
# RAW is a clone of the raw-data repository (the inputs below), OUT this folder.
# Environment: PYTHONPATH at main 3c35f0c's hpkernel build, OPENBLAS_NUM_THREADS=1, nice 10, 2 threads.
RAW=$1
OUT=$2
WHAT=${3:-all}
PY=${PY:-/Users/nathan/venv-314/bin/python3}
B5146=I461-win2/probeG03125a/anm_pin3_D242.5146.npz
ACC=I461-win2/probeG0078/dz0_pin3_D242.5225_a0.007812.npz
REF=I461-win2/probeG03125b/dz0_pin3_D242.5459_a0.031250.npz
B231=I462-win/chain_d10/anm_pin3_D231.1312.npz
D232=I513-win/run_d10/dz0_pin3_D232.1312_a1.000000.npz
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
  one ray_planted ray planted
  one ray_planted_mut_w0 ray planted --mutate=w0
  one ray_planted_mut_B ray planted --mutate=B ;;
esac
case $WHAT in ref|all) one ray_ref ray "$RAW" $REF $B5146 --threads=2 ;; esac
case $WHAT in acc|all) one ray_acc ray "$RAW" $ACC $B5146 --threads=2 ;; esac
case $WHAT in d232|all) one ray_d232 ray "$RAW" $D232 $B231 --threads=2 --tensors=1 ;; esac
case $WHAT in classA|all) one ray_classA ray "$RAW" $CLA $B248 --threads=2 --tensors=1 ;; esac
