#!/usr/bin/env bash
# #529 supplement: sigma_5's convergence with more iterations, --its=64 and --its=256 (k=5, no reduced block), ACC and REF, 2 threads each, four at once.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I529-win2
BASE=I461-win2/probeG03125a/anm_pin3_D242.5146.npz
ACC=I461-win2/probeG0078/dz0_pin3_D242.5225_a0.007812.npz
REF=I461-win2/probeG03125b/dz0_pin3_D242.5459_a0.031250.npz
export PYTHONFAULTHANDLER=1
cd /d/choptuik-i529/hp || exit 9
job() {
  local name=$1 att=$2; shift 2
  echo "$name start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  "$PY" -u dz0_weak.py $RAW $att $BASE --k=5 --threads=2 --json=$R/$name.json "$@" > $R/$name.log 2>&1
  echo "$name exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
}
job acc_k5_its64 $ACC --its=64 &
job acc_k5_its256 $ACC --its=256 &
job ref_k5_its64 $REF --its=64 &
job ref_k5_its256 $REF --its=256 &
wait
echo "run_i529_its done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
