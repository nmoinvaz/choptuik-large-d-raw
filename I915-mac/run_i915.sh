#!/bin/bash
# #915: the kernel's solutions at eta = 0.3, D 10.5 and at eta = 1, D 10.475 on M = 24 and 48, from #913's M = 32
# states resampled by run_eta.py --from, with the band solver. One process, 2 threads, nice 10, each run behind
# gate.sh (1-minute load below 31 at its start). A converged run is followed by a run from its state with --tol 1e-30.
# From the root of the checkout: run_i915.sh <output directory> <seed directory>
OUT=$1; SEEDS=$2
SITE=<site of #652>
PY=python3
GATE="$(dirname "$0")/gate.sh"
export PYTHONPATH=$SITE VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
one() {  # tag, eta, D, M, seed state
    local tag=$1 eta=$2 D=$3 M=$4 seed=$5
    bash "$GATE" 31 "$OUT/gate.log" nice -n 10 $PY matter/sigma_ms/run_eta.py --eta $eta --D $D --M $M --out "$OUT" \
        --solver band --threads 2 --it 40 --from "$seed" --tag ${tag}_M$M > "$OUT/${tag}_M$M.txt" 2>&1
    local rc=$?
    echo "$(date -u '+%F %T') UTC ${tag}_M$M exit $rc" >> "$OUT/gate.log"
    if [ $rc = 0 ]; then
        bash "$GATE" 31 "$OUT/gate.log" nice -n 10 $PY matter/sigma_ms/run_eta.py --eta $eta --D $D --M $M --out "$OUT" \
            --solver band --threads 2 --it 4 --tol 1e-30 --from "$OUT/sm_${tag}_M$M.npz" --tag ${tag}_polish_M$M \
            > "$OUT/${tag}_polish_M$M.txt" 2>&1
        echo "$(date -u '+%F %T') UTC ${tag}_polish_M$M exit $?" >> "$OUT/gate.log"
    fi
}
one eta0.3_D10.5 0.3 10.5 24 "$SEEDS/sm_hi_D10.5_polish_M32.npz"
one eta0.3_D10.5 0.3 10.5 48 "$SEEDS/sm_hi_D10.5_polish_M32.npz"
one eta1_D10.475 1 10.475 48 "$SEEDS/sm_ctrlB_D10.475_polish_M32.npz"
one eta1_D10.475 1 10.475 24 "$SEEDS/sm_ctrlB_D10.475_polish_M32.npz"
