#!/usr/bin/env bash
# #529 (a) and the Q half of (c): four dz0_weak.py jobs of 2 threads at once (acc/ref x its 16 / reduced), then the control --mutate=D on REF's reduced job (must exit 1).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I529-win2
BASE=I461-win2/probeG03125a/anm_pin3_D242.5146.npz
ACC=I461-win2/probeG0078/dz0_pin3_D242.5225_a0.007812.npz
REF=I461-win2/probeG03125b/dz0_pin3_D242.5459_a0.031250.npz
export PYTHONFAULTHANDLER=1
cd /d/choptuik-i529/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "810396b" ] || { echo "D:/choptuik-i529 is not at 810396b" >&2; exit 9; }
job() {   # job NAME ATTEMPT extra-args...
  local name=$1 att=$2; shift 2
  echo "$name start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  "$PY" -u dz0_weak.py $RAW $att $BASE --k=5 --threads=2 --json=$R/$name.json "$@" > $R/$name.log 2>&1
  echo "$name exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
}
job acc_k5_its16 $ACC --its=16 &
job acc_k5_red $ACC --its=24 --reduced=1 --h=1e-31 &
job ref_k5_its16 $REF --its=16 &
job ref_k5_red $REF --its=24 --reduced=1 --h=1e-31 &
wait
echo "control ref_k5_red_ctl_D start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
"$PY" -u dz0_weak.py $RAW $REF $BASE --k=5 --its=24 --reduced=1 --h=1e-31 --threads=2 --mutate=D > $R/ref_k5_red_ctl_D.log 2>&1
echo "control ref_k5_red_ctl_D exit $? (must be nonzero) $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
echo "run_i529 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
