#!/bin/bash
# #913: sigdss's eta = 0.3 states at D 10.5 on the kernel (M = 32) with the band solver, and the control (start B of
# #845, eta = 1, D 10.475) first. One process, 2 threads, nice 10, each run behind gate.sh (1-minute load below 31 at
# its start). A converged run is followed by one more Newton step (--tol 1e-30) from its state.
# From the root of the checkout: run_i913.sh <output directory> <seed directory>
OUT=$1; SEEDS=$2
SITE=<site of #652>
PY=python3
GATE="$(dirname "$0")/gate.sh"
export PYTHONPATH=$SITE VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
one() {  # tag, eta, D, seed file
    local tag=$1 eta=$2 D=$3 seed=$4
    bash "$GATE" 31 "$OUT/gate.log" nice -n 10 $PY matter/sigma_ms/run_eta.py --eta $eta --D $D --M 32 --out "$OUT" \
        --solver band --threads 2 --it 40 --sigdss "$seed" --kc_seed 15 --tag ${tag}_M32 > "$OUT/$tag.txt" 2>&1
    local rc=$?
    echo "$(date -u '+%F %T') UTC $tag exit $rc" >> "$OUT/gate.log"
    if [ $rc = 0 ]; then
        bash "$GATE" 31 "$OUT/gate.log" nice -n 10 $PY matter/sigma_ms/run_eta.py --eta $eta --D $D --M 32 --out "$OUT" \
            --solver band --threads 2 --it 4 --tol 1e-30 --from "$OUT/sm_${tag}_M32.npz" --tag ${tag}_polish_M32 \
            > "$OUT/${tag}_polish.txt" 2>&1
        echo "$(date -u '+%F %T') UTC ${tag}_polish exit $?" >> "$OUT/gate.log"
    fi
}
one ctrlB_D10.475 1 10.475 solver/matter/data/sigdss_sol_m1hi_D10.4750_eta1.0000.npy
one hi_D10.5 0.3 10.5 "$SEEDS/walk2_hi_10.5.npy"
one up_D10.5 0.3 10.5 "$SEEDS/walk3_up_10.5.npy"
one march_D10.5 0.3 10.5 solver/matter/data/sigdss_sol_m03hi_D10.5000_eta0.3000.npy
