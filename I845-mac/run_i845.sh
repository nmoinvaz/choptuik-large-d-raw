#!/bin/bash
# #845 stage 3: the kernel at D 10.475, eta = 1, M = 32 with the deflated Newton (run_eta.py --solver band), from starts
# B and A of #652. One process, 2 threads, nice 10, each run behind gate.sh (1-minute load below 31).
# From the root of the checkout: run_i845.sh <output directory> <seed directory>
OUT=$1; SEEDS=$2
SITE=<site of #652>
PY=python3
GATE="$(dirname "$0")/gate.sh"
export PYTHONPATH=$SITE VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
COMMON="--eta 1 --D 10.475 --M 32 --out $OUT --solver band --threads 2 --it 40"
# start B: continued from the pilot's end state (3 + 3 iterations from the sigdss seed m1hi, Delta 0.9935)
bash "$GATE" 31 "$OUT/gate.log" nice -n 10 $PY matter/sigma_ms/run_eta.py $COMMON --from "$OUT/sm_pilotB_D10.475_M32.npz" \
    --tag bandB_D10.475_M32 > "$OUT/bandB.txt" 2>&1
echo "bandB exit $?" >> "$OUT/gate.log"
# start A: from the sigdss seed m1up, Delta 1.0340
bash "$GATE" 31 "$OUT/gate.log" nice -n 10 $PY matter/sigma_ms/run_eta.py $COMMON \
    --sigdss "$SEEDS/sigdss_m1up_D10.4746_eta1.0000.npy" --kc_seed 15 --tag bandA_D10.475_M32 > "$OUT/bandA.txt" 2>&1
echo "bandA exit $?" >> "$OUT/gate.log"
