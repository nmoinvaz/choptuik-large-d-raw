#!/bin/bash
# #1109 stage 1c with the Rust block 12: one root. usage: run_root.sh NAME STUB STATE LO HI [--pin=...]
# STUB and STATE are file names under ~/scratch1102/in. Run as a systemd user unit
# (OPENBLAS_NUM_THREADS=1, RAYON_NUM_THREADS=2, timeout 14400).
NAME=$1; STUB=$2; STATE=$3; LO=$4; HI=$5; shift 5
RAW=/home/nathan/Source/choptuik-large-d-raw-1102/I1109-dh610
IN=/home/nathan/scratch1102/in
cd /home/nathan/Source/choptuik-ell1fast/solver/matter || exit 9
export OPENBLAS_NUM_THREADS=1 RAYON_NUM_THREADS=2
echo "$NAME start lo $LO hi $HI $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> $RAW/exits_1109.txt
timeout 14400 /home/nathan/Source/venv-i1058/bin/python -u d18_secant.py run $IN/$STUB $IN/$STATE 23.0 $LO $HI \
  $RAW/$NAME.jsonl --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2 "$@" >> $RAW/$NAME.log 2>&1
echo "$NAME exit $? $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> $RAW/exits_1109.txt
