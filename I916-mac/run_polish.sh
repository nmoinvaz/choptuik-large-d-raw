#!/bin/bash
# #916: one more Newton step (--tol 1e-30) for the chain points that stopped between 1e-30 and 1e-28. Each behind the gate.
OUT=$1
J=$(dirname "$0")
SITE=<site of #652>
export PYTHONPATH=$SITE VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
for D in 9.6875 9.75 9.8125 10.1 10.9375 11; do
    bash "$J/gate.sh" 31 "$OUT/gate.log" nice -n 10 python3 matter/sigma_ms/run_eta.py --eta 0.3 --D $D --M 32 \
        --out "$OUT" --solver band --threads 2 --it 4 --tol 1e-30 --from "$OUT/sm_eta0.3_D${D}_M32.npz" \
        --tag eta0.3_D${D}_polish_M32 > "$OUT/polish_D$D.txt" 2>&1
    echo "$(date -u '+%F %T') UTC polish D $D exit $?" >> "$OUT/gate.log"
done
