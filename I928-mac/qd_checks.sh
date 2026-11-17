#!/bin/bash
# #928: the two checks of the quad-double stage (qd_protocol.md). The running job's leaf process is stopped while
# they run and continued after, so that 2 threads are in use at any time.
J=$(cd "$(dirname "$0")" && pwd)
OUT=$J/out
PY=python3
export PYTHONPATH=<site of #918> VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
PIDS=$(pgrep -f 'matter/sigma_ms/(mode_lam|run_eta)\.py')
[ -n "$PIDS" ] && kill -STOP $PIDS
trap '[ -n "$PIDS" ] && kill -CONT $PIDS' EXIT
echo "$(date -u '+%F %T') UTC qd checks start (stopped: $PIDS)" >> "$OUT/runs.log"
nice -n 10 $PY matter/sigma_ms/run_eta.py --eta 0.3 --D 12.375 --M 32 --from "$J/out_seeds/sm_eta0.3_D12.375_dd_conv.npz" \
    --out "$OUT" --tag eta0.3_D12.375_qdcheck_M32 --solver band --threads 2 --it 4 --qd --qd_jac dd --qd_it 6 \
    > "$OUT/qd_check1.txt" 2>&1
echo "$(date -u '+%F %T') UTC qd check 1 exit $?" >> "$OUT/runs.log"
nice -n 10 $PY "$J/qd_after.py" "$OUT/sm_eta0.3_D12.375_qdcheck_M32.npz" "$J/out_seeds/sm_eta0.3_D12.375_dd_conv.npz" >> "$OUT/qd_check1.txt" 2>&1
nice -n 10 $PY matter/sigma_ms/run_eta.py --eta 0.3 --D 12.5 --M 32 --from "$J/out_seeds/sm_eta0.3_D12.5_dd_stalled.npz" \
    --out "$OUT" --tag eta0.3_D12.5_qdcheck_M32 --solver band --threads 2 --it 4 --tol 3e-27 --qd --qd_jac dd --qd_it 6 \
    > "$OUT/qd_check2.txt" 2>&1
echo "$(date -u '+%F %T') UTC qd check 2 exit $?" >> "$OUT/runs.log"
nice -n 10 $PY "$J/qd_after.py" "$OUT/sm_eta0.3_D12.5_qdcheck_M32.npz" "$J/out_seeds/sm_eta0.3_D12.5_dd_stalled.npz" >> "$OUT/qd_check2.txt" 2>&1
echo "$(date -u '+%F %T') UTC qd checks done" >> "$OUT/runs.log"
