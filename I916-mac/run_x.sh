#!/bin/bash
# #916 part 1, behind the load gate (1-minute load below 31): one process, 2 threads, nice 10.
J=$(dirname "$0")
SITE=<site of #652>
export PYTHONPATH=$SITE VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
bash "$J/gate.sh" 31 "$J/out/gate.log" nice -n 10 python3 "$J/xcheck.py" "$1" \
    "$J/seeds/sm_hi_D10.5_polish_M32.npz" "$J/seeds/sm_eta0.3_D10.5_M32_nodes27_seed.npz" "$J/out/xcheck.json" > "$J/out/xcheck.txt" 2>&1
echo "$(date -u '+%F %T') UTC xcheck exit $?" >> "$J/out/gate.log"
