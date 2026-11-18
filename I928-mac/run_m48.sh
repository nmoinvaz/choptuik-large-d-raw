#!/bin/bash
# #928: M 48 at eta 1, D 13 again. The first run's double-double stage passed through max |F| 2.9e-25 and ended at
# 2.8e-24, above the hand-over limit of 1e-24, so no quad-double stage ran (out/failed/eta_eta1_D13_M48_no_handover.txt).
# Here the double-double stage's tolerance is 9e-25, a loosening inside the coordinator's limit (never looser than
# 1e-24), so the state is handed over when it first gets below it. The quad-double rule is unchanged.
J=$(cd "$(dirname "$0")" && pwd)
OUT=$J/out
PY=python3
export PYTHONPATH=<site of #918> VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
log() { echo "$(date -u '+%F %T') UTC $*" >> "$OUT/runs.log"; }
T=eta1_D13_M48
nice -n 10 $PY matter/sigma_ms/run_eta.py --eta 1 --D 13 --M 48 --from "$OUT/sm_eta1_D13_M32.npz" --out "$OUT" --tag $T \
    --solver band --threads 2 --it 40 --tol 9e-25 --handover_max 1e-24 --qd --qd_jac dd --qd_it 6 \
    --qd_accept 1e-28 --qd_first_rise 10 > "$OUT/eta_$T.txt" 2>&1
log "$T (double-double tolerance 9e-25) exit $?"
G=$($PY -c "
import json
v = None
for l in open('$OUT/sm_lam.jsonl'):
    r = json.loads(l)
    if str(r['eta']) == '1' and float(r['D']) == 13.0 and r['M'] == 32 and r.get('lam'): v = r['lam']
print(v)")
nice -n 10 $PY matter/sigma_ms/mode_lam.py "$OUT/sm_$T.npz" --out "$OUT" --guess "$G" --threads 2 \
    --gauge_window 1e-12 --widths 1e-4,1e-3,1e-2 > "$OUT/lam_$T.txt" 2>&1
log "lam $T exit $?"
log "run_m48 done"
