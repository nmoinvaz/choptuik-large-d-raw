#!/bin/bash
# #845 stage 3, start A with the floor-aware split (wip/sa-845, "newton_band knows the floor of its split"). Behind
# gate.sh (1-minute load below 31). One process, 2 threads, nice 10. From the root of the checkout:
#     run_i845_A3.sh <output directory> <seed directory>
OUT=$1; SEEDS=$2
SITE=<site of #652>
PY=python3
GATE="$(dirname "$0")/gate.sh"
export PYTHONPATH=$SITE VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
bash "$GATE" 31 "$OUT/gate.log" nice -n 10 $PY matter/sigma_ms/run_eta.py --eta 1 --D 10.475 --M 32 --out "$OUT" \
    --solver band --threads 2 --it 40 --sigdss "$SEEDS/sigdss_m1up_D10.4746_eta1.0000.npy" --kc_seed 15 \
    --tag bandA3_D10.475_M32 > "$OUT/bandA3.txt" 2>&1
echo "$(date -u '+%F %T') UTC bandA3 exit $?" >> "$OUT/gate.log"
