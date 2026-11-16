#!/bin/bash
# #845 stage 3, start A with the damped band step (wip/sa-845, "newton_band damps its step inside the band") and a
# checkpoint after every step. Behind gate.sh (1-minute load below 31). When the gate opens, the run before it (PID
# given) is stopped, so that one kernel process runs at a time. From the root of the checkout:
#     run_i845_A4.sh <output directory> <seed directory> <PID of the run before>
OUT=$1; SEEDS=$2; OLD=$3
SITE=<site of #652>
PY=python3
GATE="$(dirname "$0")/gate.sh"
export PYTHONPATH=$SITE VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
bash "$GATE" 31 "$OUT/gate.log" true
if kill -0 "$OLD" 2>/dev/null; then kill "$OLD"; echo "$(date -u '+%F %T') UTC stopped run 3 of A (PID $OLD)" >> "$OUT/gate.log"; fi
nice -n 10 $PY matter/sigma_ms/run_eta.py --eta 1 --D 10.475 --M 32 --out "$OUT" --solver band --threads 2 --it 40 \
    --sigdss "$SEEDS/sigdss_m1up_D10.4746_eta1.0000.npy" --kc_seed 15 --tag bandA4_D10.475_M32 > "$OUT/bandA4.txt" 2>&1
echo "$(date -u '+%F %T') UTC bandA4 exit $?" >> "$OUT/gate.log"
